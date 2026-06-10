# GX Works2 I/O List Lab

## 概要

GX Works2 I/O List Labは、Mitsubishi GX Works2から出力したラダーCSVとデバイスコメントCSVをPythonで解析し、PLCプログラムのI/O使用状況、コメント情報、確認項目をExcelレポートとして整理する学習・研究プロジェクトです。

このツールはPLCを制御するためのものではありません。目的は、GX Works2のCSV出力をもとに、既存プログラムの確認、文書化、保守レビューを補助することです。

## 背景

PLCのI/Oリストは、本来は設備仕様、電気図面、I/O割付をもとに作成され、PLCプログラムはその情報に従って作られます。

一方で、既存設備の保守や改造では、以下のような確認作業が発生します。

- I/Oリストが最新か分からない
- Device Commentが未登録または古い
- どのラダープログラムで特定のI/Oが使われているか確認したい
- Dレジスタ、SM/SDなどの内部デバイス使用箇所を追いたい
- ラダーCSVとコメント情報を照合して、確認すべき項目を整理したい

このプロジェクトでは、そのような確認作業をPythonで補助できるかを試しています。

## このツールが行うこと

- GX Works2ラダーCSVを読み込む
- フォルダ内の複数ラダーCSVを一括解析する
- 実際に使用されているX/Yデバイスを抽出する
- XをINPUT、YをOUTPUTとして分類する
- Mitsubishi PLCのX/Yアドレスを16進数基準で並び替える
- 同一デバイスの複数使用をまとめる
- ラダーCSV内のノート行をLogicNotesとして関連付ける
- グローバルデバイスコメントCSVを読み込む
- DeviceCommentをINPUT/OUTPUT/DEVICE_USAGEに結合する
- コメント未登録、複数箇所使用、未使用コメントなどの確認項目をCHECKシートに出力する
- X/Y以外の内部デバイスや定数をDEVICE_USAGEシートに整理する
- 解析元の行情報をRAW_DATAシートに出力する
- PLC初学者向けに命令語とデバイス種別の参考シートを出力する

## このツールが行わないこと

- PLCプログラムの正誤を自動判定すること
- GX Works2プロジェクトファイルを直接解析すること
- 電気図面、端子台、盤内配線情報を自動生成すること
- 完全な実務I/Oリストを単独で作成すること
- PLC制御ロジックを自動生成または変更すること

このツールの位置づけは、I/Oリスト作成そのものを置き換えるものではなく、GX Works2から出力した情報をもとにした文書化・確認・保守レビューの補助です。

## 入力データ

CSVファイルは、以下のフォルダに配置します。

```text
samples/ladder/*.csv
samples/device_comments/device_comments.csv
```

想定形式:

```text
ラダーCSV:
- encoding: utf-16
- delimiter: tab
- columns: ステップ番号, 命令, I/O(デバイス), ノート など

Device Comment CSV:
- encoding: utf-16
- delimiter: tab
- columns: デバイス名, コメント
```

## 出力データ

実行後、以下のファイルを生成します。

```text
output/io_list.csv
output/io_list_report.xlsx
```

Excelレポートには以下のシートを出力します。

| Sheet | 内容 |
|---|---|
| SUMMARY | プロジェクト名、生成日時、入力/出力パス、解析結果の件数概要 |
| INPUT | Xデバイスの一覧 |
| OUTPUT | Yデバイスの一覧 |
| CHECK | 人が確認すべき項目 |
| CHECK_REFERENCE | CHECK項目の意味、確認ポイント、対応例 |
| DEVICE_USAGE | X/Y以外の内部デバイス・定数の使用状況 |
| INSTRUCTION_REFERENCE | 基本ラダー命令の説明 |
| DEVICE_TYPE_REFERENCE | PLCデバイス種別の説明 |
| RAW_DATA | 解析元ラダーCSV行の追跡情報 |

## CHECKシート

CHECKシートは、エラーを断定するものではありません。人が確認すべき候補をまとめるためのシートです。

| Type | Level | Category | 意味 | 実務での確認観点 |
|---|---|---|---|---|
| MISSING_DEVICE_COMMENT | WARN | Documentation | ラダーではX/Yデバイスが使用されているが、Device Commentが登録されていない | そのアドレスが何のセンサ、ボタン、出力なのか分かりにくいため、Device Commentの補完を検討する |
| MISSING_LOGIC_NOTE | INFO | LogicContext | 対象X/Yデバイスの近くにラダーノートが見つからない | 必ずしも問題ではない。Device Commentが十分であれば参考情報として扱う |
| MULTIPLE_USED_FILES | WARN | Usage | 同じX/Yデバイスが複数のラダーCSVで参照されている | 改造や修正時に影響範囲が広がる可能性があるため、使用箇所を確認する |
| MULTIPLE_LOGIC_NOTES | WARN | LogicContext | 同じX/Yデバイスに複数のLogicNotesが関連付けられている | LogicNotesをそのまま信号名として使わず、ロジック上の文脈として確認する |
| COMMENTED_BUT_NOT_USED | WARN | Documentation | Device Commentは登録されているが、ラダーCSVでは使用されていない | 予備アドレス、削除済みロジックの残り、または解析対象外プログラムの可能性を確認する |
| SPARE_OR_UNUSED_DEVICE | INFO | Documentation | 予備・未使用として登録されており、ラダーCSVでも使用されていない | 正常な予備アドレスである可能性が高く、基本的には参考情報として扱う |

