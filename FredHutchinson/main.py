#REQUIREMENTS BEFORE YOU USE THIS PROGRAM
# Follow the formatting rules

# Column order should be as follows
# Study, Treatment, Virus, VirusID (if applicable, if not don't add),
# Lab (can be added in code), Poscrit, Antibodies
# For now Antibodies have to be added last, so that it can be appended afterwards
# In the future, I could probably figure out how to move the columns.

# Make sure there is no spacing in the column.
# Get rid of unnesccary spacing on the ends, both for rows and columns
# The third row should read the first list of data
# More rules to follow

# CHANGE EXCEL FILE TO CSV

# In the future, there will be a better interface, so user can choose what functions to use.

# Fuzzy matching will be thought about in the future
# Next Steps
# Work on a simple and effective interface

import pandas as pd
import csv
# We love pointers :DD
from copy import copy, deepcopy

# The amount of rows should never change (apart from when ic80 get concatenated to the bottom of ic50.)

# The only column changes that should be made are the additions of new antibodies.
# When there is a new column, append the name of the antibody to the header.

def main():
  
  FINALdata = organizeData('220801_Edit.csv')
  convertCSV(FINALdata)

  add = input('Would you like to add more CSVs? (y or n)? ')
  if add == 'y':
    # IN THE FUTURE, ask for user input for the new CSV they would like to add
    
    # grab temp csv and convert back into array
    oldCSV = grabCSV('temp.csv')
    #grab new csv inputted by user, then add onto temp array
    grabnewCSV = '220708_Edit.csv'
    newCSV = grabCSV(grabnewCSV)
    
    # see if temp csv and new csv are from the same study (703 or 704)

    # They are from the same study
    #print ("oldCSV[1][0]:" + oldCSV[1][3] + " vs. NewCSV[1][0]: " + newCSV[1][0] )
    #print(  str(len(oldCSV)) + " VS. " + str(len(newCSV))) 
    # if first virus is equal to each other, then data is from the same study
    # THIS WORKS :DDD, randomly adds another num column, figure out how to delete because there are two 
    if oldCSV[1][3] == newCSV[1][0]:
      # Add ic50 antibody numbers to main dataset
      for column in range(findAntiIndex(newCSV), firstIC80(newCSV)):
        for row in range (0, len(newCSV)):
            oldCSV[row].append(newCSV[row][column])
            
      # Add ic80 antibody numbers to main dataset
      for column in range(firstIC80(newCSV), len(newCSV[0])):
        for row in range (1 , len(newCSV)):
            oldCSV[row + len(newCSV) -1].append(newCSV[row][column])
      
      convertCSV(oldCSV)
      
    #They are not from the same study
    else:
      # same CSV as new CSV
      newOrgCSV = organizeData(grabnewCSV)
            
      for mainA in range(7, len(oldCSV[0])):
        sameAntiBody = False
        for newA in range(7, len(newOrgCSV[0])):
          
          # IT COMPLETELY KILLED MY GRAPH
          # FIGURE THIS OUT 
          print ( oldCSV[0][mainA] + ' vs ' + newOrgCSV[0][newA])
          if oldCSV[0][mainA] == newOrgCSV[0][newA]:
            print("We are in")
            sameAntiBody = True 
        # Once it starts iterating through the graph it breaks!!!!
        if sameAntiBody:
          for rows in range(1, len(newOrgCSV)):
              #insert the new antibody into row of main antibody
              #newOrgCSV.insert(mainA, newOrgCSV[0][newA])
              print(newOrgCSV[rows])
              #
              convertCSV(newOrgCSV)
              #del newOrgCSV[rows][newA + 1 ]
          sameAntiBody = False
        else: 
          for rows in range(1, len(newOrgCSV)):
            #insert the new antibody into row of main antibody
            newOrgCSV[rows].insert(mainA, 'N/A')
      #I am lazy
      for newA in range (7, len(newOrgCSV[0])):
        sameAntiBody = False
        for mainA in range(7, len(oldCSV[0])):
          if oldCSV[0][mainA] == newOrgCSV[0][newA]:
            sameAntiBody = True
        if not sameAntiBody:
          oldCSV[0].append(newOrgCSV[0][newA])
      #delete unneeded header
      del newOrgCSV[0]

      #for newantibody
      # combine csvs and turn into new file :D
      combinedCSV = oldCSV + newOrgCSV
      #convertCSV(combinedCSV)

            
      
            
     
        
    # if they are from the same study, then you only need to add new columns for new antibodies

    # if they are from different studies you will have to add new rows and columns for both viruses and antibodies


# Functions

