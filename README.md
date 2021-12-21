# twi_word_count
Twitterのアカデミックライセンスを用いて、任意のキーワードのツイート数を日ごとに取得するコード

# How to use
1. Set token
`twittertoken.txt`に、[Developer Portal](https://developer.twitter.com/en/portal/projects-and-apps)から取得した `Bearer token`を入力して保存します。
    - Windowsの場合
    テキストファイル（.txt）は、右クリック→「編集」で、デフォルトのメモ帳アプリから編集できます。

2. Set keywords
`keywords.txt`に、検索したい単語を入力します。
なお、入力の際は、単語毎に改行を行ってください。

```
キーワード1
キーワード2
キーワード3
```

3. Execute
ファイルを実行します。
フォルダ内のバッチファイルから、簡単に実行できます。
コマンドプロンプト上で「(キーワード) done」と表示されたら、「data」フォルダ内にcsvファイルが保存されます。