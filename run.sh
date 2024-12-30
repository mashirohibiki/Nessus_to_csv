#!/bin/bash

# 定义 Python 解释器和脚本路径
PYTHON="/usr/bin/python3"
SCRIPT="Nessus_report.py"

# 遍历 angle 目录下的所有 .html 文件
for html_file in angle/**/*.html; do
    # 检查文件是否存在
    if [ -f "$html_file" ]; then
        echo "Processing $html_file..."
        # 运行 Python 脚本，将当前 HTML 文件作为参数传递
        "$PYTHON" "$SCRIPT" "$html_file"
    else
        echo "No HTML files found in angle directory."
    fi
done