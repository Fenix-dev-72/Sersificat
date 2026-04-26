/* ==========================================
   MEDIAPARK — app.js  (shared across pages)
   ========================================== */

const API   = "https://mediapark.zapto.org/api/v1";
const MEDIA = "https://mediapark.zapto.org";

const state = {
    products: [], filteredProducts: [], categories: [],
    currentCategory: null,
    cart:     JSON.parse(localStorage.getItem('mp_cart')     || '[]'),
    wishlist: JSON.parse(localStorage.getItem('mp_wishlist') || '[]'),
    access:   localStorage.getItem('mp_access')   || null,
    refresh:  localStorage.getItem('mp_refresh')  || null,
    username: localStorage.getItem('mp_username') || null,
    sliderTimer: null, sliderIndex: 0, totalSlides: 0, otpTimer: null,
};

/* ── PRICE: 1 500 000 so'm (no decimals, space-separated) ── */
function fmt(n){
    const s = Math.round(Number(n)).toString();
    return s.replace(/\B(?=(\d{3})+(?!\d))/g," ") + " so'm";
}
function fmtNum(n){
    return Math.round(Number(n)).toString().replace(/\B(?=(\d{3})+(?!\d))/g," ");
}

function imgUrl(p){ return p?(p.startsWith('http')?p:MEDIA+p):'https://placehold.co/200x200?text=?'; }
function escStr(s){ return String(s).replace(/'/g,"\\'").replace(/"/g,'\\"'); }
function isLoggedIn(){ return !!state.access; }

/* ── TOKENS ── */
function saveTokens(access,refresh,username){
    state.access=access; state.refresh=refresh; state.username=username;
    localStorage.setItem('mp_access',access);
    localStorage.setItem('mp_refresh',refresh);
    localStorage.setItem('mp_username',username);
}
function clearTokens(){
    state.access=state.refresh=state.username=null;
    ['mp_access','mp_refresh','mp_username'].forEach(k=>localStorage.removeItem(k));
}
async function doRefreshToken(){
    if(!state.refresh) return null;
    try{
        const r=await fetch(`${API}/token/refresh/`,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({refresh:state.refresh})});
        if(!r.ok){clearTokens();updateNavAuth();return null;}
        const d=await r.json();
        state.access=d.access; localStorage.setItem('mp_access',d.access);
        if(d.refresh){state.refresh=d.refresh;localStorage.setItem('mp_refresh',d.refresh);}
        return d.access;
    }catch{return null;}
}
async function authFetch(url,opts={}){
    if(!opts.headers) opts.headers={};
    opts.headers['Content-Type']=opts.headers['Content-Type']||'application/json';
    if(state.access) opts.headers['Authorization']='Bearer '+state.access;
    let r=await fetch(url,opts);
    if(r.status===401&&state.refresh){
        const na=await doRefreshToken();
        if(na){opts.headers['Authorization']='Bearer '+na;r=await fetch(url,opts);}
    }
    return r;
}

/* ── TOAST ── */
function toast(msg,type='success'){
    let c=document.getElementById('toast-container');
    if(!c){c=document.createElement('div');c.id='toast-container';c.className='toast-container';document.body.appendChild(c);}
    const icons={success:'✅',error:'❌',info:'ℹ️'};
    const t=document.createElement('div');
    t.className='toast '+type;
    t.innerHTML='<span>'+(icons[type]||'✅')+'</span><span>'+msg+'</span>';
    c.appendChild(t);
    setTimeout(()=>t.remove(),3100);
}

/* ── SAVE ── */
function saveCart(){localStorage.setItem('mp_cart',JSON.stringify(state.cart));}
function saveWishlist(){localStorage.setItem('mp_wishlist',JSON.stringify(state.wishlist));}

function updateBadges(){
    const ct=state.cart.reduce((s,i)=>s+i.qty,0);
    document.querySelectorAll('.cart-count').forEach(el=>el.textContent=ct>0?ct:'');
    document.querySelectorAll('.wishlist-count').forEach(el=>el.textContent=state.wishlist.length>0?state.wishlist.length:'');
}
function updateNavAuth(){
    const lbl=document.getElementById('profile-label');
    if(lbl) lbl.textContent=state.username||'Kirish';
}

