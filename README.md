This script is designed to visialize FRET trajectories, including TDP, TODP, POKIT plot analysis.

**Details**

It reads all .dat files in a folder and performs a full plot analysis. 
By default, the output is saved as a PNG image. The FRET data should 
consist of three columns: the first column represents the initial FRET value, 
the second column represents the final FRET value, and the third column 
indicates the number of frames required for the transition. 

**DwellTimeRangeDivisionCondition.json**
The file DwellTimeRangeDivisionCondition.json is used to manage dwell time classifications. It defines four different ranges, with each range being associated with a specific color. You could modify this file to adapt it to your data.

**FractionOfMoleculesDivisionCondition.json**
The FractionOfMoleculesDivisionCondition.json is used to manage fraction fo molecules classifications. It defines four different ranges, with each range being associated with a specific radius.The keyword "one circle" means to draw a single circle in a set of concentric circles, while the keyword "two circles" means to draw two circles in concentric circles, and so on. You could modify this file to adapt it to your data.

**Usage**
'''bash
python -m FRETHeatMap <folder with FRET data> -n <[40] number-bin> -f <figure-name> -t <[png] type-of-figure> -a  <[TDP, TODP or POKIT] analysis-method> -tf<[5] time-per-frame>
'''

**Example usages**
1. default: python -m FRETHeatMap FRETDataFolder
2. revise number of bin: python -m FRETHeatMap FRETDataFolder -n 40
3. set figure name: python -m  FRETHeatMap FRETDataFolder -f example
3. set figure format: python -m FRETHeatMap FRETDataFolder -t png
4. Only use a analysis method: python -m FRETHeatMap FRETDataFolder -a TDP
5. set duration time of a frame 10ms:  python -m FRETHeatMap FRETDataFolder -tf 10
