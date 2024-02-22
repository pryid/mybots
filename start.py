import subprocess

def run_script(script_name):
    subprocess.run(["python", script_name])

# Список скриптов для запуска
scripts = ["tts_checker/main.py", "sberprimeplus/main.py", "sitrim/main.py", "musarskoy/main.py"]

for script in scripts:
    run_script(script)
