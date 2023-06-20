from dataclasses import dataclass
from datetime import date
import random
import sys
import os

# a struct that neatly contains sets of lines in the text file
@dataclass
class lineData:
    type : int
    # Case Guide:
    # 0: Unmovable lines (# comment),
    # 1: Grouped lines (any order) (""" comment blocks),
    # 2: Movable lines (no annot.)
    lines : "list[str]"

# function that displays the source code file without the line associated with the multiple-choice problem
def displayFile(fout, lineIdx, qnum):
    idx = 0
    for lds in lineCollection:
        for line in lds.lines:
            if (idx == lineIdx) :
                fout.write("##### QUESTION #####\n")
            else :
                fout.write(str(line))
        idx += 1

# function that populates lineCollection and toRearrange with src code lines and non-omitted line indices, respectively
def fileParser(lineCollection, toRearrange):
    curLine = 0  # index in lineCollection
    commentBlockIndx = []  # index of comment block whose elements are to be rearranged
    while src:
        line = src.readline()
        if len(line) == 0:
            break
        if line[0] == "#":  # Case 0: line comment
            lineCollection.append(lineData(0, [line]))
        elif "\"\"\"" in line:  # Case 1 (or 2)
            if len(line.split("=")) == 1:  # Case 1: comment block
                commentBlock = [] # this list will hold all the lines in this comment block.
                commentBlock.append(line)
                foundPair = False  
                while src:  # keep reading lines until another """ is found.
                    line1 = src.readline()
                    if len(line1) == 0:
                        break
                    if "\"\"\"" in line1 and len(line1.split("=")) == 1:
                        commentBlock.append(line1)
                        foundPair = True
                        break
                    else:
                        commentBlock.append(line1)
                if foundPair == False: 
                    print("One of your \"\"\" is missing a closing pair!")
                    print(" Line" + (curLine+1) + ": " + line)
                    exit()
                lineCollection.append(lineData(1, commentBlock))
                commentBlockIndx.append(curLine)
            else:  # Case 2: the """ is a string argument and not a comment
                lineCollection.append(
                    lineData(2, [line]))
                toRearrange.append(curLine)
                curLine += 1  
                foundPair = False 
                while src:  # keep reading lines until another """ is found.
                    line1 = src.readline()
                    if len(line1) == 0:
                        break
                    if "\"\"\"" in line1:
                        lineCollection.append(lineData(2, [line1]))
                        toRearrange.append(curLine)
                        foundPair = True
                        break
                    else:
                        lineCollection.append(lineData(2, [line1]))
                        toRearrange.append(curLine)
                        curLine += 1
                if foundPair == False:  # error!
                    print("One of your \"\"\" is missing a closing pair!")
                    exit()
        else:  # Case 3: no annotation
            lineCollection.append(lineData(3, [line]))
            toRearrange.append(curLine)
        curLine += 1

try:
    # Open source code file
    if len(sys.argv) == 1:
        print("You must provide a file name argument!")
        print("Use: \"python3 choices.py <filename>.txt\"")
        exit()
    filename = sys.argv[1]

    print("Opening: ", filename, "...\n")
    src = open(filename, "r")

    # Create a reports folder
    try:
        os.makedirs("report")
    except FileExistsError:
        # directory already exists
        pass

    # Open/create test output file
    srcOut = open('report/MultipleChoice{'+str(filename)+'}.txt', "w")


    # Parse src and populate lineCollection and toRearrange
    lineCollection = []   # contains all lines of the input file, but groups comment blocks into a single element
    toRearrange = []      # index of code lines that can be scrambled
    fileParser(lineCollection, toRearrange)

    # create multiple-choice problem for each non-omitted line
    qnum = 1
    for idx in toRearrange:

        srcOut.write("QUESTION #"+str(qnum)+"\n\n")

        # Display source code file
        displayFile(srcOut, idx, qnum)

        srcOut.write("\n\n\nWhich line below belongs on the marked line in the source code file?\n\n")

        # list choices
        choices = [None] * 4
        choices[0] = lineCollection[idx].lines

        # loop that populates choices
        for i in range(1, 4):

            # ensures that choices aren't duplicated
            choice = lineCollection[toRearrange[random.randint(0, len(toRearrange)-1)]].lines
            while (choice in choices):
                choice = lineCollection[toRearrange[random.randint(0, len(toRearrange)-1)]].lines

            choices[i] = choice
        
        random.shuffle(choices)

        # writes possible answers to out file 
        letters = ["a. ", "b. ", "c. ", "d. "]
        for i in range(0, 4):
            if (choices[i][0].lstrip() == "") :
                srcOut.write(letters[i]+"\n")
            else:
                srcOut.write(letters[i]+choices[i][0].lstrip())
        srcOut.write("\n\n\n\n")

        qnum += 1
except:
    print("Crashed!")
    # Open/create report file (FAILURE)
    reportFile = open('report/choicesReport.txt', 'a')
    reportFile.write("\n")

    # Variable for how space to use up for the filename column (there's probably a more efficient way of doing this, but I'm not sure))
    justifySpace = 30
    reportFileName = "|" + filename.ljust(justifySpace)
    reportDateRun = "| " + date.today().strftime("%b-%d-%Y")
    reportPass = " | F |"
    reportFile.write(reportFileName + reportDateRun + reportPass)
    reportFile.close()
    exit()

# Open/create report file (SUCCESS!)
reportFile = open('report/choicesReport.txt', 'a')
reportFile.write("\n")

# Variable for how space to use up for the filename column (there's probably a more efficient way of doing this, but I'm not sure))
justifySpace = 30
reportFileName = "|" + filename.ljust(justifySpace)
reportDateRun = "| " + date.today().strftime("%b-%d-%Y")
reportPass = " | P |"
reportFile.write(reportFileName + reportDateRun + reportPass)

reportFile.close()
srcOut.close()


# close files
# src.close()
# srcOut.close()
# reportFile.close()