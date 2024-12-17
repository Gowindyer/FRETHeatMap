import argparse

parser = argparse.ArgumentParser(description="Data visualization for FRET trajectories, including TDP, TODP and POKIT plot analysis.")
parser.add_argument("data",
                    type=str,
                    help="The path of FRET trajectories data")
parser.add_argument("-n",
                    "--number-bin",
                    type=int,
                    default=40,
                    help="The number of bin to divide FRET data")
parser.add_argument("-tf",
                    "--time-per-frame",
                    type=int,
                    default=5,
                    help="The duration time of per frame,unit is ms")

parser.add_argument("-f",
                    "--figure-name",
                    type=str,
                    default=False,
                    help="The number of bin to divide FRET data")

parser.add_argument("-t",
                    "--type-of-figure",
                    type=str,
                    default='png',
                    help="The type of figure. Such pdf, png and so on")

parser.add_argument("-a",
                    "--analysis-method",
                    type=str,
                    default=False,
                    help="You can use only one method to analyze the data, and it can be set to TDP, TODP, or POKIT.")

