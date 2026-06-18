import streamlit as st
import sqlite3 
#軽量データベースインポート

st.title("就活管理アプリ")
company_name = st.text_input("会社名")

#データベースjob_app.dbに接続
conn = sqlite3.connect("job_app.db")
#SQL実行担当作成
cursor = conn.cursor()

if st.button("保存"): #保存ボタンが押された時の処理---------------------
    # 同じ会社があるか確認
    cursor.execute(
        #companiesテーブルからcompany_nameが入力された会社名と同じ物を探す
       "SELECT * FROM companies WHERE company_name = ?",
        (company_name,)
    )
    #最初に見つかった1件を受け取る⇔同じ会社があるか判断
    result = cursor.fetchone()

    if result: #見つかったなら
        st.warning("既に登録されています")
    else: #みつかった以外の時
        cursor.execute(
            #新しいデータ (company_name)をcompanies(company_name)に追加
            "INSERT INTO companies (company_name) VALUES (?)",
            (company_name,)
        )

        #データベースの変更を確定
        conn.commit()

        st.success("登録しました！")
    
#登録企業名一覧表示--------------------------------
cursor.execute("SELECT * FROM companies")
rows = cursor.fetchall()
st.subheader("登録済み企業")

for row in rows:
    st.write(row[1])

#-------------------------------------------------

#データベースの接続を終了する
conn.close()
