import streamlit as st
import math
import requests

# Initialize expression in session state

if "expression" not in st.session_state:
    st.session_state.expression = ""

# Add number or operator
def add_to_expression(value):
    st.session_state.expression += str(value)

# Clear expression
def clear_expression():
    st.session_state.expression = ""

# Initialize toggle state
if "show_scientific" not in st.session_state:
    st.session_state.show_scientific = False

# Toggle button
def toggle_scientific():
    st.session_state.show_scientific = not st.session_state.show_scientific

st.button("🔬 Scientific Mode", on_click=toggle_scientific)

def convert_currency(amount,from_currency,to_currency):
    url=f"https://api.exchangerate-api.com/v4/latest/{from_currency}"
    response=requests.get(url)
    data=response.json()
    if response.status_code==200 and to_currency in data['rates']:
        convertion_rate=data['rates'][to_currency]
        return amount*convertion_rate
    else:
        return None

# Evaluate expression
def evaluate_expression():
    try:
        # Safe eval with math functions
        allowed_funcs = {
            "sin": math.sin,
            "cos": math.cos,
            "tan": math.tan,
            "log": math.log,      
            "log10": math.log10,  
            "sqrt": math.sqrt,
            "exp": math.exp,
            "pi": math.pi,
            "e": math.e,
            "pow": pow           
        }

        # Replace ^ with pow
        expression = st.session_state.expression.replace("^", "**")

        st.session_state.expression = str(eval(expression, {"__builtins__": None}, allowed_funcs))
    except Exception as e:
        st.session_state.expression = "Error"


# UI
st.title("🧮 Calculator")

st.text_input("Expression", st.session_state.expression, key="display",disabled=True)

if st.session_state.show_scientific != True:
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.button("7", on_click=add_to_expression, args=("7",), use_container_width=True)
        st.button("4", on_click=add_to_expression, args=("4",), use_container_width=True)
        st.button("1", on_click=add_to_expression, args=("1",), use_container_width=True)
        st.button("C", on_click=clear_expression, use_container_width=True)

    with col2:
        st.button("8", on_click=add_to_expression, args=("8",), use_container_width=True)
        st.button("5", on_click=add_to_expression, args=("5",), use_container_width=True)
        st.button("2", on_click=add_to_expression, args=("2",), use_container_width=True)
        st.button("0", on_click=add_to_expression, args=("0",), use_container_width=True)

    with col3:
        st.button("9", on_click=add_to_expression, args=("9",), use_container_width=True)
        st.button("6", on_click=add_to_expression, args=("6",), use_container_width=True)
        st.button("3", on_click=add_to_expression, args=("3",), use_container_width=True)
        st.button(".", on_click=add_to_expression, args=(".",), use_container_width=True)

    with col4:
        st.button("➕", on_click=add_to_expression, args=("+",), use_container_width=True)
        st.button("➖", on_click=add_to_expression, args=("-",), use_container_width=True)
        st.button("✖️", on_click=add_to_expression, args=("*",), use_container_width=True)
        st.button("/", on_click=add_to_expression, args=("/",), use_container_width=True)

    st.button("=", on_click=evaluate_expression, use_container_width=True)

