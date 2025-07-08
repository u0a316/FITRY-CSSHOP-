#!/bin/bash

# Interaktif prompt
read -e -p "Nama Pembeli: " CUSTOMER
read -e -p "Total Harga (Rp): " PRICE_QTY
read -e -p "Email kamu: " EMAIL_CUSTOMER
read -e -p "Link Unduhan Produk: " LINK_PRODUCT

# Buat JSON data
json=$(jq -n \
  --arg CUSTOMER "$CUSTOMER" \
  --arg PRICE_QTY "$PRICE_QTY" \
  --arg EMAIL_CUSTOMER "$EMAIL_CUSTOMER" \
  --arg LINK_PRODUCT "$LINK_PRODUCT" \
  '{
    CUSTOMER: $CUSTOMER,
    PRICE_QTY: $PRICE_QTY,
    EMAIL_CUSTOMER: $EMAIL_CUSTOMER,
    LINK_PRODUCT: $LINK_PRODUCT
  }'
)

# Simpan ke data.json (optional)
echo "$json" > body.json

# Render dengan mustache
mustache <(echo "$json") body.mustache
