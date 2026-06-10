// 检测 1688 待收货订单列表的总页数
// 返回: { totalPages: <number>, totalOrders: <number> }
(()=>{
  function findPagination(root,depth){
    if(depth>15)return null;
    const walker=document.createTreeWalker(root,NodeFilter.SHOW_ELEMENT);
    let node;
    while(node=walker.nextNode()){
      if(node.tagName==='LU-PAGINATION'&&node.shadowRoot)return node;
      if(node.shadowRoot){
        const r=findPagination(node.shadowRoot,depth+1);
        if(r)return r;
      }
    }
    return null;
  }
  const pag=findPagination(document,0);
  if(!pag)return JSON.stringify({totalPages:1,totalOrders:0,err:'no pagination found'});
  const sr=pag.shadowRoot;
  const sp = sr.querySelector('.simple-page');
  const spc = sr.querySelector('.simple-page-count');

  // 优先从 .simple-page 文本提取 "X/ Y" 的 Y
  let totalPages=1;
  if(sp){
    const m=sp.textContent.match(/\/\s*(\d+)/);
    if(m)totalPages=parseInt(m[1]);
  }
  if(totalPages===1 && spc){
    const m=spc.textContent.match(/\/\s*(\d+)/);
    if(m)totalPages=parseInt(m[1]);
  }

  const totalOrders = pag.total || 0;
  return JSON.stringify({totalPages, totalOrders});
})()