elif st.session_state.show_scientific:
    col1,col2,col3,col4,col5, col6, col7, col8 = st.columns(8)
    
    with col1:
        st.button("7", on_click=add_to_expression, args=("7",), use_container_width=True)
        st.button("4", on_click=add_to_expression, args=("4",), use_container_width=True)
        st.button("1", on_click=add_to_expression, args=("1",), use_container_width=True)
        st.button("C", on_click=clear_expression, use_container_width=True)

    with col2:
        st.button("8", on_click=add_to_expression, args=("8",), use_container_width=True)
        st.button("5", on_click=add_to_expression, args=("5",), use_container_width=True)
        st.button("2", on_click=add_to_expression, args=("2",), use_container_width=True)
        st.button("0", on_click=add_to_expression, args=("0",), use_container_width=True)

    with col3:
        st.button("9", on_click=add_to_expression, args=("9",), use_container_width=True)
        st.button("6", on_click=add_to_expression, args=("6",), use_container_width=True)
        st.button("3", on_click=add_to_expression, args=("3",), use_container_width=True)
        st.button(".", on_click=add_to_expression, args=(".",), use_container_width=True)

    with col4:
        st.button("➕", on_click=add_to_expression, args=("+",), use_container_width=True)
        st.button("➖", on_click=add_to_expression, args=("-",), use_container_width=True)
        st.button("✖️", on_click=add_to_expression, args=("*",), use_container_width=True)
        st.button("/", on_click=add_to_expression, args=("/",), use_container_width=True)

    st.button("=", on_click=evaluate_expression, use_container_width=True)

    with col5:
        st.button("sin", on_click=add_to_expression, args=("sin(",), use_container_width=True)
        st.button("cos", on_click=add_to_expression, args=("cos(",), use_container_width=True)
        st.button("tan", on_click=add_to_expression, args=("tan(",), use_container_width=True)
        st.button("log", on_click=add_to_expression, args=("log(",), use_container_width=True)

    with col6:
        st.button("√", on_click=add_to_expression, args=("sqrt(",), use_container_width=True)
        st.button("^", on_click=add_to_expression, args=("^(",), use_container_width=True)
        st.button("π", on_click=add_to_expression, args=("pi",), use_container_width=True)
        st.button("e", on_click=add_to_expression, args=("e",), use_container_width=True)

    with col7:
        st.button("(", on_click=add_to_expression, args=("(",), use_container_width=True)
        st.button(")", on_click=add_to_expression, args=(")",), use_container_width=True)
        st.button("exp", on_click=add_to_expression, args=("exp(",), use_container_width=True)

