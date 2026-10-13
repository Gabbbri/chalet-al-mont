const photos=[...document.querySelectorAll('.chalet-gallery a, .room-photo')];const dialog=document.querySelector('.gallery-dialog');let current=0;function showPhoto(i){current=(i+photos.length)%photos.length;const source=photos[current];dialog.querySelector('img').src=source.href;dialog.querySelector('img').alt=source.querySelector('img').alt;dialog.querySelector('.gallery-counter').textContent=`${current+1} / ${photos.length}`;}photos.forEach((a,i)=>a.addEventListener('click',e=>{e.preventDefault();showPhoto(i);dialog.showModal();}));dialog.querySelector('.gallery-close').onclick=()=>dialog.close();dialog.querySelector('.gallery-prev').onclick=()=>showPhoto(current-1);dialog.querySelector('.gallery-next').onclick=()=>showPhoto(current+1);dialog.addEventListener('keydown',e=>{if(e.key==='ArrowLeft'){e.preventDefault();showPhoto(current-1);}if(e.key==='ArrowRight'){e.preventDefault();showPhoto(current+1);}});dialog.addEventListener('click',e=>{if(e.target===dialog)dialog.close();});
// The three collections can be browsed independently, like the Cavallar galleries.
document.querySelectorAll('[data-space-gallery]').forEach(gallery=>{
  const slides=[...gallery.querySelectorAll('.room-photo')];
  const thumbs=[...gallery.querySelectorAll('[data-photo]')];
  let index=0;
  function select(next){
    index=(next+slides.length)%slides.length;
    const selectedImage=slides[index].querySelector('img');
    if(selectedImage.dataset.src){
      if(selectedImage.dataset.srcset)selectedImage.srcset=selectedImage.dataset.srcset;
      selectedImage.src=selectedImage.dataset.src;
      delete selectedImage.dataset.src;delete selectedImage.dataset.srcset;
    }
    slides.forEach((slide,i)=>{slide.hidden=i!==index;slide.tabIndex=i===index?0:-1;});
    thumbs.forEach((thumb,i)=>thumb.setAttribute('aria-pressed',String(i===index)));
    const strip=thumbs[index]?.parentElement;
    if(strip&&strip.scrollWidth>strip.clientWidth)strip.scrollTo({left:thumbs[index].offsetLeft-(strip.clientWidth-thumbs[index].clientWidth)/2,behavior:window.matchMedia('(prefers-reduced-motion: reduce)').matches?'auto':'smooth'});
    gallery.querySelector('.space-count').textContent=`${String(index+1).padStart(2,'0')} / ${String(slides.length).padStart(2,'0')}`;
  }
  gallery.querySelectorAll('[data-step]').forEach(button=>button.addEventListener('click',()=>select(index+Number(button.dataset.step))));
  thumbs.forEach(button=>button.addEventListener('click',()=>select(Number(button.dataset.photo))));
  let touchStart=null;
  gallery.querySelector('.space-slides').addEventListener('touchstart',event=>{touchStart=event.touches.length===1?{x:event.touches[0].clientX,y:event.touches[0].clientY}:null;},{passive:true});
  gallery.querySelector('.space-slides').addEventListener('touchend',event=>{if(!touchStart||!event.changedTouches.length)return;const dx=event.changedTouches[0].clientX-touchStart.x;const dy=event.changedTouches[0].clientY-touchStart.y;touchStart=null;if(Math.abs(dx)>55&&Math.abs(dx)>Math.abs(dy)*1.5)select(index+(dx<0?1:-1));},{passive:true});
  select(0);
  gallery.addEventListener('keydown',event=>{if(event.key==='ArrowLeft'||event.key==='ArrowRight'){event.preventDefault();select(index+(event.key==='ArrowRight'?1:-1));}});
});
