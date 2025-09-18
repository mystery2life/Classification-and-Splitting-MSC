import os
from dotenv import load_dotenv
load_dotenv()

# map DI labels -> our internal doc types
DOC_TYPE_MAP = {
    "paystub": "paystub",
    "employmentverificationform": "ev_form",
    "ev_form": "ev_form",

    "bankstatement": "bank_stmt",
    "bank statement": "bank_stmt",

    "driverlicense": "dl",
    "driver license": "dl",
    "dl": "dl",

    "passport": "passport",
    "ssn": "ssn",
}

class Settings:
    AZ_DI_ENDPOINT: str = os.getenv("AZ_DI_ENDPOINT", "").strip()
    AZ_DI_KEY: str = os.getenv("AZ_DI_KEY", "").strip()
    DI_CLASSIFIER_MODEL_ID: str = os.getenv("DI_CLASSIFIER_MODEL_ID", "").strip()
    CONF_PRIMARY: float = float(os.getenv("CONF_PRIMARY", "0.80"))
    CONF_SECONDARY: float = float(os.getenv("CONF_SECONDARY", "0.65"))

settings = Settings()