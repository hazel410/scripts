import subprocess
from os import rename, path, listdir, remove
from mutagen.flac import FLAC
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, APIC, error
from re import sub

"""
converts music from my library to be put
on my sony walkman nwz-e385

specification document used for reference
https://web.archive.org/web/20180913152244/http://helpguide.sony.net/gbmig/44666681/v1/eng/contents/10/01/01/01.html
"""

# consts
THIS_DIR = path.expanduser('~/Repos/personal/scripts/')
WALKMAN_DIR = path.expanduser('~/Music/walkman/MUSIC/')
PLAYLISTS_DIR = path.join(WALKMAN_DIR, '_Playlists')
SHELL_DIR = '/bin/bash'
FFMPEG_SCRIPT = path.join(THIS_DIR, 'flactomp3.sh')

MP3_BITRATE_K = 320 # this must be within [32, 320]
JPG_PX = 256 # must be divisble by 2
PRINT_STATUS = True
PRINT_DEBUG = True

ART_NAME = '_coverart.jpg'
REPLACE_CHAR = '%'

BAD_CHAR_REGEX = '[<>:"/\\|?*]'
TIT_TAG = 'TITLE'
BAD_TAGS = ['LYRICS', 'COMMENT', 'COPYRIGHT', 'LABEL', 'PUBLISHER']

# print wrappers
def dPrint(arg):
  if PRINT_DEBUG:
    print(f'{'debug: '}{arg}')

def sPrint(arg):
  if PRINT_STATUS:
    print(f'{'status: '}{arg}')

# shell funcs
def getFlacAlbumDirList(): 
  sPrint('getting album dirs...')
  command = f'find "{WALKMAN_DIR}" -mindepth 3 -type f -name "*.flac" -print0'
  process = subprocess.run(
    command,
    capture_output=True,
    shell=True,
    text=True,
    executable=SHELL_DIR
  )
  flacList = process.stdout.split("\x00")[:-1]
  dirList = []
  # this is prob super inefficient but ... shrug
  for flacPath in flacList:
    dirName = path.dirname(flacPath)
    if dirName not in dirList:
      dirList.append(dirName)
  return dirList

def convertFLACtoMP3s():
  #TODO: make this not reference an external file ... somehow
  sPrint('converting FLACs to MP3s...')
  subprocess.run([path.join(THIS_DIR, FFMPEG_SCRIPT)])

def formatCoverArt(artPath):
  subprocess.run(
    f'magick "{artPath}" -resize {JPG_PX}x{JPG_PX} -interlace none "{artPath}"',
    shell=True,
    executable=SHELL_DIR
  )

# metadata handlers
def sanitizeNames(albumDirList):
  sPrint('santizing FLAC names...')
  for albumDir in albumDirList:
    for song in listdir(albumDir):
      songPath = path.join(albumDir, song)
      audioFile = FLAC(songPath)
      trackTitle = f'{audioFile.get(TIT_TAG)[0]}.flac'
      santizedName = sub(BAD_CHAR_REGEX, REPLACE_CHAR, trackTitle)
      if trackTitle != santizedName:
        rename(songPath, path.join(path.dirname(songPath), santizedName))
        dPrint(f'sanitized name of ({path.basename(albumDir)})')
    
def removeTags(albumDirList):
  sPrint('removing bad FLAC tags...')
  for albumDir in albumDirList:
    artPath = '-1'
    for song in listdir(albumDir):
      songPath = path.join(albumDir, song)
      audioFile = FLAC(songPath)
      for badTag in BAD_TAGS:
        if audioFile.get(badTag) == None:
          continue
        else:
          audioFile.pop(badTag)
      audioFile.save()
      dPrint(f'removed tags of ({path.basename(albumDir)})')

def popCoverArt(albumDirList):
  """
  get cover art from album, write cover art to file, 
  and delete cover art tag for all songs in album
  """
  sPrint('popping FLAC cover art...')
  for albumDir in albumDirList:
    # skip playlists dir, write code later
    if albumDir == PLAYLISTS_DIR:
      continue
    
    artPath = path.join(albumDir, ART_NAME)

    # if not previously popped, pop the cover art
    dPrint(artPath)
    if not path.isfile(artPath):
      firstSong = listdir(albumDir)[0]
      firstAudioFile = FLAC(path.join(albumDir, firstSong))
      coverArt = firstAudioFile.pictures
      if len(coverArt) > 1:
        raise RuntimeError(f'error: has two pictures ({firstSong})')
      with open(artPath, 'wb') as f:
        f.write(coverArt[0].data)
      dPrint(f'wrote {artPath}')
      formatCoverArt(artPath)
      dPrint(f'converted {artPath}')
    
    # remove album art from all songs
    for fileName in listdir(albumDir):
      if fileName[-5:].lower() != '.flac':
        continue
      audioFile = FLAC(path.join(albumDir, fileName))
      audioFile.clear_pictures()
      audioFile.save()

def addFormattedCoverArt(albumDirList):
  sPrint('adding cover art to MP3s...')
  for albumDir in albumDirList:
    artPath = path.join(albumDir, ART_NAME)
    if not path.isfile(artPath):
      raise RuntimeError(f'error: not a file {artPath}')
    for fileName in listdir(albumDir):
      if fileName[-4:].lower() != '.mp3':
        continue
      songPath = path.join(albumDir, fileName)
      # Source - https://stackoverflow.com/a/75268284
      # Posted by ccpizza, modified by community. See post 'Timeline' for change history
      # Retrieved 2026-11-18, License - CC BY-SA 4.0
      audioFile = MP3(songPath, ID3=ID3)
      audioFile.tags.add(
        APIC(
          encoding=3,
          mime="image/jpeg",
          type=3,
          desc='Cover',
          data=open(artPath, mode='rb').read()
        )
      )
      # END stack overflow 
      audioFile.save()
    remove(artPath)


# main lol
def main():
  AlbumDirList = getFlacAlbumDirList()
  sanitizeNames(AlbumDirList)
  removeTags(AlbumDirList)
  popCoverArt(AlbumDirList)
  convertFLACtoMP3s()
  addFormattedCoverArt(AlbumDirList)
  sPrint('done! :3')

main()