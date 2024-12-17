import numpy as np
import matplotlib.pyplot as plt
import matplotlib.cm as cm
import json
import os

__location__ = os.path.dirname(os.path.abspath(__file__))
class FRETHEATMAP():
    def __init__(self):

        """
        """
        self.dwellTimeCondition = json.load(open(f'{__location__}/DwellTimeRangeDivisionCondition.json','r'))
        self.FractionOfMoleculesCondition = json.load(open(f'{__location__}/FractionOfMoleculesDivisionCondition.json')) 
    def getTransitionsTimesMap(self,FRETdata,FRETbin):
        """
        get the times of transition events.

        Parameter
        ---------
        FRETdata: numpy.array
           FRET data

        FRETbin: numpy.array
           The bin of FRET for histogram
        
        Return
        ------
        TransitionsTimesMap: numpy.array
           Times of transition events array
        """
        numbin = len(FRETbin)-1
        self.TransitionsTimesMap = np.zeros((numbin, numbin), dtype=float)
        self.dwellTime = np.zeros((numbin, numbin), dtype=float)
        for i_d in FRETdata:
            initialFretIndex = False
            finalFretIndex = False
            for i,i_f in enumerate(FRETbin):
                for j,j_f in enumerate(FRETbin[1:]):
                    if i_d[0] >= i_f and i_d[0] < j_f:
                        initialFretIndex = i
                    if i_d[1] >= i_f and i_d[1] < j_f:
                        finalFretIndex = i
            if not initialFretIndex or not finalFretIndex:
                print(i_d[i],initialFretIndex,finalFretIndex)
            self.TransitionsTimesMap[initialFretIndex, finalFretIndex] += 1
            self.dwellTime[initialFretIndex, finalFretIndex] += i_d[2]
         
        return self.TransitionsTimesMap

    def getMoleculeExistMap(self,FRETdata,FRETbin):
        """
        get Molecules exists array
        
        Parameter
        ---------
        FRETdata: numpy.array
           FRET data
        
        FRETbin: numpy.array
           The bin of FRET for histogram
     
        Return
        ------
        MoleculeExistsMap: numpy.array
           The molecules exist if the value of the array element is 1, 
           otherwise they do not exist.
        """
        numbin = len(FRETbin)-1
        MoleculeExistMap = np.zeros((numbin,numbin),dtype=float)
        TransitionsTimesMap = self.getTransitionsTimesMap(FRETdata,FRETbin)
        occureMoleculesIndex = np.argwhere(TransitionsTimesMap!=0)
        for iidx in occureMoleculesIndex:
            MoleculeExistMap[iidx[0],iidx[1]] =1
           
        return MoleculeExistMap

        
    def getFractionOfMolecules(self, FRETdataFiles, FRETbin):
        """
        get Fraction of Molecules

        Parameter
        ---------
        FRETdataFiles: list
           The list of FRET data files

        FRETbin: numpy.array
           The bin of FRET for histogram

        Return
        ------
        FractionOfMolecules: numpy.array
           Fraction of molecules
        """
        numbin = len(FRETbin) - 1
        self.FractionOfMolecules = np.zeros((numbin, numbin), dtype=float)
        for fretPath in FRETdataFiles:
            fretdata = np.loadtxt(fretPath,dtype=float)
            MoleculeExistMap =self.getMoleculeExistMap(fretdata, FRETbin)
            self.FractionOfMolecules = self.FractionOfMolecules + MoleculeExistMap
        self.FractionOfMolecules = self.FractionOfMolecules/len(FRETdataFiles)

        return self.FractionOfMolecules

    def getNumberOfEvents(self, FRETdataFiles, FRETbin):
        """
        get Fraction of Molecules

        Parameter
        ---------
        FRETdataFiles: list
           The list of FRET data files

        FRETbin: numpy.array
           The bin of FRET for histogram

        Return
        ------
        NumberOfEvents: numpy.array
           Number Of events
        """
        numbin = len(FRETbin) - 1
        self.NumberOfEvents = np.zeros((numbin, numbin), dtype=float)
        self.totalDwellTime = np.zeros((numbin, numbin), dtype=float)
        for fretPath in FRETdataFiles:
            fretdata = np.loadtxt(fretPath,dtype=float)
            self.getTransitionsTimesMap(fretdata, FRETbin)
            self.NumberOfEvents += self.TransitionsTimesMap
            self.totalDwellTime += self.dwellTime
        return self.NumberOfEvents

    def getDataForPOKIT(self, FRETdataFiles, FRETbin, timeFrame):
        """
        get Fraction of molecules and averaged dwell time for POKIT.

        Parameter
        ---------
        FRETdataFiles: list
           The list of FRET data files

        FRETbin: numpy.array
           The bin of FRET for histogram

        timeFrame: float
           The duration of a frame

        Return
        ------
        POKIT: dictionary
           
        """
        numbin = len(FRETbin) - 1
        fret = (FRETbin[:-1] + FRETbin[1:])/2
        self.getNumberOfEvents(FRETdataFiles, FRETbin)
        self.getFractionOfMolecules(FRETdataFiles, FRETbin)
        eventIndex = np.argwhere(self.NumberOfEvents!=0)
        self.POKITData = {'Initial FRET': [],'Final FRET': [], 'Average dwell times':[], 'Fraction of molecules':[]}
        for idx in eventIndex:
            dwelltime = self.totalDwellTime[idx[0], idx[1]]*timeFrame
            numofevents = self.NumberOfEvents[idx[0], idx[1]]
            fractionOfmol = self.FractionOfMolecules[idx[0], idx[1]]
            self.POKITData['Initial FRET'].append(fret[idx[0]])
            self.POKITData['Final FRET'].append(fret[idx[1]])
            self.POKITData['Average dwell times'].append(dwelltime/numofevents)
            self.POKITData['Fraction of molecules'].append(fractionOfmol)

    def plotHeatMap(self, data, colorBarLabel, figureName='headmap', figuretype='png'):
        """
        To plot head map 

        Parameter
        ---------
        data: numpy.array
           The raw data

        figureName: str
           The name of figure
        """
        fig, ax = plt.subplots(figsize=(4.6,4.6))
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.spines['top'].set_linewidth(2)
        ax.spines['right'].set_linewidth(2)
        cs = ax.imshow(data,interpolation='bilinear',cmap=cm.jet,
                origin='lower',extent=[0,1,0,1],vmax=data.max(),vmin=data.min())
        diagonal= np.linspace(0,1,20)
        ax.plot(diagonal,diagonal,'--',color='white',lw=2)
        ax.set_xlabel('Initial FRET',fontsize=20)
        ax.set_ylabel('Final FRET',fontsize=20)
        ax.set_xticks(np.arange(0,1.2,0.2))
        ax.set_yticks(np.arange(0,1.2,0.2))
        cbar = fig.colorbar(cs,fraction=0.046, pad=0.04)
        cbar.ax.get_yaxis().labelpad = 20
        cbar.set_label(label=colorBarLabel, rotation=270,size='18')
        cbar.ax.tick_params(labelsize=12)
        ax.tick_params(which='both',labelsize='xx-large',width=2)
        plt.savefig('%s.%s'%(figureName, figuretype), dpi=600,bbox_inches='tight')

    def plotTDP(self, FRETdataFiles, numbin=40, timeFrame=0,figureName='TDP', figuretype='png'):
        """
        plot TDP figure

        Parameter
        ---------
        FRETdataFiles: list
           The list of FRET data files

        numbin: int
           The number of bin

        """
        FRETbin = np.linspace(0, 1,numbin+1)
        NumberOfEvents = self.getNumberOfEvents(FRETdataFiles,FRETbin)
        if figureName !='TDP':
            figureName = '%s_TDP'%figureName
        self.plotHeatMap(NumberOfEvents,'Number of Events', figureName=figureName, figuretype=figuretype)

    def plotTODP(self, FRETdataFiles, numbin, timeFrame=0, figureName='TODP', figuretype='png'):
        """
        plot TODP figure

        Parameter
        ---------
        FRETdataFiles: list
           The list of FRET data files

        numbin: numpy.array
           The number of bin for histogram
        """
        FRETbin = np.linspace(0, 1,numbin+1)
        FractionOfMolecules = self.getFractionOfMolecules(FRETdataFiles, FRETbin)
        if figureName !='TODP':
            figureName = '%s_TODP'%figureName
        self.plotHeatMap(FractionOfMolecules, 'Fraction of Molecules', figureName=figureName, figuretype=figuretype)

    def draw_concentric_circles(self, ax, x, y, number_Circle, circle_color):
        # norm = Normalize(vmin=0, vmax=1)
        # cmap = plt.get_cmap(cmap)
        radius = np.array([2,4,6,8])*0.008
        for i in range(number_Circle):
            circle = plt.Circle((x, y), radius[i], fill=False, 
                                edgecolor=circle_color, lw=2,alpha=0.5)
            ax.add_patch(circle)

    def DwellTimeRangeDivision(self, DwellTime):
        dtc = self.dwellTimeCondition
        if DwellTime >= dtc["red"][0] and DwellTime < dtc["red"][1]:
            color = "red"
        elif DwellTime >=  dtc["purple"][0] and DwellTime < dtc["purple"][1]:
            color = 'purple'
        elif DwellTime >= dtc["green"][0] and DwellTime < dtc["green"][1]:
            color = 'green'
        elif DwellTime >= dtc["blue"][0]   and DwellTime < dtc["blue"][1]:
            color = 'blue'
        elif DwellTime >=dtc["black"][0]:
            color = 'black'

        return color

    def FractionOfMoleculesDivision(self, fractionOfMolecules):
        fmdc = self.FractionOfMoleculesCondition
        if fractionOfMolecules >= fmdc['one circle'][0] and fractionOfMolecules < fmdc['one circle'][1]:
            numberCircle = 1
        elif fractionOfMolecules >= fmdc['two circle'][0] and fractionOfMolecules < fmdc['two circle'][1]:
            numberCircle = 2
        elif fractionOfMolecules > fmdc['three circle'][0] and fractionOfMolecules < fmdc['three circle'][1]:
            numberCircle = 3
        elif fractionOfMolecules >= fmdc['four circle'][0]:
            numberCircle = 4
        return numberCircle

    def plotPOKIT(self, FRETdataFiles, numbin, timeFrame=5, figureName='POKIT', figuretype='png'):
        
        FRETbin = np.linspace(0, 1,numbin+1)
        self.getDataForPOKIT(FRETdataFiles, FRETbin,timeFrame)
        # Initialize
        initial_fret = self.POKITData['Initial FRET'] 
        final_fret = self.POKITData['Final FRET']
        fractionOfMolecules = self.POKITData['Fraction of molecules']
        dwellTime = self.POKITData['Average dwell times']
        
        fig, ax = plt.subplots(figsize=(4.6, 4))
        # Draw concentric circles with variable colors
        for x, y, fraction, dwell in zip(initial_fret, final_fret, fractionOfMolecules,dwellTime):
            # Generate a new set of color values for each concentric circle
            numberCircle = self.FractionOfMoleculesDivision(fraction)
            color_for_concentric_circle = self.DwellTimeRangeDivision(dwell) 
            self.draw_concentric_circles(ax, x, y, number_Circle=numberCircle, circle_color=color_for_concentric_circle)

        # Add a diagonal reference line (y=x)
        ax.plot([0, 1], [0, 1], '--',color='k', linewidth=3)

        # Set the limits and labels
        ax.set_xlim(0, 1)
        ax.set_ylim(0, 1)
        ax.set_xlabel('Initial FRET',fontsize=24)
        ax.set_ylabel('Final FRET',fontsize=24)
        ax.spines['bottom'].set_linewidth(2)
        ax.spines['left'].set_linewidth(2)
        ax.spines['top'].set_linewidth(2)
        ax.spines['right'].set_linewidth(2)
        ax.set_xticks(np.arange(0,1.2,0.2))
        ax.set_yticks(np.arange(0,1.2,0.2))
        ax.tick_params(which='both',labelsize='xx-large',width=2)
        if figureName !='POKIT':
            figureName = '%s_POKIT'%figureName
        plt.savefig('%s.%s'%(figureName, figuretype), dpi=600, bbox_inches='tight')

