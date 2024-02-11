現在インストールされているライブラリを保存
```
$ pip freeze > requirements.txt
```
テキストファイルに書かれたものをまとめてインストール
```
$ pip install -r requirements.txt
```

仮想環境を作成
```
python -m venv .venv
```
仮想環境をアクティベート
```
. .venv/bin/activate
```

仮想環境を終了
```
deactivate
```