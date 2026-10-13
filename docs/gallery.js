const reducedMotion = () => window.matchMedia('(prefers-reduced-motion: reduce)').matches;
async function ready(image) {
  if (image.dataset.src) {
    if (image.dataset.srcset) image.srcset = image.dataset.srcset;
    image.src = image.dataset.src;
    delete image.dataset.src; delete image.dataset.srcset;
  }
  try { await image.decode(); } catch { /* Keep controls usable after a failed image download. */ }
}
async function slideAcross(outgoing, incoming, direction) {
  incoming.hidden = false;
  if (reducedMotion()) return;
  // The incoming slide shares the outgoing slide's viewport without changing its height.
  incoming.classList.add('slide-incoming');
  const options = {duration:320, easing:'cubic-bezier(.22,.68,.25,1)', fill:'both'};
  const animations = [
    outgoing.animate([{transform:'translateX(0)'},{transform:`translateX(${-direction*100}%)`}], options),
    incoming.animate([{transform:`translateX(${direction*100}%)`},{transform:'translateX(0)'}], options)
  ];
  await Promise.all(animations.map(animation => animation.finished.catch(() => {})));
  // Hide before releasing animation styles, avoiding a flash of the previous photograph.
  outgoing.hidden = true;
  incoming.classList.remove('slide-incoming');
  animations.forEach(animation => animation.cancel());
}
function swipe(surface, change) {
  let start = null;
  let blockClickUntil = 0;
  surface.addEventListener('touchstart', event => {
    start = event.touches.length===1 ? {x:event.touches[0].clientX,y:event.touches[0].clientY} : null;
  }, {passive:true});
  surface.addEventListener('touchcancel', () => {start=null;}, {passive:true});
  surface.addEventListener('touchend', event => {
    if (!start || !event.changedTouches.length) return;
    const dx = event.changedTouches[0].clientX-start.x, dy = event.changedTouches[0].clientY-start.y;
    start=null;
    if (Math.abs(dx)>45 && Math.abs(dx)>Math.abs(dy)*1.5) {
      blockClickUntil=Date.now()+450;
      change(dx<0?1:-1);
    }
  }, {passive:true});
  surface.addEventListener('click', event => {
    if(Date.now()<blockClickUntil){event.preventDefault();event.stopPropagation();}
  }, true);
}
const photos = [...document.querySelectorAll('.chalet-gallery a, .room-photo')];
const dialog = document.querySelector('.gallery-dialog');
const view = dialog.querySelector('.gallery-view');
let current = 0, lightboxBusy = false;
function imageFor(index) {
  const image = document.createElement('img');
  image.src = photos[index].href;
  image.alt = photos[index].querySelector('img').alt;
  return image;
}
function counter() {dialog.querySelector('.gallery-counter').textContent=`${current+1} / ${photos.length}`;}
async function showPhoto(next, direction=1) {
  if(lightboxBusy)return;
  const index=(next+photos.length)%photos.length;
  if(index===current)return;
  lightboxBusy=true;
  const outgoing=view.querySelector('img'), incoming=imageFor(index);
  incoming.hidden=true;
  view.append(incoming);
  await ready(incoming);
  await slideAcross(outgoing,incoming,direction);
  outgoing.remove();incoming.hidden=false;current=index;counter();lightboxBusy=false;
}
photos.forEach((anchor,index)=>anchor.addEventListener('click',event=>{
  event.preventDefault();
  if(lightboxBusy)return;
  current=index;view.replaceChildren(imageFor(index));counter();dialog.showModal();
}));
dialog.querySelector('.gallery-close').onclick=()=>dialog.close();
dialog.querySelector('.gallery-prev').onclick=()=>showPhoto(current-1,-1);
dialog.querySelector('.gallery-next').onclick=()=>showPhoto(current+1,1);
dialog.addEventListener('keydown',event=>{
  if(event.key==='ArrowLeft'||event.key==='ArrowRight'){
    event.preventDefault();const step=event.key==='ArrowRight'?1:-1;showPhoto(current+step,step);
  }
});
dialog.addEventListener('click',event=>{if(event.target===dialog)dialog.close();});
swipe(view,step=>showPhoto(current+step,step));

document.querySelectorAll('[data-space-gallery]').forEach(gallery=>{
  const slides=[...gallery.querySelectorAll('.room-photo')];
  const thumbs=[...gallery.querySelectorAll('[data-photo]')];
  let index=0, busy=false;
  function update() {
    slides.forEach((slide,i)=>{slide.hidden=i!==index;slide.tabIndex=i===index?0:-1;});
    thumbs.forEach((thumb,i)=>thumb.setAttribute('aria-pressed',String(i===index)));
    const strip=thumbs[index]?.parentElement;
    if(strip&&strip.scrollWidth>strip.clientWidth)strip.scrollTo({left:thumbs[index].offsetLeft-(strip.clientWidth-thumbs[index].clientWidth)/2,behavior:reducedMotion()?'auto':'smooth'});
    gallery.querySelector('.space-count').textContent=`${String(index+1).padStart(2,'0')} / ${String(slides.length).padStart(2,'0')}`;
  }
  async function select(next,direction=next>index?1:-1) {
    const target=(next+slides.length)%slides.length;
    if(busy||target===index)return;
    busy=true;
    await ready(slides[target].querySelector('img'));
    slides[target].tabIndex=-1;
    await slideAcross(slides[index],slides[target],direction);
    index=target;update();busy=false;
  }
  gallery.querySelectorAll('[data-step]').forEach(button=>button.addEventListener('click',()=>{
    const step=Number(button.dataset.step);select(index+step,step);
  }));
  thumbs.forEach(button=>button.addEventListener('click',()=>select(Number(button.dataset.photo))));
  swipe(gallery.querySelector('.space-slides'),step=>select(index+step,step));
  gallery.addEventListener('keydown',event=>{
    if(event.key==='ArrowLeft'||event.key==='ArrowRight'){
      event.preventDefault();const step=event.key==='ArrowRight'?1:-1;select(index+step,step);
    }
  });
  update();
  // Fetch neighbouring inline images only when their collection approaches the viewport.
  const observer=new IntersectionObserver(entries=>{
    if(entries.some(entry=>entry.isIntersecting)){
      ready(slides[1]?.querySelector('img')||slides[0].querySelector('img'));
      observer.disconnect();
    }
  },{rootMargin:'200px'});
  observer.observe(gallery);
});
