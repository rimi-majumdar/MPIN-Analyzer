from datetime import date
from mpin_analyzer import analyze_pin

COMMON_4 = {"1234","0000","1111","1212","1122","2222","9999","4321","2580","0852"}
COMMON_6 = {"123456","000000","111111","112233","121212","654321","777777","999999","101010","222222"}

def T(pin, L, dob=None, spouse=None, anniv=None):
    return analyze_pin(pin, L, dob, spouse, anniv, COMMON_4 if L==4 else COMMON_6)

def test_cases():
    # Common 4-digit
    assert T("1234",4)[0]=="WEAK" and "COMMONLY_USED" in T("1234",4)[1]
    assert T("0000",4)[0]=="WEAK"
    # Non-common 4-digit strong
    assert T("7391",4)[0]=="STRONG"
    # DOB matches (self)
    assert T("0101",4, dob=date(1998,1,1))[0]=="WEAK"
    # Spouse matches
    assert T("3112",4, spouse=date(1999,12,31))[0]=="WEAK"
    # Anniversary matches
    assert T("1225",4, anniv=date(2020,12,25))[0]=="WEAK"
    # Combined reasons
    s,r = T("1234",4, dob=date(1990,12,34-3))  # invalid day avoided; just ensure common still flags
    assert "COMMONLY_USED" in r
    # 6-digit common
    assert T("123456",6)[0]=="WEAK"
    # 6-digit non-common strong
    assert T("583041",6)[0]=="STRONG"
    # 6-digit DOB patterns
    assert T("010190",6, dob=date(1990,1,1))[0]=="WEAK"    # ddmmyy
    assert T("900101",6, dob=date(1990,1,1))[0]=="WEAK"    # yymmdd
    assert T("010190",6, spouse=date(1990,1,1))[0]=="WEAK"
    assert T("010190",6, anniv=date(1990,1,1))[0]=="WEAK"
    # Edge: wrong length -> WEAK
    assert T("123",4)[0]=="WEAK"
    # Edge: non-digit -> WEAK
    assert T("12a4",4)[0]=="WEAK"
    # More non-common strongs
    assert T("4709",4)[0]=="STRONG"
    assert T("9074",4)[0]=="STRONG"
    assert T("135790",6)[0]=="STRONG"
    # Another combined 6-digit
    s,r = T("112233",6, spouse=date(2011,2,3))
    assert s=="WEAK"
