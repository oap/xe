import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
import numpy as np
from datetime import datetime, timedelta

# Page Config
st.set_page_config(page_title="Currency Exchange Analyzer", layout="wide")

# --- Language Support ---
TRANSLATIONS = {
    "English": {
        "title": "💱 Universal Currency Analyzer",
        "desc": "This dashboard helps you decide **when to exchange currencies** (e.g., CAD to USD, CNY to EUR).\nIt analyzes historical trends, calculates technical indicators (RSI), and compares the current rate against moving averages.",
        "settings": "Settings",
        "language": "Language",
        "source_currency": "Source Currency (From)",
        "target_currency": "Target Currency (To)",
        "timeframe": "Timeframe",
        "current_rate": "Current Rate",
        "avg_30": "30-Day Average",
        "rsi_help": "<30: Oversold (Good time to buy?), >70: Overbought",
        "decision": "Decision Signal",
        "historical": "Historical Performance",
        "converter": "🧮 Quick Converter",
        "amount": "Amount in {currency}",
        "more_than_avg": "🎉 This is **{diff:,.2f} {target} MORE** than the 30-day average.",
        "less_than_avg": "📉 This is **{diff:,.2f} {target} LESS** than the 30-day average.",
        "disclaimer": "Data source: Yahoo Finance. Disclaimer: This is for informational purposes only, not financial advice.",
        "good_uptrend": "GOOD (Uptrend)",
        "caution": "CAUTION (Overbought)",
        "opportunity": "OPPORTUNITY? (Oversold)",
        "wait": "WAIT (Downtrend)",
        "neutral": "NEUTRAL",
        "index_value": "Index Value",
        "points": "Points",
        "per_unit": "{target} per 1 {source}",
        "unit_per_unit": "1 {source} = {rate:.4f} {target}",
        "inverse_rate": "1 {target} = {rate:.4f} {source}",
        "base_currency": "Base Currency View",
        "help_title": "📖 Help & Documentation",
    },
    "简体中文": {
        "title": "💱 通用汇率分析器",
        "desc": "此仪表盘帮助您决定**何时进行货币兑换** (如 CAD 换 USD, CNY 换 EUR)。\n它通过分析历史趋势、计算技术指标 (RSI) 并比较当前汇率与移动平均线来提供参考。",
        "settings": "设置",
        "language": "语言",
        "source_currency": "持有货币 (卖出)",
        "target_currency": "目标货币 (买入)",
        "timeframe": "时间范围",
        "current_rate": "当前汇率",
        "avg_30": "30天平均线",
        "rsi_help": "<30: 超卖 (买入良机?), >70: 超买",
        "decision": "决策信号",
        "historical": "历史走势",
        "converter": "🧮 快速换算",
        "amount": "{currency} 金额",
        "more_than_avg": "🎉 比30天平均水平 **多换 {diff:,.2f} {target}**。",
        "less_than_avg": "📉 比30天平均水平 **少换 {diff:,.2f} {target}**。",
        "disclaimer": "数据来源: Yahoo Finance. 免责声明: 仅供参考，不构成理财建议。",
        "good_uptrend": "优 (上升趋势)",
        "caution": "谨慎 (超买)",
        "opportunity": "机会? (超卖)",
        "wait": "观望 (下跌趋势)",
        "neutral": "中立",
        "index_value": "指数数值",
        "points": "点数",
        "per_unit": "每1 {source} 兑换 {target}",
        "unit_per_unit": "1 {source} = {rate:.4f} {target}",
        "inverse_rate": "1 {target} = {rate:.4f} {source}",
        "base_currency": "基准视角",
        "help_title": "📖 帮助与文档",
    }
}

