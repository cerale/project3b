#NAME: Alejandra Cervantes,Ryan Miyahara
#EMAIL: alecer@ucla.edu,rmiyahara144@gmail.com
#ID: 104844623,804585999

import sys
import csv

everything_is_ok = True

def main():
    #Check argument
    if (len(sys.argv) != 2):
        print("Please use this program in the following format: ./lab3 CSVFILE", file=sys.stderr)
        sys.exit(1)
    filename = sys.argv[1]
    if (len(filename) < 4):
        print("Please use this program in the following format: ./lab3 CSVFILE", file=sys.stderr)
        sys.exit(1)
    format = filename[len(filename) - 4:]
    if (format != ".csv"):
        print("Please use this program in the following format: ./lab3 CSVFILE", file=sys.stderr)
        sys.exit(1)

    #Take in data

    if everything_is_ok:
        sys.exit(0) #Successful exit
    else:
        sys.exit(2) #Inconsistency found, everything is not ok

if __name__ == "__main__":
    main()