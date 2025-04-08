def parse(text, start, char):
  i = start
  returnVal = ""
  while text[i] != char:
    returnVal += text[i]
    i += 1
  return returnVal
