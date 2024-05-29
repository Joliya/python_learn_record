#!/bin/bash

# 检查参数个数
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 INPUT_FILE OUTPUT_DIR"
    exit 1
fi

# 读取输入文件和输出目录参数
INPUT_FILE="$1"
OUTPUT_DIR="$2"

# LibreOffice 命令的路径
LIBREOFFICE="/Applications/LibreOffice.app/Contents/MacOS/soffice"

# 创建输出目录，如果它不存在的话
mkdir -p "${OUTPUT_DIR}"

# 执行 LibreOffice 命令
$LIBREOFFICE --convert-to docx:"Office Open XML Text" "${INPUT_FILE}" --outdir "${OUTPUT_DIR}"