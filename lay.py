import subprocess
import sys

def main():
    print("\033[0;36m======================================\033[0m")
    print("\033[0;36m     PEMANGGIL APLIKASI HP (PYTHON)   \033[0m")
    print("\033[0;36m======================================\033[0m")

    print("\033[0;32m[*] Memuat seluruh aplikasi HP...\033[0m")

    try:
        # Ambil daftar package dari Android
        cmd_output = subprocess.check_output("cmd package list packages", shell=True, text=True)
        packages = [line.replace("package:", "").strip() for line in cmd_output.strip().split("\n") if line]
        packages.sort()
    except Exception as e:
        print(f"\033[0;31m[!] Gagal mengambil daftar aplikasi: {e}\033[0m")
        sys.exit(1)

    # Kirim daftar aplikasi ke fzf untuk dipilih
    try:
        fzf_input = "\n".join(packages)
        process = subprocess.Popen(
            ["fzf", "--prompt=📱 Cari & Pilih Aplikasi: "],
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
        
        # Perintah intent launcher Android (tanpa butuh permission khusus)
        launch_cmd = (
            f"am start --user 0 -a android.intent.action.MAIN "
            f"-c android.intent.category.LAUNCHER -package {selected_package}"
        )
        
        result = subprocess.run(launch_cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        
        # Fallback jika am start gagal
        if result.returncode != 0:
            subprocess.run(
                f"monkey -p {selected_package} -c android.intent.category.LAUNCHER 1",
                shell=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
    else:
        print("\033[0;31m[!] Batal memilih aplikasi.\033[0m")

if __name__ == "__main__":
    main()