/* ── CART ── */
window.addToCart=function(id,name,price,img){
    toast('🔧 Savatcha tizimi hali ishlab chiqilmoqda','info');
};
window.changeQty=function(id,delta){
    const it=state.cart.find(i=>i.id===id);if(!it)return;
    it.qty+=delta;
    if(it.qty<=0)state.cart=state.cart.filter(i=>i.id!==id);
    saveCart();updateBadges();
    if(typeof renderCartPage==='function')renderCartPage();
    if(typeof renderCartDrawer==='function')renderCartDrawer();
};
window.removeFromCart=function(id){
    state.cart=state.cart.filter(i=>i.id!==id);
    saveCart();updateBadges();
    if(typeof renderCartPage==='function')renderCartPage();
    if(typeof renderCartDrawer==='function')renderCartDrawer();
};

/* Cart Drawer (index page) */
function renderCartDrawer(){
    const c=document.getElementById('cart-items');
    const f=document.getElementById('cart-footer');
    if(!c)return;
    if(!state.cart.length){
        c.innerHTML='<div class="cart-empty"><svg width="64" height="64" viewBox="0 0 24 24" fill="none" stroke="#ccc" stroke-width="1.5"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg><p>Savatcha bosh</p></div>';
        if(f)f.style.display='none';return;
    }
    const total=state.cart.reduce((s,i)=>s+i.price*i.qty,0);
    c.innerHTML=state.cart.map(item=>'<div class="cart-item"><img src="'+imgUrl(item.img)+'" alt="'+item.name+'" onerror="this.src=\'https://placehold.co/60?text=?\'">'
        +'<div class="cart-item-info"><div class="cart-item-name" title="'+item.name+'">'+item.name+'</div>'
        +'<div class="cart-item-price">'+fmt(item.price*item.qty)+'</div>'
        +'<div class="cart-item-controls"><button class="qty-btn" onclick="changeQty('+item.id+',-1)">−</button>'
        +'<span class="qty-val">'+item.qty+'</span>'
        +'<button class="qty-btn" onclick="changeQty('+item.id+',1)">+</button></div></div>'
        +'<span class="remove-item" onclick="removeFromCart('+item.id+')">✕</span></div>').join('');
    if(f){f.style.display='block';const te=document.getElementById('cart-total-price');if(te)te.textContent=fmt(total);}
}
function openCartDrawer(){
    toast('🔧 Savatcha tizimi hali ishlab chiqilmoqda','info');
}
function closeCartDrawer(){
    document.getElementById('cart-overlay')?.classList.remove('open');
    document.getElementById('cart-drawer')?.classList.remove('open');
    document.body.style.overflow='';
}

/* ── WISHLIST ── */
window.toggleWishlist=function(id,name){
    toast('🔧 Sevimlilar tizimi hali ishlab chiqilmoqda','info');
};

/* ── HERO SLIDER ── */
function renderHeroSection(ads,dailyProd){
    const hw=document.getElementById('hero-wrapper');if(!hw)return;
    let slider='';
    if(ads&&ads.length>0){
        const slides=ads.map((a,i)=>'<div class="ad-slide '+(i===0?'active':'')+'"><img src="'+MEDIA+a.image+'" alt="Promo" loading="lazy"></div>').join('');
        const dots=ads.map((_,i)=>'<button class="slider-dot '+(i===0?'active':'')+'" onclick="goToSlide('+i+')"></button>').join('');
        slider='<div class="slider-container">'+slides+'<div class="slider-dots">'+dots+'</div></div>';
        state.totalSlides=ads.length;startSlider();
    }else{
        slider='<div class="slider-container"><div class="ad-slide active"><div class="slider-placeholder"><div class="promo-tag">Chegirmalar Festivali</div><h2>Yillik Katta<br>Aksiya!</h2><p>Eng yaxshi texnikalar — eng yaxshi narxlarda</p><button class="slider-cta" onclick="filterByCategory(null)">Mahsulotlarni korish</button></div></div></div>';
    }
    let daily='';
    if(dailyProd&&dailyProd.image&&dailyProd.image.length>0){
        daily='<div class="daily-container"><div class="daily-card"><div class="daily-header"><h4>🔥 Kun mahsuloti</h4><div class="timer" id="daily-timer">--:--:--</div></div><div class="daily-body"><img src="'+imgUrl(dailyProd.image[0]?.image)+'" alt="'+dailyProd.name+'" onerror="this.src=\'https://placehold.co/120?text=?\'">'
            +'<p class="daily-name">'+dailyProd.name+'</p><div class="daily-price-box"><span class="price">'+fmt(dailyProd.price)+'</span>'
            +'<button class="daily-cart-btn" onclick="addToCart('+dailyProd.id+',\''+escStr(dailyProd.name)+'\','+dailyProd.price+',\''+(dailyProd.image[0]?.image||'')+'\')">🛒</button></div></div></div></div>';
    }
    hw.innerHTML=slider+daily;
    if(daily)startDailyTimer();
}
function startSlider(){
    if(state.sliderTimer)clearInterval(state.sliderTimer);
    state.sliderTimer=setInterval(()=>{state.sliderIndex=(state.sliderIndex+1)%state.totalSlides;goToSlide(state.sliderIndex);},4500);
}
window.goToSlide=function(idx){
    state.sliderIndex=idx;
    document.querySelectorAll('.ad-slide').forEach((s,i)=>s.classList.toggle('active',i===idx));
    document.querySelectorAll('.slider-dot').forEach((d,i)=>d.classList.toggle('active',i===idx));
};
function startDailyTimer(){
    const end=new Date();end.setHours(23,59,59,0);
    function tick(){let d=Math.max(0,end-new Date());const h=String(Math.floor(d/3600000)).padStart(2,'0');d%=3600000;const m=String(Math.floor(d/60000)).padStart(2,'0');d%=60000;const s=String(Math.floor(d/1000)).padStart(2,'0');const el=document.getElementById('daily-timer');if(el)el.textContent=h+':'+m+':'+s;}
    tick();setInterval(tick,1000);
}

