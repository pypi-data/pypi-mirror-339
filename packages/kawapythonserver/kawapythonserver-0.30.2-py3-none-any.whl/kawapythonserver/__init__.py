import os
from pathlib import Path

min_kywy_version = '0.29.0'

current_file = Path(__file__)
os.environ["PACKAGE_ROOT_PATH"] = str(current_file.parent.parent)
