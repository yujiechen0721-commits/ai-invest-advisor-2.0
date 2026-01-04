import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime, timedelta

# --- 頁面基本配置 ---
st.set_page_config(
    page_title="AI Pro 投資領航員",
    page_icon="💎",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- 專業深色美化 CSS ---
st.markdown("""
    <style>
    .main { background-color: #f8f9fa; }
    .stMetric { background-color: #ffffff; padding: 15px; border-radius: 10px; box-shadow: 0 2px 4px rgba(0,0,0,0.05); }
    div[data-testid="stExpander"] { background-color: white; border-radius: 10px; }
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    .stButton>button { width: 100%; border-radius: 5px; height: 3em; background-color: #007bff; color: white; }
    </style>
    """, unsafe_allow_html=True)

# --- 導覽列設計 ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/2622/2622814.png", width=80)
    st.title("AI 投資領航員")
    st.markdown("---")
    menu = st.radio(
        "功能導覽",
        ["🏠 數據首頁", "🎯 智能資產配置", "🔍 全球市場追蹤", "📚 投資知識庫"]
    )
    st.markdown("---")
    st.caption("版本 v2.1.0 | 數據由 Yahoo Finance 提供")

# ==========================================
# 🏠 數據首頁：市場快訊與核心指標
# ==========================================
if menu == "🏠 數據首頁":
    st.title("今日全球市場概況")
    
    # 頂部指標
    col1, col2, col3, col4 = st.columns(4)
    with col1: st.metric("台股加權 (TWII)", "18,234.5", "+1.25%")
    with col2: st.metric("標普 500 (SPY)", "4,783.2", "-0.12%")
    with col3: st.metric("恐懼與貪婪指數", "68", "貪婪")
    with col4: st.metric("美債 10Y 殖利率", "4.15%", "-0.05")

    st.markdown("### 🚀 熱門主題分析")
    c1, c2 = st.columns(2)
    with c1:
        st.info("💡 **AI 觀點**：目前半導體板塊顯示出強勁的動能，建議關注 2330.TW 的支撐位。")
    with c2:
        st.warning("⚠️ **風險提示**：通膨數據將於明日公佈，市場波動可能加劇。")

    st.markdown("### 📅 近期關鍵事件")
    event_data = {
        "日期": ["2024-01-10", "2024-01-15", "2024-01-20"],
        "事件": ["美國 CPI 公佈", "台積電法說會", "聯準會利率決策"],
        "重要性": ["⭐⭐⭐", "⭐⭐", "⭐⭐⭐"]
    }
    st.table(pd.DataFrame(event_data))

# ==========================================
# 🎯 智能資產配置：互動式規劃器
# ==========================================
elif menu == "🎯 智能資產配置":
    st.title("🎯 智能投資組合建議")
    
    col_l, col_r = st.columns([1, 2])
    
    with col_l:
        st.subheader("參數設定")
        user_age = st.slider("年齡", 18, 80, 30)
        user_budget = st.number_input("每月預計投入 (TWD)", 5000, 500000, 10000, 5000)
        user_risk = st.select_slider("風險承擔意願", options=["保守", "穩健", "平衡", "成長", "激進"], value="平衡")
        
        generate = st.button("生成分析報告")

    if generate:
        with col_r:
            st.subheader("分析結果")
            
            # 簡單配置邏輯
            alloc = {"台股龍頭": 40, "全球股票": 30, "美國公債": 20, "現金備用": 10}
            if user_risk == "激進": alloc = {"台股龍頭": 60, "全球股票": 30, "加密貨幣": 10}
            
            # 圓餅圖
            fig = go.Figure(data=[go.Pie(labels=list(alloc.keys()), values=list(alloc.values()), hole=.4)])
            fig.update_layout(margin=dict(t=0, b=0, l=0, r=0), height=300)
            st.plotly_chart(fig, use_container_width=True)
            
            st.success(f"建議策略：**{user_risk}型配置**")
            st.write(f"預計在 {user_age+20} 歲時，透過複利效應，您的資產規模將極大化。")
            
            with st.expander("查看具體代碼建議"):
                st.write("- **0050.TW** (佔比 40%)")
                st.write("- **VT** (佔比 30%)")
                st.write("- **BND** (佔比 30%)")

# ==========================================
# 🔍 全球市場追蹤：專業看盤區
# ==========================================
elif menu == "🔍 全球市場追蹤":
    st.title("🔍 即時數據監控")
    
    target = st.text_input("請輸入股票或 ETF 代碼 (例如: 2330.TW, TSLA, 0050.TW)", "2330.TW")
    
    if target:
        try:
            with st.spinner('正在獲取最新數據...'):
                df = yf.download(target, period="6mo")
                
                # 指標卡片
                last_price = df['Close'].iloc[-1]
                change = df['Close'].iloc[-1] - df['Close'].iloc[-2]
                
                c1, c2, c3 = st.columns(3)
                c1.metric("當前價格", f"{last_price:,.2f}", f"{change:,.2f}")
                c2.metric("半年最高", f"{df['High'].max():,.2f}")
                c3.metric("半年最低", f"{df['Low'].min():,.2f}")
                
                # K 線圖
                fig = go.Figure(data=[go.Candlestick(
                    x=df.index,
                    open=df['Open'], high=df['High'],
                    low=df['Low'], close=df['Close'],
                    increasing_line_color='#ef5350', decreasing_line_color='#26a69a'
                )])
                fig.update_layout(title=f"{target} 走勢圖", xaxis_rangeslider_visible=False, height=500)
                st.plotly_chart(fig, use_container_width=True)
        except:
            st.error("無法讀取數據，請確認代碼是否正確。")

# ==========================================
# 📚 投資知識庫：教育功能
# ==========================================
elif menu == "📚 投資知識庫":
    st.title("📚 投資必修課")
    
    topics = {
        "新手入門": ["什麼是複利？", "定期定額 vs 單筆投入", "ETF 是什麼？"],
        "進階策略": ["資產撥備與再平衡", "技術指標 KD/RSI 應用", "財報分析基礎"],
        "心理素質": ["如何應對股市大跌？", "克服貪婪與恐懼"]
    }
    
    tab1, tab2, tab3 = st.tabs(["基礎概念", "技術分析", "投資心理"])
    
    with tab1:
        st.markdown("""
        ### 為什麼要投資？
        投資的核心在於對抗通膨。若通膨率為 3%，現在的 100 萬在 20 年後購買力僅剩約 54 萬。
        ### 定期定額的威力
        這是一種利用「時間」攤平「成本」的策略，適合大多數上班族。
        """)
        st.video("https://www.youtube.com/watch?v=dQw4w9WgXcQ") # 此處可放教學影片連結

    with tab2:
        st.info("這裡可以放置更多關於如何閱讀本站圖表的教學。")
        
    with tab3:
        st.warning("投資成功的關鍵不在於智商，而在於自律。")

# --- 頁尾 ---
st.markdown("---")
st.markdown("<center> AI 投資領航員 © 2024 | 本網站僅供學習參考，不構成任何投資建議 </center>", unsafe_allow_html=True)
