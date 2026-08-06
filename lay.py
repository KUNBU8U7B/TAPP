import subprocess
import sys

def main():
    print("\033[0;36m======================================\033[0m")
    print("\033[0;36m     PEMANGGIL APLIKASI HP (PYTHON)   \033[0m")
    print("\033[0;36m======================================\033[0m")

    print("\033[0;32m[*] Memuat aplikasi non-sistem (user apps)... \033[0m")

    try:
        # Menampilkan HANYA aplikasi pihak ke-3 (opsi -3) agar aplikasi sistem tidak memenuhi layar
        cmd_output = subprocess.check_output("cmd package list packages -3", shell=True, text=True)
        packages = [line.replace("package:", "").strip() for line in cmd_output.strip().split("\n") if line]
        packages.sort()
    except Exception as e:
        print(f"\033[0;31m[!] Gagal mengambil daftar aplikasi: {e}\033[0m")
        sys.exit(1)

    if not packages:
        print("\033[0;31m[!] Tidak ada aplikasi pihak ke-3 yang ditemukan.\033[0m")
        sys.exit(1)

    # Pilih aplikasi via fzf
    try:
        fzf_input = "\n".join(packages)
        process = subprocess.Popen(
            ["fzf", "--prompt=📱 Cari Aplikasi: "],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        selected_package, _ = process.communicate(input=fzf_input)
        selected_package = selected_package.strip()
    except FileNotFoundError:
        print("\033[0;31m[!] Paket 'fzf' belum terinstall. Jalankan: pkg install fzf -y\033[0m")
        sys.exit(1)

    if selected_package:
        print(f"\033[0;32m[✓] Membuka {selected_package}...\033[0m")
        
        # Perintah monkey terbaik untuk memicu intent LAUNCHER ke layar depan
        launch_cmd = f"monkey -p {selected_package} -c android.intent.category.LAUNCHER 1"
        
        subprocess.run(
            launch_cmd,
            shell=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )
    else:
        print("\033[0;31m[!] Batal memilih aplikasi.\033[0m")

if __name__ == "__main__":
    main()