/* ── POPULAR CATEGORIES ── */
function renderPopularCategories(cats){
    const c=document.getElementById('popular-categories-grid');if(!c)return;
    const active=cats.filter(x=>x.is_active_dashboard);
    if(!active.length){c.parentElement.style.display='none';return;}
    // "Barcha kategoriyalar" oxirida ko'rsatish uchun
    const allCard='<div class="pop-cat-card pop-cat-all" onclick="filterByCategory(null)"><div class="pop-cat-info pop-cat-all-label">Barcha kategoriyalar</div><div class="pop-cat-arrow">→</div></div>';
    c.innerHTML=active.map(cat=>'<div class="pop-cat-card" onclick="filterByCategory('+cat.id+')"><div class="pop-cat-info">'+cat.name+'</div><div class="pop-cat-img"><img src="'+imgUrl(cat.image)+'" alt="'+cat.name+'" onerror="this.src=\'https://placehold.co/80?text=?\'"></div></div>').join('')+allCard;
}

/* ── HEADER NAV ── */
function renderHeaderNav(cats){
    const list=document.getElementById('category-list');if(!list)return;
    list.innerHTML='<li class="category-item '+(state.currentCategory===null?'active-cat':'')+'" data-id="all" onclick="filterByCategory(null,this)">Barchasi</li>'
        +cats.map(c=>'<li class="category-item '+(state.currentCategory===c.id?'active-cat':'')+'" data-id="'+c.id+'" onclick="filterByCategory('+c.id+',this)">'+c.name+'</li>').join('');
}

/* ── PRODUCT GRID ── */
function renderProducts(prods){
    const ca=document.getElementById('content-area');if(!ca)return;
    if(!prods||!prods.length){ca.innerHTML='<div class="empty-msg"><svg width="60" height="60" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="1"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"/></svg><p>Bu kategoriyada mahsulot topilmadi.</p></div>';return;}
    ca.innerHTML='<div class="product-grid">'+prods.map(p=>{
        const fi=p.image&&p.image.length>0?imgUrl(p.image[0]?.image):'https://placehold.co/200?text=?';
        const iw=state.wishlist.includes(p.id);
        const id_img=p.image&&p.image.length>0?p.image[0]?.image:'';
        return '<div class="product-card" onclick="goToDetail('+p.id+')">'
            +'<div class="p-badge">0/0/12</div>'
            +'<button class="p-wishlist-btn '+(iw?'active':'')+'" data-wish-id="'+p.id+'" onclick="event.stopPropagation();toggleWishlist('+p.id+',\''+escStr(p.name)+'\')" title="'+(iw?'Sevimlilardan olib tashlash':'Sevimlilarga qoshish')+'">♥</button>'
            +'<div class="p-image-box"><img src="'+fi+'" alt="'+p.name+'" loading="lazy" onerror="this.src=\'https://placehold.co/200?text=?\'"></div>'
            +'<h3 class="p-title">'+p.name+'</h3>'
            +'<div class="p-installment-info">dan '+fmtNum(Math.round(p.price/12))+' som/oy</div>'
            +'<div class="p-footer"><span class="p-price">'+fmt(p.price)+'</span>'
            +'<button class="p-cart-btn" onclick="event.stopPropagation();addToCart('+p.id+',\''+escStr(p.name)+'\','+p.price+',\''+escStr(id_img)+'\')">'
            +'<svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg>'
            +'</button></div></div>';
    }).join('')+'</div>';
}

