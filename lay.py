import subprocess
import sys

def main():
    print("\033[0;36m======================================\033[0m")
    print("\033[0;36m     PEMANGGIL APLIKASI HP (PYTHON)   \033[0m")
    print("\033[0;36m======================================\033[0m")

    print("\033[0;32m[*] Memuat daftar aplikasi... \033[0m")

    try:
        # Mengambil daftar package user app
        cmd_output = subprocess.check_output("cmd package list packages -3", shell=True, text=True)
        packages = [line.replace("package:", "").strip() for line in cmd_output.strip().split("\n") if line]
        packages.sort()
    except Exception as e:
        print(f"\033[0;31m[!] Gagal mengambil aplikasi: {e}\033[0m")
        sys.exit(1)

    # Pilih via fzf
    try:
        fzf_input = "\n".join(packages)
        process = subprocess.Popen(
            ["fzf", "--prompt=📱 Pilih Aplikasi: "],
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
            text=True
        )
        selected_package, _ = process.communicate(input=fzf_input)
        selected_package = selected_package.strip()
    except FileNotFoundError:
        print("\033[0;31m[!] fzf belum terinstall. Ketik: pkg install fzf -y\033[0m")
        sys.exit(1)

    if selected_package:
        print(f"\033[0;32m[✓] Membuka {selected_package}...\033[0m")
        
        # Opsi 1: Coba jalankan lewat termux-open-url (Intent universal)
        run_status = subprocess.run(f"termux-open-url android-app://{selected_package}", shell=True)
        
        # Opsi 2: Jika termux-open-url tidak respon, gunakan monkey dengan opsi -v (Verbose/Forced)
        if run_status.returncode != 0:
            subprocess.run(
                f"monkey -p {selected_package} -v 1",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    else:
        print("\033[0;31m[!] Batal memilih.\033[0m")

if __name__ == "__main__":
    main()