# klctool - Karaoke Lyrics Card Creation Support Tool

[English](https://github.com/AmasaShiro/klctool/blob/main/README_en.md)

![サンプル画像](resources/sample.jpeg)  

カラオケ好きな皆さん！練習のとき歌詞カードほしくないですか？でも歌詞カードを作るのって結構面倒… これはそんな面倒な作業をお手伝いするツールです。  

歌詞を収めたマークダウン形式のファイルを AI (Google Gemini) でひらがな化、ワードプロセッサーの LibreOffice Writer 形式に変換して複雑な編集ができるようにします。  

また YouTube でお気に入りのシーンをスクリーンショットで撮るなどした画像を背景画像として使えるように加工します。  

このツールであなただけの歌詞カードを作りませんか？  

感想・意見は X、Issue などでお待ちしています！

## 概要

- コマンドラインツール: klctool
  - 歌詞のひらがな化: Google Gemini でひらがな化
  - odt形式に変換: Pandoc で LibreOffice Writer で編集できる用に変換
  - 背景画像の加工: 画像を歌詞カードの背景として使えるように加工・調整

## 想定ユーザ

- カラオケ好きな人
- 歌詞カードを作るのが好きな人
- PC でコマンドラインを使うことができる人
- AI の間違いを笑って許せる人

## 必要ソフトウェアなど

- Python
- Pandoc
- LibreOffice Writer

- Google Gemini API キー

## 使い方

1. 歌詞準備
   1. 歌詞を収めたファイルをサンプルのフォーマットに従い準備します。[サンプル](lyrics-sample.md)  
      - ファイルの先頭で `---` で囲んだ部分に次の3つのプロパティを記述すると、ODT形式への変換時にのヘッダ部分に埋め込みます。
        - vc-title
        - vc-artist
        - vc-collab (タイアップ情報など。アニメのタイトルなど)
      - マークダウン形式のヘッダ (`# アーティスト - 曲名`など)
      - 歌詞
   2. 以下のような編集もしておきます。
      - 発音の揺れを確定: 行く(いく/ゆく)など 「いく」なのか「ゆく」なのか
      - インデント: 全角空白で行頭を段付 (全角を使用するのはマークダウン形式のため)
      - 実際の歌唱どおりに: 「何百年経ったって」→「何百年経ってたって」など (ClariS / PRIMALove)
      - 難読・読み替えにルビ: 「自らを見失った絵画」→「自らを見失った[絵画] (メイク)」など (可不 / フォニイ)
2. 背景画像の準備  
   YouTube でお気に入りのシーンをフルスクリーン(PC)でスクリーンショットするなどして画像ファイルを準備します。
3. `klctool` 実行  
   1. `klctool hira 歌詞ファイル名`  
      準備した歌詞ファイルをAIでひらがな化して追加。変換忘れや間違いがあったときは笑って再実行
   2. `klctool odt ひらがな化した歌詞ファイル名`  
      ひらがな化した歌詞ファイルをワードプロセッサ LibreOffice Writer で扱える odt 形式に変換
   3. `klctool img 画像ファイル名1 画像ファイル名2` (画像ファイルは1つでも可)  
      準備した画像ファイルを odt 形式に変換したファイルにあうよう加工・調整
      - 余分な部分 (プレイヤー部分) をトリミング
      - 不透明度 80% でマスク
4. 歌詞の編集  
   ひらがな化した歌詞を変換間違い修正、カラオケで歌いやすいように母音や長音の追加などの編集をします。Google Music Font などの音楽系の記号を使うとわかりやすいかも。
5. 背景画像設定
   背景画像を LibreOffice Writer でページの背景に指定します。
   - メニューから【書式】→【ページスタイル...】→【背景】→【画像】→【追加/インポート】で画像を指定
   - 【オプション】→【スタイル】で【いっぱいに伸ばす】を選択し【適用】または【OK】を押す
   - 左右ページで異なる背景画像を使う場合移管ページスタイルで背景画像を設定します。
     - 1ページ目: 標準ページスタイル
     - 2ページ目: 右ページスタイル
     - 3ページ目: 左ページスタイル
6. 歌詞カードの完成  
   LibreOffice Writer で PDF形式でエクスポートし、タブレットに転送、または印刷するなどしてカラオケで使います。自分の歌唱録音を聞いて気づいたことをメモすると捗るかも。

## セットアップ

### 前提ソフトウェア

まだインストールしていない場合はインストールします。

> [!TIP]  
> それぞれのソフトウェアの配布元サイトなどで確認し適切にインストールしてください  

例: Mac: Homebrew でインストール

```zsh
brew install pandoc
brew install --cask obsidian
brew install --cask libreoffice
brew install --cask libreoffice-language-pack
```

例: Windows: winget でインストール

```cmd
winget install --id=JohnMacFarlane.Pandoc  -e
winget install --id=Obsidian.Obsidian  -e
winget install --id=TheDocumentFoundation.LibreOffice  -e
```

#### Google Gemini の API キー

以下の Google AI Studio サイトで Gemini API キーを作成します。

https://aistudio.google.com/

> [!TIP]  
> 無料枠の API キーでも使えます (2025 年 3 月現在)

作成した API キーを設定ファイル gemini-2.0-flash-exp.api_key.toml に設定します。ファイルに API キーを格納するのが不安な場合、以下の方法でも API キーを指定できます。

- コマンドラインオプションで API キーを指定
- 環境変数 `GOOGLE_API_KEY` に API キーを設定
- コマンドラインオプションで API キーを格納したファイルを指定 (toml)

### klctool

```zsh
pip install klctool
```

## klctool コマンドラインオプション

### 共通オプション

```zsh
klctool [-h] [--debug] [--config-dir CONFIG_DIR]
     {hiragana,hira,convert2odt,odt,adjustimage,img} ...
 -h, --help                   ヘルプを表示する
 --debug, -d                  デバッグモードを有効にする
 --config-dir, -c CONFIG_DIR  設定ファイルのディレクトリを指定する
```

### サブコマンド ひらがな化 hiragana (hira)

input_files で指定したマークダウン形式の歌詞ファイルをひらがな化します。ひらがな化したファイルは元のファイルのフォルダにファイル名末尾に `_hiranaga` をつけて保存します。

```zsh
klctool hiragana [-h] [--output-dir OUTPUT_DIR] [--output-suffix OUTPUT_SUFFIX]
                [--model-name MODEL_NAME] [--api-key-file API_KEY_FILE]
                [--api-key API_KEY] [--prompt-file PROMPT_FILE]
                input_files [input_files ...]
 input_files                          入力ファイル 複数指定可能
 -h, --help                           ヘルプを表示する
 --output-dir, -o OUTPUT_DIR          出力フォルダ
 --output-suffix, -s OUTPUT_SUFFIX    出力ファイル名サフィックス
 --model-name, -m MODEL_NAME          AIモデル名
 --api-key-file, -a API_KEY_FILE      APIキーファイル名
 --api-key, -k API_KEY                APIキー
 --prompt-file, -p PROMPT_FILE        プロンプト格納ファイル名
```

- Google Gemini の API キーは以下の順序で優先的に使用します。
  1. オプション --api-key
  2. 環境変数 `GOOGLE_API_KEY`
  3. オプション --api-key-file
  4. 設定ファイル `config.toml` の `api_key_file` で指定されたファイル

- --output-dir を指定した場合、ひらがな化したファイルを指定したフォルダに保存します。
- --output-suffix を指定した場合、指定したサフィックスをつけます。
- --api-key を指定した場合、API_KEY として使用します。
- --api-key-file を指定した場合、API キー格納ファイルとして使用します。
- --prompt-file を指定した場合、プロンプト格納ファイルとして使用します。

### サブコマンド odtファイルへ変換 convert2odt (odt)

input_files で指定したマークダウン形式の歌詞ファイルを Pandoc で odt 形式に変換し、歌詞ファイルと同じフォルダに保存します。
odt テンプレートではタイトル、アーティスト、タイアップ情報をヘッダに埋め込みます。

```zsh
klctool convert2odt [-h] [--output-dir OUTPUT_DIR] [--template-odt TEMPLATE_ODT]
                   [--lua-script LUA_SCRIPT]
                   input_files [input_files ...]
 input_files                      入力ファイル 複数指定可能
 -h, --help                       ヘルプを表示する
 --output-dir, -o OUTPUT_DIR      出力フォルダ
 --template-odt, -t TEMPLATE_ODT  テンプレートODTファイル名
 --lua-script, -s LUA_SCRIPT      Luaスクリプトファイル名
```

- --output-dir を指定した場合、odt 形式に変換したファイルを指定したフォルダに保存します。
- --template-odt を指定した場合、テンプレートファイルとして使用します。
- --lua-script を指定した場合、スクリプトファイルとして使用します。

### サブコマンド 画像ファイル調整・加工 adjustimage (img)

input_files で指定した png ファイルを加工します。加工したファイルは元のファイルのフォルダにファイル名末尾に `_processed` をつけて保存します。

```zsh
klctool adjustimage [-h] [--output-dir OUTPUT_DIR] [--paper-size PAPER_SIZE]
                   [--mask-strength MASK_STRENGTH] [--mask-color MASK_COLOR]
                   [--output-suffix OUTPUT_SUFFIX] [--movie-aspect-ratio MOVIE_ASPECT_RATIO]
                   input_files [input_files ...]
 input_files                                 入力画像ファイル 複数指定可能
 -h, --help                                  ヘルプを表示する
 --output-dir, -o OUTPUT_DIR                 出力フォルダ
 --paper-size, -p PAPER_SIZE                 用紙サイズ
 --mask-strength, -m MASK_STRENGTH           マスク強度 単位 %
 --mask-color, -c MASK_COLOR                 マスク色
 --output-suffix, -s OUTPUT_SUFFIX           出力ファイル名サフィックス
 --movie-aspect-ratio, -a MOVIE_ASPECT_RATIO アスペクト比
 --dpi, -d  DPI                              出力画像のDPI
 --fit-mode, -f {trim,pad}                   アスペクト比をあわせる方法(デフォルトtrim)
```

- --output-dir を指定した場合、加工したファイルを指定したフォルダに保存します。
- --paper-size を指定した場合、指定した用紙サイズに合わせます。
- --mask-strength を指定した場合、指定したマスク強度でマスクします。
- --mask-color を指定した場合、指定した色を背景色としてマスクします。
- --output-suffix を指定した場合、指定したサフィックスをつけます。
- --movie-aspect-ratioを指定した場合、指定した値を入力画像の必要部分のアスペクト比としてトリミングします。
- --dpiを指定した場合、指定した値で画像ファイルサイズの確認を行い、大きい場合は画像を縮小します。
- --fit-modeで、最終調整をトリムでするか、余白追加でするかを指定します。デフォルトはトリムです。

## カスタマイズ

- 設定ファイル場所:
  - macOS / Linux: ~/.config/klctool/
  - Windows: %APPDATA%

``` zsh
.config
└── klctool
    ├── config.toml  # デフォルト設定値など
    ├── gemini-2.0-flash-exp.api_key.toml  # api_key
    ├── gemini-2.0-flash-exp.prompt.toml   # プロンプト
    ├── klctool-edit.lua # lua スクリプト - Pandoc 用
    ├── klctool.odt      # odt テンプレートファイル
    └── paper-size.toml # 用紙サイズ定義
```

## ライセンス

MIT License

使用したライブラリのライセンスはそれぞれのライセンス下にあります。

## 開発・テスト環境

- MacBook Air Retina, 13-inch, 2018 Intel
- MacOS Sonoma 14.7.4
- Python 3.13.2
- Pandoc 3.6.4
- LibreOffice Version: 25.2.1.2 (X86_64) / LibreOffice Community / 日本語言語パック

## 貢献

- 上記以外の環境での動作報告をお待ちしています。特に Linux、Windows では動作確認できていません。
- バグ報告は Issue まで。

## その他

このプロジェクトは以下の学習目的で作成しました。ご意見、ご質問は大歓迎です。

- Python
- mise en place / uv
- Git / GitHub
- Python のパッケージング
- AI プログラミング
- nuitka

## 謝辞

- コードは Google Gemini で生成しました。優秀ですね。ありがとう Gemini!
- すべての OSS 開発者に感謝を！
