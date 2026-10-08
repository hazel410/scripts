#!/bin/bash'

# Source - https://stackoverflow.com/a/55762551
# Posted by Filippos, modified by community. See post 'Timeline' for change history
# Retrieved 2026-10-08, License - CC BY-SA 4.0

for f in *.flac
  do ffmpeg -i "${f}" -ab 320k -map_metadata 0 -id3v2_version 3 "${f%.*}".mp3
done;
