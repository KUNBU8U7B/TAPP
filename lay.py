import subprocess
import sys
import os
import zipfile
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
import climage

console = Console()

def get_apps():
    try:
        cmd_output = subprocess.check_output("cmd package list packages -3", shell=True, text=True)
        packages = [line.replace("package:", "").strip() for line in cmd_output.strip().split("\n") if line]
        packages.sort()
        return packages
    except Exception as e:
        console.print(f"[bold red][!] Gagal mengambil aplikasi: {e}[/bold red]")
        sys.exit(1)

def show_app_icon(package_name):
    """Mencari path APK, mengekstrak ikon, dan menampilkannya di TUI"""
    try:
        # 1. Cari lokasi APK di sistem Android
        path_output = subprocess.check_output(f"pm path {package_name}", shell=True, text=True).strip()
        apk_path = path_output.replace("package:", "").split("\n")[0]
        
        # 2. Ekstrak icon dari APK
        temp_icon = "/sdcard/Download/temp_icon.png"
        with zipfile.ZipFile(apk_path, 'r') as zip_ref:
            # Cari file launcher icon di dalam zip/apk
            icon_files = [f for f in zip_ref.namelist() if 'ic_launcher' in f and f.endswith('.png')]
            if icon_files:
                # Ambil icon dengan resolusi tertinggi (biasanya paling akhir)
                target_icon = icon_files[-1]
                with zip_ref.open(target_icon) as source, open(temp_icon, "wb") as target:
                    target.write(source.read())
                
                # 3. Render icon ke karakter TUI
                converted_icon = climage.convert(temp_icon, width=25)
                console.print(Panel(converted_icon, title="[bold cyan]Ikon Aplikasi[/bold cyan]", expand=False))
                
                # Hapus file temporary
                if os.path.exists(temp_icon):
                    os.remove(temp_icon)
    except Exception:
        # Jika gagal ekstraksi ikon, lewati tanpa crash
        pass

def main():
    console.clear()
    
    # Header Banner TUI
    banner = Panel.fit(
        "[bold cyan]📱 LAUNCHER APLIKASI HP[/bold cyan]\n[dim]TUI + Real Icon Render[/dim]",
        border_style="magenta"
    )
    console.print(banner)

    packages = get_apps()

    # Buat Tabel TUI
    table = Table(title="[bold green]Daftar Aplikasi Pihak Ke-3[/bold green]", show_header=True, header_style="bold yellow")
    table.add_column("No", justify="center", style="cyan", no_wrap=True)
    table.add_column("Package Name", style="white")

    for idx, pkg in enumerate(packages, start=1):
        table.add_row(str(idx), pkg)

    console.print(table)
    console.print()

    choice = Prompt.ask("[bold choice]Pilih Nomor / Nama Aplikasi[/bold choice] (q untuk keluar)")

    if choice.lower() == 'q':
        console.print("[yellow]Keluar...[/yellow]")
        sys.exit(0)

    selected_package = ""
    if choice.isdigit():
        num = int(choice)
        if 1 <= num <= len(packages):
            selected_package = packages[num - 1]
    else:
        matches = [p for p in packages if choice.lower() in p.lower()]
        if matches:
            selected_package = matches[0]

    if selected_package:
        # Tampilkan Ikon Asli Aplikasi di TUI
        show_app_icon(selected_package)
        
        console.print(Panel(f"[bold green]✓ Membuka {selected_package}...[/bold green]", border_style="green"))
        subprocess.run(f"termux-open-url android-app://{selected_package}", shell=True)
    else:
        console.print("[bold red][!] Aplikasi tidak ditemukan![/bold red]")

if __name__ == "__main__":
    main()