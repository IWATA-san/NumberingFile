# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

# Tkinterライブラリのインポート
import tkinter as tk
import tkinter.ttk as ttk

# auto gui alert用
import pyautogui as ag

# ファイル管理用
import glob

# SQLite
import sqlite3

# seleniumライブラリのインポート
# import webbrowser

############################################################
class app(tk.Frame):
    def callback(event):
        # 条件一覧取得
        
        #　フォルダ・ファイル一覧 取得
        txtstr = txt.get()
        if txtstr != "":
            #autogui(alert)
            #agcls.alert(txtstr)
            
            # ファイル一覧取得
            files = glob.glob(txtstr)   # 条件追加する
            for file in files:
                print(file)


            # 検索するやーつ
            # url = 'https://www.google.co.jp/search?q=' + search_word
            # webbrowser.open(url)
            # txt.delete(0, tk.END)


    # 登録ボタンクリック時
    def RegDB():
        # 取得＆チェック
        txtno = RegNo.get()
        txtname = RegName.get()
        #txtrmk = RegRemark.get()
        if txtno == "" or txtname == "":
            agcls.alert("No. と 名字 は必須です。")
            return

        # SQLite接続

        # insert処理        

        print("DBG:RegDB")

    # データ取得（仮）
    def SelDB():
        print("DBG:SelDB")
        



# アラート出力
class agcls():
    def alert(str):
        ag.alert(text=str, title='アラート', button='OK')

    def msgdlg(str):
        ag.prompt(text=str, title='アラート', default='msgab')

# DB処理
class DB():
    def init_sqlite():
        # 空のデータベースを作成して接続する
        dbname = "database.db"
        c = sqlite3.connect(dbname)
        c.execute("PRAGMA foreign_keys = 1")

        # 既にデータベースが登録されている場合は、ddlの発行でエラーが出るのでexceptブロックで回避する
        try:
            # acc_dataテーブルの定義    
            ddl = """
            CREATE TABLE acc_data
            ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                no INTEGER NOT NULL UNIQUE,
                name text NOT NULL UNIQUE,
                remark text
                );
            """
            c.execute(ddl)

            # サンプル登録
            c.execute("INSERT INTO acc_data(no, name, remark) VALUES('01', '岩田', '備考');")
            c.execute("INSERT INTO acc_data(no, name, remark) VALUES('02', '丹羽', 'ビコウ');")
            c.execute("INSERT INTO acc_data(no, name, remark) VALUES('03', '山田', 'Bikou');")
            c.execute("COMMIT;")
            print("success init_sqlite")

        except:
                pass

    def Chk_acc_data():
        dbname = "database.db"
        c = sqlite3.connect(dbname)
        for r in c.execute("select * from acc_data"):
            print(r)
            

########################################
# 処理開始
DB.init_sqlite()
DB.Chk_acc_data()   #DBG
root = tk.Tk()

# Windowの定義 常に最前表示
root.attributes("-topmost", True)
root.title("すぐぐる")
root.geometry("420x500")

# フレームの作成（フレームをrootに配置,フレーム淵を2pt,フレームの形状をridge）
frame = tk.Label(root, bd=2, relief="raised")
# フレームを画面に配置し、横方向に余白を拡張する
frame.pack(fill="x")

# 入力ボタン
InBtn = tk.Button(frame, text="登録")
InBtn.pack(side="left")    # 左寄せ
FinBtn = tk.Button(frame,text="終了")
FinBtn.pack(anchor="ne")

###
#ラベル
label = tk.Label(root, text="フォルダ")
#label.place(x=10, y=30)
label.pack(fill="x")

# テキストボックス
txt = tk.Entry(width=65)
#txt.place(x=10, y=50)
txt.pack()
#txt.insert(0, 'テキスト文字列')
txt.insert(0, './*')

#ラベル
label = tk.Label(root, text="置換リスト")
label.pack(fill="x")

###
# ツリービュー（表形式のやつ）
tree = ttk.Treeview(root)
# 列インデックスの作成
tree["columns"] = (1,2,3)
# 表スタイルの設定(headingsはツリー形式ではない、通常の表形式)
tree["show"] = "headings"
# 各列の設定(インデックス,オプション(今回は幅を指定))
tree.column(1,width=75)
tree.column(2,width=75)
tree.column(3,width=100)
# 各列のヘッダー設定(インデックス,テキスト)
tree.heading(1,text="付与No.")
tree.heading(2,text="検索キー")
tree.heading(3,text="備考")

# レコードの作成
# 1番目の引数-配置場所（ツリー形式にしない表設定ではブランクとする）
# 2番目の引数-end:表の配置順序を最下部に配置
#             (行インデックス番号を指定することもできる)
# 3番目の引数-values:レコードの値をタプルで指定する
tree.insert("","end",values=("01","岩田","備考"))
tree.insert("","end",values=("02","丹羽","ビコウ"))
tree.insert("","end",values=("03","山田","Bikou"))
# ツリービューの配置
tree.pack()
#tree.place(x = 10, y = 80)

###
# 登録フォーム
# ラベル
label = tk.Label(root, text="【登録】No. 名字 ビコウ")
label.pack(fill="x")
# テキストボックス
RegNo = tk.Entry(width=20)
RegNo.pack()
RegName = tk.Entry(width=20)
RegName.pack()
RegRemark = tk.Entry(width=40)
RegRemark.pack()
# ボタン
RegBtn = tk.Button(root, text="登録", command=lambda:app.RegDB())
RegBtn.pack()

# エンターで検索処理
root.bind('<Return>', app.callback)
root.mainloop()