## DeviceCommentとLogicNotesの違い

`DeviceComment`は、デバイスアドレス自体に付けられた説明です。

```text
X50 = CH1 count start signal
```

これは「このアドレスは何か」を表します。

`LogicNotes`は、ラダーCSV内でロジックの近くに書かれている説明です。

```text
X50がONしたとき、Count enable commandをONする
```

これは「このロジックは何をしているか」を表します。

そのため、I/OリストではDeviceCommentを信号名として扱い、LogicNotesはロジック文脈の参考情報として扱います。

## DEVICE_USAGEシート

`DEVICE_USAGE`シートは、I/Oリストには含めない内部デバイスや定数の使用状況を確認するための補助シートです。

X/Yデバイスは`INPUT`、`OUTPUT`シートで確認するため、`DEVICE_USAGE`シートではX/Yを除外し、以下のようなデバイスを中心に出力します。

```text
SM
SD
D
K
M
T
C
```

出力項目:

```text
UsageCategory
DeviceType
Device
DeviceComment
Occurrences
UsedFiles
Instructions
Locations
```

これにより、Dレジスタ、特殊リレー、特殊データレジスタ、定数がどこで使用されているかを確認できます。

`UsageCategory`では、以下のように用途を大まかに分類します。

| UsageCategory | 対象例 | 意味 |
|---|---|---|
| InternalDevice | D, M, L, B, W, R, ZR | プログラム内部で使用するデバイス |
| SpecialDevice | SM, SD | PLC CPUや特殊機能に関連するシステムデバイス |
| Constant | K, H | 命令パラメータとして使われる固定値 |
| TimerCounter | T, C | タイマ・カウンタ系デバイス |
| Other | その他 | 上記に分類されないデバイス |

## REFERENCEシート

Excelレポートには、PLC初学者やレビュー担当者が結果を読みやすくするための参考シートも出力します。

```text
INSTRUCTION_REFERENCE
DEVICE_TYPE_REFERENCE
CHECK_REFERENCE
```

`INSTRUCTION_REFERENCE`では、`LD`、`AND`、`OR`、`ANI`、`OUT`、`SET`、`RST`、`MOV`、`DMOV`などの基本ラダー命令を説明します。

`DEVICE_TYPE_REFERENCE`では、`X`、`Y`、`M`、`SM`、`D`、`SD`、`K`などのPLCデバイス種別を説明します。

`CHECK_REFERENCE`では、`MISSING_DEVICE_COMMENT`、`MULTIPLE_USED_FILES`などのCHECK項目について、意味、確認ポイント、対応例を説明します。

## 処理の流れ

```text
GX Works2
→ ラダーCSVを出力
→ グローバルデバイスコメントCSVを出力
→ PythonでCSVを読み込み
→ X/Yデバイスを抽出
→ DeviceCommentと結合
→ CHECK項目を生成
→ DEVICE_USAGEを生成
→ Excelレポートを作成
```

## 実行方法

CSVファイルを所定のフォルダに配置したうえで、以下を実行します。

```powershell
python main.py
```

実行後、`output`フォルダにCSVとExcelレポートが生成されます。

## 今後の改善案

- 入力/出力パスを指定できるコマンドラインオプションの追加
- 既存I/OリストExcelとの比較
- Device Commentの日本語/韓国語/英語整理
- CHECK項目の追加
- テストケース用CSVの自動検証

## サンプルデータ

このプロジェクトでは、Mitsubishi Electricが公開しているGX Works2サンプルプロジェクトを学習目的で使用しています。

```text
https://www.mitsubishielectric-fa.cn/fb/english/melsoft_library/fa/products/cnt/plceng/download/library/mitsubishi/ld_lcpu_e/index.html
```

## プロジェクトの位置づけ

このプロジェクトは、PLC制御プログラムを作るためのものではなく、PLCエンジニアリングにおける確認・文書化・保守レビューを補助するための実験的なツールです。

AIやPythonを使って、GX Works2から得られるデータをどのように整理し、実務に近い確認作業へつなげられるかを学ぶことを目的としています。
