import subprocess
from os import rename, path, listdir, remove
from mutagen.flac import FLAC, Picture
from mutagen.id3 import PictureType
from re import sub

WALKMAN_DIR = path.expanduser('~/Music/walkman/MUSIC/')
PLAYLISTS_DIR = path.join(WALKMAN_DIR, '_Playlists')
THIS_DIR = path.expanduser('~/Repos/personal/scripts/')
FFMPEG_SCRIPT = 'flactomp3.sh'
SHELL_DIR = '/bin/bash'

MP3_BITRATE_K = 320
JPEG_PIXELS = 256
VERBOSE = True

FLAC_EXT = '.flac'
TIT_TAG = 'TITLE'
VSTS = 'status: '
VERR = 'error: '
ART_NAME = '_coverart.jpg'
BAD_CHAR_REGEX = '[<>:"/\\|?*]'
REPLACE_CHAR = '%'
BAD_TAGS = ['LYRICS', 'COMMENT', 'COPYRIGHT', 'LABEL', 'PUBLISHER']

def vprint(arg):
  if VERBOSE:
    print(arg)

def getAlbumDirList():
  vprint(f'{VSTS}getting album dirs...')
  command = f'find "{WALKMAN_DIR}" -mindepth 2 -type d'
  process = subprocess.run(
    command,
    capture_output=True,
    shell=True,
    text=True,
    executable=SHELL_DIR
  )
  return process.stdout.strip().splitlines()

def convertFLACtoMP3s():
  vprint(f'{VSTS}converting FLACs to MP3s...')
  subprocess.run([path.join(THIS_DIR, FFMPEG_SCRIPT)])

def sanitizeNames(albumDirList):
  for albumDir in albumDirList:
    vprint(f'{VSTS}sanitizing names ({path.basename(albumDir)})...')
    for song in listdir(albumDir):
      songPath = path.join(albumDir, song)
      if songPath[-5:].lower() != FLAC_EXT:
        continue
      audioFile = FLAC(songPath)
      trackTitle = f'{audioFile.get(TIT_TAG)[0]}{FLAC_EXT}'
      santizedName = sub(BAD_CHAR_REGEX, REPLACE_CHAR, trackTitle)
      if trackTitle != santizedName:
        rename(songPath, path.join(path.dirname(songPath), santizedName))
    
def sanitizeTags(albumDirList):
  for albumDir in albumDirList:
    vprint(f'{VSTS}sanitizing tags ({path.basename(albumDir)})...')
    artPath = '-1'
    for song in listdir(albumDir):
      songPath = path.join(albumDir, song)
      if songPath[-5:].lower() != FLAC_EXT:
        continue
      audioFile = FLAC(songPath)
      for badTag in BAD_TAGS:
        if audioFile.get(badTag) == None:
          continue
        else:
          audioFile.pop(badTag)
      audioFile.save()

def sanitizeCoverArt(albumDirList):
  for albumDir in albumDirList:
    rawArtPath = path.join(albumDir, ART_NAME)
    formattedArtPath = f'{rawArtPath[:-4]}.jpg'
    if albumDir == PLAYLISTS_DIR:
      continue
    for song in listdir(albumDir):
      audioFile = FLAC(path.join(albumDir, song))
      if not path.isfile(formattedArtPath):
        pics = audioFile.pictures
        if len(pics) > 1:
          raise RuntimeError(f'{VERR}has two pictures ({listdit(albumDir[0])})')
        with open(rawArtPath, "wb") as f:
          f.write(pics[0].data)
        vprint(f'{VSTS}formatting {rawArtPath}')
        subprocess.run(
          f'magick "{rawArtPath}" -resize 256x256 -interlace none "{formattedArtPath}"',
          shell=True,
          executable=SHELL_DIR,
        )
      audioFile.clear_pictures()
      pic = Picture()
      with open(formattedArtPath, "rb") as f:
        pic.data = f.read()
      pic.type = PictureType.COVER_FRONT
      pic.mime = u"image/jpeg"
      pic.width = JPEG_PIXELS
      pic.height = JPEG_PIXELS
      pic.depth = 16
      audioFile.add_picture(pic)
      audioFile.save()
      remove(rawArtPath)

def main():
  albumDirList = getAlbumDirList()
  sanitizeNames(albumDirList)
  sanitizeTags(albumDirList)
  sanitizeCoverArt(albumDirList)
  convertFLACtoMP3s()

main()