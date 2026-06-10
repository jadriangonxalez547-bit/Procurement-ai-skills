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
  if(!pag)return JSON.stringify({ok:false,reason:'no pag'});
  const sr=pag.shadowRoot;
  const next=sr.querySelector('.ui-page-next');
  if(!next)return JSON.stringify({ok:false,reason:'no next btn'});
  if(next.disabled)return JSON.stringify({ok:false,reason:'disabled'});
  next.click();
  return JSON.stringify({ok:true});
})()