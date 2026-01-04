# pages/investment_advisor.py (投資建議生成器頁面：基於原代碼，提升互動性)
import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# === AI 資產配置建議 ===
def get_ai_allocation(age, monthly_save, risk):
    base = {
        "0050.TW": 0.4, "0056.TW": 0.3, "VT": 0.2, "BND": 0.1
    }
    if risk == "保守":
        base["BND"] += 0.2; base["VT"] -= 0.1; base["0050.TW"] -= 0.1
    elif risk == "積極":
        base["VT"] += 0.2; base["BND"] -= 0.1; base["0056.TW"] -= 0.1
    st.info(f"**AI 小秘書建議（{age}歲，每月投入 {monthly_save:,.0f} 元，風險：{risk}）**\n"
            f"根據現代投資組合理論，建議資產配置：")
    for t, w in base.items():
        name = {"0050.TW":"台灣50", "0056.TW":"高股息", "VT":"全球股票", "BND":"美國債券"}[t]
        st.write(f"• **{name}** (`{t}`): {w*100:.0f}%")
    return base

# === 模擬 20 年複利 ===
def simulate_portfolio(allocation, monthly_save, years=20):
    end_date = datetime.now()
    start_date = f"{end_date.year - years}-01-01"
    total_monthly_return = 0.0
    valid_count = 0
    for ticker, weight in allocation.items():
        try:
            data = yf.download(ticker, start=start_date, end=end_date, progress=False)
            if data.empty:
                continue
            close_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
            monthly_return = data[close_col].resample('M').last().pct_change().mean()
            if pd.notna(monthly_return):
                total_monthly_return += monthly_return * weight
                valid_count += 1
        except:
            continue
    if valid_count == 0:
        total_monthly_return = 0.005  # 預設 0.5%/月
    months = years * 12
    future_value = 0.0
    values = []
    for m in range(months):
        future_value = future_value * (1 + total_monthly_return) + monthly_save
        if m % 12 == 0:
            values.append(future_value)
    return values

# 頁面介面
st.title("投資建議生成器")
st.markdown("---")
st.write("輸入您的個人資訊，AI 將生成專屬投資建議與長期模擬。")

with st.form(key="investment_form"):
    col1, col2 = st.columns(2)
    with col1:
        age = st.slider("年齡", 20, 60, 30)
        monthly_save = st.number_input("每月投入 (元)", 1000, 50000, 5000, 1000)
    with col2:
        risk = st.selectbox("風險偏好", ["保守", "中性", "積極"])
        submit_button = st.form_submit_button(label="生成投資建議")

if submit_button:
    allocation = get_ai_allocation(age, monthly_save, risk)
    values = simulate_portfolio(allocation, monthly_save)
    years = list(range(0, 21))
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=years, y=values, mode='lines+markers', name='您的組合', line=dict(color='#00C853')))
    
    # 台股對比（增加互動：可切換顯示）
    show_twse = st.checkbox("顯示台股加權指數對比", value=True)
    if show_twse:
        try:
            twse_data = yf.download("^TWII", period="20y", progress=False)
            if not twse_data.empty:
                close_col = 'Adj Close' if 'Adj Close' in twse_data.columns else 'Close'
                twse_ret = twse_data[close_col].resample('M').last().pct_change().mean()
                if pd.notna(twse_ret):
                    tv = 0.0
                    tvs = []
                    for m in range(240):
                        tv = tv * (1 + twse_ret) + monthly_save
                        if m % 12 == 0:
                            tvs.append(tv)
                    fig.add_trace(go.Scatter(x=years, y=tvs, mode='lines+markers', name='台股加權指數', line=dict(color='#FF5722')))
        except:
            st.warning("無法載入台股數據，請稍後再試。")
    
    fig.update_layout(
        title="20 年複利模擬",
        xaxis_title="年",
        yaxis_title="總資產 (元)",
        legend=dict(x=0.02, y=0.98),
        template="plotly_white",
        hovermode="x unified"  # 提升互動：統一 hover 顯示
    )
    st.plotly_chart(fig, use_container_width=True)
    st.success(f"**20 年後預估資產：{values[-1]:,.0f} 元**")
    
    # 增加下載報告功能（提升專業性）
    report_data = pd.DataFrame({"年": years, "您的組合 (元)": [f"{v:,.0f}" for v in values]})
    if show_twse and 'tvs' in locals():
        report_data["台股加權指數 (元)"] = [f"{tv:,.0f}" for tv in tvs]
    csv = report_data.to_csv(index=False).encode('utf-8')
    st.download_button("下載報告 (CSV)", csv, "investment_report.csv", "text/csv")

# LINE 簡訊模擬（置於 expander，提升互動）
with st.expander("模擬 LINE 每日盤後簡訊"):
    st.markdown(
        """
        <div style="background-color: #1a1a2e; color: white; padding: 15px; border-radius: 10px; border-left: 5px solid #00C853;">
        <strong style="font-size: 16px;">LINE 每日盤後簡訊（模擬功能）</strong><br><br>
        • <strong>時間</strong>：每日 18:00 自動推播<br>
        • <strong>內容</strong>：今日投資組合表現 + 最新模擬<br>
        • <strong>技術</strong>：使用 LINE Messaging API 實現（未來整合）
        </div>
        """,
        unsafe_allow_html=True
    )
