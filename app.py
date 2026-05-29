import streamlit as st

st.title("就活管理アプリ")

company_name = st.text_input("会社名")

if st.button("保存"):
    st.write("保存しました！")
    st.write(company_name)