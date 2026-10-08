from os import listdir
from os import rename
from os.path import join
from os.path import isdir
from sys import argv

def rreplace(oldSubstring, newSubstring, path="./"):
  dirContents = listdir(path)
  for entry in dirContents:
    entryPath = join(path, entry)
    if(isdir(entryPath)):
      rreplace(oldSubstring, newSubstring, entryPath)
    else:
      rename(entryPath, entryPath.replace(oldSubstring, newSubstring))

if __name__ == "__main__":
  if len(argv) == 3:
    rreplace(argv[1], argv[2])
  elif len(argv) == 4:
    rreplace(argv[1], argv[2], argv[3])
  else:
    raise RuntimeError('error: valid number of arguments not provided')
