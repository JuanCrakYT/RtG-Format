# RtG-CLI 命令規則

## 1. 一般結構

RtG-CLI 命令由主命令和可選參數組成。
通用格式：

`rtg <指令> [<參數>]`

`rtg` 後的第一個參數決定將執行哪個命令或外掛。

範例：

`rtg image`

`rtg preview`

`rtg help image`

---

## 2. 已註冊命令

主命令必須在 RtG-CLI 配置中註冊。
命令透過其內部鍵識別。

範例：

`image`

`image` 鍵識別對應的外掛，無論顯示給用戶的名稱是什麼。
範例：

`image` → `RtG Image`

`preview` → `RtG Preview`

顯示的名稱不得用作命令識別符。

---

## 3. RtG-CLI 命令和外掛命令

RtG-CLI 和外掛可以有各自的命令和參數。

在識別外掛之前，命令和參數屬於 RtG-CLI。
識別外掛後，前綴決定每個參數歸屬：

- 無連字符 (`-`) → 屬於外掛。
- 雙連字符 (`--`) → 屬於外掛。
- 單連字符 (`-`) → 屬於 RtG-CLI。

範例：

`rtg image convert`

- `image` → 外掛。
- `convert` → 外掛命令。

範例：

`rtg image --width 128`

- `image` → 外掛。
- `--width` → 外掛參數。
- `128` → 外掛參數的值。

範例：

`rtg image -lang`

- `image` → 外掛。
- `-lang` → RtG-CLI 參數。

---

## 4. 系統參數

在識別外掛之前，RtG-CLI 使用其自身的語法規則。
長系統選項使用雙連字符：

`rtg --version`
`rtg --help`

系統縮寫使用單連字符：

`rtg -v`
`rtg -h`
`rtg -l`

識別外掛後，以單連字符 (`-`) 開頭的選項屬於 RtG-CLI。

範例：

`rtg image -lang`
`rtg image -en`

---

## 5. 外掛識別前後的參數

RtG-CLI 參數根據出現在外掛識別前還是後可能具有不同含義。

識別外掛前，參數屬於 RtG-CLI。

例如：

`rtg --lang`

顯示 RtG-CLI 可用語言。

識別外掛後，參數按外掛的所有權規則解釋。

例如：

`rtg image -lang`

查詢 `image` 外掛的可用語言。

這樣，參數的位置決定其上下文，防止全局 RtG-CLI 參數與外掛識別後使用的參數混淆。

---

## 6. 系統參數的位置

系統參數不得出現在其影響的命令或外掛之前（當參數依賴該命令時）。

正確範例：

`rtg help image -en`

錯誤範例：

`rtg help -en image`

這兩個範例中，系統命令 `help` 使用此結構，因此第二個範例不正確：
`help <target> <options>`

位置必須明確確定哪個命令接收參數。

---

## 7. 外掛命令和參數

命令作為單獨的終端參數編寫。
命令不得包含空格，除非用引號括起。

後續參數可由外掛按其自身介面使用。

例如：

`rtg image convert image`

可解釋為：

- `image` → 外掛
- `convert` → 外掛命令
- `image` → 命令參數

---

## 8. 外掛命令中的連字符使用

識別外掛後：

- 無連字符的參數屬於外掛。
- 雙連字符或更多 (`--`) 的參數屬於外掛。
- 單連字符 (`-`) 的參數屬於 RtG-CLI。

範例：

`rtg image convert`
`convert` → 外掛。

`rtg image --width 128`
`--width` → 外掛。

`rtg image -lang`
`-lang` → RtG-CLI。

---

## 9. 外掛命令介面

外掛特定命令由外掛程序自身定義。
RtG-CLI 透過外掛配置的 `program commands` 屬性定位其命令介面。

該屬性包含提供程序命令介面的檔案路徑。

範例：

```json
"program commands": [
    "../tools/RtG Image/commands.py"
]
```

RtG-CLI 可使用此介面發現或執行外掛可用命令，但不得假定或修改其內部命令含義。

外掛可定義未直接註冊為 RtG-CLI 命令的額外命令。

程序內部實現可在外掛間不同，只要提供與 RtG-CLI 規則相容的介面。

---

## 10. 語言

外掛可用語言透過其配置定義。

範例：

`lang: ["es", "en"]`

翻譯文本使用對應的語言代碼識別。

範例：

`content.zh-TW`
`content.en`

RtG-CLI 使用的語言選擇器必須視為系統參數。

範例：

`rtg help image -en`

---

## 11. 預設語言

若未指定 `-<語言>`，RtG-CLI 將使用 `rules` 中定義的第一種語言。
若指定了 `-<語言>`，RtG-CLI 將在該語言可用時使用它。

`assets.json` 中 `rules` 物件定義的第一種語言為規則的預設語言。

用戶未指定語言請求規則時，RtG-CLI 必須使用該第一種語言。

例如：

```json
"rules": {
    "es": "./rules.es.md",
    "en": "./rules.en.md"
}
```

此時：