HELP_DOCS = {
    "English": """
### 💡 How to use
1. **Select Currencies:** Choose your Source (what you have) and Target (what you want).
2. **Select Timeframe:** View historical trends (1mo, 1y, etc.).
3. **Base Currency View:** Toggle between:
    - **Source:** Shows "1 Source = X Target". Your buying power.
    - **Target:** Shows "1 Target = X Source". The cost of the target currency.

### 📊 Indicators Explained
- **RSI (Relative Strength Index):**
    - **< 30 (Oversold):** The currency might be undervalued. Potential buying opportunity 🟢.
    - **> 70 (Overbought):** The currency might be overvalued. Careful, it might drop 🔴.
- **SMA (Simple Moving Average):**
    - **SMA 30 (Orange):** Short-term average trend.
    - **SMA 100 (Blue):** Long-term average trend.
    - If the Rate is **above** SMA 30, it indicates a short-term **uptrend**.

### 🚦 Decision Signals
- **GOOD:** Rate > 30-day Average (Uptrend) AND RSI is not overbought (<70).
- **OPPORTUNITY?:** RSI is < 30 (Oversold). Market might correct upwards.
- **CAUTION:** RSI is > 70 (Overbought). Market might correct downwards.
- **WAIT:** Rate < 30-day Average (Downtrend).
""",
    "简体中文": """
### 💡 如何使用
1. **选择货币:** 选择您的持有货币 (源) 和目标货币。
2. **选择时间范围:** 查看历史趋势 (1个月, 1年等)。
3. **基准视角:** 切换视角:
    - **Source (源货币):** 显示 "1 源货币 = X 目标货币"。查看您的**购买力**。
    - **Target (目标货币):** 显示 "1 目标货币 = X 源货币"。查看目标货币的**成本**。

### 📊 指标说明
- **RSI (相对强弱指数):**
    - **< 30 (超卖):** 货币可能被低估。可能是买入良机 🟢。
    - **> 70 (超买):** 货币可能被高估。需谨慎，可能会下跌 🔴。
- **SMA (移动平均线):**
    - **SMA 30 (橙色):** 短期平均趋势。
    - **SMA 100 (蓝色):** 长期平均趋势。
    - 如果当前汇率 **高于** SMA 30，通常表示短期处于**上升趋势**。

### 🚦 决策信号
- **优 (GOOD):** 汇率 > 30天平均线 (上升趋势) 且 RSI 未超买 (<70)。
- **机会? (OPPORTUNITY):** RSI < 30 (超卖)。市场可能会反弹。
- **谨慎 (CAUTION):** RSI > 70 (超买)。市场可能会回调。
- **观望 (WAIT):** 汇率 < 30天平均线 (下跌趋势)。
"""
}

# Sidebar - Language Selector (First item)
st.sidebar.header("Settings") # Placeholder, will be overwritten visually but keeps structure
lang_choice = st.sidebar.radio("Language / 语言", ["English", "简体中文"])
t = TRANSLATIONS[lang_choice]

# Title and Description
st.title(t["title"])
st.markdown(t["desc"])

# Sidebar Controls
st.sidebar.markdown("---")
st.sidebar.header(t["settings"])

# Currency List
CURRENCIES = ["CNY", "USD", "CAD", "EUR", "GBP", "JPY", "AUD", "NZD", "CHF", "SGD", "HKD"]
EXTRAS = ["DXY (US Dollar Index)"]

# Source Selection
source_currency = st.sidebar.selectbox(t["source_currency"], CURRENCIES, index=0)

# Target Selection
# Remove source from target list to avoid 1:1, but keep logic simple
target_options = [c for c in CURRENCIES if c != source_currency] + EXTRAS
# Default to USD if available and not source, else CAD
default_target_index = 0
if "USD" in target_options:
    default_target_index = target_options.index("USD")
elif "CAD" in target_options:
    default_target_index = target_options.index("CAD")

target_currency = st.sidebar.selectbox(t["target_currency"], target_options, index=default_target_index)

timeframe = st.sidebar.selectbox(t["timeframe"], ["1mo", "3mo", "6mo", "1y", "2y", "5y"], index=3)

# Base Currency Selection (Only if not DXY)
is_dxy = target_currency == "DXY (US Dollar Index)"
base_selection = source_currency # Default

if not is_dxy:
    base_selection = st.sidebar.radio(
        t["base_currency"],
        [source_currency, target_currency],
        help="Select which currency is the '1' in '1 Base = ? Quote'"
    )

# Ticker Construction Logic
# We try to construct a ticker. We will try SourceTarget=X first.
# If it fails, get_data will try TargetSource=X and invert.
# DXY is special.
if is_dxy:
    ticker = "DX-Y.NYB"
else:
    # Standard format for Yahoo Finance
    ticker = f"{source_currency}{target_currency}=X"

