RtG-CLI — 帮助
===============

RtG-CLI 是 RtG-Format 生态系统的命令行界面。
它允许发现和执行插件、查询语言、查看规则和版本。

用法
-----

  rtg [选项] <命令> [参数]

  第一个参数标识要执行的命令或插件。

  示例:
    rtg image
    rtg preview
    rtg help image


系统命令
----------

  -h, --help        显示此通用帮助
  -v, --version     显示 RtG-CLI 版本
  -l, --lang        列出 RtG-CLI 中可用的语言
  -r, --rules       显示 RtG-CLI 规则
  -c, --commands    列出 RtG-CLI 内部命令
  -a, --addons      列出具有用户可见文档的插件
  -language <语言>    设置启动文本 (void) 的语言

命令: help
-------------

  rtg help                    # 通用帮助 (此屏幕)
  rtg help <命令>             # 特定命令/插件的帮助
  rtg help <命令> -<语言>      # 特定语言的帮助 (例如: -es, -en)
  rtg help <命令> -lang        # 该命令的可用语言

  示例:
    rtg help image
    rtg help image -en
    rtg help image -lang


命令: version
-----------------

  rtg -v
  rtg --version

  显示版本以及所有可用语言的版本内容。


命令: rules
--------------

  rtg -r
  rtg --rules
  rtg -r -<语言>   # 特定语言的规则 (例如: rtg -r -en)

  默认使用 'rules' 中定义的第一种语言 (西班牙语)。


命令: lang
-------------

  rtg -l
  rtg --lang

  列出所有可用语言，按类别组织:
  Version, Rules, Help, Void, 以及每个插件。


命令: commands
------------------

  rtg -c
  rtg --commands

  仅列出 RtG-CLI 内部命令。
  不包含插件命令。


命令: addons
---------------

  rtg -a
  rtg --addons

  列出具有用户可见文档/帮助的插件。
  没有文档的已注册插件不会显示在这里。


命令: language
-----------------

  rtg -language <语言>

  选择启动文本 (void) 的语言。
  该语言必须存在于 assets.json 的 'void-language' 中。

  示例:
    rtg -language en


可用插件
------------

  image      | RtG Image        - 图像转换器
  preview    | RtG Preview      - RtG-Format 构建的 3D 查看器
  test-addon | RtG Test Addon   - 用于 CLI 验证的测试插件


语言
------

语言用单个连字符表示: -es, -en, -pt 等。
语言不会更改内部命令名称。

  rtg help image -es    # 西班牙语帮助
  rtg help image -en    # 英语帮助
  rtg -r -en            # 英语规则

  查看插件的语言:
    rtg help image -lang

  -lang 的含义取决于其位置:
    rtg --lang          # RtG-CLI 语言 (插件前)
    rtg image -lang     # 插件语言 (插件后)


插件参数
-----------

识别插件后, 参数按前缀分类:

  无连字符       -> 插件        (例如: convert, file.png)
  --选项         -> 插件        (例如: --width 128)
  -选项          -> RtG-CLI     (例如: -lang, -en)

示例:
  rtg image convert file.png     # convert, file.png -> 插件
  rtg image --width 128          # --width 128 -> 插件
  rtg image -lang                # -lang -> RtG-CLI (插件语言)
  rtg image -en                  # -en -> RtG-CLI (语言选择器)


带空格的参数
---------------

包含空格的参数必须用引号括起:

  rtg image "my image.png" "output.json"

RtG-CLI 保留参数顺序并按原样传递给插件。


更多信息
------------

  rtg help <命令>      # 插件的详细帮助
  rtg help <命令> -lang  # 该插件的语言
  rtg --addons         # 查看所有有文档的插件
  rtg --commands       # 查看内部命令