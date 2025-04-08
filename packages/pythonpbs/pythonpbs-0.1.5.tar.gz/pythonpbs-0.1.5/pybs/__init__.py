from pathlib import Path
import importlib.metadata
version = importlib.metadata.version("pythonpbs")
__version__ = version

PROJECT_ROOT = Path(__file__).parent.parent
NAME = "PyBS"

PBS_SCRIPT_DIR = PROJECT_ROOT / "pbs_scripts"
DEFAULT_PBS_SCRIPT_PATH = PBS_SCRIPT_DIR / "gpu.pbs"

SSH_CONFIG_PATH = "~/.ssh/config"
# TODO: replace this path with something from `platformdirs`

if __name__ == "__main__":
    print(PROJECT_ROOT)
