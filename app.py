import streamlit as st
import sqlite3 #軽量データベースインポート
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams["font.family"] = "Yu Gothic"

st.title("就活管理アプリ")

company_name = st.text_input("会社名")
status = st.selectbox(
    "応募状況",
    ["応募前", "応募済", "書類選考", "面接予定", "内定", "返信待ち"]
)
apply_date = st.date_input("応募日")
memo = st.text_area("メモ")
url = st.text_input("URL")

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
            "INSERT INTO companies (company_name, status, application_date, memo, url) VALUES (?, ?, ?, ?,?)",
            (company_name,status, apply_date, memo, url)
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
    search_results = []
    for row in display_rows:
        
        if search_word in row[1]:
            search_results.append(row)

    display_rows = search_results
    
    if len(display_rows) == 0:
        st.warning("該当する企業がありません")

# 応募状況フィルター
status_filter = st.selectbox(
    "応募状況絞り込み",
    ["すべて", "応募前", "応募済", "書類選考", "面接予定", "内定", "返信待ち"]
)

if status_filter != "すべて":
    filter_results = []

    for row in display_rows:
        if row[2] == status_filter:
            filter_results.append(row)
            
    display_rows = filter_results
            
    if len(display_rows) == 0:
        st.warning("該当する企業がありません")


# 応募状況をデータフレームで表示----------
df = pd.DataFrame(
rows,
columns=["ID", "会社名", "応募状況", "応募日", "メモ", "URL"]
)
status_count = df["応募状況"].value_counts()
fig, ax = plt.subplots(figsize=(1.6,1.6))
wedges, texts = ax.pie(
    status_count.values,
    colors=[
    "#A8D8EA",
    "#AAE3A2",
    "#FFD3B6",
    "#FFAAA5",
    "#D4A5A5",
    "#C7CEEA"
    ]
    
)

if len(rows) == 0:
    st.info(
    "まだ企業が登録されていません😊"
    )
else:
    col1, col2 = st.columns([3,7])
    with col1:
        status_colors = {
        "応募前": "#A8D8EA",
        "応募済": "#AAE3A2",
        "返信待ち": "#FFD3B6",
        "書類選考": "#FFAAA5",
        "面接予定": "#D4A5A5",
        "内定": "#C7CEEA"
        }
        for status, count in status_count.items():
            st.markdown(
                f'<span style="color:red">■ {status}　{count}件</span>',
                unsafe_allow_html=True
            )
                

    with col2:
        st.pyplot(
            fig,
            use_container_width=False
        )
        # st.pyplot(fig)



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


# 登録企業一覧表示--------------------
st.subheader("応募状況")

for row in display_rows:

    st.subheader(row[1])

    new_apply_date = st.date_input(
        "応募日",
        value=row[3],
        key=f"apply_date_{row[0]}"
    )
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

    new_memo = st.text_area(
        "メモ",
        value=row[4],
        height=80,
        key=f"memo_{row[0]}"
    )

    new_url = st.text_input(
        "URL",
        value=row[5],
        key=f"URL_{row[0]}"
    )
    if row[5]:
        st.link_button(
            "🌐 企業研究する",
            row[5]
    )

    button_col1, button_col2, _ = st.columns([1,1,8])
    
    with button_col1:
        if st.button("変更", key=f"edit_{row[0]}"):

            cursor.execute(
                """
                UPDATE companies
                SET status = ?, memo = ?, application_date = ?, url = ?
                WHERE id = ?
                """,
                (new_status, new_memo, new_apply_date, new_url, row[0])
            )

            conn.commit()

            # 再描画後に表示する成功メッセージを保存
            st.session_state["message"] = "✅ 変更しました"
            st.session_state["message_id"] = row[0]

            # 最新データを反映するため再描画
            st.rerun()

            

    with button_col2:
        delete_clicked = st.button("削除", key=f"delete_{row[0]}")

    # 削除ボタンが押されたら確認対象のIDを保存    
    if delete_clicked:
        st.session_state["confirm_delete"] = row[0]

    # 削除確認中のIDと現在の行IDが一致した場合のみ警告を表示
    
    if st.session_state.get("confirm_delete") == row[0]:
        st.warning(
            "⚠ 本当に削除しますか？\n削除すると復元できません"
        )
        confirm_col1, confirm_col2, _ = st.columns([1,2,7])

        with confirm_col1:

            if st.button("はい", key=f"confirm_{row[0]}"):
                cursor.execute(
                    "DELETE FROM companies WHERE id = ?",
                    (row[0],)
                )
                conn.commit()


                # 削除確認状態を解除
                st.session_state.pop("confirm_delete")

                # 最新状態を反映するため再描画
                st.rerun()

        with confirm_col2:

            if st.button("いいえ", key=f"cancel_{row[0]}"):
                # 削除確認状態を解除
                st.session_state.pop("confirm_delete")
                # 最新状態を反映するため再描画
                st.rerun()


    # 変更完了メッセージが保存されていたら表示
    if (st.session_state.get("message") and st.session_state.get("message_id") == row[0]):
        st.success(st.session_state["message"])

        # 表示後は削除して次回表示されないようにする
        st.session_state.pop("message")
        st.session_state.pop("message_id")


    st.divider()

    

#データベースの接続を終了する
conn.close()