# Data Fetching
@st.cache_data(ttl=3600)
def get_data(source, target, period):
    
    def clean_data(df):
        # 1. Drop NaNs
        df = df.dropna()
        # 2. Filter invalid prices
        if 'Close' in df.columns:
            df = df[df['Close'] > 0]
        # 3. Filter extreme outliers (> 20% daily change)
        # This catches "bad ticks" where price jumps to 0 or massive value
        if 'Close' in df.columns:
            pct_change = df['Close'].pct_change()
            # Keep rows where pct_change is NaN (first row) OR abs change < 0.2
            mask = (pct_change.isna()) | (pct_change.abs() < 0.20)
            df = df[mask]
        return df

    is_dxy = target == "DXY (US Dollar Index)"
    
    if is_dxy:
        data = yf.download("DX-Y.NYB", period=period, progress=False)
        if data.empty: return None
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
        
        df = clean_data(data.copy())
        if df.empty: return None
        
        # DXY is just points, no "Inverse" really, but for code safety:
        df['Close_Inv'] = df['Close']
        df['Open_Inv'] = df['Open']
        df['High_Inv'] = df['High']
        df['Low_Inv'] = df['Low']
        return df

    # Attempt 1: Source -> Target (e.g. CADUSD=X)
    t1 = f"{source}{target}=X"
    data = yf.download(t1, period=period, progress=False)
    
    if data is not None and not data.empty:
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
        df = clean_data(data.copy())
        
        if not df.empty:
            # Raw data is already Source->Target
            df['Close_Inv'] = 1 / df['Close']
            df['Open_Inv'] = 1 / df['Open']
            df['High_Inv'] = 1 / df['Low'] 
            df['Low_Inv'] = 1 / df['High']
            return df

    # Attempt 2: Target -> Source (e.g. USDCAD=X)
    t2 = f"{target}{source}=X"
    data = yf.download(t2, period=period, progress=False)
    
    if data is not None and not data.empty:
        if isinstance(data.columns, pd.MultiIndex): data.columns = data.columns.droplevel(1)
        df = clean_data(data.copy())
        
        if not df.empty:
            # Raw data is Target->Source. We need to FLIP it to make 'Close' match Source->Target
            # So 'Close' becomes 1/RawClose
            # And 'Close_Inv' becomes RawClose
            
            raw_open = df['Open']
            raw_high = df['High']
            raw_low = df['Low']
            raw_close = df['Close']
            
            # Invert to get Source->Target (Primary View)
            df['Open'] = 1 / raw_open
            df['High'] = 1 / raw_low  # Swap High/Low
            df['Low'] = 1 / raw_high
            df['Close'] = 1 / raw_close
            
            # "Inv" view (Target->Source) is actually the raw data
            df['Open_Inv'] = raw_open
            df['High_Inv'] = raw_high
            df['Low_Inv'] = raw_low
            df['Close_Inv'] = raw_close
            
            return df

    return None

data = get_data(source_currency, target_currency, timeframe)

if data is None:
    st.error(f"Could not fetch data for {source_currency} -> {target_currency}. Please try a different pair.")
    st.stop()

# Prepare Analysis Data based on Selection
# Logic: 
# 'Close' is ALWAYS 1 Source = ? Target
# 'Close_Inv' is ALWAYS 1 Target = ? Source

if is_dxy:
    plot_open = data['Open']
    plot_high = data['High']
    plot_low = data['Low']
    plot_close = data['Close']
    display_rate_label = t["index_value"]
    y_axis_label = t["points"]
    
elif base_selection == source_currency:
    # User wants Source View (1 Source = ? Target) -> Use 'Close'
    plot_open = data['Open']
    plot_high = data['High']
    plot_low = data['Low']
    plot_close = data['Close']
    display_rate_label = t["unit_per_unit"].format(source=source_currency, rate=plot_close.iloc[-1], target=target_currency)
    y_axis_label = t["per_unit"].format(source=source_currency, target=target_currency)

else:
    # User wants Target View (1 Target = ? Source) -> Use 'Close_Inv'
    plot_open = data['Open_Inv']
    plot_high = data['High_Inv']
    plot_low = data['Low_Inv']
    plot_close = data['Close_Inv']
    display_rate_label = t["unit_per_unit"].format(source=target_currency, rate=plot_close.iloc[-1], target=source_currency)
    y_axis_label = t["per_unit"].format(source=target_currency, target=source_currency)




# Calculations (on Selected Data)




# SMA




sma_30 = plot_close.rolling(window=30).mean()




sma_100 = plot_close.rolling(window=100).mean()









# RSI




def calculate_rsi(series, period=14):




    delta = series.diff()




    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()




    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()




    rs = gain / loss




    return 100 - (100 / (1 + rs))









rsi = calculate_rsi(plot_close)









# Latest Data Points




latest_date = data.index[-1]




# Accessing scalar values using .iloc[-1] and .item() to ensure we get a float, not a Series




current_rate = plot_close.iloc[-1].item() if isinstance(plot_close.iloc[-1], pd.Series) else plot_close.iloc[-1]




prev_rate = plot_close.iloc[-2].item() if isinstance(plot_close.iloc[-2], pd.Series) else plot_close.iloc[-2]




change_pct = ((current_rate - prev_rate) / prev_rate) * 100









