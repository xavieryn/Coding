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
