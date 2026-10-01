# RtG-CLI 命令规则

## 1. 一般结构

RtG-CLI 命令由主命令和可选参数组成。
通用格式：

`rtg <命令> [<参数>]`

`rtg` 后的第一个参数决定将执行哪个命令或插件。

示例：

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. 已注册命令

主命令必须在 RtG-CLI 配置中注册。
命令通过其内部键标识。

示例：

`image`

`image` 键标识对应的插件，无论显示给用户的名称是什么。
示例：

`image` → `RtG Image`

`preview` → `RtG Preview`

显示的名称不得用作命令标识符。

---

## 3. RtG-CLI 命令和插件命令

RtG-CLI 和插件可以有各自的命令和参数。

在识别插件之前，命令和参数属于 RtG-CLI。
识别插件后，前缀决定每个参数归属：

- 无连字符 (`-`) → 属于插件。
- 双连字符 (`--`) → 属于插件。
- 单连字符 (`-`) → 属于 RtG-CLI。

示例：

`rtg image convert`

- `image` → 插件。
- `convert` → 插件命令。

示例：

`rtg image --width 128`

- `image` → 插件。
- `--width` → 插件参数。
- `128` → 插件参数的值。

示例：

`rtg image -lang`

- `image` → 插件。
- `-lang` → RtG-CLI 参数。

---

## 4. 系统参数

在识别插件之前，RtG-CLI 使用其自身的语法规则。
长系统选项使用双连字符：

`rtg --version`
`rtg --help`

系统缩写使用单连字符：

`rtg -v`
`rtg -h`
`rtg -l`

识别插件后，以单连字符 (`-`) 开头的选项属于 RtG-CLI。

示例：

`rtg image -lang`
`rtg image -en`

---

## 5. 插件识别前后的参数

RtG-CLI 参数根据出现在插件识别前还是后可能具有不同含义。

识别插件前，参数属于 RtG-CLI。

例如：

`rtg --lang`

显示 RtG-CLI 可用语言。

识别插件后，参数按插件的所有权规则解释。

例如：

`rtg image -lang`

查询 `image` 插件的可用语言。

这样，参数的位置决定其上下文，防止全局 RtG-CLI 参数与插件识别后使用的参数混淆。

---

## 6. 系统参数的位置

系统参数不得出现在其影响的命令或插件之前（当参数依赖该命令时）。

正确示例：

`rtg help image -en`

错误示例：

`rtg help -en image`

这两个示例中，系统命令 `help` 使用此结构，因此第二个示例不正确：
`help <target> <options>`

位置必须明确确定哪个命令接收参数。

---

## 7. 插件命令和参数

命令作为单独的终端参数编写。
命令不得包含空格，除非用引号括起。

后续参数可由插件按其自身接口使用。

例如：

`rtg image convert image`

可解释为：

- `image` → 插件
- `convert` → 插件命令
- `image` → 命令参数

---

## 8. 插件命令中的连字符使用

识别插件后：

- 无连字符的参数属于插件。
- 双连字符或更多 (`--`) 的参数属于插件。
- 单连字符 (`-`) 的参数属于 RtG-CLI。

示例：

`rtg image convert`
`convert` → 插件。

`rtg image --width 128`
`--width` → 插件。

`rtg image -lang`
`-lang` → RtG-CLI。

---

## 9. 插件命令接口

插件特定命令由插件程序自身定义。
RtG-CLI 通过插件配置的 `program commands` 属性定位其命令接口。

该属性包含提供程序命令接口的文件路径。

示例：

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI 可使用此接口发现或执行插件可用命令，但不得假定或修改其内部命令含义。

插件可定义未直接注册为 RtG-CLI 命令的额外命令。

程序内部实现可在插件间不同，只要提供与 RtG-CLI 规则兼容的接口。

---

## 10. 语言

插件可用语言通过其配置定义。

示例：

`lang: ["es", "en"]`

翻译文本使用对应的语言代码标识。

示例：

`content.zh`
`content.en`

RtG-CLI 使用的语言选择器必须视为系统参数。

示例：

`rtg help image -en`

---

## 11. 默认语言

若未指定 `-<语言>`，RtG-CLI 将使用 `rules` 中定义的第一种语言。
若指定了 `-<语言>`，RtG-CLI 将在该语言可用时使用它。

`assets.json` 中 `rules` 对象定义的第一种语言为规则的默认语言。

用户未指定语言请求规则时，RtG-CLI 必须使用该第一种语言。

例如：

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

此时：

`rtg -r`
和
`rtg --rules`

将以西班牙语显示规则，因为 `es` 是首个定义的语言。
请求其他语言需使用对应选择器：

