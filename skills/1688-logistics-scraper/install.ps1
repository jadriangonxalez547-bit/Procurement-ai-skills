<#
.SYNOPSIS
  1688 Logistics Scraper 一键安装（Windows）

.DESCRIPTION
  - 检查 Python 环境
  - 安装 openpyxl
  - 询问是否安装 Kimi WebBridge
  - 复制 skill 到 ~/.claude/skills/1688-logistics-scraper/

.EXAMPLE
  irm https://raw.githubusercontent.com/jadriangonxalez547-bit/Procurement-ai-skills/main/skills/1688-logistics-scraper/install.ps1 | iex
#>

$ErrorActionPreference = 'Stop'
$SkillName = '1688-logistics-scraper'
$SkillSrc = $PSScriptRoot  # 脚本所在目录（即 skill 目录）
$SkillDst = Join-Path $env:USERPROFILE ".claude\skills\$SkillName"

Write-Host ""
Write-Host "🚀 1688 物流抓取 Skill 安装器" -ForegroundColor Cyan
Write-Host "================================" -ForegroundColor Cyan
Write-Host ""

# 1. 检查 Python
Write-Host "[1/5] 检查 Python..." -NoNewline
try {
  $py = python --version 2>&1
  if ($LASTEXITCODE -ne 0) { throw "Python not found" }
  Write-Host " ✅ $py" -ForegroundColor Green
} catch {
  Write-Host " ❌" -ForegroundColor Red
  Write-Host "请先安装 Python 3.8+：https://www.python.org/downloads/" -ForegroundColor Yellow
  exit 1
}

# 2. 安装 openpyxl
Write-Host "[2/5] 安装 openpyxl..." -NoNewline
try {
  python -m pip install --quiet openpyxl 2>&1 | Out-Null
  if ($LASTEXITCODE -ne 0) { throw "pip install failed" }
  Write-Host " ✅" -ForegroundColor Green
} catch {
  Write-Host " ❌" -ForegroundColor Red
  Write-Host "请手动执行: pip install openpyxl" -ForegroundColor Yellow
  exit 1
}

# 3. 检查 Kimi WebBridge
Write-Host "[3/5] 检查 Kimi WebBridge..." -NoNewline
$wb = Get-Command kimi-webbridge -ErrorAction SilentlyContinue
if ($wb) {
  $status = & kimi-webbridge status 2>&1 | Out-String
  if ($status -match '"running":true') {
    Write-Host " ✅ 已运行" -ForegroundColor Green
  } else {
    Write-Host " ⚠️  已安装但未运行" -ForegroundColor Yellow
    Write-Host "   启动命令: kimi-webbridge start" -ForegroundColor Gray
  }
} else {
  Write-Host " ❌ 未安装" -ForegroundColor Yellow
  $ans = Read-Host "   是否现在安装? (Y/n)"
  if ($ans -eq "" -or $ans -eq "Y" -or $ans -eq "y") {
    Write-Host "   正在安装 Kimi WebBridge..." -NoNewline
    try {
      irm https://cdn.kimi.com/webbridge/install.ps1 | iex
      Write-Host " ✅" -ForegroundColor Green
    } catch {
      Write-Host " ❌ 安装失败" -ForegroundColor Red
      Write-Host "   请手动执行: irm https://cdn.kimi.com/webbridge/install.ps1 | iex" -ForegroundColor Gray
    }
  } else {
    Write-Host "   跳过，请稍后手动安装: irm https://cdn.kimi.com/webbridge/install.ps1 | iex" -ForegroundColor Gray
  }
}

# 4. 提示 Chrome 扩展
Write-Host "[4/5] Kimi WebBridge Chrome 扩展..." -ForegroundColor Yellow
Write-Host "   ⚠️  请手动在 Chrome 安装扩展: https://kimi.com/features/webbridge"
$ans = Read-Host "   安装完成后按 Enter 继续"

# 5. 复制 skill 到 ~/.claude/skills/
Write-Host "[5/5] 复制 skill 到 $SkillDst ..." -NoNewline
try {
  if (Test-Path $SkillDst) {
    $ans = Read-Host "   目标已存在，是否覆盖? (Y/n)"
    if ($ans -eq "" -or $ans -eq "Y" -or $ans -eq "y") {
      Remove-Item -Recurse -Force $SkillDst
    } else {
      Write-Host " ❌ 跳过" -ForegroundColor Red
      exit 1
    }
  }
  # 排除本地数据文件
  $exclude = @('orders_data.json', '*.xlsx', '~*')
  Copy-Item -Path "$SkillSrc\*" -Destination $SkillDst -Recurse -Force
  # 清理数据文件
  Get-ChildItem -Path $SkillDst\scripts -Include 'orders_data.json','*.xlsx','~*' -ErrorAction SilentlyContinue | Remove-Item -Force
  Write-Host " ✅" -ForegroundColor Green
} catch {
  Write-Host " ❌ 复制失败: $_" -ForegroundColor Red
  exit 1
}

Write-Host ""
Write-Host "🎉 安装完成！" -ForegroundColor Green
Write-Host ""
Write-Host "📋 使用步骤：" -ForegroundColor Cyan
Write-Host "   1. 在 Chrome 登录 1688 账号" -ForegroundColor White
Write-Host "   2. 重启 Claude Code（让 skill 生效）" -ForegroundColor White
Write-Host "   3. 对 Claude Code 说：" -ForegroundColor White
Write-Host "      " -NoNewline
Write-Host "抓取 1688 待收货订单" -ForegroundColor Yellow
Write-Host ""
Write-Host "📁 Skill 位置: $SkillDst" -ForegroundColor Gray
Write-Host ""
