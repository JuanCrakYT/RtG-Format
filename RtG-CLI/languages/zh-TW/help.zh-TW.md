RtG-CLI — 説明
=================

RtG-CLI 是 RtG-Format 生態系統的命令列介面。
它允許發現和執行外掛、查詢語言、查看規則和版本。

用法
-----

  rtg [選項] <指令> [參數]

  第一個參數識別要執行的指令或外掛。

  範例:
    rtg image
    rtg preview
    rtg help image


系統指令
----------

  -h, --help        顯示此通用說明
  -v, --version     顯示 RtG-CLI 版本
  -l, --lang        列出 RtG-CLI 中可用的語言
  -r, --rules       顯示 RtG-CLI 規則
  -c, --commands    列出 RtG-CLI 內部指令
  -a, --addons      列出具有用戶可見文件的外掛
  -language <語言>    設定啟動文字 (void) 的語言

指令: help
-------------

  rtg help                    # 通用說明 (此畫面)
  rtg help <指令>             # 特定指令/外掛的說明
  rtg help <指令> -<語言>      # 特定語言的說明 (例如: -es, -en)
  rtg help <指令> -lang        # 該指令的可用語言

  範例:
    rtg help image
    rtg help image -en
    rtg help image -lang


指令: version
-----------------

  rtg -v
  rtg --version

  顯示版本以及所有可用語言的版本內容。


指令: rules
--------------

  rtg -r
  rtg --rules
  rtg -r -<語言>   # 特定語言的規則 (例如: rtg -r -en)

  預設使用 'rules' 中定義的第一種語言 (西班牙語)。


指令: lang
-------------

  rtg -l
  rtg --lang

  列出所有可用語言，按類別組織:
  Version, Rules, Help, Void, 以及每個外掛。


指令: commands
------------------

  rtg -c
  rtg --commands

  僅列出 RtG-CLI 內部指令。
  不包含外掛指令。


指令: addons
---------------

  rtg -a
  rtg --addons

  列出具有用戶可見文件/說明的外掛。
  沒有文件的已註冊外掛不會顯示在這裡。


指令: language
-----------------

  rtg -language <語言>

  選擇啟動文字 (void) 的語言。
  該語言必須存在於 assets.json 的 'void-language' 中。

  範例:
    rtg -language en


可用外掛
------------

  image      | RtG Image        - 影像轉換器
  preview    | RtG Preview      - RtG-Format 建構的 3D 檢視器
  test-addon | RtG Test Addon   - 用於 CLI 驗證的測試外掛


語言
------

語言用單一連字符表示: -es, -en, -pt 等。
語言不會更改內部指令名稱。

  rtg help image -es    # 西班牙語說明
  rtg help image -en    # 英語說明
  rtg -r -en            # 英語規則

  查看外掛的語言:
    rtg help image -lang

  -lang 的含義取決於其位置:
    rtg --lang          # RtG-CLI 語言 (外掛前)
    rtg image -lang     # 外掛語言 (外掛後)


外掛參數
-----------

識別外掛後, 參數按前綴分類:

  無連字符       -> 外掛        (例如: convert, file.png)
  --選項         -> 外掛        (例如: --width 128)
  -選項          -> RtG-CLI     (例如: -lang, -en)

範例:
  rtg image convert file.png     # convert, file.png -> 外掛
  rtg image --width 128          # --width 128 -> 外掛
  rtg image -lang                # -lang -> RtG-CLI (外掛語言)
  rtg image -en                  # -en -> RtG-CLI (語言選擇器)


帶空格的參數
---------------

包含空格的參數必須用引號括起:

  rtg image "my image.png" "output.json"

RtG-CLI 保留參數順序並按原樣傳遞給外掛。


更多資訊
------------

  rtg help <指令>      # 外掛的詳細說明
  rtg help <指令> -lang  # 該外掛的語言
  rtg --addons         # 查看所有有文件的外掛
  rtg --commands       # 查看內部指令