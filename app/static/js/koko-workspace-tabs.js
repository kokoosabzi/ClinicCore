/* Koko workspace tabs — lightweight per-session navigation history. */
(() => {
  "use strict";
  const root=document.documentElement;
  const path=window.location.pathname;
  if(path==="/login"||path==="/") return;
  const host=document.getElementById("koko-workspace-tabs");
  if(!host) return;
  const storageKey="cliniccore.koko.tabs.v1";
  const labels=[
    [/^\/dashboard$/,"داشبورد"],
    [/^\/patients(?:\/new)?$/,"بیماران"],
    [/^\/patients\/\d+$/,"پرونده بیمار"],
    [/^\/appointments(?:\/new)?$/,"نوبت‌ها"],
    [/^\/appointments\/\d+\/reschedule$/,"تغییر نوبت"],
    [/^\/financial/,"امور مالی"],
    [/^\/messages/,"پیام‌ها"],
    [/^\/users/,"کاربران"],
    [/^\/settings/,"تنظیمات"]
  ];
  const labelFor=(p)=>{const match=labels.find(([re])=>re.test(p));return match?match[1]:(document.querySelector("main h1,main h2")?.textContent?.trim()||document.title||"صفحه");};
  const read=()=>{try{const value=JSON.parse(sessionStorage.getItem(storageKey)||"[]");return Array.isArray(value)?value.filter(x=>x&&typeof x.path==="string"&&typeof x.label==="string"):[]}catch{return[]}};
  let tabs=read();
  if(!tabs.some(x=>x.path===path))tabs.push({path,label:labelFor(path)});
  tabs=tabs.slice(-8);
  const save=()=>{try{sessionStorage.setItem(storageKey,JSON.stringify(tabs))}catch{}};
  const render=()=>{
    host.replaceChildren();
    tabs.forEach(tab=>{
      const item=document.createElement("div");
      item.className="koko-tab"+(tab.path===path?" active":"");
      const link=document.createElement("a");link.href=tab.path;link.textContent=tab.label;link.setAttribute("aria-current",tab.path===path?"page":"false");
      const close=document.createElement("button");close.type="button";close.className="koko-tab-close";close.textContent="×";close.setAttribute("aria-label","بستن "+tab.label);
      close.addEventListener("click",()=>{
        const index=tabs.findIndex(x=>x.path===tab.path);
        tabs=tabs.filter(x=>x.path!==tab.path);
        if(tab.path===path){const next=tabs[Math.min(index,tabs.length-1)]||{path:"/dashboard"};save();window.location.assign(next.path);return}
        save();render();
      });
      item.append(link,close);host.append(item);
    });
    save();
  };
  render();
  document.addEventListener("click",event=>{
    const link=event.target.closest("a[href]");
    if(!link||link.origin!==location.origin||link.target==="_blank"||event.defaultPrevented||event.button!==0||event.metaKey||event.ctrlKey||event.shiftKey||event.altKey)return;
    const next=new URL(link.href);
    if(next.pathname==="/login"||next.pathname==="/logout"||next.pathname.startsWith("/print/"))return;
    if(!tabs.some(x=>x.path===next.pathname))tabs.push({path:next.pathname,label:labelFor(next.pathname)});
    tabs=tabs.slice(-8);save();
  });
})();
