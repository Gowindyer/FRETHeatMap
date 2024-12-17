from .utils import FRETHEATMAP
from .argparser import parser
import glob


if __name__ == "__main__":

    args = parser.parse_args()
    
    dataFolder = args.data
    # find all data file 
    FRETFiles = glob.glob(dataFolder + '/*.dat')
    numbin = args.number_bin
    
    figureName = args.figure_name
    typeOfFigure = args.type_of_figure 

    analysisMethod = args.analysis_method
    timeframe = args.time_per_frame

    FRETHeatMap = FRETHEATMAP()
    analysisFunc = {'TDP': FRETHeatMap.plotTDP, 
                    'TODP': FRETHeatMap.plotTODP, 
                    'POKIT': FRETHeatMap.plotPOKIT} 
    if analysisMethod:
        if figureName:
           analysisFunc[analysisMethod](FRETFiles, numbin, timeFrame=timeframe, figureName='%s'%figureName,figuretype=typeOfFigure)
        else:
           analysisFunc[analysisMethod](FRETFiles, numbin, timeFrame=timeframe, figuretype=typeOfFigure)
    else:
        for func in analysisFunc:
            if figureName:
               analysisFunc[func](FRETFiles, numbin, timeFrame=timeframe, figureName='%s'%figureName,figuretype=typeOfFigure)
            else:
               analysisFunc[func](FRETFiles, numbin, timeFrame=timeframe, figuretype=typeOfFigure)
