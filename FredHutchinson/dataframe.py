import pandas as pd

def main():
  

  header = [
  'Study', 'Treatment', 'Virus', 'VirusID', 'AssayID', 'Lab', 'Poscrit'
  ]
  df = pd.read_csv('CSV/220708_Edit.csv')

  #print(df.columns)
  #print(len(df.index))
  df.columns = df.iloc[0]
  df = df[1:]
  
  
  study(df)
  addTreatment(df)
  addLab(df)
  addNullVirusID(df, df.columns)
  addNullAssayID(df, df.columns)

 

def study(data):
  virusName = data.loc[1][0]
  searchStudy = virusName.find('70')
  study = virusName[searchStudy - 1:searchStudy + 3 ]
  data.insert(0, 'Study', study)

def addTreatment(data):
  # asks for treatment like Placebo or VRC01, and will add the treatment to each row
  treatment = input("Enter the treatment: ")
  data.insert(2,'Treatment', treatment )

def addLab(data):
  #asks for lab name and will add the lab to each row
  labName = input("Enter the Lab: ")
  data.insert(3,'Lab', labName )

def addNullVirusID(data, header):
  # Sees if header has vIRUS ID, if not, then add column with N/A
    ID = False
    for i in range(len(data.loc[1])):
    #  data[1] is the header row
    # 220801 has 'PTID', so it messed up code (function used to look for just 'ID') Need to find a better way to find rather than typing just ID. 
      if data.loc[1][i].upper().find('VIRUS ID') != -1:
        ID = True
        # If there is no virus ID, add N/A
        break
    if not ID:
      data.insert(4, 'VIRUS ID', 'N/A')

def addNullAssayID(data, header):
  # Sees if header has vIRUS ID, if not, then add column with N/A
    ID = False
    for i in range(len(data.loc[1])):
    #  data[1] is the header row
    # 220801 has 'PTID', so it messed up code (function used to look for just 'ID') Need to find a better way to find rather than typing just ID. 
      if data.loc[1][i].upper().find('ASSAY ID') != -1:
        ID = True
        # If there is no virus ID, add N/A
        break
    if not ID:
      data.insert(5, 'ASSAY ID', 'N/A')






if __name__ == '__main__':
  main()