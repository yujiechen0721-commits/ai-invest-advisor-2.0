# pages/personal_settings.py (個人化設定頁面：新增功能，提升互動性)
import streamlit as st

st.title("個人化設定")
st.markdown("---")
st.write("儲存您的偏好，獲得更個人化的體驗。")

# 使用 session_state 模擬用戶資料（未來可整合資料庫）
if "user_profile" not in st.session_state:
    st.session_state.user_profile = {}

with st.form(key="profile_form"):
    name = st.text_input("姓名", value=st.session_state.user_profile.get("name", ""))
    email = st.text_input("電子郵件", value=st.session_state.user_profile.get("email", ""))
    notify = st.checkbox("啟用 LINE 盤後通知（模擬）", value=st.session_state.user_profile.get("notify", False))
    submit = st.form_submit_button("儲存設定")

if submit:
    st.session_state.user_profile = {"name": name, "email": email, "notify": notify}
    st.success("設定已儲存！")
    
    if notify:
        st.info("已啟用模擬 LINE 通知：每日 18:00 推送投資更新。")

# 顯示目前設定
st.subheader("目前設定")
st.json(st.session_state.user_profile)
