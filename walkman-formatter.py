from tinytag import TinyTag
from os import rename, path, system, listdir
from sys import stdout
from mutagen.id3 import ID3

# config consts 
WALKMAN_DIR = path.expanduser("~/Music/walkman/MUSIC/")
PLAYLISTS_DIR = path.join(WALKMAN_DIR, "_Playlists")
MP3_BITRATE_K = 320

# helpers
def tryPrependTrackNo(songPath):
  audio = TinyTag.get(songPath)
  trackNo = audio.track
  trackTitle = audio.title
  folderPath, fileName = path.split(songPath)
  if fileName == f'{trackNo:02} {trackTitle}':
    return 0
  else: 
    # note this probably breaks if more than 99 songs in an album? probably not too big a concern
    rename(songPath, path.join(folderPath, f'{trackNo:02} {trackTitle}'))

def tryConvertFLACtoMP3(flacPath):
  if flacPath[:-5].lower == '.flac' 
    system(f'ffmpeg -i "{flacPath}" -v error -ab {MP3_BITRATE_K}k -map_metadata 0 -id3v2_version 3 "{flacPath[:-4]}".mp3')
    system(f'rm {flacPath}')
    return 1
  else if flacPath[:-4].lower == '.mp3':
    return 0

def tryStripMetadata(songPath):
  pass

# the big one
def main(): 
  """assumes the following dir structure
  WALKMAN_DIR
  ├── PLAYLISTS_DIR/
  │   ├── playlist1/
  │   │   └── ...
  │   └── playlist2/
  │       └── ...
  ├── artist1/
  │   ├── album1/
  │   │   └── ...
  │   └── album2/
  │       └── ...
  └── artist2/
      ├── album1/
      │   └── ...
      └── album2/
          └── ...
  i.e., every song is three directories deep (WALKMAN_DIR/artist/album/song.mp3)"""
  
  # pre loop inits
  totalArtists = len(listdir(WALKMAN_DIR))
  currentNum = 0
  flacsConvertedNum = 0
  songsFormattedNum = 0

  # evil loop time
  for artist in listdir(WALKMAN_DIR):
    currentNum += 1
    stdout.write(f'\rstatus: artist progress {currentNum}/{totalArtists}')
    artist_dir = path.join(WALKMAN_DIR, artist)
  
    for album in listdir(artist_dir):
      album_dir = path.join(artist_dir, album)
      for song in listdir(album_dir):
        song_dir = path.join(album_dir, song)
        flacsConvertedNum += tryConvertFLACtoMP3(song_dir)
        if artist_dir != PLAYLISTS_DIR:
          songsFormattedNum += tryPrependTrackNo(song_dir)
  
  stdout.write(f'\n\rstats.num_renamed: {songsFormattedNum}')
  stdout.write(f'\n\rstats.flacs_converted: {flacsConvertedNum}\n')
  
main()