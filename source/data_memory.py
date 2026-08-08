import time

def cek_ram():
    info_ram = {}

    with open('/proc/meminfo' , 'r') as f:
        for line in f:
            parts = line.split()
            kunci = parts[0].rstrip(':')
            nilai = int(parts[1])
            info_ram[kunci] = nilai

    Total_kb     = info_ram.get('MemTotal' , 0)
    Availabel_kb = info_ram.get('MemAvailabel' , 0)
    Used_kb      = Total_kb - Availabel_kb

    Total_gb     = Total_kb / (1024 * 1024)
    Used_gb      = Used_kb / (1024 * 1024)

    Persen_terpakai = (Used_kb / Total_kb) * 100 if Total_kb > 0 else 0

    return Used_gb , Total_gb , Persen_terpakai

print("=== TES BACA RAM NATIVE TERMUX ===")
try:
    while True:
        terpakai, total, persen = cek_ram()
        print(f"\rRAM Terpakai: {terpakai:.2f} GB / {total:.2f} GB ({persen:.1f}%)", end="")
        time.sleep(1)
except KeyboardInterrupt:
    print("\nSelesai!")