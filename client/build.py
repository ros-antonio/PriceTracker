import subprocess
import sys

def build():
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--windowed",
        "--name", "PriceTracker",
        "--clean",
        "main.py",
    ]
    print("Building executable...")
    subprocess.run(cmd, check=True)
    print("\n✅ Done! Executable is in: client/dist/PriceTracker.exe")
    print("   Move it anywhere next to data.json's parent folder,")
    print("   or keep it in client/dist/ — it uses relative paths.")

if __name__ == "__main__":
    build()
