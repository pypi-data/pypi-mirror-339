#!/bin/bash
# 测试发布脚本 - 用于测试包的构建和上传到TestPyPI

# 确保脚本在错误时立即停止
set -e

echo "===== CMD AI 测试发布脚本 ====="
echo "此脚本将构建包并上传到TestPyPI，用于测试发布流程"
echo

# 检查是否安装了必要的工具
command -v python >/dev/null 2>&1 || { echo "需要安装Python"; exit 1; }
python -c "import build" >/dev/null 2>&1 || { echo "需要安装build: pip install build"; exit 1; }
python -c "import twine" >/dev/null 2>&1 || { echo "需要安装twine: pip install twine"; exit 1; }
command -v curl >/dev/null 2>&1 || { echo "需要安装curl"; exit 1; }
# command -v jq >/dev/null 2>&1 || { echo "需要安装jq"; exit 1; }

# 获取包名
echo ">> 检查包名可用性..."
PACKAGE_NAME=$(grep -E "^name\s*=" pyproject.toml | cut -d '"' -f 2 | cut -d "'" -f 2)
if [ -z "$PACKAGE_NAME" ]; then
    echo "错误：无法从pyproject.toml获取包名"
    exit 1
fi
echo ">> 包名: $PACKAGE_NAME"

# 检查是否在TestPyPI已存在
TESTPYPI_URL="https://test.pypi.org/pypi/$PACKAGE_NAME/json"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $TESTPYPI_URL)
if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "警告: 包名'$PACKAGE_NAME'在TestPyPI上已存在"
    read -p "是否继续? 这将上传一个新版本 [y/N]: " continue_upload
    if [[ $continue_upload != [yY] && $continue_upload != [yY][eE][sS] ]]; then
        echo "建议在pyproject.toml中修改包名后再试"
        exit 0
    fi
else
    echo ">> 包名'$PACKAGE_NAME'在TestPyPI上可用"
fi

# 检查是否在PyPI已存在
PYPI_URL="https://pypi.org/pypi/$PACKAGE_NAME/json"
HTTP_STATUS=$(curl -s -o /dev/null -w "%{http_code}" $PYPI_URL)
if [ "$HTTP_STATUS" -eq 200 ]; then
    echo "警告: 包名'$PACKAGE_NAME'在PyPI上已存在"
    read -p "是否继续? 如果这不是您的包，后续发布可能会失败 [y/N]: " continue_pypi
    if [[ $continue_pypi != [yY] && $continue_pypi != [yY][eE][sS] ]]; then
        echo "建议在pyproject.toml中修改包名后再试"
        exit 0
    fi
else
    echo ">> 包名'$PACKAGE_NAME'在PyPI上可用"
fi

# 清理旧的构建文件
echo ">> 清理旧的构建文件..."
rm -rf dist build *.egg-info

# 构建包
echo ">> 构建分发包..."
python -m build

# 确认TestPyPI上传
echo
echo ">> 分发包已构建完成。接下来将上传到TestPyPI进行测试."
echo ">> 您需要一个TestPyPI账号: https://test.pypi.org/account/register/"
echo
read -p "是否继续上传到TestPyPI? [y/N]: " confirm
if [[ $confirm != [yY] && $confirm != [yY][eE][sS] ]]; then
    echo "已取消上传。您可以稍后手动运行:"
    echo "twine upload --repository-url https://test.pypi.org/legacy/ dist/*"
    exit 0
fi

# 上传到TestPyPI
echo ">> 上传到TestPyPI..."
twine upload --repository-url https://test.pypi.org/legacy/ dist/*

echo
echo ">> 上传完成!"
echo ">> 您可以使用以下命令测试安装:"
echo "uv pip install --index-url https://test.pypi.org/simple/ $PACKAGE_NAME"

echo
echo ">> 如果测试成功，可以使用以下命令发布到正式PyPI:"
echo "twine upload dist/*"

echo
echo "===== 测试发布流程完成 =====" 