`rtg -r -en`

`rules` 内语言顺序仅决定默认语言，不改变可用语言。

此规则也适用于其他语言选择器，如：

`rtg help image -es`

---

## 12. 语言不改变命令

更改语言仅修改 RtG-CLI 显示的文本。
不改变内部命令名称。

示例：

`rtg help image -es`

和

`rtg help image -en`

仍引用同一命令：

`image`

---

## 13. 帮助

通用帮助通过以下方式获取：

`rtg help`

特定命令帮助通过以下方式获取：

`rtg help <命令>`

可请求特定语言的帮助：

`rtg help <命令> -<语言>`

示例：

`rtg help image -en`

---

## 14. 语言查询

插件可用语言可通过以下方式查询：

`rtg help <命令> -lang`

示例：

`rtg help image -lang`

此选项属于 RtG-CLI，而非插件。

---

## 15. 插件不得修改系统规则

插件可定义自身命令和参数，但不得重新定义 RtG-CLI 保留参数的含义。

例如，插件不得使用 `-h` 赋予系统帮助不同含义。
RtG-CLI 保留的名称优先于插件命令。
RtG-CLI 保留的命令和选项必须由 CLI 接口显式定义。
插件不得重新定义保留选项的行为。

---

## 16. 标识符与名称的分离

插件内部键用于标识它。
插件名称仅用作描述信息或向用户显示。

示例：

`image` → 内部标识符

`RtG Image` → 显示名称

不得假定显示名称可用作命令。

---

## 17. 命令必须是确定性的

RtG-CLI 必须能基于命令结构和规则，而非程序描述性名称，判断参数归属系统还是插件。

示例：

`rtg help image -en`

必须始终以相同方式解释：

`rtg` → CLI

`help` → CLI 命令

`image` → 插件

`-en` → CLI 选项

---

## 18. 未知参数

识别插件后，RtG-CLI 必须按前缀确定每个参数归属。

* 无连字符参数属于插件。
* 双连字符或更多 (`--`) 参数属于插件。
* 单连字符 (`-`) 参数属于 RtG-CLI。

若 RtG-CLI 收到未知系统参数，必须报告该选项不存在。

插件参数必须原样传递给插件，RtG-CLI 不得尝试解释其含义。

---

## 19. 不假设未注册命令

RtG-CLI 不得仅因存在相关文件夹、文件或程序就认为命令有效。

命令必须在相应配置中定义。

---

## 20. 兼容性

插件必须遵循 RtG-CLI 语法规则以正确集成。
插件内部实现可完全不同，但其命令接口必须遵循 RtG-CLI 确立的规则。

---

## 21. 优先级规则

识别插件后，单连字符 (`-`) 保留给 RtG-CLI。
插件不得使用以单连字符开头的参数。
以双连字符 (`--`) 或无连字符开头的参数属于插件。

---

## 22. 插件参数

识别插件后，RtG-CLI 不得假定插件特定参数的含义。

属于插件的参数必须传递给插件程序处理。

示例：

`rtg image --width 128`

RtG-CLI 将 `image` 识别为插件。

`--width 128` 对应 RtG Image 接口，必须由该插件处理。

---

## 23. 带空格的参数

包含空格的参数必须用引号括起，以便终端将其视为单个参数。

示例：

`rtg image "C:\Users\User\Downloads\我的图片.png" "C:\Users\User\Downloads\输出.json"`

完整路径必须作为单个参数接收。

---

## 24. 插件参数必须保留

除非系统规则明确规定，RtG-CLI 不得修改、移除或重新解释发往插件的参数。

参数必须按用户提供的顺序传递给插件。

---

## 25. 完整示例

插件命令：

`rtg image`

帮助：

`rtg help image`

英文帮助：

`rtg help image -en`

查询语言：

`rtg help image -lang`

CLI 版本：

`rtg --version`

CLI 帮助：

`rtg --help`

插件特定选项：

`rtg image --width 128`

插件特定选项带值：

`rtg image --output file.json`

组合：

`rtg image image.png --output output.json`

此例中：

* `image` 标识插件。
* `image.png` 是插件参数。
* `--output` 是插件选项。
* `output.json` 是该选项的值。
* 这些参数均不应被解释为系统选项。

---

## 26. 启动文本语言

`rtg -language <语言>` 选择 RtG-CLI 显示的启动文本语言。

该语言必须存在于 `void-language` 中。

示例：

`rtg -language zh`

显示以下中定义的文本：

`void-language.zh`

若未指定 `-language`，RtG-CLI 使用 `void`。

若请求的语言不可用，RtG-CLI 必须报告语言不可用。