window.goToDetail=function(id){window.location.href='detail.html?id='+id;};

/* ── FILTER & SORT ── */
window.filterByCategory=function(id){
    state.currentCategory=id;
    document.querySelectorAll('.category-item').forEach(li=>li.classList.toggle('active-cat',id===null?li.dataset.id==='all':parseInt(li.dataset.id)===id));
    const t=document.getElementById('dynamic-title');
    if(t){if(!id){t.textContent='Barcha mahsulotlar';}else{const c=state.categories.find(x=>x.id===id);t.textContent=c?c.name:'Mahsulotlar';}}
    const ca=document.getElementById('content-area');
    if(ca)ca.innerHTML='<div class="product-grid skeleton-grid">'+Array(8).fill('<div class="skeleton-block prod-skel"></div>').join('')+'</div>';
    fetchDashboard(id);
    window.scrollTo({top:400,behavior:'smooth'});
};
window.sortProducts=function(){
    const v=document.getElementById('sort-select')?.value;
    let s=[...state.filteredProducts];
    if(v==='price-asc')s.sort((a,b)=>a.price-b.price);
    else if(v==='price-desc')s.sort((a,b)=>b.price-a.price);
    else if(v==='name-asc')s.sort((a,b)=>a.name.localeCompare(b.name));
    renderProducts(s);
};

/* ── SEARCH ── */
function setupSearch(){
    const inp=document.getElementById('search-input');
    const dd=document.getElementById('search-dropdown');
    if(!inp||!dd)return;
    let t;
    inp.addEventListener('input',()=>{
        clearTimeout(t);const q=inp.value.trim().toLowerCase();
        if(!q){dd.classList.remove('active');return;}
        t=setTimeout(()=>{
            const res=state.products.filter(p=>p.name.toLowerCase().includes(q)).slice(0,6);
            if(!res.length){dd.innerHTML='<div class="search-result-item"><div class="item-info"><div class="item-name">Natija topilmadi</div></div></div>';}
            else{dd.innerHTML=res.map(p=>{const im=p.image&&p.image[0]?imgUrl(p.image[0].image):'https://placehold.co/42?text=?';return '<div class="search-result-item" onclick="goToDetail('+p.id+');dd.classList.remove(\'active\');inp.value=\'\'"><img src="'+im+'" alt="'+p.name+'" onerror="this.src=\'https://placehold.co/42?text=?\'"><div class="item-info"><div class="item-name">'+p.name+'</div><div class="item-price">'+fmt(p.price)+'</div></div></div>';}).join('');}
            dd.classList.add('active');
        },280);
    });
    document.addEventListener('click',e=>{if(!inp.contains(e.target)&&!dd.contains(e.target))dd.classList.remove('active');});
}

/* ── DASHBOARD FETCH ── */
async function fetchDashboard(catId=null){
    try{
        let url=API+'/dashboard/';if(catId)url+='?category_id='+catId;
        const r=await fetch(url);if(!r.ok)throw new Error();
        const d=await r.json();
        if(!catId){
            state.products=d.products||[];state.categories=d.categories||[];
            renderHeroSection(d.advertisement,d.products[0]);
            renderPopularCategories(d.categories);
            renderHeaderNav(d.categories);
        }
        state.filteredProducts=d.products||[];
        renderProducts(state.filteredProducts);
    }catch{
        const ca=document.getElementById('content-area');
        if(ca)ca.innerHTML='<div class="empty-msg"><p>Malumotlarni yuklab bolmadi.<br><small>Backend: http://127.0.0.1:8000</small></p></div>';
        const hw=document.getElementById('hero-wrapper');
        if(hw&&hw.querySelector('.hero-skeleton'))hw.innerHTML='<div class="slider-container"><div class="ad-slide active"><div class="slider-placeholder"><div class="promo-tag">MediaPark</div><h2>Backend<br>ulanmagan</h2><p>http://127.0.0.1:8000</p></div></div></div>';
        const pg=document.getElementById('popular-categories-grid');if(pg)pg.innerHTML='';
        renderHeaderNav([]);
    }
}

