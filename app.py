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
memo = st.text_area("メモ")

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
            "INSERT INTO companies (company_name, status, application_date, memo) VALUES (?, ?, ?, ?)",
            (company_name,status, apply_date, memo)
        )

        #データベースの変更を確定
        conn.commit()

        st.success("登録しました！")


#操作画面--------------------------------

st.subheader("検索・絞り込み")
# 応募日ソート表示------------
sort_order = st.selectbox(
    "応募日並び順",
    ["新しい順", "古い順"]
)
if sort_order == "新しい順":
    cursor.execute("""
    SELECT * FROM companies
    ORDER BY application_date DESC
    """)

else:
    cursor.execute("""
    SELECT * FROM companies
    ORDER BY application_date ASC
    """)

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

# 応募状況フィルター
status_filter = st.selectbox(
    "応募状況絞り込み",
    ["すべて", "応募前", "応募済", "書類選考", "面接予定", "内定", "返信待ち"]
)

if status_filter != "すべて":
    display_rows = []

    for row in rows:
        if row[2] == status_filter:
            display_rows.append(row)
            
    if len(display_rows) == 0:
        st.warning("該当する企業がありません")


# 応募状況をデータフレームで表示----------
df = pd.DataFrame(
rows,
columns=["ID", "会社名", "応募状況", "応募日", "メモ"]
)
status_count = df["応募状況"].value_counts()
# st.write(status_count)

# 応募状況をサマリーとして表示------------
st.subheader("応募状況サマリー")

st.write(f"登録企業数：{len(rows)}件")

statuses = list(status_count.items())
half = len(statuses) // 2 + len(statuses) % 2

col1, col2 = st.columns(2)
with col1:
    for status, count in statuses[:half]:
        st.write(f"{status}：{count}件")

with col2:
    for status, count in statuses[half:]:
        st.write(f"{status}：{count}件")


# 登録企業名一覧表示--------------------
st.subheader("応募状況")
for row in display_rows:
    col1, col2, col3, col4, col5 = st.columns([3,2,2,1,2])

    with col1:
        st.write(row[1])

    with col2:
        status_list = [
            "応募前",
            "応募済",
            "書類選考",
            "面接予定",
            "内定",
            "返信待ち"
        ]

        new_status = st.selectbox(
            "応募状況",
            status_list,
            index=status_list.index(row[2]),
            key=f"status_{row[0]}"
        )

    with col3:
        new_apply_date = st.date_input(
            "応募日",
            value=row[3],
            key=f"apply_date_{row[0]}"
            )
        # if row[3] is None:
        #     st.write("未設定")
        # else:
        #     st.write(row[3])
                        
    
    with col4:
        if st.button("削除", key=row[0]):

            cursor.execute(
                "DELETE FROM companies WHERE id = ?",
                (row[0],)
            )

            conn.commit()
            st.rerun()

    
    with col5:
        new_memo = st.text_area(
            "メモ",
            value=row[4],
            key=f"memo_{row[0]}"
        )
        if row[4] is None:
            st.write("未入力")
        else:
            st.write(row[4])

        if st.button("変更", key=f"edit_{row[0]}"):

            cursor.execute(
                """
                UPDATE companies
                SET status = ?, memo = ?, application_date = ?
                WHERE id = ?
                """,
                (new_status, new_memo, new_apply_date, row[0])
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
