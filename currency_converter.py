import streamlit as st
import requests
import pandas as pd
import plotly.express as px
from datetime import datetime
from typing import Dict, Tuple

# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Khazabi Currency Converter",
    page_icon="💱",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# API CONFIGURATION
# ============================================================

API_URL = "https://open.er-api.com/v6/latest/USD"

# Fallback rates in case the internet/API is unavailable
FALLBACK_RATES = {
    "USD": 1.0,
    "EUR": 0.92,
    "GBP": 0.79,
    "INR": 83.25,
    "JPY": 155.0,
    "CAD": 1.36,
    "AUD": 1.51,
    "CHF": 0.90,
    "CNY": 7.23,
    "SGD": 1.35,
    "AED": 3.67,
    "SAR": 3.75,
    "NZD": 1.63,
    "KRW": 1380.0,
    "MYR": 4.70,
    "THB": 35.50
}

POPULAR_CURRENCIES = [
    "USD",
    "EUR",
    "GBP",
    "INR",
    "JPY",
    "CAD",
    "AUD",
    "CHF",
    "CNY",
    "SGD",
    "AED",
    "SAR",
    "NZD",
    "KRW",
    "MYR",
    "THB"
]

# ============================================================
# CUSTOM CSS
# ============================================================

st.markdown("""
<style>

.main {
    background-color: #f5f7fb;
}

.main-title {
    font-size: 42px;
    font-weight: 800;
    text-align: center;
    color: #DB2777;
    margin-bottom: 5px;
}

.sub-title {
    text-align: center;
    color: #64748b;
    font-size: 18px;
    margin-bottom: 30px;
}

.card {
    padding: 25px;
    border-radius: 18px;
    background: white;
    box-shadow: 0px 5px 20px rgba(0,0,0,0.08);
    margin-bottom: 20px;
}

.result-box {
    padding: 25px;
    border-radius: 18px;
    background: linear-gradient(135deg, #E11D48, #F472B6);
    color: white;
    text-align: center;
}

.result-value {
    font-size: 35px;
    font-weight: 800;
}

.footer {
    text-align: center;
    color: #F9A8D4;
    margin-top: 40px;
    padding: 20px;
}

</style>
""", unsafe_allow_html=True)

# ============================================================
# FETCH EXCHANGE RATES
# ============================================================

@st.cache_data(ttl=3600)
def fetch_exchange_rates() -> Tuple[Dict[str, float], str, bool]:

    try:

        response = requests.get(
            API_URL,
            timeout=10
        )

        response.raise_for_status()

        data = response.json()

        if data.get("result") == "success":

            rates = data.get("rates", {})

            timestamp = data.get(
                "time_last_update_unix"
            )

            if timestamp:
                last_updated = datetime.fromtimestamp(
                    timestamp
                ).strftime("%d-%m-%Y %H:%M:%S")
            else:
                last_updated = "Just now"

            return rates, last_updated, True

    except Exception:
        pass

    return (
        FALLBACK_RATES,
        "Offline / Fallback Data",
        False
    )

# ============================================================
# CURRENCY CONVERSION FUNCTION
# ============================================================

def convert_currency(
    amount: float,
    from_currency: str,
    to_currency: str,
    rates: Dict[str, float]
):

    usd_amount = amount / rates[from_currency]

    converted_amount = (
        usd_amount * rates[to_currency]
    )

    exchange_rate = (
        rates[to_currency] /
        rates[from_currency]
    )

    return converted_amount, exchange_rate

# ============================================================
# SIDEBAR
# ============================================================

with st.sidebar:

    st.markdown("## 💱 Khazabi")

    st.markdown("---")

    st.markdown("### 📖 How to Use")

    st.markdown("""
    **1.** Enter the amount.

    **2.** Select the source currency.

    **3.** Select the target currency.

    **4.** Click **Swap** to exchange currencies.

    **5.** View the converted amount.

    **6.** Check the market comparison chart.
    """)

    st.markdown("---")

    st.markdown("### 🌍 Popular Currencies")

    for currency in POPULAR_CURRENCIES:
        st.write(f"💰 {currency}")

    st.markdown("---")

    st.info(
        "Exchange rates are automatically updated every hour."
    )

    st.markdown("---")

    st.markdown(
        "**Developed by Khazabi ❤️**"
    )

# ============================================================
# MAIN TITLE
# ============================================================

