"""1688 订单物流抓取主循环

用法:
  python page_loop.py [--session SESSION_NAME] [--pages auto|N] [--sleep S]

默认:
  --session 1688-logistics
  --pages auto (自动检测总页数)
  --sleep 4

输出:
  <脚本所在目录>/orders_data.json
"""
import json, urllib.request, time, sys, os, argparse

def call(action, code, session):
    payload = json.dumps({'action':action,'args':{'code':code},'session':session}, ensure_ascii=False)
    req = urllib.request.Request('http://127.0.0.1:10086/command',
                                  data=payload.encode('utf-8'),
                                  headers={'Content-Type':'application/json'})
    with urllib.request.urlopen(req, timeout=30) as resp:
        return json.loads(resp.read().decode('utf-8'))

# 解析参数
parser = argparse.ArgumentParser()
parser.add_argument('--session', default='1688-logistics', help='WebBridge session 名')
parser.add_argument('--pages', default='auto', help='总页数（auto=自动检测，N=固定值）')
parser.add_argument('--sleep', type=float, default=4.0, help='每页等待秒数')
args = parser.parse_args()

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
extract_path = os.path.join(SCRIPT_DIR, 'extract_one_page.js')
next_path = os.path.join(SCRIPT_DIR, 'click_next.js')
detect_path = os.path.join(SCRIPT_DIR, 'detect_pages.js')

with open(extract_path, 'r', encoding='utf-8') as f:
    extract_js = f.read()
with open(next_path, 'r', encoding='utf-8') as f:
    next_js = f.read()
with open(detect_path, 'r', encoding='utf-8') as f:
    detect_js = f.read()

SESSION = args.session
SLEEP = args.sleep

# 自动检测总页数
if args.pages == 'auto':
    print(f'🔍 正在自动检测总页数...')
    # 先强制跳回第 1 页（避免上次留下的状态）
    nav_back_js = 'window.location.href = "https://air.1688.com/app/ctf-page/trade-order-list/buyer-order-list.html?tradeStatus=waitbuyerreceive&spm=a360q.31656570.topmenu.dmyorder&page=1&pageSize=10";'
    call('evaluate', nav_back_js, SESSION)
    time.sleep(3)  # 等待页面完全加载
    print(f'   已跳回第 1 页，等待加载...')

    r = call('evaluate', detect_js, SESSION)
    if not r.get('ok'):
        print(f'❌ 检测失败: {r}', file=sys.stderr)
        sys.exit(1)
    raw = r['data']['value']
    info = json.loads(raw) if isinstance(raw, str) else raw
    TOTAL_PAGES = info.get('totalPages', 27)
    total_orders = info.get('totalOrders', 0)
    print(f'   检测到: {total_orders} 单 / {TOTAL_PAGES} 页')
else:
    TOTAL_PAGES = int(args.pages)
    total_orders = '?'
    print(f'📌 使用固定页数: {TOTAL_PAGES}')

print(f'⚙️  配置: session={SESSION}, pages={TOTAL_PAGES}, sleep={SLEEP}s')
print()

all_orders = []

for page in range(1, TOTAL_PAGES + 1):
    # 抓取当前页
    r = call('evaluate', extract_js, SESSION)
    if not r.get('ok'):
        print(f'第{page}页抓取失败: {r}', file=sys.stderr)
        time.sleep(2)
        continue
    raw = r['data']['value']
    items = json.loads(raw) if isinstance(raw, str) else raw
    all_orders.extend(items)
    print(f'第{page:>2}/{TOTAL_PAGES} 页: 抓取 {len(items)} 条 (累计 {len(all_orders)})')

    if page >= TOTAL_PAGES:
        break

    # 翻页
    r2 = call('evaluate', next_js, SESSION)
    if not r2.get('ok'):
        print(f'第{page}页翻页失败: {r2}', file=sys.stderr)
        break
    time.sleep(SLEEP)

# 保存到脚本所在目录
out_path = os.path.join(SCRIPT_DIR, 'orders_data.json')
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_orders, f, ensure_ascii=False, indent=2)
print(f'\n✅ 共抓取 {len(all_orders)} 条订单，已保存到: {out_path}')
