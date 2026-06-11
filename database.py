import sqlite3
# SQLiteデータベースを操作するためのライブラリを読み込む

conn = sqlite3.connect("job_app.db")
# job_app.dbというデータベースに接続する
# 存在しない場合は新しく作成される

cursor = conn.cursor()
# SQLを実行するためのカーソル（操作担当）を作成する

cursor.execute("""
CREATE TABLE IF NOT EXISTS companies (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    company_name TEXT
)
""")
# companiesテーブルを作成する
# IF NOT EXISTS → 既に存在する場合は作成しない
# id → 自動採番される主キー
# company_name → 会社名を保存する列

conn.commit()
# データベースへの変更を確定する

conn.close()
# データベース接続を終了する

print("データベース作成完了")
# 処理完了メッセージを表示する