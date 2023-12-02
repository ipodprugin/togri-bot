import re
from typing import Pattern


TENDER_ID_REGEX: Pattern = re.compile("^\d{8,}$")