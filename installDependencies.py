import subprocess
import sys

packages = [ 'telegram', 'pytelegrambotapi','matplotlib', 'numpy']
for package in packages:
    subprocess.check_call([sys.executable, '-m', 'pip', 'install', package])