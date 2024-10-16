import psutil
import time
from datetime import datetime

log_file = "/home/Script/Minne forbruk/process_log.txt"
error_file = "/home/Script/Minne forbruk/error_log.txt"
ram_threshold = 20

def log_high_ram_usage():
    with open(log_file, "a") as file:
        total_memory = psutil.virtual_memory().total
        available_memory = psutil.virtual_memory().available
        available_memory_percentage = (available_memory / total_memory) * 100

        file.write(f"\n----- {datetime.now()} -----")
        file.write(f"Processes using more than {ram_threshold}% of available RAM:\n")

        for process in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                memory_percent = process.info['memory_percent']

                if memory_percent >= ram_threshold:
                    file.write(f"\nNAME: {process.info['name']}")
                    file.write(f"PID: {process.info['pid']}")
                    file.write(f"Memory usage: {memory_percent:.2f}%\n")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass

def write_to_error_file(error):
    with open(error_file, "a") as file:
        file.write(f"\n ----- {datetime.now()} -----")
        file.write(f"Error: {error}")

if __name__ == "__main__":
    while True:
        try:
            log_high_ram_usage()
        except Exception as e:
            write_to_error_file(e)
        time.sleep(60)
