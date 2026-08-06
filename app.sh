#!/bin/bash

# Warna untuk tampilan terminal
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${CYAN}======================================${NC}"
echo -e "${CYAN}       PEMANGGIL APLIKASI HP          ${NC}"
echo -e "${CYAN}======================================${NC}"

# Cek apakah paket termux-api dan jq terinstall
if ! command -v jq &> /dev/null || ! command -v fzf &> /dev/null; then
    echo -e "${RED}[!] Paket pendukung belum lengkap.${NC}"
    echo -e "Silakan jalankan di Termux: ${GREEN}pkg install termux-api jq fzf -y${NC}"
    exit 1
fi

echo -e "${GREEN}[*] Memuat daftar aplikasi...${NC}"

# Ambil daftar aplikasi dari Android dan pilih pakai fzf
APP=$(termux-launcher-apps | jq -r '.[] | "\(.appName) | \(.packageName)"' 2>/dev/null | fzf --prompt="📱 Pilih Aplikasi: ")

if [ -n "$APP" ]; then
    # Ekstrak package name
    PACKAGE=$(echo "$APP" | awk -F'| ' '{print $2}')
    APP_NAME=$(echo "$APP" | awk -F'| ' '{print $1}')
    
    echo -e "${GREEN}[✓] Membuka $APP_NAME...${NC}"
    
    # Jalankan aplikasi lewat perintah monkey Android
    monkey -p "$PACKAGE" -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1
else
    echo -e "${RED}[!] Batal memilih aplikasi.${NC}"
fi