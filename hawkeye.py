import subprocess
from subprocess import DEVNULL
import os
import signal
import sys
import argparse

parser = argparse.ArgumentParser(prog = 'Hawkeye', description = 'Hawkeye')
parser.add_argument('-v', '--verbose', action='store_true')
parser.add_argument('-b', '--browser', action='store_true')
args = parser.parse_args()

root_dir = os.path.dirname(__file__)
os.chdir(os.path.join(root_dir))
sketcher_server = subprocess.Popen(['python3', './SketcherServer.py'],
    stdout=DEVNULL if not args.verbose else None,
    stderr=DEVNULL if not args.verbose else None)

os.chdir(os.path.join(root_dir, 'web'))
web_server_env = os.environ.copy()
if not args.browser:
    web_server_env["BROWSER"] = "none"
web_server = subprocess.Popen(['npm', 'start'],
    env=web_server_env,
    stdout=DEVNULL if not args.verbose else None,
    stderr=DEVNULL if not args.verbose else None)

def signal_handler(sig, frame):
    print("Exit the Hawkeye server...")
    sketcher_server.kill()
    web_server.kill()
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)
print("Hawkeye server is running...")
print("Connect to http://localhost:3000")
print("Press Ctrl+C to exit the Hawkeye server.")
signal.pause()
