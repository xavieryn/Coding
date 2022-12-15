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
import organize

# The amount of rows should never change (apart from when ic80 get concatenated to the bottom of ic50.)

# The only column changes that should be made are the additions of new antibodies.
# When there is a new column, append the name of the antibody to the header.

def main():
  
  FINALdata = organizeData('CSV/220801_Edit.csv')
  convertCSV(FINALdata)

  add = input('Would you like to add more CSVs? (y or n)? ')
  if add == 'y':
    # IN THE FUTURE, ask for user input for the new CSV they would like to add
    
    # grab temp csv and convert back into array
    oldCSV = grabCSV('CSV/ProbBroken.csv')
    #grab new csv inputted by user, then add onto temp array
    grabnewCSV = 'CSV/HVTN_704_Edit2.csv'
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
          #print ( oldCSV[0][mainA] + ' vs ' + newOrgCSV[0][newA])
          if oldCSV[0][mainA] == newOrgCSV[0][newA]:
            sameAntiBody = True 
        # Once it starts iterating through the graph it breaks!!!!
        if sameAntiBody:
          for rows in range(1, len(newOrgCSV)):
              #insert the new antibody into row of main antibody
              #newOrgCSV.insert(mainA, newOrgCSV[0][newA])
              #print(newOrgCSV[rows])
              
              convertCSV(newOrgCSV)
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
      convertCSV(combinedCSV)

            
      
            
     
        
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
  organize.study(data, rows)
  organize.addTreatment(data, rows)
  organize.addNullVirusID(data, rows)
  organize.addNullAssayID(data, rows)
  organize.addLab(data, rows)
  organize.addAntiBody(data)
  FINALdata = organize.addPoscrit(data, rows)

  
  return FINALdata
  


# converts code into CSV
def convertCSV(data):
  dataframe_array = pd.DataFrame(data)
  dataframe_array.to_csv('CSV/FINALDATA.csv', index=False)

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
    if organize.hasNumbers(CSV[0][i]):
      return i
      
def findAntiName(CSV):
  for i in range(len(CSV[0])):

    # if finds number (knows that it is a antibody)
    if organize.hasNumbers(CSV[0][i]):
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
