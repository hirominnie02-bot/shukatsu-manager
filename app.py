import streamlit as st
import sqlite3 
#軽量データベースインポート

st.title("就活管理アプリ")

company_name = st.text_input("会社名")

if st.button("保存"): #保存ボタンが押された時の処理
    #データベースjob_app.dbに接続
    conn = sqlite3.connect("job_app.db")

    #SQL実行担当作成
    cursor = conn.cursor()

    #SQL実行命令
    cursor.execute(
        "INSERT INTO companies (company_name) VALUES (?)", 
        # 第一引数：実行するSQL文
        # companiesテーブルのcompany_name列にデータを追加する
        (company_name,), 
        # 第二引数：プレースホルダー(?)に渡す実際の値
    )

    cursor.execute("SELECT * FROM companies")
    rows = cursor.fetchall()
    st.write(rows)

    #データベースの変更を確定
    conn.commit()

    #データベースの接続を終了する
    conn.close()
