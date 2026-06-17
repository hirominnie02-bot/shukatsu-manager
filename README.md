# Shukatsu Manager
就職活動の応募企業を管理するためのWebアプリです。
Python、Streamlit、SQLiteを使用して開発しています。

## 概要
応募した企業の情報を登録・管理できるアプリです。
現在は以下の機能を実装しています。

* 企業名の登録
* SQLiteへのデータ保存
* 登録済み企業一覧表示
* 重複企業の登録防止

## 使用技術

* Python
* Streamlit
* SQLite
* Git / GitHub

## 学習ポイント

このアプリを通して以下を学習しました。

* SQLiteデータベースの基本操作
* SQL（INSERT / SELECT / WHERE）
* Pythonからのデータベース接続
* fetchone() と fetchall() の使い分け
* Git / GitHub を利用したバージョン管理
* StreamlitによるWebアプリ開発

## 今後の実装予定

* 応募状況管理機能
* 企業情報編集機能
* 企業削除機能
* 応募日管理
* 検索機能
* UI改善

## 実行方法

必要ライブラリをインストール

```bash
pip install -r requirements.txt
```

アプリを起動

```bash
streamlit run app.py
```

## 制作目的

就職活動で応募した企業情報を整理・管理するために制作しました。

また、Python、SQL、Streamlitの学習を兼ねたポートフォリオとして開発を進めています。
