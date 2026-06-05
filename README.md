# GX Works2 I/O List Lab

## 概要

このリポジトリは、Mitsubishi GX Works2から出力したCSVデータをPythonで解析し、PLCのI/Oリスト整理と確認作業を自動化するための学習・研究プロジェクトです。

目的は、GX Works2のCSV出力をそのまま見るだけではなく、ラダー内で実際に使用されているX/Yデバイスを抽出し、Device Commentと結合して、確認しやすいExcelレポートとして出力することです。

## 目的

このプロジェクトは、ポートフォリオであると同時に、PLC実務で発生しやすい文書整理・確認作業をPythonでどこまで自動化できるかを試すための記録です。

特に以下のような確認作業を補助することを目指しています。

- ラダーCSV内で使用されているX/Yデバイスの抽出
- 入力(INPUT)と出力(OUTPUT)の分類
- Device Comment CSVとの結合
- ロジック周辺のノート情報の整理
- コメント未登録や複数箇所使用などの確認項目の出力
- Excel形式のI/Oレポート作成

## 現在の機能

- GX Works2ラダーCSVの読み込み
- フォルダ内の複数CSVファイルを一括解析
- X/Yデバイスのみを抽出
- XをINPUT、YをOUTPUTとして分類
- Mitsubishi PLCのX/Yアドレスを16進数基準で並び替え
- 同一デバイスの重複使用をまとめて表示
- ラダーCSV内のノート行をLogicNotesとして関連付け
- グローバルデバイスコメントCSVを読み込み
- DeviceComment列としてI/O一覧に結合
- CHECKシートで確認項目を出力
- RAW_DATAシートで解析元データを追跡可能にする
- CSVとExcelの両方でレポートを出力

## 出力ファイル

```text
output/io_list.csv
output/io_list_report.xlsx
```

Excelレポートには以下のシートを出力します。

```text
SUMMARY
INPUT
OUTPUT
CHECK
RAW_DATA
```

## CHECKシートの確認項目

CHECKシートは、エラーを断定するものではなく、人が確認すべき項目をまとめるためのシートです。

現在は以下の項目を出力します。

```text
MISSING_DEVICE_COMMENT
MISSING_LOGIC_NOTE
MULTIPLE_USED_FILES
MULTIPLE_LOGIC_NOTES
COMMENTED_BUT_NOT_USED
SPARE_OR_UNUSED_DEVICE
```

CHECKシートでは、確認項目を以下のカテゴリに分類します。

```text
Documentation
Usage
LogicContext
```

各項目の意味は以下の通りです。

| Type | Level | Category | 意味 | 実務での確認観点 |
|---|---|---|---|---|
| MISSING_DEVICE_COMMENT | WARN | Documentation | ラダーではX/Yデバイスが使用されているが、Device Commentが登録されていない | そのアドレスが何のセンサ、ボタン、出力なのか分かりにくいため、Device Commentの補完を検討する |
| MISSING_LOGIC_NOTE | INFO | LogicContext | 対象X/Yデバイスの近くにラダーノートが見つからない | 必ずしも問題ではない。Device Commentが十分であれば参考情報として扱う |
| MULTIPLE_USED_FILES | WARN | Usage | 同じX/Yデバイスが複数のラダーCSVで参照されている | 改造や修正時に影響範囲が広がる可能性があるため、使用箇所を確認する |
| MULTIPLE_LOGIC_NOTES | WARN | LogicContext | 同じX/Yデバイスに複数のLogicNotesが関連付けられている | LogicNotesをそのまま信号名として使わず、ロジック上の文脈として確認する |
| COMMENTED_BUT_NOT_USED | WARN | Documentation | Device Commentは登録されているが、ラダーCSVでは使用されていない | 予備アドレス、削除済みロジックの残り、または解析対象外プログラムの可能性を確認する |
| SPARE_OR_UNUSED_DEVICE | INFO | Documentation | 予備・未使用として登録されており、ラダーCSVでも使用されていない | 正常な予備アドレスである可能性が高く、基本的には参考情報として扱う |

簡単に表現すると、各CHECK項目は以下のような確認を行います。

| Type | 確認すること |
|---|---|
| MISSING_DEVICE_COMMENT | このアドレスは使われているのに、名前や説明が未登録ではないか |
| MISSING_LOGIC_NOTE | このロジック周辺の説明が不足していないか |
| MULTIPLE_USED_FILES | このアドレスが複数プログラムで使われており、影響範囲が広くないか |
| MULTIPLE_LOGIC_NOTES | このアドレスに複数の説明が付いており、意味を誤解しないか |
| COMMENTED_BUT_NOT_USED | コメントはあるが、実際には使われていないアドレスではないか |
| SPARE_OR_UNUSED_DEVICE | 予備・未使用として管理されているアドレスではないか |

## DeviceCommentとLogicNotesの違い

`DeviceComment`は、PLCデバイスアドレス自体に付けられた説明です。

例:

```text
X50 = CH1 count start signal
```

`LogicNotes`は、ラダーCSV内でロジックの近くに書かれている説明です。

例:

```text
X50がONしたとき、Count enable commandをONする
```

つまり、`DeviceComment`は「このアドレスは何か」、`LogicNotes`は「このロジックは何をしているか」を表します。

## 処理の流れ

```text
GX Works2
→ ラダーCSVを出力
→ グローバルデバイスコメントCSVを出力
→ PythonでCSVを読み込み
→ X/Yデバイスを抽出
→ DeviceCommentと結合
→ CHECK項目を生成
→ Excelレポートを作成
```

## サンプルデータについて

このプロジェクトでは、Mitsubishi Electricが公開しているGX Works2サンプルプロジェクトを学習目的で使用しています。

```text
https://www.mitsubishielectric-fa.cn/fb/english/melsoft_library/fa/products/cnt/plceng/download/library/mitsubishi/ld_lcpu_e/index.html
```

## 実行方法

```powershell
python main.py
```

実行後、`output`フォルダにCSVとExcelレポートが生成されます。