/* ── AUTH ── */
window.handleLogin=async function(){
    const un=document.getElementById('login-username')?.value.trim();
    const pw=document.getElementById('login-password')?.value;
    const err=document.getElementById('login-error');
    if(!un||!pw){if(err)err.textContent='Login va parolni kiriting!';return;}
    const btn=document.getElementById('login-btn');
    if(btn){btn.disabled=true;btn.textContent='Kirilmoqda...';}
    try{
        const r=await fetch(API+'/login/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({username:un,password:pw})});
        const d=await r.json();
        if(!r.ok){if(err)err.textContent=d.detail||'Login yoki parol notogri';return;}
        saveTokens(d.access,d.refresh,un);
        updateNavAuth();updateBadges();
        toast('Xush kelibsiz, '+un+'!','success');
        const redirect=sessionStorage.getItem('auth_redirect')||'index.html';
        sessionStorage.removeItem('auth_redirect');
        setTimeout(()=>{window.location.href=redirect;},700);
    }catch{if(err)err.textContent='Server bilan boglanib bolmadi';}
    finally{if(btn){btn.disabled=false;btn.textContent='Kirish';}}
};

window.handleLogout=function(){
    if(!isLoggedIn())return;
    if(confirm(state.username+' — tizimdan chiqmoqchimisiz?')){
        clearTokens();updateNavAuth();updateBadges();
        toast('Tizimdan chiqildi','info');
        setTimeout(()=>{window.location.href='index.html';},600);
    }
};
window.profileBtnClick=function(){
    if(isLoggedIn()) window.location.href='profile.html';
    else window.location.href='login.html';
};

/* ── OTP / REGISTER FLOW ── */
window.sendOtp=async function(){
    const email=document.getElementById('reg-email')?.value.trim();
    const err=document.getElementById('register-error');
    if(!email){if(err)err.textContent='Email kiriting!';return;}
    const btn=document.getElementById('send-otp-btn');
    if(btn){btn.disabled=true;btn.textContent='Yuborilmoqda...';}
    if(err)err.textContent='';
    try{
        const r=await fetch(API+'/verify/email-verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email})});
        const d=await r.json();
        if(!r.ok){if(err)err.textContent=d.error||'Xato yuz berdi';if(btn){btn.disabled=false;btn.textContent='Kod yuborish';}return;}
        sessionStorage.setItem('otp_email',email);
        toast('Tasdiqlash kodi emailingizga yuborildi!','info');
        setTimeout(()=>{window.location.href='otp.html';},600);
    }catch{
        if(err)err.textContent='Server bilan boglanib bolmadi';
        if(btn){btn.disabled=false;btn.textContent='Kod yuborish';}
    }
};

window.verifyOtpPage=async function(){
    const email=sessionStorage.getItem('otp_email')||'';
    const inputs=[...document.querySelectorAll('.otp-inputs input')];
    const code=inputs.map(i=>i.value).join('');
    const err=document.getElementById('otp-error');
    const suc=document.getElementById('otp-success');
    if(code.length<6){if(err)err.textContent='6 raqamli kodni toliq kiriting!';return;}
    const btn=document.getElementById('verify-btn');
    if(btn){btn.disabled=true;btn.textContent='Tekshirilmoqda...';}
    try{
        const r=await fetch(API+'/verify/otp-verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,code})});
        const d=await r.json();
        if(!r.ok){if(err)err.textContent=d.error||'Kod notogri';if(btn){btn.disabled=false;btn.textContent='Tasdiqlash';}return;}
        sessionStorage.setItem('otp_verified','1');
        if(suc)suc.textContent='✅ Email tasdiqlandi! Royxatdan otishga otilmoqda...';
        if(err)err.textContent='';
        toast('Email tasdiqlandi!','success');
        setTimeout(()=>{window.location.href='register.html';},900);
    }catch{
        if(err)err.textContent='Server bilan boglanib bolmadi';
        if(btn){btn.disabled=false;btn.textContent='Tasdiqlash';}
    }
};

function setupOtpInputs(){
    const inputs=[...document.querySelectorAll('.otp-inputs input')];
    inputs.forEach((inp,i)=>{
        inp.addEventListener('input',()=>{
            inp.value=inp.value.replace(/\D/g,'').slice(0,1);
            if(inp.value&&i<inputs.length-1)inputs[i+1].focus();
            inp.classList.toggle('filled',!!inp.value);
        });
        inp.addEventListener('keydown',e=>{if(e.key==='Backspace'&&!inp.value&&i>0)inputs[i-1].focus();});
        inp.addEventListener('paste',e=>{
            e.preventDefault();
            const p=(e.clipboardData||window.clipboardData).getData('text').replace(/\D/g,'');
            [...p].forEach((ch,j)=>{if(inputs[j]){inputs[j].value=ch;inputs[j].classList.add('filled');}});
            const nx=p.length<inputs.length?inputs[p.length]:inputs[inputs.length-1];nx.focus();
        });
    });
}

window.resendOtp=async function(){
    const email=sessionStorage.getItem('otp_email');
    if(!email){toast('Email topilmadi, royxatdan qayta oting','error');return;}
    const btn=document.getElementById('resend-btn');
    if(btn){btn.disabled=true;btn.textContent='Yuborilmoqda...';}
    try{
        const r=await fetch(API+'/verify/email-verify',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email})});
        if(!r.ok)throw new Error();
        toast('Yangi kod yuborildi!','info');
        startResendTimer(btn,60);
    }catch{toast('Xato yuz berdi','error');if(btn){btn.disabled=false;btn.textContent='Qayta yuborish';}}
};
function startResendTimer(btn,sec){
    const t=document.getElementById('otp-timer-text');
    const iv=setInterval(()=>{
        if(t)t.textContent='Qayta yuborish: '+sec+' soniya';
        if(sec<=0){clearInterval(iv);if(btn){btn.disabled=false;btn.textContent='Qayta yuborish';}if(t)t.textContent='';}
        sec--;
    },1000);
}

