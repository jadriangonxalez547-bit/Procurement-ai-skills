---
name: 1688-logistics-scraper
description: 抓取 1688 待收货订单物流信息并生成 Excel。当用户说"抓取 1688 待收货"、"导出 1688 物流"、"1688 订单物流"时使用。
---

# 1688 待收货订单物流抓取

通过 Kimi WebBridge 操作用户真实浏览器，抓取 1688 待收货 tab 下所有订单的物流信息，并生成 Excel 表格。

## 触发场景

- 用户说"抓取 1688 待收货订单物流"
- 用户说"导出 1688 订单到 Excel"
- 用户提供 1688 订单页面 URL

## 前置条件

- Kimi WebBridge 已安装（`~/.kimi-webbridge/bin/kimi-webbridge status` 返回 `running:true, extension_connected:true`）
- 用户浏览器已登录 1688

## 完整流程

### 1. 健康检查
```bash
~/.kimi-webbridge/bin/kimi-webbridge status
```
- 正常：`running:true, extension_connected:true` → 继续
- 异常：参考 [operations.md 健康检查章节]

### 2. 打开 1688 待收货页面
```bash
curl -s -X POST http://127.0.0.1:10086/command \
  -H 'Content-Type: application/json' \
  -d '{
    "action":"navigate",
    "args":{
      "url":"https://air.1688.com/app/ctf-page/trade-order-list/buyer-order-list.html?tradeStatus=waitbuyerreceive&spm=a360q.31656570.topmenu.dmyorder&page=1&pageSize=10",
      "newTab":true,
      "group_title":"1688物流抓取"
    },
    "session":"1688-logistics"
  }'
```
- 等待 5 秒加载

### 3. 抓取全部分页数据
```bash
python <skill-dir>/scripts/page_loop.py --session <当前session名>
```
- **必须传入 `--session`**，与步骤 2 的 session 名一致
- `--pages auto`（默认）：自动检测总页数（**强烈推荐**）
- `--pages N`：手动指定总页数
- `--sleep 4`：每页等待秒数（默认 4）
- 抓取过程**自动跳回第 1 页**，避免上次留下的状态
- 输出：`<skill-dir>/scripts/orders_data.json`

### 4. 生成 Excel
```bash
python <skill-dir>/scripts/gen_excel.py
```
- 输出：`<skill-dir>/scripts/1688待收货物流.xlsx`
- 包含 7 列：序号、采购订单号、订单状态、物流名称、物流单号、物流更新时间、最新物流轨迹

### 5. 告知用户文件位置
向用户报告：
- 抓取总数
- 状态分布
- Excel 文件完整路径
- JSON 备份路径

## 文件清单

| 文件 | 用途 |
|------|------|
| `scripts/extract_one_page.js` | 单页订单提取（核心） |
| `scripts/click_next.js` | 点击下一页按钮 |
| `scripts/page_loop.py` | 27 页循环抓取 |
| `scripts/gen_excel.py` | 生成 Excel 表格 |
| `references/operations.md` | 1688 技术细节（DOM 结构、正则、状态规则） |
| `references/excel-format.md` | Excel 格式规范 |

## 关键提示

- **每页等待 4 秒**：保证翻页后页面完全加载
- **状态从 `.logistics-status` 元素读取**：不要用文本搜索（会误把"待收货"当状态）
- **订单号在"订单号"标签后**：19-20 位数字
- **单号提取用非贪婪正则**：避免被后续日期粘连

详细技术规则见 [references/operations.md](references/operations.md)。

## 已知边界

- 已签收但未点"确认收货"按钮的订单，仍会出现在"待收货"tab
- 1688 页面是实时的，抓取期间订单数可能小幅波动
- 总订单数每次抓取可能少 1-3 条（已签收订单自动从 tab 消失）

## 重要：session 一致性

调用 skill 时使用的 WebBridge session 名必须全程一致。如果步骤 2 用 `--session 1688-test-skill`，那么步骤 3 的 `page_loop.py` 也必须用 `--session 1688-test-skill`。**否则会抓到错误 tab 的数据**（如：每页只 3 条）。

## 自动检测总页数

`page_loop.py` 会自动从页面读取总页数（默认 `--pages auto`）：
- 总订单数会随时间减少（已签收订单自动从 tab 消失）
- 总页数 = ceil(总订单数 / 10)
- 所以每次抓取的页数可能不同，**不要硬编码 27**

## 重抓

如需重抓：
1. 重新执行步骤 2-4
2. `orders_data.json` 会被覆盖
3. `1688待收货物流.xlsx` 会被覆盖
