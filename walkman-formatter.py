from os import rename, path, system, listdir
from sys import stdout
from time import time
from mutagen.flac import FLAC
from mutagen.mp3 import MP3

# # helpers
# def tryPrependMp3TrackNo(songPath):
#   audio = TinyTag.get(songPath, encoding='utf8')
#   trackNo = audio.track
#   trackTitle = (audio.title).replace('/', '\\')
#   folderPath, fileName = path.split(songPath)
#   if fileName == f'{trackNo:02} {trackTitle}':
#     return 0
#   else: 
#     # note this probably breaks if more than 99 songs in an album? probably not too big a concern
#     rename(songPath, path.join(folderPath, f'{trackNo:02} {trackTitle}.mp3'))
#     return 1

# def tryConvertFLACtoMP3(flacPath):
#   if flacPath[-5:].lower() == '.flac':
#     system(f'ffmpeg -i "{flacPath}" -v error -ab {MP3_BITRATE_K}k -map_metadata 0 -id3v2_version 3 "{flacPath[:-5]}.mp3"')
#     system(f'rm "{flacPath}"')
#     return 1
#   elif flacPath[-4:].lower() == '.mp3':
#     return 0
#   else:
#     raise RuntimeError(f'error: "{flacPath}" made me shit myself')

# # def tryStripMetadata(songPath):
# #   pass

# def sca

# # the big one
# def main(): 
#   """assumes the following dir structure
#   WALKMAN_DIR
#   ├── PLAYLISTS_DIR/
#   │   ├── playlist1/
#   │   │   └── ...
#   │   └── playlist2/
#   │       └── ...
#   ├── artist1/
#   │   ├── album1/
#   │   │   └── ...
#   │   └── album2/
#   │       └── ...
#   └── artist2/
#       ├── album1/
#       │   └── ...
#       └── album2/
#           └── ...
#   i.e., every song is three directories deep (WALKMAN_DIR/artist/album/song.mp3)"""
  
#   # pre loop inits
#   totalArtists = len(listdir(WALKMAN_DIR))
#   currentNum = 0
#   flacsConvertedNum = 0
#   songsFormattedNum = 0

#   # evil loop time
#   for artist in listdir(WALKMAN_DIR):
#     currentNum += 1
#     stdout.write(f'\rstatus: artist progress {currentNum}/{totalArtists}')
#     artist_dir = path.join(WALKMAN_DIR, artist)
  
#     for album in listdir(artist_dir):
#       album_dir = path.join(artist_dir, album)
#       for song in listdir(album_dir):
#         song_dir = path.join(album_dir, song)
#         flacsConvertedNum += tryConvertFLACtoMP3(song_dir)
#         if song_dir[-5:].lower() == '.flac':
#           song_dir = f'{song_dir[:-5]}.mp3'
#         if artist_dir != PLAYLISTS_DIR:
#           songsFormattedNum += tryPrependMp3TrackNo(song_dir)
  
#   stdout.write(f'\n\rstats.num_renamed: {songsFormattedNum}')
#   stdout.write(f'\n\rstats.flacs_converted: {flacsConvertedNum}\n')
  
"""
formatter workflow:
  replace disallowed chars in filename:
    ######
    if (filename == (track.title).replace(BADCHARS, GOODCHARS)):
      filename = track.title.replace(BADCHARS, GOODCHARS)
      rename or wtv

  remove unneccesary tags:
    ######
    for song in songs:
      for tag in song.tags:
        if tag in BAD_TAGS:
          tag.explodeEverywhere()

  convert embedded image to 256x256px BASELINE jpg:
    ######
    for song in songs:
      coverArt = song.cover
      if !isCoverArtFormatted(coverArt):
        coverArt = formatCoverArt(coverArt)

  convert flacs to 
    ######
    for song in songs:
      if isFLAC(song):
        convertFLACtoMP3(song)
"""


class walkmanFormatter():
  def __init__(self):
    # consts
    self.WALKMAN_DIR = path.expanduser("~/")
    self.PLAYLISTS_DIR = path.join(self.WALKMAN_DIR, "_Playlists")
    self.MP3_BITRATE_K = 320
    self.JPEG_PIXELS = 256
    self.FLAC_EXTENSION = '.flac'
    self.MP3_EXTENSION = '.mp3'
    self.BAD_CHARS = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    self.REPLACEMENT_CHAR = '{}'
    self.BAD_TAGS = ['LYRICS', 'COMMENT', 'COPYRIGHT', 'LABEL', 'PUBLISHER']
    self.VERBOSE_ERROR_PREFIX = 'error: '
    self.VERBOSE_STATUS_PREFIX = 'status: '

    # variables :3
    self.allSongPaths = []
    self.artistNumDict = {}
    self.artistSongsDict = {}

  def updateSongPathList(self):
    """
    updates the class variable self.allSongPaths with the full path of 
    every song in the walkman directory
    """
    musicDir = self.WALKMAN_DIR
    for artist in listdir(musicDir):
      artistDir = path.join(musicDir, artist)
      self.artistNumDict[artist] = 0
      self.artistSongsDict[artist] = []
      for album in listdir(artistDir):
        albumDir = path.join(artistDir, album)
        for song in listdir(albumDir):
          songDir = path.join(albumDir, song)
          self.allSongPaths.append(songDir)
          self.artistNumDict[artist] = self.artistNumDict[artist] + 1
          self.artistSongsDict[artist].append(songDir)
  
  def getAudioFile(self, songPath):
    if songPath[-5:].lower() == self.FLAC_EXTENSION:
      return FLAC(songPath)
    elif songPath[-4:].lower() == self.MP3_EXTENSION:
      return MP3(songPath)
    else:
      raise RuntimeError(f'{VERBOSE_ERROR_PREFIX}song not {self.FLAC_EXTENSION} or {self.MP3_EXTENSION}')

  def convertFLACtoMP3(self, flacPath):
    system(f'ffmpeg -i "{flacPath}" -v error -ab {self.MP3_BITRATE_K}k -map_metadata 0 -id3v2_version 3 "{flacPath[:-5]}{self.MP3_EXTENSION}"')
    system(f'rm "{flacPath}"')
  
  def convertDirToMP3(self, dir):
    for song in listdir(dir):
      if song[-5:] == self.FLAC_EXTENSION:
        self.convertFLACtoMP3(path.join(dir, song))

  # def formatBadSongNames():
  #   """
  #   checks if each song in self.allSongPaths is properly formatted,
  #   i.e. the filename of the song is the title tag of the song with
  #   disallowed characters replaced
  #   """
  #   for songPath in self.allSongPaths:
  #     audioFile = getAudioFile(songPath)
  #     fileName = path.basename(songPath)
  #     if fileName = 
  

        




# flac = FLAC('/home/hazel/Music/spotiflac/Adrianne Lenker/songs/anything.flac')   
# print(flac.tags)

# thing = walkmanFormatter()
# thing.updateSongPathList()
# for artist in thing.artistNumDict.keys():
#   numSongs = thing.artistNumDict[artist]
#   songPaths = thing.artistSongsDict[artist]
#   if numSongs < 10:
#     for path in songPaths:
#       print(path)

thing = walkmanFormatter()
thing.convertDirToMP3('/home/hazel/Music/walkman/MUSIC/Utsu-P/HAPPYPILLS')