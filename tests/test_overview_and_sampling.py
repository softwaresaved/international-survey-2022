import os
import sys
from pathlib import Path

def sha256sum(fn: Path) -> str:
    import hashlib
    m = hashlib.sha256()
    m.update(fn.read_text().encode("utf-8"))
    return m.hexdigest()

HASH = "01b57c3c85366286a2f96b026192c5ccb1875b432eccdeb9e607350195d01b8f"
CACHED_DATA = Path("cache/processed_data.csv")

def test_overview_and_sampling():
    os.environ["RSE_SURVEY_YEAR"] = "2022"
    os.environ["RSE_SURVEY_YEAR_PREV"] = "2018"
    sys.path.insert(1, str(Path(__file__).parent.parent))
    import survey.overview_and_sampling
    survey.overview_and_sampling.run()
    assert sha256sum(CACHED_DATA) == HASH
