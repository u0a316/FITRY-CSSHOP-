#!/bin/bash

# Jika $1 ada, pakai sebagai ORDER_NUMBER, jika tidak, minta input interaktif
if [ -n "$1" ]; then
  ORDER_NUMBER="$1"
else
  read -e -p "Nomor Order: " ORDER_NUMBER
fi

# Buat JSON
json=$(jq -n \
  --arg ORDER_NUMBER "$ORDER_NUMBER" \
  '{ "ORDER_NUMBER": $ORDER_NUMBER }'
)


echo "$json" > subject.json

# Render template
mustache <(echo "$json") subject.mustache
