RtG-CLI — ヘルプ
=================

RtG-CLI は RtG-Format エコシステムのコマンドラインインターフェースです。
アドオンの発見と実行、言語のクエリ、ルールとバージョンの表示を可能にします。

使用方法
----------

  rtg [オプション] <コマンド> [引数]

  最初の引数が実行するコマンドまたはアドオンを識別します。

  例:
    rtg image
    rtg preview
    rtg help image


システムコマンド
------------------

  -h, --help        この一般的なヘルプを表示
  -v, --version     RtG-CLI のバージョンを表示
  -l, --lang        RtG-CLI で利用可能な言語を一覧表示
  -r, --rules       RtG-CLI のルールを表示
  -c, --commands    RtG-CLI の内部コマンドを一覧表示
  -a, --addons      ユーザーから見えるドキュメントを持つアドオンを一覧表示
  -u, --usage       一般的な使用法情報を表示 (新規)
  -u-<言語>         特定言語の使用法を表示 (例: -u-es, -u-en) (新規)
  --usage-<言語>     特定言語の使用法を表示 (例: --usage-es, --usage-en) (新規)
  -language <言語>    起動テキスト (void) の言語を設定

コマンド: help
-----------------

  rtg help                    # 一般的なヘルプ (この画面)
  rtg help <コマンド>         # 特定のコマンド/アドオンのヘルプ
  rtg help <コマンド> -<言語>   # 特定言語のヘルプ (例: -es, -en)
  rtg help <コマンド> -lang      # そのコマンドで利用可能な言語
  rtg help -u                  # 一般的な使用法 (新規)
  rtg help -u-<言語>           # 特定言語の使用法 (例: -u-es) (新規)
  rtg help --usage             # 一般的な使用法 (新規)
  rtg help --usage-<言語>       # 特定言語の使用法 (例: --usage-es) (新規)
  rtg help usage               # 一般的な使用法 (代替構文, 新規)

  例:
    rtg help image
    rtg help image -en
    rtg help image -lang
    rtg help -u
    rtg help -u-en
    rtg help --usage-es


コマンド: version
--------------------

  rtg -v
  rtg --version

  バージョンと、すべての利用可能な言語でのバージョン内容を表示。


コマンド: rules
------------------

  rtg -r
  rtg --rules
  rtg -r -<言語>   # 特定言語のルール (例: rtg -r -en)

  デフォルトでは 'rules' で定義された最初の言語 (スペイン語) を使用。


コマンド: lang
-----------------

  rtg -l
  rtg --lang

  すべての利用可能な言語をカテゴリ別に一覧表示:
  Version, Rules, Help, Void, およびアドオンごと。


コマンド: commands
---------------------

  rtg -c
  rtg --commands

  RtG-CLI の内部コマンドのみを一覧表示。
  アドオンコマンドは含まない。


コマンド: addons
-------------------

  rtg -a
  rtg --addons

  ユーザーから見えるドキュメント/ヘルプを持つアドオンを一覧表示。
  ドキュメントのない登録済みアドオンはここに表示されない。


コマンド: usage
------------------

  rtg -u
  rtg --usage
  rtg -u-<言語>         # 特定言語の使用法 (例: -u-es, -u-en) (新規)
  --usage-<言語>         特定言語の使用法を表示 (例: --usage-es, --usage-en) (新規)

  要求された言語での一般的な使用法情報 (void) を表示。
  言語は assets.json の 'void-language' に存在する必要がある。


コマンド: language
---------------------

  rtg -language <言語>

  起動テキスト (void) の言語を選択。
  その言語は assets.json の 'void-language' に存在する必要がある。

  例:
    rtg -language en


利用可能なアドオン
--------------------

  image      | RtG Image        - 画像コンバーター
  preview    | RtG Preview      - RtG-Format ビルドの 3D ビューア
  test-addon | RtG Test Addon   - CLI 検証用テストアドオン


言語
-------

言語は単一のハイフンで示される: -es, -en, -pt 等。
言語は内部コマンド名を変更しない。

  rtg help image -es    # スペイン語ヘルプ
  rtg help image -en    # 英語ヘルプ
  rtg -r -en            # 英語ルール

  アドオンの言語を見る:
    rtg help image -lang

  -lang の意味は位置によって異なる:
    rtg --lang          # RtG-CLI 言語 (アドオン前)
    rtg image -lang     # アドオン言語 (アドオン後)


アドオン引数
---------------

アドオンが識別された後、引数は前缀によって分類される:

  ハイフンなし      -> アドオン        (例: convert, file.png)
  --オプション       -> アドオン        (例: --width 128)
  -オプション        -> RtG-CLI       (例: -lang, -en)

例:
  rtg image convert file.png     # convert, file.png -> アドオン
  rtg image --width 128          # --width 128 -> アドオン
  rtg image -lang                # -lang -> RtG-CLI (アドオン言語)
  rtg image -en                  # -en -> RtG-CLI (言語セレクター)


スペースを含む引数
---------------------

スペースを含む引数は引用符で囲む必要がある:

  rtg image "my image.png" "output.json"

RtG-CLI は引数の順序を保持し、そのままアドオンに渡す。


詳細情報
-------------

  rtg help <コマンド>      # アドオンの詳細ヘルプ
  rtg help <コマンド> -lang  # そのアドオンの言語
  rtg --addons             # すべてのドキュメント付きアドオンを表示
  rtg --commands           # 内部コマンドを表示