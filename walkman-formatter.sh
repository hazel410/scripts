#!/bin/bash

declare -r WALKMAN_DIR="$HOME/Music/walkman/MUSIC/"
declare -r MP3_BITRATE_K=320
declare -r JPEG_PIXELS=256
declare -r FLAC_EXT=".flac"
declare -r MP3_EXT=".mp3"
declare -r REPLACEMENT_CHAR="{}"
declare -ar BAD_CHARS=("<" ">" ":" "\"" "/" "\\" "|" "?" "*")
declare -ar BAD_TAGS=("LYRICS" "COMMENT" "COPYRIGHT" "LABEL" "PUBLISHER")

for char in "${BAD_CHARS[@]}"; do
  echo "$char"
done

# convert png -> baseline jpg 
# magick {name}.png -resize 256x256 -interlace none {name}.jpg 

# convert flac -> mp3
# ffmpeg -i "{flacPath}" -v error -ab {MP3_BITRATE_K}k -map_metadata 0 -id3v2_version 3 "{flacPath[:-5]}.mp3"



