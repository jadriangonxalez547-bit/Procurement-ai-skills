# Procurement AI Skills

采购与供应链场景 AI Skills 集合。

本仓库用于沉淀和管理可复用的 AI Skills、工作流、提示词和自动化方案，帮助提升采购、供应商管理、对账、订单跟踪和数据处理效率。

## 当前 Skills

### 📦 [1688 Logistics Scraper](skills/1688-logistics-scraper/)

批量抓取 1688 订单物流状态和最新物流轨迹，生成 Excel 表格。

> ✅ **已实现** — 一键安装可用

### 📊 [Supplier Reconciliation](skills/supplier-reconciliation/)

供应商送货单与我司入库单智能对账。

> 🚧 规划中

### 🛃 [Customs Declaration Checker](skills/customs-declaration-checker/)

Excel 与 PDF 报关单智能核对。

> 🚧 规划中

## 规划中

* Supplier Management Assistant
* Procurement Workflow Assistant
* AI Training Assistant
* Feishu Knowledge Assistant

## 适用场景

* 采购管理
* 供应商管理
* 对账审核
* 订单跟踪
* AI 自动化办公

## 快速开始

每个 skill **独立安装**。进入对应 skill 目录查看安装说明：

```bash
# 以 1688 物流抓取为例
# 🪟 Windows
irm https://raw.githubusercontent.com/jadriangonxalez547-bit/Procurement-ai-skills/main/skills/1688-logistics-scraper/install.ps1 | iex

# 🍎 macOS / 🐧 Linux
curl -fsSL https://raw.githubusercontent.com/jadriangonxalez547-bit/Procurement-ai-skills/main/skills/1688-logistics-scraper/install.sh | bash
```

安装后，重启 Claude Code，对它说：

> "抓取 1688 待收货订单"

## 仓库结构

```
Procurement-ai-skills/
├── README.md                       # 本文件
├── LICENSE                         # MIT
├── .gitignore
│
└── skills/
    ├── 1688-logistics-scraper/     # ✅ 已实现
    │   ├── SKILL.md
    │   ├── README.md
    │   ├── requirements.txt
    │   ├── install.ps1 / install.sh
    │   ├── references/
    │   └── scripts/
    │
    ├── supplier-reconciliation/    # 🚧 占位
    │   ├── SKILL.md
    │   └── README.md
    │
    └── customs-declaration-checker/# 🚧 占位
        ├── SKILL.md
        └── README.md
```

## 如何贡献新 Skill

1. 在 `skills/` 下创建新目录，命名格式 `kebab-case-name`
2. 创建 `SKILL.md`（含 YAML frontmatter）+ `README.md`
3. 实现 `scripts/`、`references/` 等
4. 编写 `install.ps1` + `install.sh` 一键安装脚本
5. 提交 PR

参考 [1688 Logistics Scraper](skills/1688-logistics-scraper/) 的完整结构。

## License

MIT © Jadrian

## Author

Jadrian
