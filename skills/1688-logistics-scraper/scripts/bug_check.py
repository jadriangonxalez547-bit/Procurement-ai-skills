#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
1688 物流抓取 - BUG 体检脚本
- 订单号完整性（19位数字、无重复、无缺失）
- 状态白名单
- 状态-轨迹一致性（"已投递/已放在/投放" 视为"已签收"的同义词）
- 时间格式 YYYY-MM-DD HH:MM:SS
- 单号格式（白名单包括"买家自提"/"卖家自行配送"/"不需要物流"等合法值）
- 空字段检查
"""
import json, os, re, sys
from collections import Counter

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(SCRIPT_DIR, 'orders_data.json')

# ====== 配置：白名单 ======
STATUS_WHITELIST = {
    '运输中', '已揽件', '已发货', '已签收', '派送中', '待收货',
    '物流异常提醒', '无',
}

# 状态-轨迹一致性："已签收"的同义关键词
# 涵盖：直接签收 / 投递 / 放在 / 投放 / 派送 / 暂放快递柜 / 送达 等
SIGNED_KEYWORDS = [
    '签收', '已签收',         # 收件人签收
    '投递', '已投递', '已按址投递',  # 投递
    '放在', '已放在',         # 放在某处
    '投放', '已投放', '放置', '已放置',  # 投放
    '派送', '已派送', '派送成功', '派送至',  # 派送
    '暂放',                    # 快递柜/驿站暂放
    '送达', '已送达', '已顺利送达',  # 送达
]

# 单号白名单（合法值）
EXNO_WHITELIST_PATTERN = re.compile(
    r'^[A-Z0-9]+$'           # 标准快递单号
    r'|^无$'                 # 无单号
    r'|^买家自提$'           # 自提
    r'|^卖家自行配送$'       # 卖家自行配送
    r'|^不需要物流$'         # 不需要物流
    r'|^其他$'               # 其他
)

# 时间格式
TIME_PATTERN = re.compile(r'^\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}$|^无$')


def load_data():
    with open(SRC, 'r', encoding='utf-8') as f:
        return json.load(f)


def check(data):
    oids = [o['orderId'] for o in data]
    status_cnt = Counter(o['status'] for o in data)
    mismatches = []
    bad_status = {s: c for s, c in status_cnt.items() if s not in STATUS_WHITELIST}

    for o in data:
        s = o['status']; t = o['latestTrack'] or ''
        if s == '已签收' and t != '无' and not any(kw in t for kw in SIGNED_KEYWORDS):
            mismatches.append((o['orderId'], s, t[:60]))
        if s == '运输中' and t != '无' and ('签收' in t or '已签收' in t):
            mismatches.append((o['orderId'], s, t[:60]))
        if s == '已发货' and ('本人签收' in t or '顺利送达' in t) and '签收' in t:
            mismatches.append((o['orderId'], s, t[:60] + ' [BUG1]'))

    bad_time = sum(1 for o in data if not TIME_PATTERN.match(o['updateTime'] or ''))
    bad_exno = sum(1 for o in data if not EXNO_WHITELIST_PATTERN.match(o['expressNo'] or ''))
    empty = sum(1 for o in data if not o['orderId'] or not o['expressName'] or not o['expressNo'])

    return {
        'total': len(data),
        'oid_valid': all(len(o) == 19 and o.isdigit() for o in oids),
        'oid_dup': len(oids) - len(set(oids)),
        'oid_missing': sum(1 for o in oids if not o),
        'status_cnt': status_cnt,
        'bad_status': bad_status,
        'mismatches': mismatches,
        'bad_time': bad_time,
        'bad_exno': bad_exno,
        'empty': empty,
    }


def report(r):
    print('=' * 60)
    print(' 1688 物流抓取 - BUG 体检报告')
    print('=' * 60)
    print(f" 抓取总数: {r['total']} 单")
    print()

    def mark(ok):
        return '✅' if ok else '❌'

    print(f"[1] 订单号 19位       {mark(r['oid_valid'] and r['oid_dup']==0 and r['oid_missing']==0)}  "
          f"全部19位={r['oid_valid']}, 重复={r['oid_dup']}, 缺失={r['oid_missing']}")
    print(f"[2] 状态白名单        {mark(not r['bad_status'])}  "
          f"异常={r['bad_status'] if r['bad_status'] else '无'}")
    print(f"[3] 状态-轨迹一致性    {mark(not r['mismatches'])}  矛盾={len(r['mismatches'])}")
    print(f"[4] 时间格式          {mark(r['bad_time']==0)}  异常={r['bad_time']}")
    print(f"[5] 单号格式          {mark(r['bad_exno']==0)}  异常={r['bad_exno']}")
    print(f"[6] 空字段            {mark(r['empty']==0)}  缺失={r['empty']}")

    print()
    print(' 状态分布:')
    for s, n in sorted(r['status_cnt'].items(), key=lambda x: -x[1]):
        bar = '█' * min(n // 2, 60)
        print(f'   {s:15s} {n:3d}  {bar}')

    if r['mismatches']:
        print()
        print(f" 状态-轨迹矛盾详情（前 5 个）:")
        for oid, s, t in r['mismatches'][:5]:
            print(f"   {oid}  {s}  →  {t}")

    # 总评
    all_pass = (r['oid_valid'] and r['oid_dup']==0 and r['oid_missing']==0
                and not r['bad_status'] and not r['mismatches']
                and r['bad_time']==0 and r['bad_exno']==0 and r['empty']==0)
    print()
    print('=' * 60)
    if all_pass:
        print(' 🟢 总评：全部通过，无 BUG')
    else:
        print(f" 🟡 总评：{sum([not r['bad_status'], not r['mismatches'], r['bad_time']==0, r['bad_exno']==0, r['empty']==0, r['oid_valid'] and r['oid_dup']==0 and r['oid_missing']==0])}/6 项通过")
    print('=' * 60)

    return 0 if all_pass else 1


if __name__ == '__main__':
    data = load_data()
    r = check(data)
    sys.exit(report(r))
