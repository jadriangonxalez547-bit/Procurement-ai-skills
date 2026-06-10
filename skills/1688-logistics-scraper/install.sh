#!/bin/bash
# 1688 Logistics Scraper 一键安装（macOS / Linux）
# 用法: curl -fsSL https://raw.githubusercontent.com/jadriangonxalez547-bit/Procurement-ai-skills/main/skills/1688-logistics-scraper/install.sh | bash

set -e

SKILL_NAME="1688-logistics-scraper"
SKILL_SRC="$(cd "$(dirname "${BASH_SOURCE[0]:-$0}")" && pwd 2>/dev/null || echo "$PWD")"
SKILL_DST="$HOME/.claude/skills/$SKILL_NAME"

echo ""
echo "🚀 1688 物流抓取 Skill 安装器"
echo "================================"
echo ""

# 1. 检查 Python
echo -n "[1/5] 检查 Python..."
if command -v python3 &> /dev/null; then
  PY=python3
  echo " ✅ $($PY --version 2>&1)"
elif command -v python &> /dev/null; then
  PY=python
  echo " ✅ $($PY --version 2>&1)"
else
  echo " ❌"
  echo "请先安装 Python 3.8+: https://www.python.org/downloads/" >&2
  exit 1
fi

# 2. 安装 openpyxl
echo -n "[2/5] 安装 openpyxl..."
$PY -m pip install --quiet openpyxl 2>&1 > /dev/null
echo " ✅"

# 3. 检查 Kimi WebBridge
echo -n "[3/5] 检查 Kimi WebBridge..."
if command -v kimi-webbridge &> /dev/null; then
  status=$(kimi-webbridge status 2>&1)
  if echo "$status" | grep -q '"running":true'; then
    echo " ✅ 已运行"
  else
    echo " ⚠️  已安装但未运行"
    echo "   启动命令: kimi-webbridge start"
  fi
else
  echo " ❌ 未安装"
  read -p "   是否现在安装? (Y/n) " ans
  if [[ -z "$ans" || "$ans" == "Y" || "$ans" == "y" ]]; then
    echo -n "   正在安装 Kimi WebBridge..."
    curl -fsSL https://cdn.kimi.com/webbridge/install.sh | bash 2>&1 > /dev/null || true
    echo " ✅"
  else
    echo "   跳过，请稍后手动安装"
  fi
fi

# 4. 提示 Chrome 扩展
echo "[4/5] Kimi WebBridge Chrome 扩展..."
echo "   ⚠️  请手动在 Chrome 安装扩展: https://kimi.com/features/webbridge"
read -p "   安装完成后按 Enter 继续"

# 5. 复制 skill
echo -n "[5/5] 复制 skill 到 $SKILL_DST ..."
if [ -d "$SKILL_DST" ]; then
  read -p "   目标已存在，是否覆盖? (Y/n) " ans
  if [[ -z "$ans" || "$ans" == "Y" || "$ans" == "y" ]]; then
    rm -rf "$SKILL_DST"
  else
    echo " ❌ 跳过"
    exit 1
  fi
fi
mkdir -p "$SKILL_DST"
# 复制但排除本地数据
for item in "$SKILL_SRC"/*; do
  name=$(basename "$item")
  case "$name" in
    orders_data.json|*.xlsx|~*) continue ;;
  esac
  cp -r "$item" "$SKILL_DST/"
done
# 清理 scripts 目录中的数据文件
rm -f "$SKILL_DST/scripts/orders_data.json"
rm -f "$SKILL_DST/scripts"/*.xlsx
rm -f "$SKILL_DST/scripts"/~*
echo " ✅"

echo ""
echo "🎉 安装完成！"
echo ""
echo "📋 使用步骤："
echo "   1. 在 Chrome 登录 1688 账号"
echo "   2. 重启 Claude Code（让 skill 生效）"
echo "   3. 对 Claude Code 说："
echo "      抓取 1688 待收货订单"
echo ""
echo "📁 Skill 位置: $SKILL_DST"
echo ""
