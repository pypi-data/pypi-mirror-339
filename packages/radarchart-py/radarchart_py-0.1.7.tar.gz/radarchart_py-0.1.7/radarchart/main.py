import subprocess
import os


def main():
    print("Hello from RadarChart!")

    script_path = os.path.join(os.path.dirname(__file__), "ui.py")
    subprocess.run(["streamlit", "run", script_path])

    print("streamlit closed")


if __name__ == "__main__":
    main()
