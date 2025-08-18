from datetime import date
from pathlib import Path

ALLOWED_REASONS = {
    "COMMONLY_USED",
    "DEMOGRAPHIC_DOB_SELF",
    "DEMOGRAPHIC_DOB_SPOUSE",
    "DEMOGRAPHIC_ANNIVERSARY",
}

def load_common_pins(path: str) -> set[str]:
    p = Path(path)
    if not p.exists():
        # Fallback minimal sets so the app still runs if data files are missing
        return {
            "0000","1111","1234","1122","1212","2222","9999","2580","0852","4321",
            "000000","111111","123456","654321","112233","121212","101010","222222","777777","999999"
        }
    with p.open("r", encoding="utf-8") as f:
        return {line.strip() for line in f if line.strip().isdigit()}

def _patterns_from_date(dt: date, length: int) -> set[str]:
    """Generate common MPIN patterns from a date for 4 or 6 digits."""
    if not isinstance(dt, date):
        return set()
    dd = f"{dt.day:02d}"
    mm = f"{dt.month:02d}"
    yyyy = f"{dt.year:04d}"
    yy = yyyy[-2:]

    if length == 4:
        # typical 4-digit patterns: ddmm, mmdd, yymm, mmyy
        return {dd + mm, mm + dd, yy + mm, mm + yy}
    elif length == 6:
        # typical 6-digit patterns: ddmmyy, yymmdd, mmddyy, yyyymm
        return {dd + mm + yy, yy + mm + dd, mm + dd + yy, yyyy + mm}
    return set()

def analyze_pin(pin: str,
                pin_length: int,
                dob: date | None,
                spouse_dob: date | None,
                anniversary: date | None,
                common_set: set[str]) -> tuple[str, list[str]]:
    """Return (strength, reasons[]) per assignment spec."""
    reasons: list[str] = []
    # Basic validation
    if not pin or not pin.isdigit() or len(pin) != pin_length:
        return "WEAK", ["COMMONLY_USED"]  # minimal safe default

    # Part A/D: common pins
    if pin in common_set:
        reasons.append("COMMONLY_USED")

    # Part B/C: demographics
    if dob and pin in _patterns_from_date(dob, pin_length):
        reasons.append("DEMOGRAPHIC_DOB_SELF")
    if spouse_dob and pin in _patterns_from_date(spouse_dob, pin_length):
        reasons.append("DEMOGRAPHIC_DOB_SPOUSE")
    if anniversary and pin in _patterns_from_date(anniversary, pin_length):
        reasons.append("DEMOGRAPHIC_ANNIVERSARY")

    # Only allowed reasons
    reasons = [r for r in reasons if r in ALLOWED_REASONS]
    strength = "WEAK" if reasons else "STRONG"
    return strength, reasons