latest_rsi = rsi.iloc[-1].item() if isinstance(rsi.iloc[-1], pd.Series) else rsi.iloc[-1]




latest_sma_30 = sma_30.iloc[-1].item() if isinstance(sma_30.iloc[-1], pd.Series) else sma_30.iloc[-1]









# For the converter captions, we need both rates regardless of selection




# Close is Source->Target, Close_Inv is Target->Source (based on our get_data contract)




rate_source_to_target = data['Close'].iloc[-1].item()




rate_target_to_source = data['Close_Inv'].iloc[-1].item()









# --- Dashboard Layout ---









# 1. Key Metrics Row




col1, col2, col3, col4 = st.columns(4)




with col1:




    st.metric(t["current_rate"], f"{current_rate:.4f}", f"{change_pct:.2f}%")




    if not is_dxy:




        st.caption(display_rate_label) 




with col2:




    st.metric(t["avg_30"], f"{latest_sma_30:.4f}", delta=f"{current_rate - latest_sma_30:.4f}")




with col3:




    st.metric("RSI (14)", f"{latest_rsi:.1f}", help=t["rsi_help"])




with col4:




    # Logic for "Good Time?"




    # Simple heuristic:




    # Good if Rate > SMA_30 (trending up) AND RSI < 70 (not overbought yet)




    # OR if RSI < 30 (Oversold bounce candidate)




    




    status = t["neutral"]




    color = "off"




    




    if current_rate > latest_sma_30:




        if latest_rsi < 70:




            status = t["good_uptrend"]




            color = "normal" # green usually




        else:




            status = t["caution"]




            color = "inverse"




    elif latest_rsi < 30:




        status = t["opportunity"]




        color = "normal"




    else:




        status = t["wait"]




        color = "off"




        




    st.metric(t["decision"], status)









# 2. Main Chart




st.subheader(t["historical"])









fig = go.Figure()









# Candlestick




fig.add_trace(go.Candlestick(x=data.index,




                open=plot_open,




                high=plot_high,




                low=plot_low,




                close=plot_close,




                name='Rate'))









# SMAs




fig.add_trace(go.Scatter(x=data.index, y=sma_30, line=dict(color='orange', width=1), name='SMA 30'))




fig.add_trace(go.Scatter(x=data.index, y=sma_100, line=dict(color='blue', width=1), name='SMA 100'))









fig.update_layout(




    title=f"{source_currency} -> {target_currency} ({display_rate_label})",




    yaxis_title=y_axis_label,




    xaxis_rangeslider_visible=False,




    height=500




)









st.plotly_chart(fig, use_container_width=True)









# 3. Converter Tool (Only for currencies)




if not is_dxy:




    st.divider()




    st.subheader(t["converter"])




    c1, c2 = st.columns([1, 2])




    




    if base_selection == source_currency:




        # View: Source -> Target (1 Source = X Target)




        # Input: Source Currency, Output: Target Currency




        # Rate: Close (Source->Target)




        




        input_label = t["amount"].format(currency=source_currency)




        input_currency = source_currency




        output_currency = target_currency




        




        with c1:




            amount = st.number_input(input_label, value=1000, step=100)




        with c2:




            converted = amount * current_rate




            st.success(f"{amount:,.0f} {input_currency} = **{converted:,.2f} {output_currency}**")




            




            # Comparison




            avg_converted = amount * latest_sma_30




            diff = converted - avg_converted




            if diff > 0:




                st.caption(t["more_than_avg"].format(diff=diff, target=output_currency))




            else:




                st.caption(t["less_than_avg"].format(diff=abs(diff), target=output_currency))




    else:




        # View: Target -> Source (1 Target = X Source)




        # Input: Target Currency, Output: Source Currency




        # Rate: Close_Inv (Target->Source) which IS 'current_rate' in this branch




        




        input_label = t["amount"].format(currency=target_currency)




        input_currency = target_currency




        output_currency = source_currency




        




        with c1:




            amount = st.number_input(input_label, value=1000, step=100)




        with c2:




            converted = amount * current_rate




            st.success(f"{amount:,.0f} {input_currency} = **{converted:,.2f} {output_currency}**")




            




            # Comparison




            avg_converted = amount * latest_sma_30




            diff = converted - avg_converted




            if diff > 0:




                st.caption(t["more_than_avg"].format(diff=diff, target=output_currency))




            else:




                st.caption(t["less_than_avg"].format(diff=abs(diff), target=output_currency))

# Help / Documentation
st.divider()
with st.expander(t["help_title"]):
    st.markdown(HELP_DOCS[lang_choice])

# Footer
st.markdown("---")
st.caption(t["disclaimer"])