st.markdown(
    '<div class="main-title">'
    '💱 Khazabi Currency Converter'
    '</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="sub-title">'
    '🌍 Real-Time Global Currency Converter & Analytics'
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# LOAD EXCHANGE RATES
# ============================================================

rates, last_updated, is_live = fetch_exchange_rates()

if not is_live:

    st.warning(
        "⚠️ Live exchange rates could not be loaded. "
        "Using fallback rates."
    )

# Combine API currencies with fallback currencies
currency_list = sorted(
    set(rates.keys()).union(FALLBACK_RATES.keys())
)

# ============================================================
# SESSION STATE
# ============================================================

if "from_currency" not in st.session_state:
    st.session_state.from_currency = "USD"

if "to_currency" not in st.session_state:
    st.session_state.to_currency = "INR"

# ============================================================
# SWAP FUNCTION
# ============================================================

def swap_currencies():

    temp = st.session_state.from_currency

    st.session_state.from_currency = (
        st.session_state.to_currency
    )

    st.session_state.to_currency = temp

# ============================================================
# CURRENCY INPUT SECTION
# ============================================================

st.markdown(
    '<div class="card">',
    unsafe_allow_html=True
)

col1, col2, col3, col4 = st.columns(
    [2.5, 2.5, 1, 2.5]
)

# Amount

with col1:

    amount = st.number_input(
        "💰 Amount",
        min_value=0.01,
        value=100.0,
        step=10.0,
        format="%.2f"
    )

# From Currency

with col2:

    from_currency = st.selectbox(
        "🌐 From Currency",
        currency_list,
        key="from_currency"
    )

# Swap

with col3:

    st.write("")

    st.button(
        "🔄 Swap",
        on_click=swap_currencies,
        use_container_width=True
    )

# To Currency

with col4:

    to_currency = st.selectbox(
        "🌎 To Currency",
        currency_list,
        key="to_currency"
    )

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

# ============================================================
# CALCULATE CONVERSION
# ============================================================

converted_amount, exchange_rate = convert_currency(
    amount,
    from_currency,
    to_currency,
    rates
)

# ============================================================
# RESULT BOX
# ============================================================

st.markdown(
    '<div class="result-box">',
    unsafe_allow_html=True
)

st.write(
    f"### {amount:,.2f} {from_currency}"
)

st.markdown(
    f'<div class="result-value">'
    f'{converted_amount:,.2f} {to_currency}'
    f'</div>',
    unsafe_allow_html=True
)

st.write(
    f"1 {from_currency} = "
    f"{exchange_rate:.4f} {to_currency}"
)

st.markdown(
    '</div>',
    unsafe_allow_html=True
)

st.write("")

# ============================================================
# RATE INFORMATION
# ============================================================

col1, col2, col3 = st.columns(3)

# Exchange Rate

with col1:

    st.metric(
        "💱 Exchange Rate",
        f"{exchange_rate:.4f}"
    )

# Inverse Rate

with col2:

    inverse_rate = 1 / exchange_rate

    st.metric(
        "🔁 Inverse Rate",
        f"{inverse_rate:.4f}"
    )

# Live Status

with col3:

    status = "🟢 Live" if is_live else "🟠 Offline"

    st.metric(
        "📡 Rate Status",
        status
    )

st.write("")

st.caption(
    f"🕐 Last Updated: {last_updated}"
)

# ============================================================
# QUICK CONVERSION
# ============================================================

st.markdown("---")

st.subheader("⚡ Quick Conversion")

quick_amounts = [
    1,
    10,
    50,
    100,
    500,
    1000
]

quick_data = []

for value in quick_amounts:

    result, _ = convert_currency(
        value,
        from_currency,
        to_currency,
        rates
    )

    quick_data.append({
        f"{from_currency} Amount": value,
        f"{to_currency} Value": round(
            result,
            2
        )
    })

quick_df = pd.DataFrame(
    quick_data
)

st.dataframe(
    quick_df,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# MARKET COMPARISON
# ============================================================

st.markdown("---")

st.subheader(
    f"📊 {amount:,.2f} {from_currency} "
    "Market Comparison"
)

comparison_data = []

for currency in POPULAR_CURRENCIES:

    if currency in rates:

        value, _ = convert_currency(
            amount,
            from_currency,
            currency,
            rates
        )

        comparison_data.append({
            "Currency": currency,
            "Converted Value": value
        })

comparison_df = pd.DataFrame(
    comparison_data
)

# ============================================================
# PLOTLY BAR CHART
# ============================================================

fig = px.bar(
    comparison_df,
    x="Currency",
    y="Converted Value",
    text_auto=".2f",
    title=(
        f"{amount:,.2f} {from_currency} "
        "Equivalent Values"
    ),
    color="Converted Value",
    color_continuous_scale="Blues"
)

fig.update_layout(
    height=450,
    xaxis_title="Currency",
    yaxis_title="Converted Value",
    showlegend=False,
    margin=dict(
        l=20,
        r=20,
        t=60,
        b=20
    )
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# ============================================================
# CURRENCY RATE TABLE
# ============================================================

st.markdown("---")

st.subheader("🌍 Currency Rates")

table_data = []

for currency in POPULAR_CURRENCIES:

    if currency in rates:

        table_data.append({
            "Currency": currency,
            "Rate vs USD": round(
                rates[currency],
                4
            )
        })

rates_df = pd.DataFrame(
    table_data
)

st.dataframe(
    rates_df,
    use_container_width=True,
    hide_index=True
)

# ============================================================
# FOOTER
# ============================================================

st.markdown(
    """
    <div class="footer">
        💱 <b>Khazabi Currency Converter</b><br>
        Real-time currency conversion and analytics<br>
        Made with ❤️ using Python + Streamlit
    </div>
    """,
    unsafe_allow_html=True
)