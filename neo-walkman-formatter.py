import subprocess
from os import rename, path, listdir
from mutagen.flac import FLAC, Picture
from re import sub

WALKMAN_DIR = path.expanduser('~/Music/walkman/MUSIC/')
PLAYLISTS_DIR = path.join(WALKMAN_DIR, '_Playlists')
MP3_BITRATE_K = 320
JPEG_PIXELS = 256
FLAC_EXT = '.flac'
TIT_TAG = 'TITLE'
BAD_CHAR_REGEX = '[<>:"/\\|?*]'
REPLACE_CHAR = '%'
ART_NAME = 'silly-billy-time.jpg'
BAD_TAGS = ['LYRICS', 'COMMENT', 'COPYRIGHT', 'LABEL', 'PUBLISHER']

def getFlacPathList():
  command = f'find /home/hazel/Music/walkman/MUSIC/ -mindepth 3 -type f -name "*{FLAC_EXT}"'
  process = subprocess.run(
    command,
    capture_output=True,
    shell=True,
    text=True,
    executable="/bin/bash",
  )
  return process.stdout.strip().splitlines()

def formatCoverArt(artPath):
  if artPath[-4:].lower() == '.png' or artPath[-4:].lower() == '.jpg':
    command = f'magick {artPath} -resize 256x256 -interlace none {artPath[:-4]}.jpg'
  elif artPath[-5:].lower() == '.jpeg':
    command = f'magick {artPath} -resize 256x256 -interlace none {artPath[:-5]}.jpg'
  else:
    raise RuntimeError('also didnt code this')

def sanitizeFlacNames(flacPathList):
  for flacPath in flacPathList:
    audioFile = FLAC(flacPath)
    trackTitle = f'{audioFile.get(TIT_TAG)[0]}{FLAC_EXT}'
    santizedName = sub(BAD_CHAR_REGEX, REPLACE_CHAR, trackTitle)
    if trackTitle != santizedName:
      rename(flacPath, path.join(path.dirname(flacPath), santizedName))
    
def sanitizeTags(flacPathList):
  for flacPath in flacPathList:
    # remove bad tags
    audioFile = FLAC(flacPath)
    for badTag in BAD_TAGS:
      if audioFile.get(badTag) == None:
        continue
      else:
        audioFile.pop(badTag)
    
    # get picture
    artPath = path.join(path.dirname(flacPath), ART_NAME)
    if path.isfile(artPath):
      continue
    else:
      pics = audioFile.pictures
      if len(pics) > 1:
        raise RuntimeError('you didnt program this')
      else:
        with open(artPath, "wb") as f:
          f.write(pics[0].data)
        formatCoverArt(artPath)
    
    # overwrite original picture

def convertFLACtoMP3s(flacPathList):
  pass

def main():
  flacPathList = getFlacPathList()
  sanitizeFlacNames(flacPathList)
  flacPathList = getFlacPathList() # update paths due to renaming above
  
  sanitizeTags(flacPathList)
  
  # convertFLACtoMP3s()

main()