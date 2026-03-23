#!/usr/local/bin/python3.7

FILE_DATA = "./data.txt"

# 日本語を扱うために必要な設定
import os, sys, io, cgi, re
sys.stdin, sys.stdout, sys.etderr =  [
    open(sys.stdin.fileno(),  'r', encoding='UTF-8'),
    open(sys.stdout.fileno(), 'w', encoding='UTF-8'),
    open(sys.stderr.fileno(), 'w', encoding='UTF-8')]
out = lambda s: print(s, end="\n")
form = cgi.FieldStorage()

# パラメータを確認して処理を分岐
def check_param():
    m = get_form('m', 'show')
    if m == "show":
        mode_show()
    elif m == "add":
        mode_add()
    elif m == "rm":
        mode_remove()
    else:
        out_html("パラメータの間違い")

# TODOの一覧を表示する
def mode_show():
    items = load_items()
    t = "<h1>褒めるTODO</h1><div id='items'>"
    for no, it in enumerate(items):
        k = "todo.py?m=rm&no="+str(no)
        a = "<a href='" + k + "'>❎️</a> "
        t += "<p>" + a + it + "</p>"
    t += "<form><p class='frm'>TODO: "
    t += input_tag('text', 'todo', '')
    t += input_tag('hidden', 'm', 'add')
    t += input_tag('submit', '', '追加')
    t += "</p></form></div>"
    out_html(t)

# 新規TODOを追加する
def mode_add():
    todo = get_form('todo', '')
    if todo == '':
        out_html('追加するテキストがありません')
        return
    items = load_items()
    items.append(todo)
    save_items(items)
    s = "<div id='items'><p>書き込ました。<br/>"
    s += "素晴らしい！いつも頑張ってますね！</p>"
    s += "<a href='todo.py'>戻る</a></div>"
    out_html(s)

# アイテムを削除
def mode_remove():
    no = int(get_form('no', '-1'))
    if no < 0:
        out_html('番号の間違い')
        return
    items = load_items()
    del items[no]
    save_items(items)
    out_html('削除しました。<a href="todo.py">戻る</a>')

# アイテムを読み込む
def load_items():
    text = "test1\ntest2\ntest3\n"
    if os.path.exists(FILE_DATA):
        with open(FILE_DATA, 'rt', encoding="utf-8") as f:
            text = f.read()
    items = text.strip().split("\n")
    return items

# アイテムを保存
def save_items(items):
    text = "\n".join(items)
    with open(FILE_DATA, 'wt', encoding="utf-8") as f:
        f.write(text)

# HTMLを出力する
def out_html(html):
    out("Content-type: text/html; charset=utf-8")
    out("")
    out("<html><head>")
    out('<link href="/style.css" rel="stylesheet">')
    out("</head><body>" + html)
    out("</body></html>")

# <input>タグを返す
def input_tag(type, name, value):
    s = '<input type="{}" name="{}" value="{}">'
    return s.format(type, name, value)

# フォームの値を取得して返す
def get_form(name, defvalue):
    if name in form:
        return form[name].value
    return defvalue



if __name__ == '__main__':
    check_param()
