# 1688 Logistics Scraper

> 批量抓取 1688 待收货订单的物流状态和最新物流轨迹，并生成 Excel 表格。

通过 Claude Code + Kimi WebBridge 操作真实浏览器，自动翻页、解析 Shadow DOM、生成可视化 Excel。

---

## ⚡ 一键安装

🪟 **Windows**:
```powershell
irm https://raw.githubusercontent.com/jadriangonxalez547-bit/Procurement-ai-skills/main/skills/1688-logistics-scraper/install.ps1 | iex
```

🍎 **macOS / 🐧 Linux**:
```bash
curl -fsSL https://raw.githubusercontent.com/jadriangonxalez547-bit/Procurement-ai-skills/main/skills/1688-logistics-scraper/install.sh | bash
```

安装脚本会：
1. ✅ 检查并安装 Python 依赖（`openpyxl`）
2. ✅ 检查并提示安装 Kimi WebBridge
3. ✅ 复制 skill 到 `~/.claude/skills/1688-logistics-scraper/`

---

## 📦 前置依赖

| 依赖 | 说明 | 安装方式 |
|------|------|---------|
| Python 3.8+ | 脚本运行环境 | [python.org](https://www.python.org/downloads/) |
| Kimi WebBridge daemon | 浏览器自动化服务 | `irm https://cdn.kimi.com/webbridge/install.ps1 \| iex` |
| Kimi WebBridge Chrome 扩展 | 浏览器控制端 | [kimi.com/features/webbridge](https://kimi.com/features/webbridge) |
| 1688 登录态 | 抓取需登录 | 在 Chrome 登录 1688 |

---

## 🎯 使用

安装后，重启 Claude Code（让 skill 生效），然后说：

> "抓取 1688 待收货订单"

Claude Code 会自动：
1. 打开 1688 待收货订单页
2. 自动翻页抓取所有 27 页（**页数自动检测**）
3. 解析每条订单的物流信息
4. 生成 Excel 表格

输出文件位于 `~/.claude/skills/1688-logistics-scraper/scripts/`：
- `1688待收货物流.xlsx` — 主输出
- `orders_data.json` — 原始数据备份

---

## 📊 输出 Excel 字段

| 序号 | 采购订单号 | 订单状态 | 物流名称 | 物流单号 | 物流更新时间 | 最新物流轨迹 |
|------|------------|----------|----------|----------|--------------|--------------|
| 1 | 5119...1233 | 已签收 | 中通快递 | 79010...1250 | 2026-06-09 15:30:47 | 15:30:47【长沙市】快件已到达... |
| 2 | 5118...0415 | 已发货 | 申通快递 | 77342...7444 | 无 | 无 |

状态值（带颜色高亮）：
- 🟢 已签收 / 🟡 派送中 / 🔵 已揽件 / 🔵 已发货 / 🔴 运输中 / 🟠 物流异常提醒 / ⚪ 无

---

## 🔧 工作原理

### 技术要点

- **Shadow DOM 递归遍历**：1688 订单页使用大量自定义元素（`<order-item>`、`<lu-pagination>`）
- **状态字段精准抓取**：从 `.logistics-status` 元素读取（避免误把"待收货" tab 状态当物流状态）
- **单号非贪婪正则**：避免被后续日期粘连（`790102698612502026-06-09...`）
- **自动分页**：从页面实时读取总页数（不硬编码）
- **自动跳回**：每次启动强制跳回第 1 页（避免上次的页状态）

### 数据流

```
1688 页面 → Kimi WebBridge → 递归 Shadow DOM
        → 解析 6 个字段 → JSON 备份
        → 生成 Excel（带颜色/筛选/冻结）
```

详细技术文档：[references/operations.md](references/operations.md)

---

## 📁 文件结构

```
1688-logistics-scraper/
├── SKILL.md                    # Claude Code skill 入口
├── README.md                   # 本文件
├── requirements.txt            # pip 依赖
├── install.ps1                 # Windows 安装
├── install.sh                  # macOS/Linux 安装
├── references/
│   ├── operations.md           # 1688 技术细节
│   └── excel-format.md         # Excel 格式规范
└── scripts/
    ├── detect_pages.js         # 自动检测总页数
    ├── extract_one_page.js     # 单页提取
    ├── click_next.js           # 翻页
    ├── page_loop.py            # 27 页循环
    └── gen_excel.py            # 生成 Excel
```

---

## 🐛 故障排除

| 问题 | 原因 | 解决 |
|------|------|------|
| `kimi-webbridge` 命令未找到 | 未安装 WebBridge | `irm https://cdn.kimi.com/webbridge/install.ps1 \| iex` |
| 每页只抓 3 条 | session 名不一致 | 重新跑 `page_loop.py` 用正确 `--session` |
| Excel 打开报错 | 缺 openpyxl | `pip install openpyxl` |
| 浏览器无反应 | Chrome 扩展未启用 | 启用 Kimi WebBridge 扩展 |
| 抓不到 1688 数据 | 未登录 | 在 Chrome 登录 1688 |

更多细节见 [SKILL.md](SKILL.md) 的"已知边界"和"session 一致性"章节。

---

## 📜 License

MIT
