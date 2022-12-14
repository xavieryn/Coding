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

# Fuzzy matching will be thought about in the future
# Next Steps
# Work on a simple and effective interface 

import pandas as pd
import csv
import glob
import Organize

# FILE PATHS WITH GLOB
path = 'CSV'
allFiles = glob.glob(path+ '/*.csv')

#print(allFiles)
#print(glob.glob(path +'/*.csv'))

def main():
  
  finalData = organizeData(allFiles[0])
  
  for csv in range(1, len(allFiles)):
    
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
      

    
    #They are not from the same study
    else:
      # same CSV as new CSV
      newOrgCSV = organizeData(grabTempData)

      #Starts from first antibody      
      for mainA in range(7, len(finalData[0])):
        sameAntiBody = False
        # Look for if the two column's are the same antibody
        for newA in range(7, len(newOrgCSV[0])):
          
          if finalData[0][mainA] == newOrgCSV[0][newA]:
            sameAntiBody = True 
        if not sameAntiBody: 
          for rows in range(1, len(newOrgCSV)):
            #insert the new antibody into row of main antibody
            newOrgCSV[rows].insert(mainA, None)
      
      
      # See if the antibody is new and if it is, then add to header   
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
      finalData = newOrgCSV + finalData


  addNA(finalData)
  convertCSV(finalData)

            
# Functions
def organizeData(csv):
  header = [
  'Study', 'Treatment', 'Virus', 'VirusID', 'AssayID', 'Lab', 'Poscrit'
  ]
  data = grabCSV(csv)
  data.insert(0, header)
  rows = len(data)
  Organize.study(data, rows)
  Organize.addTreatment(data, rows, csv)
  Organize.addNullVirusID(data, rows)
  Organize.addNullAssayID(data, rows)
  Organize.addLab(data, rows)
  Organize.addAntiBody(data)
  FINALdata = Organize.addPoscrit(data, rows)

  
  return FINALdata
  
# converts code into CSV
def convertCSV(data):
  finalFileName = 'OrganizeCSV/FINALDATAWITHOUTSIGNS.csv'
  dataframe = pd.DataFrame(data)
  dataframe.to_csv(finalFileName, index=False, header=False, date_format=False)
  
  #set column names equal to values in row index position 0
  dataframe.columns = dataframe.iloc[0]
  #remove first row from DataFrame
  dataframe = dataframe[1:]

  dataframe = dataframe.applymap(lambda x: x.replace('<','') if x != None else x)
  dataframe = dataframe.applymap(lambda x: x.replace('>','') if x != None else x)
  print(dataframe.head((1)))
  dataframe['VRC34.01'] = dataframe['VRC34.01'].astype(float)

  print(dataframe['VRC34.01'].mean(skipna=True))
  dataframe.to_csv(finalFileName, index=False, header=False, date_format=False)
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

# Adds N/A to every empty cell
def addNA(finalData):
  for i in range(len(finalData)):
    for j in range(len(finalData[i])):
      if finalData[i][j] == '':
        finalData[i][j] = None
    # Append N/A to array until it is the same length as header 
    while len(finalData[i]) < len(finalData[0]):
      finalData[i].append(None)




if __name__ == '__main__':
  main()
