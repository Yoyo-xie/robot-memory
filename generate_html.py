#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
生成 Robot Memory 网页

注意：此脚本直接嵌入 prompts_data.js 的内容到 HTML 中，
保持转义字符（如 \n）不被转换，避免 JavaScript 解析错误。

关键点：使用函数作为替换参数，避免反向引用问题
"""

import re

def generate_html():
    # 读取 prompts_data.js
    with open('prompts_data.js', 'r', encoding='utf-8') as f:
        js_data = f.read()

    # 验证格式：检查是否包含转义的换行符
    if '\\n' not in js_data:
        print("[ERROR] prompts_data.js does not contain escaped \\n")
        print("        Make sure newlines in JSON are escaped as \\n")
        return False

    # 读取当前的 index.html 作为模板（保留样式）
    try:
        with open('index.html', 'r', encoding='utf-8') as f:
            html_template = f.read()
    except FileNotFoundError:
        print("[ERROR] index.html not found")
        return False

    # 提取数据（去掉 'const PROMPTS_DATA=' 和结尾的 ';'）
    data_match = re.search(r'const PROMPTS_DATA\s*=\s*(\[.*?\]);', js_data, re.DOTALL)
    if not data_match:
        print("[ERROR] Cannot extract data from prompts_data.js")
        return False

    new_data = data_match.group(1)  # 只获取数组部分 [...]
    new_statement = f'const PROMPTS_DATA={new_data};'

    # 检查当前HTML中的数据
    current_match = re.search(r'const PROMPTS_DATA\s*=\s*\[.*?\];', html_template, re.DOTALL)
    if current_match:
        current_data = current_match.group(0)

        # 检查是否需要更新
        if current_data == new_statement:
            print("[OK] index.html is already up to date")
            count = html_template.count('"title":')
            print(f"[OK] Prompts count: {count}")
            return True

    # 使用函数替换（避免反向引用问题）
    def replacement_func(match):
        return new_statement

    pattern = r'const PROMPTS_DATA\s*=\s*\[.*?\];'
    new_html = re.sub(pattern, replacement_func, html_template, flags=re.DOTALL)

    # 验证替换是否成功
    if new_html == html_template:
        print("[ERROR] No replacement made - PROMPTS_DATA not found")
        return False

    # 保存
    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(new_html)

    # 验证格式（检查是否仍有转义的 \n）
    if '\\n' in new_html:
        print("[OK] index.html updated")
        print("[OK] Escaped newlines (\\n) preserved")

        # 统计提示词数量
        count = new_html.count('"title":')
        print(f"[OK] Prompts count: {count}")
        return True
    else:
        print("[WARNING] Escaped newlines may have been converted")
        return False

if __name__ == '__main__':
    generate_html()
