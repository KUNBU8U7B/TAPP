#!/bin/bash

# Warna Tampilan
GREEN='\033[0;32m'
CYAN='\033[0;36m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${CYAN}======================================${NC}"
echo -e "${CYAN}       PEMANGGIL APLIKASI HP          ${NC}"
echo -e "${CYAN}======================================${NC}"

if ! command -v fzf &> /dev/null; then
    echo -e "${RED}[!] Paket fzf belum terinstall.${NC}"
    echo -e "Jalankan di Termux: ${GREEN}pkg install fzf -y${NC}"
    exit 1
fi

echo -e "${GREEN}[*] Memuat seluruh aplikasi HP...${NC}"

# Ambil seluruh daftar package
APPS=$(cmd package list packages 2>/dev/null | sed 's/package://' | sort)

# Pilih aplikasi via fzf
SELECTED_PACKAGE=$(echo "$APPS" | fzf --prompt="📱 Cari & Pilih Aplikasi: ")

if [ -n "$SELECTED_PACKAGE" ]; then
    echo -e "${GREEN}[✓] Membuka $SELECTED_PACKAGE...${NC}"
    
    # 1. Coba buka pakai Activity Manager bawaan Android (Paling Ampuh)
    am start -n $(cmd package resolve-activity --brief "$SELECTED_PACKAGE" | tail -n 1) > /dev/null 2>&1
    
    # 2. Jika cara pertama gagal, gunakan fallback ke perintah monkey
    if [ $? -ne 0 ]; then
        monkey -p "$SELECTED_PACKAGE" -c android.intent.category.LAUNCHER 1 > /dev/null 2>&1
    fi
else
    echo -e "${RED}[!] Batal memilih aplikasi.${NC}"
fi