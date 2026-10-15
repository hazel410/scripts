from os import rename, path, system, listdir
from sys import stdout
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
  
class walkmanFormatter():
  def __init__(self):
    self.WALKMAN_DIR = path.expanduser("~/Music/walkman/MUSIC/")
    self.PLAYLISTS_DIR = path.join(WALKMAN_DIR, "_Playlists")
    self.MP3_BITRATE_K = 320
    self.pairsToRename = []
    self.pairsToConvert = []
    self.tagsUsed = []
  
  def updatePairsToRename(self):
    for artist in listdir(self.WALKMAN_DIR):
      artistDir = path.join(self.WALKMAN_DIR, artist)
      for album in listdir(artistDir):
        albumDir = path.join(artistDir, album)
        for song in listdir(albumDir):
          songExt = song[song.rfind('.'):].lower()
          songPath = path.join(albumDir, song)
          
          if songExt == '.flac':
            audioFile = FLAC(songPath)
          elif songExt == '.mp3':
            audioFile = MP3(songPath)
          else:
            raise RuntimeError(f'error: {songPath} is not mp3 or flac')
          
          songTitle = (audioFile['title'])[0].replace('/', '\\')
          songTrackNo = (audioFile['tracknumber'])[0]
          songNameFormatted = f'{songTrackNo:02} {songTitle}'
          
          if (artistDir != self.PLAYLISTS_DIR) and (song != songNameFormatted):
            self.pairsToRename.append((songPath, songNameFormatted))
          
          
    
  def updatePairsToConvert():
    pass

  def main():
    updatePairsToRename()
    # executePairsToRename()

    updateUsedTags()

    # updatePairsToConvert()
    # executePairsToConvert()
            

