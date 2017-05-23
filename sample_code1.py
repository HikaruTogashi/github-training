# coding: utf-8
import sys

# コマンドライン引数を取得
argv = sys.argv

if len(argv) < 2:
    print("usage: python this_script.py target_filename")
    exit()

# コマンドライン引数の最後に与えられたファイルを読み込んで行をソートし出力する
with open(argv[-1]) as f:
    lines = f.readlines()
    lines_sorted = sorted(lines)
    for l in lines_sorted:
        print(l.rstrip("\n"))