`rtg -r`
和
`rtg --rules`

將以西班牙語顯示規則，因為 `es` 是首個定義的語言。
請求其他語言需使用對應選擇器：

`rtg -r -en`

`rules` 內語言順序僅決定預設語言，不改變可用語言。

此規則也適用於其他語言選擇器，如：

`rtg help image -es`

---

## 12. 語言不改變命令

更改語言僅修改 RtG-CLI 顯示的文本。
不改變內部命令名稱。

範例：

`rtg help image -es`

和

`rtg help image -en`

仍引用同一命令：

`image`

---

## 13. 說明

通用說明透過以下方式獲取：

`rtg help`

特定命令說明透過以下方式獲取：

`rtg help <指令>`

可請求特定語言的說明：

`rtg help <指令> -<語言>`

範例：

`rtg help image -en`

---

## 14. 語言查詢

外掛可用語言可透過以下方式查詢：

`rtg help <指令> -lang`

範例：

`rtg help image -lang`

此選項屬於 RtG-CLI，而非外掛。

---

## 15. 外掛不得修改系統規則

外掛可定義自身命令和參數，但不得重新定義 RtG-CLI 保留參數的含義。

例如，外掛不得使用 `-h` 賦予系統說明不同含義。
RtG-CLI 保留的名稱優先於外掛命令。
RtG-CLI 保留的命令和選項必須由 CLI 介面顯式定義。
外掛不得重新定義保留選項的行為。

---

## 16. 識別符與名稱的分離

外掛內部鍵用於識別它。
外掛名稱僅用作描述資訊或向用戶顯示。

範例：

`image` → 內部識別符

`RtG Image` → 顯示名稱

不得假定顯示名稱可用作命令。

---

## 17. 命令必須是確定性的

RtG-CLI 必須能基於命令結構和規則，而非程序描述性名稱，判斷參數歸屬系統還是外掛。

範例：

`rtg help image -en`

必須始終以相同方式解釋：

`rtg` → CLI

`help` → CLI 命令

`image` → 外掛

`-en` → CLI 選項

---

## 18. 未知參數

識別外掛後，RtG-CLI 必須按前綴確定每個參數歸屬。

* 無連字符參數屬於外掛。
* 雙連字符或更多 (`--`) 參數屬於外掛。
* 單連字符 (`-`) 參數屬於 RtG-CLI。

若 RtG-CLI 收到未知系統參數，必須報告該選項不存在。

外掛參數必須原樣傳遞給外掛，RtG-CLI 不得嘗試解釋其含義。

---

## 19. 不假設未註冊命令

RtG-CLI 不得僅因存在相關資料夾、檔案或程式就認為命令有效。

命令必須在相應配置中定義。

---

## 20. 相容性

外掛必須遵循 RtG-CLI 語法規則以正確整合。
外掛內部實現可完全不同，但其命令介面必須遵循 RtG-CLI 確立的規則。

---

## 21. 優先級規則

識別外掛後，單連字符 (`-`) 保留給 RtG-CLI。
外掛不得使用以單連字符開頭的參數。
以雙連字符 (`--`) 或無連字符開頭的參數屬於外掛。

---

## 22. 外掛參數

識別外掛後，RtG-CLI 不得假定外掛特定參數的含義。

屬於外掛的參數必須傳遞給外掛程序處理。

範例：

`rtg image --width 128`

RtG-CLI 將 `image` 識別為外掛。

`--width 128` 對應 RtG Image 介面，必須由該外掛處理。

---

## 23. 帶空格的參數

包含空格的參數必須用引號括起，以便終端將其視為單個參數。

範例：

`rtg image "C:\Users\User\Downloads\我的圖片.png" "C:\Users\User\Downloads\輸出.json"`

完整路徑必須作為單個參數接收。

---

## 24. 外掛參數必須保留

除非系統規則明確規定，RtG-CLI 不得修改、移除或重新解釋發往外掛的參數。

參數必須按用戶提供的順序傳遞給外掛。

---

## 25. 完整範例

外掛命令：

`rtg image`

說明：

`rtg help image`

英文說明：

`rtg help image -en`

查詢語言：

`rtg help image -lang`

CLI 版本：

`rtg --version`

CLI 說明：

`rtg --help`

外掛特定選項：

`rtg image --width 128`

外掛特定選項帶值：

`rtg image --output file.json`

組合：

`rtg image image.png --output output.json`

此例中：

* `image` 識別外掛。
* `image.png` 是外掛參數。
* `--output` 是外掛選項。
* `output.json` 是該選項的值。
* 這些參數均不應被解釋為系統選項。

---

## 26. 啟動文字語言

`rtg -language <語言>` 選擇 RtG-CLI 顯示的啟動文字語言。

該語言必須存在於 `void-language` 中。

範例：

`rtg -language zh-TW`

顯示以下中定義的文字：

`void-language.zh-TW`

若未指定 `-language`，RtG-CLI 使用 `void`。

若請求的語言不可用，RtG-CLI 必須報告語言不可用。