# エクセルをそのままcsvにしたファイルを正規化する。

[エクセルをそのままcsvにしたファイルを正規化する。](https://qiita.com/toshikawa/items/901b2d68461dd1ae085c)で書いたpythonをここで改良してこうと考えます。

## ローカルでの確認方法
S3に保存する出力にしているので、結果は出ないけど
`python-lambda-local -f main lambda.py event.json`
で確認可能です。

やっぱりファイル出力する場合は

```python:output
#書き込み
filename='seika_'+date+'.csv'

with open(filename, 'w', encoding='utf-8') as w:
    w.write(csvfile)
```
に変えて貰えばいいと思います。

## .gitignoreの書き方
```configration:.gitignore
.gitignore
__pycache__/
seika_*
```

ローカルで確認すると`__pychache__`フォルダができるので、githubにあげない用設定しています。

