# pages/asset_analyzer.py (資產分析工具頁面：新增功能，提升專業性)
import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.title("資產分析工具")
st.markdown("---")
st.write("選擇資產，查看歷史表現與實時報價。")

tickers = ["0050.TW", "0056.TW", "VT", "BND", "^TWII"]
selected_ticker = st.selectbox("選擇資產", tickers)

period = st.selectbox("時間範圍", ["1mo", "3mo", "6mo", "1y", "2y", "5y", "10y", "20y", "max"])

if st.button("分析資產"):
    data = yf.download(selected_ticker, period=period, progress=False)
    if not data.empty:
        close_col = 'Adj Close' if 'Adj Close' in data.columns else 'Close'
        
        # 實時報價
        latest = yf.Ticker(selected_ticker).info
        st.subheader("實時資訊")
        col1, col2, col3 = st.columns(3)
        col1.metric("最新價格", f"{latest.get('regularMarketPrice', 'N/A')} {latest.get('currency', '')}")
        col2.metric("今日漲跌", f"{latest.get('regularMarketChangePercent', 'N/A'):.2f}%")
        col3.metric("市值", f"{latest.get('marketCap', 'N/A') / 1e9:.2f}B")
        
        # 歷史圖表
        fig = go.Figure()
        fig.add_trace(go.Candlestick(x=data.index,
                                     open=data['Open'], high=data['High'], low=data['Low'], close=data[close_col],
                                     name=selected_ticker))
        fig.update_layout(title=f"{selected_ticker} 歷史表現",
                          xaxis_title="日期", yaxis_title="價格",
                          template="plotly_white",
                          xaxis_rangeslider_visible=True)  # 增加互動：範圍滑桿
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.error("無法載入數據，請檢查資產代碼。")
