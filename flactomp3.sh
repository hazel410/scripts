#!/bin/bash

find ~/Music/walkman/MUSIC/ -mindepth 3 -type f -name "*.flac" -print0 | xargs -0 -P 16 -I {} bash -c '
  input="$1"
  output="${input%.flac}.mp3"
  ffmpeg -nostdin -y -i "$input" -v error -ab 320k -map_metadata 0 -id3v2_version 3 "$output" && rm "$input"
' _ {}