window.handleRegister=async function(){
    const email=sessionStorage.getItem('otp_email')||'';
    const un=document.getElementById('reg-username')?.value.trim();
    const pw=document.getElementById('reg-password')?.value;
    const pw2=document.getElementById('reg-password2')?.value;
    const err=document.getElementById('register-error');
    const suc=document.getElementById('register-success');
    if(sessionStorage.getItem('otp_verified')!=='1'){if(err)err.textContent='Avval email tasdiqlash kerak (OTP)!';return;}
    if(!email||!un||!pw){if(err)err.textContent='Barcha maydonlarni toldiring!';return;}
    if(pw.length<9){if(err)err.textContent='Parol kamida 9 ta belgi bolishi kerak!';return;}
    if(pw2&&pw!==pw2){if(err)err.textContent='Parollar mos kelmadi!';return;}
    const btn=document.getElementById('register-btn');
    if(btn){btn.disabled=true;btn.textContent='Royxatdan otilmoqda...';}
    try{
        const r=await fetch(API+'/register/',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({email,username:un,password:pw,role:'user'})});
        const d=await r.json();
        if(!r.ok){const m=Object.values(d).flat().join(', ');if(err)err.textContent=m||'Xato yuz berdi';return;}
        sessionStorage.removeItem('otp_verified');sessionStorage.removeItem('otp_email');
        if(suc)suc.textContent='🎉 Muvaffaqiyatli royxatdan otdingiz!';
        toast("Royxatdan otildi! Endi kiring.",'success');
        setTimeout(()=>{window.location.href='login.html';},1200);
    }catch{if(err)err.textContent='Server bilan boglanib bolmadi';}
    finally{if(btn){btn.disabled=false;btn.textContent='Royxatdan otish';}}
};

