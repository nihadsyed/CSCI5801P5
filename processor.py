# Prompt user for source code filename
from dataclasses import dataclass
from random import randint
import sys
import os


# filename = input("Enter name of source code file you wish to import: ")
if len(sys.argv) == 1:
    print("You must provide a file name argument!")
    print("Use: \"python project4Alt.py <filename>.txt\"")
    exit()
filename = sys.argv[1]

# Open source code file
print("Opening: ", filename, "...\n")
src = open(filename, "r")

# a struct that neatly contains sets of lines in the text file.


@dataclass
class lineData:
    # type: int
    # Case Guide:
    # 0: Unmovable lines (# comment),
    # 1: Grouped lines (any order) (""" comment blocks),
    # 2: Movable lines (no annot.)
    lines: "list[str]"

# Read src file
# rearrangedDict = {}  # dictionary containing final rearrangement of src file lines
# lineCollection: list[lineData] #contains an ordered list of lines.
# toRearrange: list[int] #contains int indices of lineCollection that can be scrambled

# function that prints the lineCollection contents.


def printLineCollection(file):
    ind = 0
    for lds in lineCollection:
        for line in lds.lines:
            if ind in toRearrange:  # DEBUG
                file.write("Y " + str(line))  # DEBUG
            else:  # DEBUG
                file.write("N " + str(line))  # DEBUG
            # file.write(line) #ONCE COMPLETE, REMOVE THE ABOVE DEBUG STATEMENTS AND UNCOMMENT THIS.
        ind += 1


def scrambleStuff(iterations):
    count = 0
    # print(lineCollection)
    while count < iterations:  # shuffling lines for movable single lines.
        i = randint(0, len(toRearrange)-1)
        j = randint(0, len(toRearrange)-1)
        a = toRearrange[i]
        b = toRearrange[j]
        if a == b:
            continue
        temp = lineCollection[a]
        lineCollection[a] = lineCollection[b]
        lineCollection[b] = temp
        count += 1
    for cb in commentBlockIndx:  # shuffling lines within comment blocks
        count = 0
        while count < iterations:
            i = randint(0, len(lineCollection[cb].lines)-1)
            j = randint(0, len(lineCollection[cb].lines)-1)
            temp = lineCollection[cb].lines[i]
            lineCollection[cb].lines[i] = lineCollection[cb].lines[j]
            lineCollection[cb].lines[j] = temp
            count += 1
            # print(lineCollection[cb].lines)
            # # print("t")


# Logic:
# One line will be read at a time.
# It will be categorized and grouped together (if applicable) into the lineCollection.
# The advantage of lineData is that all grouped lines ("""), all grouped lines are a single index in the lineCollection.
# This makes randomization easier as you don't have to fiddle around with moving multiple lines together.
curLine = 0  # counter; keep track of index in lineCollection
# This contains all the lines of the input file, but groups comment blocks into a single element.
lineCollection = []
toRearrange = []  # index of code lines that can be scrambled
commentBlockIndx = []  # index of comment block whose elements are to be rearranged
while src:
    line = src.readline()
    if len(line) == 0:
        break
    if line[0] == "#":  # case 0 (line comment)
        # REMOVE DEBUG TEXT LATER
        lineCollection.append(lineData(0, ["CASE 0  " + line]))
    elif "\"\"\"" in line:  # case 1 (or 2)
        if len(line.split("=")) == 1:  # case 1 (comment block; i.e. not a string variable.)
            # this list will hold all the lines in this comment block.
            commentBlock = []
            commentBlock.append("CASE1ST " + line)  # REMOVE DEBUG TEXT LATER
            foundPair = False  # checker: if the following while loop is exited without finding the end """, then the file's formatted incorrectly...
            while src:  # keep reading lines until another """ is found.
                line1 = src.readline()
                if len(line1) == 0:
                    break
                # if this is an endquote (and make sure it's not another quote inside!)
                if "\"\"\"" in line1 and len(line1.split("=")) == 1:
                    # REMOVE DEBUG TEXT LATER
                    commentBlock.append("CASE1EN " + line1)
                    foundPair = True
                    break
                else:
                    # REMOVE DEBUG TEXT LATER
                    commentBlock.append("CASE1NX " + line1)
            if foundPair == False:  # error!
                # REMOVE DEBUG TEXT LATER
                print("One of your \"\"\" is missing a closing pair!")
                print(" Line" + (curLine+1) + ": " + line)
                exit()
            lineCollection.append(lineData(1, commentBlock))
            commentBlockIndx.append(curLine)
            # toRearrange.append(curLine)
        else:  # case 2. The """ is a string argument and not a comment! Each line are still seperate elements in lineCollection. This distinction is done to avoid errors involving """.
            lineCollection.append(
                lineData(2, ["CASE 2Q " + line]))  # REMOVE DEBUG TEXT LATER
            toRearrange.append(curLine)
            curLine += 1  # increment
            foundPair = False  # checker: if the following while loop is exited without finding the end """, then the file's formatted incorrectly...
            while src:  # keep reading lines until another """ is found.
                line1 = src.readline()
                if len(line1) == 0:
                    break
                if "\"\"\"" in line1:
                    # REMOVE DEBUG TEXT LATER
                    lineCollection.append(lineData(2, ["CASE 2Q " + line1]))
                    toRearrange.append(curLine)
                    foundPair = True
                    # not incrementing curLine because that will happen later.
                    break
                else:
                    # REMOVE DEBUG TEXT LATER
                    lineCollection.append(lineData(2, ["CASE 2Q " + line1]))
                    toRearrange.append(curLine)
                    curLine += 1
            if foundPair == False:  # error!
                print("One of your \"\"\" is missing a closing pair!")
                exit()
    else:  # case 2(no annotation; to be shuffled!)
        # REMOVE DEBUG TEXT LATER
        lineCollection.append(lineData(3, ["CASE 2S " + line]))
        toRearrange.append(curLine)
    curLine += 1
    # print(line)

# Scrambling the code.
# The argument of scrambleStuff determines how many iterations of scrambling should be done.
# Ideally, pick a large value unless it takes too long to process
scrambleStuff(1000)

# Test: printing out to a file.
try:
    os.makedirs("report")
except FileExistsError:
    # directory already exists
    pass
# overwrite all contents.

testOutput = open('report/{}ReorderOutput.txt'.format(filename.split(".")[0]), "w")
printLineCollection(testOutput)
testOutput.close()
src.close()
