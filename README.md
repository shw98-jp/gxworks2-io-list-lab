# GX Works2 I/O List Lab

## 概要

このリポジトリは、Mitsubishi GX Works2から出力したCSVデータをPythonで解析し、PLCのI/Oリスト整理作業を自動化できるかを試すための学習・研究プロジェクトです。

最初から完成された業務用ツールを作ることだけを目的とするのではなく、PLCプログラムのデータ構造やGX Works2のCSV出力形式を理解しながら、繰り返し発生する文書整理作業をどのように自動化できるかを探ることを目的としています。

初期目標は、GX Works2日本語版からエクスポートしたラダープログラムCSV、またはデバイスコメントCSVを読み込み、X/Yアドレスを抽出して入力・出力に分類し、一覧表とチェック結果をExcelレポートとして生成することです。

## 目的

このプロジェクトは、ポートフォリオであると同時に、個人的な学習・研究の記録でもあります。

PLCの実務で繰り返し発生するI/Oリスト整理、アドレス確認、コメント未入力チェックなどの作業をPythonで自動化できるかを試し、その過程をコードとドキュメントとして残すことを目標としています。

## 初期機能目標

- GX Works2日本語版からエクスポートしたCSVファイルの読み込み
- X/Yデバイスアドレスの抽出
- Xアドレスを入力、Yアドレスを出力として分類
- PLCアドレス順に並び替え
- コメント未入力項目のチェック
- 重複アドレスのチェック
- INPUT / OUTPUT / ERROR シートを含むExcelレポートの生成

## サンプルデータについて

`samples/ladder/01CmnPgm.csv` は、Mitsubishi Electric が公開している GX Works2 サンプルプロジェクトから、学習目的でラダープログラムをCSV出力したものです。

`link` : https://www.mitsubishielectric-fa.cn/fb/english/melsoft_library/fa/products/cnt/plceng/download/library/mitsubishi/ld_lcpu_e/index.html

## 処理の流れ

```text
GX Works2
→ CSV Export
→ PythonでCSVを読み込み
→ X/Yアドレスを抽出
→ 入力・出力に分類
→ 未入力・重複をチェック
→ Excelレポートを生成