# Country -> Currency Code dictionary
country_currency_dict = {
    "AFN": "Afghanistan",
    "EUR": "Akrotiri and Dhekelia",
    "ALL": "Albania",
    "DZD": "Algeria",
    "AOA": "Angola",
    "XCD": "Anguilla",
    "ARS": "Argentina",
    "AMD": "Armenia",
    "AWG": "Aruba",
    "SHP": "Ascension Island",
    "AUD": "Australia",
    "AZN": "Azerbaijan",
    "BSD": "Bahamas, The",
    "BHD": "Bahrain",
    "BDT": "Bangladesh",
    "BBD": "Barbados",
    "BYN": "Belarus",
    "BZD": "Belize",
    "XOF": "Benin",
    "BMD": "Bermuda",
    "BTN": "Bhutan",
    "INR": "India",
    "BOB": "Bolivia",
    "USD": "United States",
    "BAM": "Bosnia and Herzegovina",
    "BWP": "Botswana",
    "BRL": "Brazil",
    "BND": "Brunei",
    "SGD": "Singapore",
    "BGN": "Bulgaria",
    "BIF": "Burundi",
    "KHR": "Cambodia",
    "XAF": "Cameroon",
    "CAD": "Canada",
    "CVE": "Cape Verde",
    "KYD": "Cayman Islands",
    "CLP": "Chile",
    "CNY": "China",
    "COP": "Colombia",
    "CDF": "Congo, Democratic Republic",
    "CRC": "Costa Rica",
    "HRK": "Croatia",
    "CUP": "Cuba",
    "XCG": "Curaçao",
    "CZK": "Czech Republic",
    "DKK": "Denmark",
    "DJF": "Djibouti",
    "DOP": "Dominican Republic",
    "EGP": "Egypt",
    "ERN": "Eritrea",
    "SZL": "Eswatini",
    "ETB": "Ethiopia",
    "FKP": "Falkland Islands",
    "FJD": "Fiji",
    "XPF": "French Polynesia",
    "GMD": "Gambia, The",
    "GEL": "Georgia",
    "GHS": "Ghana",
    "GIP": "Gibraltar",
    "GTQ": "Guatemala",
    "GNF": "Guinea",
    "GYD": "Guyana",
    "HTG": "Haiti",
    "HNL": "Honduras",
    "HKD": "Hong Kong",
    "HUF": "Hungary",
    "ISK": "Iceland",
    "IDR": "Indonesia",
    "IRR": "Iran",
    "IQD": "Iraq",
    "ILS": "Israel",
    "JOD": "Jordan",
    "KZT": "Kazakhstan",
    "KES": "Kenya",
    "KPW": "North Korea",
    "KRW": "South Korea",
    "KWD": "Kuwait",
    "KGS": "Kyrgyzstan",
    "LAK": "Laos",
    "LBP": "Lebanon",
    "LSL": "Lesotho",
    "LYD": "Libya",
    "CHF": "Liechtenstein",
    "MOP": "Macau",
    "MGA": "Madagascar",
    "MWK": "Malawi",
    "MYR": "Malaysia",
    "MVR": "Maldives",
    "MRU": "Mauritania",
    "MUR": "Mauritius",
    "MXN": "Mexico",
    "MDL": "Moldova",
    "MNT": "Mongolia",
    "MAD": "Morocco",
    "MZN": "Mozambique",
    "MMK": "Myanmar",
    "NAD": "Namibia",
    "NPR": "Nepal",
    "NZD": "New Zealand",
    "NIO": "Nicaragua",
    "NGN": "Nigeria",
    "MKD": "North Macedonia",
    "NOK": "Norway",
    "OMR": "Oman",
    "PKR": "Pakistan",
    "PGK": "Papua New Guinea",
    "PYG": "Paraguay",
    "PEN": "Peru",
    "PHP": "Philippines",
    "PLN": "Poland",
    "QAR": "Qatar",
    "RON": "Romania",
    "RUB": "Russia",
    "RWF": "Rwanda",
    "SAR": "Saudi Arabia",
    "RSD": "Serbia",
    "SCR": "Seychelles",
    "SLL": "Sierra Leone",
    "SBD": "Solomon Islands",
    "SOS": "Somalia",
    "SSP": "South Sudan",
    "LKR": "Sri Lanka",
    "SDG": "Sudan",
    "SRD": "Suriname",
    "SEK": "Sweden",
    "SYP": "Syria",
    "TWD": "Taiwan",
    "TJS": "Tajikistan",
    "TZS": "Tanzania",
    "THB": "Thailand",
    "TOP": "Tonga",
    "TTD": "Trinidad and Tobago",
    "TND": "Tunisia",
    "TRY": "Turkey",
    "TMT": "Turkmenistan",
    "UGX": "Uganda",
    "UAH": "Ukraine",
    "AED": "United Arab Emirates",
    "GBP": "United Kingdom",
    "UYU": "Uruguay",
    "UZS": "Uzbekistan",
    "VUV": "Vanuatu",
    "VEF": "Venezuela",
    "VND": "Vietnam",
    "YER": "Yemen",
    "ZMW": "Zambia",
    "ZWG": "Zimbabwe"
}


# Currency converter section
st.subheader("💱 Currency Converter")
amount = st.number_input("Amount", min_value=0.0)

# Select currencies from dictionary keys
from_currency = st.selectbox("From Currency", list(country_currency_dict.keys()))
to_currency = st.selectbox("To Currency", list(country_currency_dict.keys()))

if st.button("Convert"):
    converted_amount = convert_currency(amount, from_currency, to_currency)
    if converted_amount:
        st.success(
            f"{amount} {from_currency} ({country_currency_dict[from_currency]}) = "
            f"{converted_amount:.2f} {to_currency} ({country_currency_dict[to_currency]})"
        )
    else:
        st.error("Conversion failed. Please check the currencies and try again.")

