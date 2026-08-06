#!/bin/bash

# Warna Tampilan
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}======================================${NC}"
echo -e "${CYAN}       PEMANGGIL APLIKASI HP          ${NC}"
echo -e "${CYAN}======================================${NC}"

# Cek fzf
if ! command -v fzf &> /dev/null; then
    echo -e "${RED}[!] Paket fzf belum terinstall.${NC}"
    echo -e "Jalankan di Termux: ${GREEN}pkg install fzf -y${NC}"
    exit 1
fi

echo -e "${GREEN}[*] Memuat daftar aplikasi HP...${NC}"

# Mengambil daftar package aplikasi bawaan android
SELECTED_PACKAGE=$(pm list packages -3 | sed 's/package://' | fzf --prompt="📱 Pilih Package Aplikasi: ")

if [ -n "$SELECTED_PACKAGE" ]; then
    echo -e "${GREEN}[✓] Membuka $SELECTED_PACKAGE...${NC}"
    
    # Buka aplikasi menggunakan monkey
    monkey -p "$SELECTED_PACKAGE" -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1
else
    echo -e "${RED}[!] Batal memilih aplikasi.${NC}"
fi