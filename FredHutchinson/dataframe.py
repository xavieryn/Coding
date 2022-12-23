import pandas as pd

def main():
  

  header = [
  'Study', 'Treatment', 'Virus', 'VirusID', 'AssayID', 'Lab', 'Poscrit'
  ]
  df = pd.read_csv('CSV/220708_Edit.csv')

  print(df.columns)
  print(len(df.index))
  df.columns = df.iloc[0]
  df = df[1:]
  print(df.columns)
  print(len(df.index))
  

  addTreatment(df)

  print(df)

def addTreatment(data):
  # asks for treatment like Placebo or VRC01, and will add the treatment to each row
  treatment = input("Enter the treatment: ")
  data.insert(1,'Treatment', treatment )

def addLab(data):
  #asks for lab name and will add the lab to each row
  labName = input("Enter the Lab: ")
  data.insert(2,'Lab', labName )



if __name__ == '__main__':
  main()