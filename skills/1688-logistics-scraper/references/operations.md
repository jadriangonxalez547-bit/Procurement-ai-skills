# 1688 页面技术细节

## 页面 URL

```
https://air.1688.com/app/ctf-page/trade-order-list/buyer-order-list.html?tradeStatus=waitbuyerreceive&spm=a360q.31656570.topmenu.dmyorder&page=1&pageSize=10
```

参数说明：
- `tradeStatus=waitbuyerreceive` → 待收货 tab
- `pageSize=10` → 每页 10 条
- 共 27 页（用户共 270 单左右）

## Shadow DOM 结构

1688 订单列表使用大量 Shadow DOM 自定义元素。

### 关键自定义元素

| 元素 | 说明 | 真实内容位置 |
|------|------|-------------|
| `<order-item>` | 单个订单卡片 | `shadowRoot` |
| `<lu-pagination>` | 分页控件 | `shadowRoot` |

### 递归遍历所有 `<order-item>`

```javascript
function findOrderItems(root, depth, items) {
  if (depth > 15) return;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
  let node;
  while (node = walker.nextNode()) {
    if (node.tagName === 'ORDER-ITEM' && node.shadowRoot) {
      items.push(node);
    }
    if (node.shadowRoot) {
      findOrderItems(node.shadowRoot, depth + 1, items);
    }
  }
}
```

### 遍历 `<lu-pagination>` 找翻页按钮

```javascript
function findPagination(root, depth) {
  if (depth > 15) return null;
  const walker = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
  let node;
  while (node = walker.nextNode()) {
    if (node.tagName === 'LU-PAGINATION' && node.shadowRoot) {
      return node;
    }
    if (node.shadowRoot) {
      const r = findPagination(node.shadowRoot, depth + 1);
      if (r) return r;
    }
  }
  return null;
}
```

按钮 class：
- 上一页：`.ui-page-prev`
- 下一页：`.ui-page-next`

## 6 个状态值

| 状态 | 含义 | 来源 |
|------|------|------|
| 已签收 | 快递已签收 | `.logistics-status` |
| 派送中 | 快递员派送中 | `.logistics-status`（但实际页面很少返回此值） |
| 已发货 | 商家已发货 | `.logistics-status` |
| 已揽件 | 快递员已揽件 | `.logistics-status` |
| 运输中 | 快件运输途中 | `.logistics-status` |
| 待收货 | 订单级 tab 状态 | `.order-status`（**不要用作物流状态**） |

⚠️ 特殊值：`物流异常提醒` —— 出现于"退回签收"等异常情况

## 关键 DOM 元素

| Class | 内容 | 用途 |
|-------|------|------|
| `.logistics-status` | "已签收"/"已发货"/... | **物流状态（主）** |
| `.order-status` | "待收货" | 订单级 tab 状态（**忽略**） |
| `.entry-status-label` | "已发货" | 条目标签（统一值，不区分签收） |
| `.simple-page` | "1/ 27" | 当前页/总页数 |

## 数据提取正则

### 订单号
```javascript
// 在文本中找"订单号"标签后的 15-22 位数字
for (let i = 0; i < lines.length - 1; i++) {
  if (lines[i] === '订单号' || lines[i].indexOf('订单号') >= 0) {
    const m = lines[i + 1].match(/^(\d{15,22})$/);
    if (m) { orderId = m[1]; break; }
  }
}
```

### 物流名称和单号
第一行格式：`物流名：单号[日期时间][轨迹]`

```javascript
// 物流名支持中英文，后缀可选
const em = firstLine.match(/^([一-鿿A-Z]+(?:快递|速运|速递|快运|邮政|物流)?)\s*[：:]\s*(.+)$/);

// 特殊：买家自提
const om = firstLine.match(/^(其他)\s*[：:]\s*(.+)$/);
```

### 单号提取（关键！）
```javascript
// 非贪婪正则，遇到日期或时间格式立即停止
const noMatch = rawNo.match(/^([A-Z0-9]+?)(?=\d{4}-\d{2}-\d{2}|\d{2}:\d{2}:\d{2}|【|\[|$)/);
```

**反例**：`790102698612502026-06-09...` 
- 单号是 `79010269861250`（14 位）
- 后面 `2026-06-09` 是日期
- 贪婪正则会把整段都匹配成单号

### 物流轨迹
```javascript
// 格式：HH:MM:SS + 【地点】 + 事件描述
const tracks = text.match(/(\d{2}:\d{2}:\d{2})\s*[【\[]([^】\]]+)[】\]]\s*([^\n]+)/g);
```

## 已知陷阱

| 陷阱 | 解决方案 |
|------|---------|
| 单号后紧跟日期 | 非贪婪正则 `^([A-Z0-9]+?)(?=...)` |
| 物流名称简写"优速" | 后缀 `?(?:快递\|速运\|物流)?` |
| 无轨迹订单 | 状态显示"已发货"，轨迹显示"无" |
| 买家自提 | 物流名"其他"，单号"买家自提" |
| 分页在 shadow DOM | 递归 findPagination |
| "已到达"被误识别 | keyword 排除"到达"，归为"运输中" |
| ".logistics-status"返回"待收货" | 显式排除 `if(t && t!=='待收货')` |

## 状态识别逻辑（按优先级）

```javascript
// 1. 主：抓取 .logistics-status 元素
const lsEl = allEls.find(e => /(^|\s)logistics-status(\s|$)/.test(e.className));
if (lsEl) {
  const t = (lsEl.textContent || '').trim();
  if (t && t !== '待收货') {
    status = t;  // 接受任何值，包括"物流异常提醒"
  }
}

// 2. 兜底1：从轨迹文字推断
const statusKeywords = [
  { kw: '已签收', status: '已签收' },
  { kw: '已由',   status: '已签收' },
  { kw: '派送',   status: '派送中' },
  { kw: '派件',   status: '派送中' },
  { kw: '已发往', status: '运输中' },
  { kw: '离开',   status: '运输中' },
  { kw: '已揽收', status: '已揽件' },
  { kw: '揽件',   status: '已揽件' },
];

// 3. 兜底2：原状态枚举匹配
const m = text.match(/(运输中|已揽件|已发货|已签收|派送中)/);
```

## 时间戳构造

```javascript
// 物流更新时间 = 轨迹日期 + 轨迹时间
const trackDate = firstLine.match(/(\d{4}-\d{2}-\d{2})/)?.[1];
const trackTime = latestTrack.match(/(\d{2}:\d{2}:\d{2})/)?.[1];
const updateTime = (trackDate && trackTime) ? `${trackDate} ${trackTime}` : '无';
```

## WebBridge API

### navigate
```json
{
  "action": "navigate",
  "args": {
    "url": "...",
    "newTab": true,
    "group_title": "1688物流抓取"
  },
  "session": "1688-logistics"
}
```

### evaluate
```json
{
  "action": "evaluate",
  "args": { "code": "<IIFE 形式的 JS>" },
  "session": "1688-logistics"
}
```

### click
```json
{
  "action": "click",
  "args": { "selector": ".ui-page-next" },
  "session": "1688-logistics"
}
```

## 错误处理

| 现象 | 原因 | 解决 |
|------|------|------|
| `running: false` | 守护进程未启动 | `~/.kimi-webbridge/bin/kimi-webbridge start` |
| `extension_connected: false` | 浏览器扩展断开 | 检查浏览器扩展是否启用 |
| 抓取条数波动 | 1688 实时变化 | 重抓或接受小幅差异 |
| 翻页后只抓到 0 条 | 等待时间不够 | 改 sleep(3) → sleep(4) |
