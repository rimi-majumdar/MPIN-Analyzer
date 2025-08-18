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

with st.expander("About the checks / assignment"):
    st.write("""
- Part A: 4-digit commonly used check.
- Part B: Add demographics and output **WEAK/STRONG**.
- Part C: If **WEAK**, return reasons from the allowed set only.
- Part D: Support 6-digit PINs as well.
    """)
