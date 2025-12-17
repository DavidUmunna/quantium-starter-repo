import sys
from pathlib import Path
import chromedriver_autoinstaller

# Ensure project root is on sys.path so tests can import the app module
ROOT = Path(__file__).resolve().parents[1]
if ROOT not in map(Path, map(Path, sys.path)):
    sys.path.insert(0, str(ROOT))

# Ensure chromedriver is available for dash[testing] selenium tests
chromedriver_autoinstaller.install()
