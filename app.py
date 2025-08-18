import streamlit as st
from datetime import date
from pathlib import Path
from mpin_analyzer import analyze_pin, load_common_pins

st.set_page_config(page_title="MPIN Strength Analyzer", page_icon="🔐")

st.title("🔐 MPIN Strength Analyzer")
st.caption("Checks 4 or 6 digit MPINs for commonness and demographic patterns (DOB, spouse DOB, anniversary).")

# --- Controls
length_choice = st.radio("PIN length", options=[4, 6], horizontal=True)
pin = st.text_input(f"Enter your {length_choice}-digit MPIN", type="password", max_chars=length_choice)

col1, col2, col3 = st.columns(3)
with col1:
    use_dob = st.checkbox("Provide DOB?")
    dob = st.date_input("DOB", value=date(2000, 1, 1)) if use_dob else None
with col2:
    use_spouse = st.checkbox("Provide Spouse DOB?")
    spouse_dob = st.date_input("Spouse DOB", value=date(2000, 1, 1)) if use_spouse else None
with col3:
    use_anniv = st.checkbox("Provide Anniversary?")
    anniversary = st.date_input("Anniversary", value=date(2020, 1, 1)) if use_anniv else None

# Load common pins (no hardcoding in code; values live in data files)
COMMON_4 = load_common_pins("data/common_pins_4.txt")
COMMON_6 = load_common_pins("data/common_pins_6.txt")

if st.button("Analyze"):
    if not pin.isdigit() or len(pin) != length_choice:
        st.error(f"Please enter exactly {length_choice} digits.")
    else:
        strength, reasons = analyze_pin(
            pin=pin,
            pin_length=length_choice,
            dob=dob,
            spouse_dob=spouse_dob,
            anniversary=anniversary,
            common_set=COMMON_4 if length_choice == 4 else COMMON_6
        )
        st.subheader(f"Strength: {strength}")
        if reasons:
            st.warning(f"Weak reasons: {reasons}")
        else:
            st.success("No weak reasons found. Looks strong ✅")
with st.expander("ℹ️ How this analyzer works"):
    st.markdown("""
    The MPIN Strength Analyzer evaluates your PIN using these rules:

    1. **Commonly Used Check**  
       - If your PIN is in a list of frequently used 4-digit or 6-digit PINs, it's flagged as **WEAK**.

    2. **Demographics Check**  
       - If your PIN matches obvious patterns from your **DOB**, **Spouse DOB**, or **Anniversary**  
         (like `ddmm`, `mmdd`, `yymm`, or `ddmmyy`), it is flagged as **WEAK**.

    3. **Reasons **  
       - If the PIN is weak, the app shows **why**:  
         - `COMMONLY_USED`  
         - `DEMOGRAPHIC_DOB_SELF`  
         - `DEMOGRAPHIC_DOB_SPOUSE`  
         - `DEMOGRAPHIC_ANNIVERSARY`

    4. **Strength Output**  
       - If no rules are triggered → **STRONG**  
       - If one or more rules are triggered → **WEAK**
    """)

