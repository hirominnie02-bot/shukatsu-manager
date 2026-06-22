import streamlit as st
import sqlite3 #軽量データベースインポート
import pandas as pd


st.title("就活管理アプリ")
company_name = st.text_input("会社名")
status = st.selectbox(
    "応募状況",
    ["応募前", "応募済", "書類選考", "面接予定", "内定", "返信待ち"]
)
apply_date = st.date_input("応募日")

#データベースjob_app.dbに接続
conn = sqlite3.connect("job_app.db")
#SQL実行担当作成
cursor = conn.cursor()

if st.button("保存"): #保存ボタンが押された時の処理---------------------
    # 同じ会社があるか確認
    cursor.execute(
        #companiesテーブルからcompany_nameが入力された会社名と同じ物を探す
       "SELECT * FROM companies WHERE company_name = ?",
        (company_name,) #プレースホルダー(?)に値を渡す時はタプル形式で渡す
    )
    #最初に見つかった1件を受け取る⇔同じ会社があるか判断
    result = cursor.fetchone()

    if result: #見つかったなら
        st.warning("既に登録されています")
    else: #みつかった以外の時
        cursor.execute(
            #新しいデータ (company_name)をcompanies(company_name)に追加
            "INSERT INTO companies (company_name, status, application_date) VALUES (?, ?, ?)",
            (company_name,status, apply_date)
        )

        #データベースの変更を確定
        conn.commit()

        st.success("登録しました！")


#操作画面--------------------------------
cursor.execute("SELECT * FROM companies")
rows = cursor.fetchall()


#検索機能--------------------------------
search_word = st.text_input("会社名検索") 

display_rows = rows
if search_word:
    display_rows = []

    for row in rows:
        if search_word in row[1]:
            display_rows.append(row)
    
    if len(display_rows) == 0:
            st.warning("該当する企業がありません")



# 応募状況をデータフレームで表示----------
df = pd.DataFrame(
rows,
columns=["ID", "会社名", "応募状況", "応募日"]
)
status_count = df["応募状況"].value_counts()
# st.write(status_count)

# 応募状況をサマリーとして表示------------
st.subheader("応募状況サマリー")
st.write(f"登録企業数：{len(rows)}件")
for status, count in status_count.items():
    st.write(f"{status}：{count}件")

# 登録企業名一覧表示--------------------
for row in display_rows:
    col1, col2, col3, col4, col5 = st.columns([3,2,2,2,1])

    with col1:
        st.write(row[1])

    with col2:
        st.write(row[2])

    with col3:
        new_status = st.selectbox(
            "応募状況",
            ["応募前", "応募済", "書類選考", "面接予定", "内定", "返信待ち"],
            key=f"status_{row[0]}"
        )
        if st.button("変更", key=f"edit_{row[0]}"):

            cursor.execute(
                """
                UPDATE companies
                SET status = ?
                WHERE id = ?
                """,
                (new_status, row[0])
            )

            conn.commit()
            st.rerun()
                        
    
    with col4:
        if row[3] is None:
            st.write("未設定")
        else:
            st.write(row[3])
    
    with col5:
        if st.button("削除", key=row[0]):

            cursor.execute(
                "DELETE FROM companies WHERE id = ?",
                (row[0],)
            )

            conn.commit()
            st.rerun()
    




#pandas使った一覧表示
# cursor.execute("SELECT * FROM companies")
# rows = cursor.fetchall()

# df = pd.DataFrame(
#     rows,
#     columns=["ID", "会社名", "応募状況"]
# )

# df["応募状況"] = df["応募状況"].fillna("未設定")

# st.dataframe(df)

# cursor.execute("""
# DELETE FROM companies
# WHERE id = 7
# """)
# conn.commit()


#-------------------------------------------------

#データベースの接続を終了する
conn.close()