/* ── DETAIL PAGE ── */
async function initDetailPage(){
    const id=new URLSearchParams(location.search).get('id');
    if(!id){window.location.href='index.html';return;}
    const wrap=document.getElementById('detail-content');if(!wrap)return;
    wrap.innerHTML='<div class="loader-spinner" style="margin:80px auto"></div>';
    try{
        const r=await fetch(API+'/product/detail/'+id+'/');
        if(!r.ok)throw new Error();
        const p=await r.json();
        const imgs=p.image||[];
        const mainImg=imgs[0]?imgUrl(imgs[0].image):'https://placehold.co/360?text=?';
        const monthly=Math.round(p.price/12);
        const iw=state.wishlist.includes(p.id);
        const fip=imgs[0]?.image||'';
        const thumbs=imgs.map((img,i)=>'<div class="detail-thumb '+(i===0?'active':'')+'" onclick="setDetailImg(\''+imgUrl(img.image)+'\',this)"><img src="'+imgUrl(img.image)+'" alt=""></div>').join('');
        const comments=p.comments&&p.comments.length
            ?'<div class="detail-comments"><h3>💬 Sharhlar ('+p.comments.length+')</h3>'+p.comments.map(c=>'<div class="comment-item"><div class="comment-user">👤 '+c.user+'</div><div class="comment-text">'+c.comment+'</div></div>').join('')+'</div>'
            :'<div class="detail-comments"><h3>💬 Sharhlar</h3><p style="color:#94a3b8;font-size:14px">Hali sharh yoq.</p></div>';

        let catName='Mahsulot';
        try{const dr=await fetch(API+'/dashboard/');const dd=await dr.json();const found=(dd.categories||[]).find(c=>c.id===p.category_id);if(found)catName=found.name;}catch{}

        wrap.innerHTML='<div class="breadcrumb"><a href="index.html">Bosh sahifa</a> › <a href="index.html">'+catName+'</a> › <span>'+p.name+'</span></div>'
            +'<div class="detail-layout"><div class="detail-gallery">'
            +'<div class="detail-main-img"><img src="'+mainImg+'" alt="'+p.name+'" id="detail-main-img" onerror="this.src=\'https://placehold.co/360?text=?\'"></div>'
            +(imgs.length>1?'<div class="detail-thumbs">'+thumbs+'</div>':'')
            +'</div><div class="detail-info">'
            +'<h1 class="detail-title">'+p.name+'</h1>'
            +'<div class="detail-price">'+fmt(p.price)+'</div>'
            +'<div class="detail-monthly">dan '+fmtNum(monthly)+' som/oy • 0/0/12</div>'
            +'<div class="detail-stock"><div class="stock-dot"></div><span class="stock-label">Mavjud</span></div>'
            +(p.description?'<p style="font-size:14px;color:#4a5568;line-height:1.75;margin-bottom:20px">'+p.description+'</p>':'')
            +'<div class="detail-actions">'
            +'<button class="detail-cart-btn" onclick="addToCart('+p.id+',\''+escStr(p.name)+'\','+p.price+',\''+escStr(fip)+'\')">'
            +'<svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round"><circle cx="9" cy="21" r="1"/><circle cx="20" cy="21" r="1"/><path d="M1 1h4l2.68 13.39a2 2 0 0 0 2 1.61h9.72a2 2 0 0 0 2-1.61L23 6H6"/></svg> Savatchaga qoshish</button>'
            +'<button class="detail-wish-btn '+(iw?'active':'')+'" data-wish-id="'+p.id+'" onclick="toggleWishlist('+p.id+',\''+escStr(p.name)+'\')" title="'+(iw?'Sevimlilardan olib tashlash':'Sevimlilarga qoshish')+'">♥</button>'
            +'</div>'+comments+'</div></div>';
    }catch{
        wrap.innerHTML='<div class="empty-msg"><p>Mahsulot malumotlari yuklanmadi.</p><a href="index.html" class="back-btn" style="margin-top:16px;display:inline-flex">← Orqaga</a></div>';
    }
}
window.setDetailImg=function(src,thumb){
    document.getElementById('detail-main-img').src=src;
    document.querySelectorAll('.detail-thumb').forEach(t=>t.classList.remove('active'));
    thumb.classList.add('active');
};

/* ── CART PAGE ── */
window.renderCartPage=function(){
    const wrap=document.getElementById('cart-page-content');if(!wrap)return;
    wrap.innerHTML='<div class="coming-soon-box" style="margin:0 auto"><div class="cs-icon">🔧</div><h2>Tez kunda</h2><p>Savatcha tizimi hali ishlab chiqilmoqda.</p><a href="index.html" class="back-btn" style="display:inline-block;margin-top:16px">← Bosh sahifa</a></div>';
};

/* ── WISHLIST PAGE ── */
window.renderWishlistPage=function(){
    const wrap=document.getElementById('wishlist-page-content');if(!wrap)return;
    wrap.innerHTML='<div class="coming-soon-box" style="margin:0 auto"><div class="cs-icon">🔧</div><h2>Tez kunda</h2><p>Sevimlilar tizimi hali ishlab chiqilmoqda.</p><a href="index.html" class="back-btn" style="display:inline-block;margin-top:16px">← Bosh sahifa</a></div>';
};