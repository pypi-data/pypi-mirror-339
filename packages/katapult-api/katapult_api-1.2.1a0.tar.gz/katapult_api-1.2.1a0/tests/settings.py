import os
from pathlib import Path

from dotenv import load_dotenv

ROOT_PATH = Path(__file__).resolve().parent.parent

load_dotenv(ROOT_PATH / ".env")

SCHEMA_ROOT = ROOT_PATH / "examples" / "schemas"

KATAPULT_API_KEY = os.environ.get("KATAPULT_API_KEY")

if not KATAPULT_API_KEY:
    raise OSError("Missing required environment variable: KATAPULT_API_KEY")

TEST_DIR_PATH = "Techserv/TEST"
