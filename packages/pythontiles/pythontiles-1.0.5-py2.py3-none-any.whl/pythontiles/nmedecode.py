from . import parse
import os

class Decoder:
  def __init__(self, filename):
    self.number = None
    self.slashnum = None
    self.filename = filename
  def num(self, number):
    if number < 1 or number %1 != 0:
      raise TypeError("Enter Correct Input")
    self.number = number
  def check_file(self):
    if not self.filename[-4:] == ".nme":
      raise TypeError("Wrong File Type")
    return os.path.isfile(self.filename)
  def file_contents(self):
    file = open(self.filename, "r")
    content = file.readlines()
    file.close()
    returnval = content[self.number]
    self.slashnum = int(content[0])
    return returnval
  def decode(self):
    if not self.check_file():
      print("ERROR FILE NOT FOUND")
      quit()
    contents = self.file_contents()
    list = []
    i = 0
    for j in range(0, self.slashnum):
      text = parse.parse(contents, i, "/")
      list.append(text)
      i += len(text) + 1
    return list
def NME_Decode_Line(filename, number):
  dcdr = Decoder(filename)
  dcdr.num(number)
  return dcdr.decode()
def NME_Decode_File(filename):
  kale = Decoder(filename)
  if not kale.check_file():
    print("ERROR FILE NOT FOUND")
    quit()
  file = open(filename, "r")
  length = len(file.readlines())
  file.close()
  lists = []
  for i in range(1, length):
    lists.append(NME_Decode_Line(filename, i))
  return lists
