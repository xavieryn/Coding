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


# The amount of rows should never change (apart from when ic80 get concatenated to the bottom of ic50.)

# The only column changes that should be made are the additions of new antibodies.
# When there is a new column, append the name of the antibody to the header.

import pandas as pd
import csv
import glob
import Organize

# FILE PATHS WITH GLOB
path = 'CSV'
allFiles = glob.glob(path+ '/*.csv')

print(allFiles)
print(glob.glob(path +'/*.csv'))
  
# FIGURE OUT WHAT FILE I NEEEEEED TO CLOSEEEEE
# https://stackoverflow.com/questions/62287259/csv-file-not-updating-until-script-is-terminated-when-continuously-appending-fil
def main():
  
  finalData = organizeData(allFiles[0])
  
  for csv in range(1, len(allFiles)):
    if csv > 1:
      finalData = grabCSV('OrganizeCSV/FINALDATA')
    # NEED TO UPDATE FINAL DATA, SO THAT THE CSV CAN APPEND
    grabTempData = (allFiles[csv])
    tempData = grabCSV(grabTempData)
     # They are from the same study
    # if first virus is equal to each other, then data is from the same study, but just with different antibodies tested 
    if finalData[1][3] == tempData[1][0]:
      # Add ic50 antibody numbers to main dataset
      for column in range(findAntiIndex(tempData), firstIC80(tempData)):
        for row in range (0, len(tempData)):
            finalData[row].append(tempData[row][column])
            
      # Add ic80 antibody numbers to main dataset
      for column in range(firstIC80(tempData), len(tempData[0])):
        for row in range (1 , len(tempData)):
            finalData[row + len(tempData) -1].append(tempData[row][column])
      
      convertCSV(finalData)

     #They are not from the same study
    else:
      # same CSV as new CSV
      newOrgCSV = organizeData(grabTempData)
            
      for mainA in range(7, len(finalData[0])):
        sameAntiBody = False
        for newA in range(7, len(newOrgCSV[0])):
          
          # IT COMPLETELY KILLED MY GRAPH
          # FIGURE THIS OUT 
          #print ( finalData[0][mainA] + ' vs ' + newOrgCSV[0][newA])
          if finalData[0][mainA] == newOrgCSV[0][newA]:
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
        for mainA in range(7, len(finalData[0])):
          if finalData[0][mainA] == newOrgCSV[0][newA]:
            sameAntiBody = True
        if not sameAntiBody:
          finalData[0].append(newOrgCSV[0][newA])
      #delete unneeded header
      del newOrgCSV[0]
      #Put newData ontop of old data
      newOrgCSV.insert(0,finalData[0])
      del finalData[0]

      #for newantibody
      # combine csvs and turn into new file :D
      combinedCSV = newOrgCSV + finalData
      convertCSV(combinedCSV)




            
      
            
# Functions

def organizeData(csv):
  header = [
  'Study', 'Treatment', 'Virus', 'VirusID', 'AssayID', 'Lab', 'Poscrit'
  ]
  data = grabCSV(csv)
  data.insert(0, header)
  rows = len(data)
  Organize.study(data, rows)
  Organize.addTreatment(data, rows)
  Organize.addNullVirusID(data, rows)
  Organize.addNullAssayID(data, rows)
  Organize.addLab(data, rows)
  Organize.addAntiBody(data)
  FINALdata = Organize.addPoscrit(data, rows)

  
  return FINALdata
  


# converts code into CSV
def convertCSV(data):
  finalFileName = 'OrganizeCSV/FINALDATA.csv'
  dataframe_array = pd.DataFrame(data)
  dataframe_array.to_csv(finalFileName, index=False)

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
    if Organize.hasNumbers(CSV[0][i]):
      return i
      
def findAntiName(CSV):
  for i in range(len(CSV[0])):

    # if finds number (knows that it is a antibody)
    if Organize.hasNumbers(CSV[0][i]):
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
