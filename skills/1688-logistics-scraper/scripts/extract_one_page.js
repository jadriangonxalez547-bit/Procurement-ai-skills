(()=>{
function findOrderItems(root,depth,items){
  if(depth>15)return;
  const walker=document.createTreeWalker(root,NodeFilter.SHOW_ELEMENT);
  let node;
  while(node=walker.nextNode()){
    if(node.tagName==='ORDER-ITEM'&&node.shadowRoot){items.push(node);}
    if(node.shadowRoot){findOrderItems(node.shadowRoot,depth+1,items);}
  }
}
function collectAll(root, out){
  const w = document.createTreeWalker(root, NodeFilter.SHOW_ELEMENT);
  let n;
  while(n=w.nextNode()){
    out.push(n);
    if(n.shadowRoot) collectAll(n.shadowRoot, out);
  }
}

const items=[];
findOrderItems(document,0,items);

const NL=String.fromCharCode(10);
const out=[];
for(const item of items){
  const allEls=[];
  collectAll(item.shadowRoot, allEls);
  const text=item.shadowRoot.textContent;
  const lines=text.split(NL).map(l=>l.trim()).filter(l=>l.length>0);

  // 订单号
  let orderId='无';
  for(let i=0;i<lines.length-1;i++){
    if(lines[i]==='订单号'||lines[i].indexOf('订单号')>=0){
      const m=lines[i+1].match(/^(\d{15,22})$/);
      if(m){orderId=m[1];break;}
    }
  }
  if(orderId==='无'){const m=text.match(/\b(\d{18,22})\b/);if(m)orderId=m[1];}

  // 物流名称/单号（第一行）
  const firstLine=lines.length>0?lines[0]:'';
  let expressName='无',expressNo='无',trackDate='';
  const em=firstLine.match(/^([一-鿿A-Z]+(?:快递|速运|速递|快运|邮政|物流)?)\s*[：:]\s*(.+)$/);
  const om=firstLine.match(/^(其他)\s*[：:]\s*(.+)$/);
  if(em){
    expressName=em[1];
    let raw=em[2];
    const nm=raw.match(/^([A-Z0-9]+?)(?=\d{4}-\d{2}-\d{2}|\d{2}:\d{2}:\d{2}|【|\[|$)/);
    if(nm)expressNo=nm[1];
    else{const n=raw.match(/^(\d+)/);expressNo=n?n[1]:raw;}
    const dm=firstLine.match(/(\d{4}-\d{2}-\d{2})/);if(dm)trackDate=dm[1];
  }else if(om){expressName=om[1];expressNo=om[2];}

  // ===== 状态识别：优先用 .logistics-status =====
  let status='无';
  // 主：抓取 .logistics-status 元素（页面 UI 上箭头指向的小字）
  const lsEl = allEls.find(e => typeof e.className==='string' && /(^|\s)logistics-status(\s|$)/.test(e.className));
  if(lsEl){
    const t=(lsEl.textContent||'').trim();
    if(t && t!=='待收货'){  // 排除 tab 状态
      status=t;
    }
  }
  // 兜底1：从轨迹文字推断
  if(status==='无'){
    const statusKeywords=[
      {kw:'已签收',status:'已签收'},{kw:'已由',status:'已签收'},{kw:'本人签收',status:'已签收'},
      {kw:'退回签收',status:'已签收'},{kw:'已代收',status:'已签收'},{kw:'已送达',status:'已签收'},{kw:'已投递',status:'已签收'},
      {kw:'正在派件',status:'派送中'},{kw:'派送',status:'派送中'},{kw:'派件',status:'派送中'},
      {kw:'已发往',status:'运输中'},{kw:'离开',status:'运输中'},
      {kw:'已揽收',status:'已揽件'},{kw:'被揽收',status:'已揽件'},{kw:'已取件',status:'已揽件'},{kw:'揽件',status:'已揽件'},{kw:'已揽',status:'已揽件'}
    ];
    for(const sk of statusKeywords){
      if(text.indexOf(sk.kw)>=0){status=sk.status;break;}
    }
  }
  // 兜底2：原状态枚举匹配（排除"待收货"作为物流状态）
  if(status==='无'){
    const m=text.match(/(运输中|已揽件|已发货|已签收|派送中)/);
    if(m)status=m[1];
  }

  // 轨迹
  const tracks=text.match(/(\d{2}:\d{2}:\d{2})\s*[【\[]([^】\]]+)[】\]]\s*([^\n]+)/g);
  let latestTrack='无',latestTrackTime='无',updateTime='无';
  if(tracks&&tracks.length>0){
    latestTrack=tracks[0].trim();
    const tm=latestTrack.match(/(\d{2}:\d{2}:\d{2})/);
    latestTrackTime=tm?tm[1]:'无';
    if(trackDate&&latestTrackTime!=='无')updateTime=trackDate+' '+latestTrackTime;
  }

  const shortTrack = latestTrack === '无' ? '无' : (latestTrack.length>200 ? latestTrack.substring(0,200)+'...' : latestTrack);
  out.push({orderId,status,expressName,expressNo,updateTime,latestTrack:shortTrack});
}
return JSON.stringify(out);
})()