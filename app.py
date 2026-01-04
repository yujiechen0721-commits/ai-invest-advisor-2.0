# app.py (主應用入口：多頁面架構，提升專業性與互動性)
import streamlit as st

# 隱藏右上角 GitHub + Fork 按鈕，並設定全局樣式
hide_menu_style = """
    <style>
    #MainMenu {visibility: hidden;}
    header {visibility: hidden;}
    .stDeployButton {display:none;}
    body {font-family: 'Segoe UI', sans-serif;}
    .stButton > button {background-color: #00C853; color: white; border: none; padding: 10px 20px; border-radius: 5px; font-weight: bold;}
    .stButton > button:hover {background-color: #009624;}
    </style>
    """
st.markdown(hide_menu_style, unsafe_allow_html=True)

# 主頁面內容
st.title("AI 投資小秘書")
st.markdown("---")
st.subheader("歡迎來到 AI 投資小秘書！")
st.write("""
    這是一個專業的 AI 輔助投資平台，幫助您根據年齡、風險偏好與每月投入金額，生成個人化資產配置建議。
    我們使用現代投資組合理論 (Modern Portfolio Theory) 結合歷史數據模擬，預估您的長期財富成長。
    
    **主要功能：**
    - **投資建議生成器**：輸入個人資訊，獲取 AI 推薦的資產配置與 20 年複利模擬圖表。
    - **資產分析工具**：查看個別資產歷史表現、實時報價與比較。
    - **教育資源**：學習投資基礎知識、風險管理與市場趨勢。
    - **個人化設定**：儲存您的偏好，接收模擬 LINE 盤後簡訊通知（未來可整合真實 API）。
    
    請從側邊欄選擇功能開始您的投資之旅！
""")

# 免責聲明（置於主頁底部）
st.markdown("---")
st.caption("免責聲明：本工具僅供教育與模擬用途，非證券投資顧問建議。歷史報酬不代表未來表現。投資有風險，請自行評估。")

# 注意：多頁面架構需在同一目錄下建立 'pages' 資料夾，並放置以下檔案：
# - pages/investment_advisor.py (投資建議生成器)
# - pages/asset_analyzer.py (資產分析工具)
# - pages/education_resources.py (教育資源)
# - pages/personal_settings.py (個人化設定)
