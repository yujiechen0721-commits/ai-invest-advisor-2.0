# pages/education_resources.py (教育資源頁面：新增內容，提升專業性)
import streamlit as st

st.title("教育資源")
st.markdown("---")
st.write("學習投資基礎知識，成為更聰明的投資者。")

tabs = st.tabs(["投資基礎", "風險管理", "市場趨勢"])

with tabs[0]:
    st.subheader("投資基礎")
    st.write("""
    - **多元化**：不要把所有雞蛋放在同一個籃子裡。
    - **複利效應**：時間是您最好的朋友，讓錢滾錢。
    - **ETF vs. 個股**：ETF 提供低成本的市場暴露。
    """)
    # 增加互動：影片嵌入（假設 YouTube 連結）
    st.video("https://www.youtube.com/embed/example_investment_basics")

with tabs[1]:
    st.subheader("風險管理")
    st.write("""
    - **風險偏好評估**：保守型偏好債券，積極型偏好股票。
    - **資產配置**：根據年齡調整股票/債券比例。
    - **止損策略**：設定規則，避免情緒決策。
    """)

with tabs[2]:
    st.subheader("市場趨勢")
    st.write("""
    - **AI 在投資**：機器學習預測市場走勢。
    - **永續投資**：ESG 因素越來越重要。
    - **全球經濟**：關注 Fed 利率與地緣政治。
    """)
    # 增加互動：外部連結
    st.markdown("[閱讀最新市場報告](https://www.example.com/market-report)")