def organizeData(csv):
  header = [
  'Study', 'Treatment', 'Virus', 'VirusID', 'AssayID', 'Lab', 'Poscrit'
  ]
  data = grabCSV(csv)
  data.insert(0, header)
  rows = len(data)
  study(data, rows)
  addTreatment(data, rows)
  addNullVirusID(data, rows)
  addNullAssayID(data, rows)
  addLab(data, rows)
  addAntiBody(data)
  FINALdata = addPoscrit(data, rows)

  
  return FINALdata
  
  
def addTreatment(data, rows):
  # asks for treatment like Placebo or VRC01, and will add the treatment to each row
  treatment = input("Enter the treatment: ")
  for i in range(1, rows):
    data[i].insert(1, treatment)


def addLab(data, rows):
  #asks for lab name and will add the lab to each row
  labName = input("Enter lab name: ")
  for i in range(1, rows):
    data[i].insert(5, labName)


def addNullVirusID(data, rows):
  ID = False
  for i in range(len(data[1])):
    #  data[1] is the header row
    # 220801 has 'PTID', so it messed up code (function used to look for just 'ID') Need to find a better way to find rather than typing just ID. 
    if data[1][i].upper().find('VIRUS ID') != -1:
      ID = True
      # If there is no virus ID, add N/A
      break
  if not ID:
    for i in range(1, rows):
      data[i].insert(3, 'N/A')


def addNullAssayID(data, rows):
  ID = False
  for i in range(len(data[1])):
    #  data[1] is the header row
    if data[1][i].upper().find('ASSAY ID') != -1:
      ID = True
      break
  # If there is no virus ID, add N/A
  if not ID:
    for i in range(1, rows):
      data[i].insert(4, 'N/A')


# converts code into CSV
def convertCSV(data):
  dataframe_array = pd.DataFrame(data)
  dataframe_array.to_csv('temp.csv', index=False)


def study(data, rows):
  for i in range(1, rows):
    index = data[i][0]
    #print(index)
    searchStudy = index.find('70')
    study = index[searchStudy - 1:searchStudy + 3 ]
    data[i].insert(0, study)


# Adds all antibodies into header
def addAntiBody(data):
  #goes into header
  for i in range(len(data[1])):

    # if finds number (knows that it is a antibody), then adds to antibody to data
    if hasNumbers(data[1][i]):

      #adds all antibody names to the actual header
      for j in range(i, (len(data[1]))):
        data[0].append(data[1][j])
      #deletes the unneeded row
      del data[1]
      break


def hasNumbers(inputString):
  return any(char.isdigit() for char in inputString)


def addPoscrit(data, rows):
  # Code will take in 2d array (single csv previously)
  # Will read virus name of first virus, then will add 50% poscrit
  # until it sees that the name of the first virus is the same again
  # (two of same virus name means it is a new poscrit)
  # when it sees the same virus name, it will add 80% poscrit to each row

  firstAntiBody = data[0][7]

  # create temp array that you will add (ic80 part)
  #We don't have to worry about memory/pointers with this deepcopy function
  tempData = deepcopy(data)
  del tempData[0]

  ic80First = 9999999

  # look for first ic80, so that you can move that antibody and all following antibodies to the bottoms rows
  for i in range(8, len(data[0])):
    if (firstAntiBody == data[0][i]):
      ic80First = i - 1
      break

  # deleting ic80 data points & adding the poscrit ic50
  for i in range(1, len(data)):

    del data[i][ic80First:len(data[i])]
    data[i].insert(6, "50%")

  # deleting ic50 & adding ic80 in temp csv
  for i in range(len(tempData)):

    del tempData[i][6:ic80First]
    tempData[i].insert(6, "%80")

  # Delete the headers that were once ic80
  del data[0][ic80First + 1:len(data[0])]

  # combine the two csvs
  return data + tempData


# Adding other csv will be very difficult
def grabCSV( name ):
  with open(name, encoding='utf8', errors='ignore') as f:

    for i, line in enumerate(f):
      # Does not grab the Headers of csv into the array

      reader = csv.reader(f)
      data = list(reader)
  return data

#find the first antibody
def findAntiIndex(CSV):
  for i in range(len(CSV[0])):

    # if finds number (knows that it is a antibody)
    if hasNumbers(CSV[0][i]):
      return i
      
def findAntiName(CSV):
  for i in range(len(CSV[0])):

    # if finds number (knows that it is a antibody)
    if hasNumbers(CSV[0][i]):
      return CSV[0][i]

def firstIC80(CSV):
  firstAnti = findAntiName(CSV)
  
  for i in range(findAntiIndex(CSV) + 1, len(CSV[0])):
    if (findAntiName(CSV) == CSV[0][i]):
      ic80First = i 
      break
  
  return ic80First
if __name__ == '__main__':
  main()
