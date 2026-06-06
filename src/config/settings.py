import os
from dotenv import load_dotenv

load_dotenv()

CAL_API_KEY    = os.getenv("CAL_API_KEY")
CAL_USERNAME   = os.getenv("CAL_USERNAME")   # harsh-dharnidharka-gz9c6k
CAL_EVENT_SLUG = os.getenv("CAL_EVENT_SLUG") # scaler-interview

missing = [k for k, v in {
    "CAL_API_KEY": CAL_API_KEY,
    "CAL_USERNAME": CAL_USERNAME,
    "CAL_EVENT_SLUG": CAL_EVENT_SLUG,
}.items() if not v]

if missing:
    print(f"Warning: Missing calendar credentials in .env: {', '.join(missing)}")