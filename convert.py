import os
import glob
import re

# 現在のフォルダ（スクリプトを置いた場所）を基準にする
TARGET_DIR = '.'

def convert_to_utf8(filepath):
    try:
        # 古いWindows標準の文字コード（cp932 / Shift_JIS）としてファイルを読み込む
        with open(filepath, 'r', encoding='cp932', errors='ignore') as f:
            content = f.read()

        # すでに新しいUTF-8のタグが入っている場合はスキップ
        if '<meta charset="UTF-8">' in content:
            return False

        # 古い <meta http-equiv=Content-Type ... charset=shift_jis> の行を探して、
        # 現代の <meta charset="UTF-8"> に丸ごと置き換える（大文字小文字を区別しない）
        content = re.sub(
            r'<meta\s+http-equiv=["\']?Content-Type["\']?\s+content=["\']?text/html;\s*charset=[a-zA-Z0-9_-]+["\']?\s*/?>',
            '<meta charset="UTF-8">',
            content,
            flags=re.IGNORECASE
        )

        # 文字コードを UTF-8 に指定して上書き保存する
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

        return True

    except Exception as e:
        print(f"エラーが発生しました ({filepath}): {e}")
        return False

def main():
    print("全ファイルのUTF-8変換を開始します...")
    count = 0
    
    # フォルダの中にあるすべての .htm と .html を探す（サブフォルダも含む）
    for ext in ('*.htm', '*.html'):
        for filepath in glob.glob(os.path.join(TARGET_DIR, '**', ext), recursive=True):
            if convert_to_utf8(filepath):
                print(f"変換完了: {filepath}")
                count += 1

    print(f"完了しました！ 合計 {count} 個のファイルをUTF-8に変換しました。")

if __name__ == "__main__":
    main()