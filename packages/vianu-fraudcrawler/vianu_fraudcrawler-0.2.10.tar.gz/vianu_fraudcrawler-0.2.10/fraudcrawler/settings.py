from pathlib import Path

# Generic settings
LOG_FMT = "%(asctime)s | %(name)s | %(funcName)s | %(levelname)s | %(message)s"
LOG_LVL = "DEBUG"
LOG_DATE_FMT = "%Y-%m-%d %H:%M:%S"
MAX_RETRIES = 3
RETRY_DELAY = 2
ROOT_DIR = Path(__file__).parents[1]

# Serp settings
GOOGLE_LOCATIONS_FILENAME = ROOT_DIR / "fraudcrawler" / "base" / "google-locations.json"
GOOGLE_LANGUAGES_FILENAME = ROOT_DIR / "fraudcrawler" / "base" / "google-languages.json"

# Enrichment settings
ENRICHMENT_DEFAULT_LIMIT = 10

# Zyte settings
ZYTE_DEFALUT_PROBABILITY_THRESHOLD = 0.1

# Processor settings
PROCESSOR_DEFAULT_MODEL = "gpt-4o"
PROCESSOR_DEFAULT_MISSING_FIELDS_RELEVANCE = 1

# Async settings
DEFAULT_N_SERP_WKRS = 10
DEFAULT_N_ZYTE_WKRS = 10
DEFAULT_N_PROC_WKRS = 10
