import sys
import os

# Reads in a large file and outputs many smaller files so that they can be opened more easily

def printUsageAndExit():
    programName = os.path.split(sys.argv[0])[1]
    print("Usage: " + programName + " FILE_TO_BE_SPLIT [NEW_FILE_SIZE(k|M )] [MAX_FILES]")
    print("Default size: 100M")
    exit()


if len(sys.argv) < 2:
    printUsageAndExit()

inFileName = sys.argv[1]     # File to be split
outputSize = 100000000          # Size to split into; default 1M  
maxFiles = 1000                 # Maximum split files to create

try:
    if len(sys.argv) > 2:
        unit = sys.argv[2][-1].lower()
        unit_map = {"k": 1000, "m": 1000000}
        outputSize = unit_map[unit] * int(sys.argv[2][:-1])

    if len(sys.argv) > 3:
        maxFiles = int(sys.argv[3])       
except:
    printUsageAndExit()

try:
    inFile = open(inFileName, "rb")
except:
    print("couldn't open input file: " + inFileName)
    exit()
    
for index in range(1, maxFiles + 1):

    contents = inFile.read(outputSize)
    if not contents:
        break
   
    inFileNamePart, inFileExt = os.path.splitext(inFileName)
    outFileName = inFileNamePart + ".part" + str(index) + inFileExt
    
    outFile = open(outFileName, "wb")
    outFile.write(contents)
    outFile.close()
    
    print("created " + outFileName)
    index += 1