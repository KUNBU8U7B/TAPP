import subprocess
import sys
import inquirer

def main():
    print("======================================")
    print("     PEMANGGIL APLIKASI HP (LIST)     ")
    print("======================================")

    try:
        cmd_output = subprocess.check_output("cmd package list packages -3", shell=True, text=True)
        packages = [line.replace("package:", "").strip() for line in cmd_output.strip().split("\n") if line]
        packages.sort()
    except Exception as e:
        print(f"[!] Gagal mengambil daftar aplikasi: {e}")
        sys.exit(1)

    questions = [
        inquirer.List(
            'package',
            message="Pilih aplikasi yang ingin dibuka",
            choices=packages,
        ),
    ]
    
    answers = inquirer.prompt(questions)
    
    if answers and answers['package']:
        selected = answers['package']
        print(f"[+] Membuka {selected}...")
        subprocess.run(f"termux-open-url android-app://{selected}", shell=True)

if __name__ == "__main__":
    main()