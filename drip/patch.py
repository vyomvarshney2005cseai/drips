import re

SRC = "/Users/vyomvarshney2005/.gemini/antigravity/brain/e636df9c-0907-45e7-9883-34692f63f063/drip steps/drip_steps_wordrobe_v3.html"

with open(SRC, 'r') as f:
    html = f.read()

# Extract everything before and after <script>
parts = html.split('<script>')
before = parts[0]
after_parts = parts[1].split('</script>')
after = after_parts[1]

NEW_JS = r"""
// ─── SUPABASE CONFIG ───
const SB_URL = 'https://ommjsygfwtncrlumhibr.supabase.co/rest/v1';
const SB_KEY = 'sb_publishable_MdazFKds1XaOrLt4kZ0yfg_YcDPCVnd';
const ADMIN_PASSWORD = 'Drip2024';
let WA_NUMBER = localStorage.getItem('ds_wa_number') || '919999999999';

// ─── STATE ───
let currentOrderProduct = null;
let selectedSize = '';
let isFeatured = false;
let currentImageData = '';
let editingProductId = null;

// ─── SUPABASE FETCH ───
async function sb(table, opts={}) {
  const {method='GET', q='', body=null} = opts;
  const url = `${SB_URL}/${table}${q?'?'+q:''}`;
  const h = {'apikey':SB_KEY,'Authorization':`Bearer ${SB_KEY}`,'Content-Type':'application/json'};
  if(method==='POST'||method==='PATCH') h['Prefer']='return=representation';
  const res = await fetch(url,{method,headers:h,body:body?JSON.stringify(body):null});
  if(!res.ok){console.error('SB err',res.status,await res.text());throw new Error('API '+res.status);}
  if(method==='DELETE') return [];
  const text = await res.text();
  return text ? JSON.parse(text) : [];
}

// ─── PRODUCT MAPPERS ───
function fromDB(r){return{id:r.id,name:r.name,price:r.price,badge:r.badge||'',desc:r.description||'',sizes:r.sizes||[],stock:r.stock,featured:r.featured,image:r.image||'',soldOut:r.sold_out,addedAt:r.added_at};}
function toDB(p){const o={};if(p.id!==undefined)o.id=p.id;if(p.name!==undefined)o.name=p.name;if(p.price!==undefined)o.price=p.price;if(p.badge!==undefined)o.badge=p.badge;if(p.desc!==undefined)o.description=p.desc;if(p.sizes!==undefined)o.sizes=p.sizes;if(p.stock!==undefined)o.stock=p.stock;if(p.featured!==undefined)o.featured=p.featured;if(p.image!==undefined)o.image=p.image;if(p.soldOut!==undefined)o.sold_out=p.soldOut;if(p.addedAt!==undefined)o.added_at=p.addedAt;return o;}

// ─── PRODUCTS CRUD ───
async function getProducts(){try{const d=await sb('products',{q:'select=*&order=added_at.desc'});return(d||[]).map(fromDB);}catch(e){console.error(e);return[];}}
async function createProductAPI(p){return sb('products',{method:'POST',body:toDB(p)});}
async function updateProductAPI(id,u){return sb('products',{method:'PATCH',q:`id=eq.${id}`,body:toDB(u)});}
async function deleteProductAPI(id){return sb('products',{method:'DELETE',q:`id=eq.${id}`});}

// ─── ORDERS CRUD ───
function orderFromDB(r){return{id:r.id,productId:r.product_id,productName:r.product_name,size:r.size,qty:r.qty,price:r.price,total:r.total,customerName:r.customer_name,phone:r.phone,address:r.address,note:r.note||'',status:r.status,placedAt:r.placed_at};}
async function getOrders(){try{const d=await sb('orders',{q:'select=*&order=placed_at.desc'});return(d||[]).map(orderFromDB);}catch(e){console.error(e);return[];}}
async function createOrderAPI(o){return sb('orders',{method:'POST',body:{id:o.id,product_id:o.productId,product_name:o.productName,size:o.size,qty:o.qty,price:o.price,total:o.total,customer_name:o.customerName,phone:o.phone,address:o.address,note:o.note,status:o.status,placed_at:o.placedAt}});}
async function updateOrderAPI(id,u){return sb('orders',{method:'PATCH',q:`id=eq.${id}`,body:u});}

// ─── CURSOR ───
const cursor=document.getElementById('cursor');const ring=document.getElementById('cursor-ring');
document.addEventListener('mousemove',e=>{cursor.style.left=e.clientX+'px';cursor.style.top=e.clientY+'px';setTimeout(()=>{ring.style.left=e.clientX+'px';ring.style.top=e.clientY+'px';},80);});
document.addEventListener('mousedown',()=>{cursor.style.width='8px';cursor.style.height='8px';});
document.addEventListener('mouseup',()=>{cursor.style.width='16px';cursor.style.height='16px';});
if('ontouchstart' in window) document.body.classList.add('touch');

// ─── NAVIGATION ───
async function showPage(page){
  document.querySelectorAll('.page').forEach(p=>p.classList.remove('active'));
  document.querySelectorAll('.nav-links a').forEach(a=>{a.classList.toggle('active',a.dataset.page===page);});
  const el=document.getElementById('page-'+page);
  if(el){el.classList.add('active');window.scrollTo(0,0);}
  if(page==='shop') await renderShop();
  if(page==='home') await renderHome();
  if(page==='orders') await renderOrders();
  if(page==='admin') await initAdmin();
  initReveal();
}
function toggleMenu(){const h=document.getElementById('hamburger');const m=document.getElementById('mobileMenu');h.classList.toggle('open');m.classList.toggle('open');}

// ─── REVEAL ANIMATION ───
function initReveal(){setTimeout(()=>{const obs=new IntersectionObserver((entries)=>{entries.forEach(e=>{if(e.isIntersecting){e.target.classList.add('visible');obs.unobserve(e.target);}});},{threshold:0.1});document.querySelectorAll('.reveal:not(.visible)').forEach(el=>obs.observe(el));},50);}

// ─── PRODUCT CARD RENDER ───
function renderCard(product){
  const stock=typeof product.stock==='number'?product.stock:999;
  const isOOS=product.soldOut||stock<=0;
  const badgeHtml=product.badge?`<div class="product-badge badge-${product.badge}">${product.badge.toUpperCase()}</div>`:'';
  const soldOverlay=isOOS?`<div class="sold-overlay"><span>OUT OF STOCK</span></div>`:'';
  const imgHtml=product.image?`<img src="${product.image}" alt="${product.name}" loading="lazy"/>`:`<div class="product-img-placeholder"><div class="ph-icon">👕</div><div class="ph-text">No Image</div></div>`;
  const sizesHtml=(product.sizes||[]).map(s=>`<button class="size-chip" onclick="selectCardSize('${product.id}','${s}',this)" data-size="${s}">${s}</button>`).join('');
  let stockClass='in-stock',stockText=`${stock} pieces available`;
  if(isOOS){stockClass='no-stock';stockText='Out of stock';}else if(stock<=5){stockClass='low-stock';stockText=`Only ${stock} left!`;}
  const stockHtml=`<div class="product-stock ${isOOS?'out':''}"><span class="stock-dot ${stockClass}"></span><span class="stock-count">${stockText}</span></div>`;
  const orderBtn=isOOS?`<button class="btn btn-secondary btn-sm" style="flex:1;opacity:.4;pointer-events:none;justify-content:center">Out of Stock</button>`:`<button class="btn btn-whatsapp btn-sm" style="flex:1;justify-content:center" onclick="openOrderModal('${product.id}')">💬 Order on WhatsApp</button>`;
  return `<div class="product-card reveal" id="card-${product.id}" data-selected-size=""><div class="product-img-wrap">${badgeHtml}${imgHtml}${soldOverlay}</div><div class="product-info"><div class="product-name">${product.name}</div><div class="product-price">₹${Number(product.price).toLocaleString('en-IN')}</div>${stockHtml}<span class="size-label">Select Size:</span><div class="product-sizes" id="sizes-${product.id}">${sizesHtml}</div><div class="product-actions">${orderBtn}</div></div></div>`;
}

// ─── RENDER HOME ───
async function renderHome(){
  const products=await getProducts();
  const featured=products.filter(p=>p.featured&&!p.soldOut&&p.stock>0);
  const newest=[...products].slice(0,4);
  const fg=document.getElementById('featured-grid');const ng=document.getElementById('new-arrivals-grid');
  if(fg) fg.innerHTML=featured.length?featured.slice(0,4).map(p=>renderCard(p)).join(''):'<div style="grid-column:1/-1;text-align:center;padding:60px;color:var(--muted);font-size:11px;letter-spacing:2px;text-transform:uppercase">New drops coming soon...</div>';
  if(ng) ng.innerHTML=newest.length?newest.map(p=>renderCard(p)).join(''):'<div style="grid-column:1/-1;text-align:center;padding:60px;color:var(--muted);font-size:11px;letter-spacing:2px;text-transform:uppercase">No arrivals yet...</div>';
  initReveal();
}

// ─── RENDER SHOP ───
async function renderShop(){
  const products=await getProducts();
  const grid=document.getElementById('shop-grid');const empty=document.getElementById('shop-empty');
  if(!grid)return;
  if(!products.length){grid.innerHTML='';empty.style.display='block';}
  else{empty.style.display='none';grid.innerHTML=products.map(p=>renderCard(p)).join('');initReveal();}
}

// ─── SELECT SIZE ON CARD ───
function selectCardSize(productId,size,btn){
  document.querySelectorAll(`#sizes-${productId} .size-chip`).forEach(b=>b.classList.remove('selected'));
  btn.classList.add('selected');
  const card=document.getElementById('card-'+productId);
  if(card)card.dataset.selectedSize=size;
}

// ─── ORDER MODAL ───
async function openOrderModal(productId){
  const products=await getProducts();
  const product=products.find(p=>p.id===productId);
  if(!product||product.soldOut||(typeof product.stock==='number'&&product.stock<=0)){showToast('This product is out of stock');return;}
  const card=document.getElementById('card-'+productId);
  const preSelected=card?card.dataset.selectedSize:'';
  if(!preSelected){showToast('⬆️ Pehle size select karo!');const sizesEl=document.getElementById('sizes-'+productId);if(sizesEl){sizesEl.style.outline='1px solid var(--warn)';setTimeout(()=>{sizesEl.style.outline='';},1500);}return;}
  currentOrderProduct=product;selectedSize=preSelected;
  document.getElementById('modal-product-name').textContent=`${product.name} — ₹${Number(product.price).toLocaleString('en-IN')}`;
  document.getElementById('order-name').value='';document.getElementById('order-phone').value='';document.getElementById('order-address').value='';document.getElementById('order-note').value='';document.getElementById('order-qty').value='1';
  const ss=document.getElementById('modal-size-selector');
  ss.innerHTML=(product.sizes||[]).map(s=>`<button class="size-btn ${s===preSelected?'active':''}" onclick="selectSize('${s}',this)">${s}</button>`).join('');
  document.getElementById('order-modal').classList.add('open');document.body.style.overflow='hidden';
}
function closeOrderModal(){document.getElementById('order-modal').classList.remove('open');document.body.style.overflow='';}
function selectSize(size,btn){selectedSize=size;document.querySelectorAll('.size-btn').forEach(b=>b.classList.remove('active'));btn.classList.add('active');}

// ─── SUBMIT ORDER ───
async function submitOrder(){
  const name=document.getElementById('order-name').value.trim();
  const phone=document.getElementById('order-phone').value.trim();
  const address=document.getElementById('order-address').value.trim();
  const qty=Number(document.getElementById('order-qty').value);
  const note=document.getElementById('order-note').value.trim();
  if(!name){showToast('Please enter your name');return;}
  if(!phone){showToast('Please enter your phone number');return;}
  if(!address){showToast('Please enter delivery address');return;}
  if(!selectedSize){showToast('Please select a size');return;}
  const product=currentOrderProduct;
  try{
    const products=await getProducts();
    const live=products.find(p=>p.id===product.id);
    if(live&&typeof live.stock==='number'){
      if(live.stock<qty){showToast(`Only ${live.stock} pieces left!`);return;}
      const newStock=live.stock-qty;
      await updateProductAPI(live.id,{stock:newStock,soldOut:newStock<=0});
    }
    const total=Number(product.price)*qty;
    const orderId='ORD-'+Date.now().toString(36).toUpperCase();
    const order={id:orderId,productId:product.id,productName:product.name,size:selectedSize,qty,price:Number(product.price),total,customerName:name,phone,address,note,status:'active',placedAt:Date.now()};
    await createOrderAPI(order);
    const msg=`🛍️ *NEW ORDER — Drip Steps & Wordrobe*\n\n━━━━━━━━━━━━━━━━━━\n*Order ID:* ${orderId}\n*Product:* ${product.name}\n*Size:* ${selectedSize}\n*Quantity:* ${qty}\n*Price:* ₹${Number(product.price).toLocaleString('en-IN')} × ${qty} = ₹${total.toLocaleString('en-IN')}\n━━━━━━━━━━━━━━━━━━\n*Customer Name:* ${name}\n*Phone:* ${phone}\n*Address:* ${address}\n${note?`*Note:* ${note}`:''}\n━━━━━━━━━━━━━━━━━━\n💰 Payment: Cash on Delivery (COD)\n📦 Order placed via drip-steps-wordrobe.store`;
    const waUrl=`https://wa.me/${WA_NUMBER}?text=${encodeURIComponent(msg)}`;
    window.open(waUrl,'_blank');
    closeOrderModal();showToast('Order placed! ID: '+orderId);
    await renderHome();await renderShop();
  }catch(e){console.error(e);showToast('Error placing order. Try again.');}
}

// ─── RENDER ORDERS ───
async function renderOrders(){
  const orders=await getOrders();
  const list=document.getElementById('orders-list');const empty=document.getElementById('orders-empty');
  if(!list)return;
  if(!orders.length){list.innerHTML='';empty.style.display='block';return;}
  empty.style.display='none';
  list.innerHTML=orders.map(o=>{
    const date=new Date(o.placedAt).toLocaleString('en-IN',{day:'numeric',month:'short',year:'numeric',hour:'2-digit',minute:'2-digit'});
    const cancelBtn=o.status==='active'?`<button class="cancel-btn" onclick="cancelOrder('${o.id}')">✕ Cancel Order</button>`:'';
    return `<div class="order-card status-${o.status}"><div class="order-top"><div><div class="order-id">${o.id}</div><div style="font-size:9px;color:var(--muted);letter-spacing:1px;margin-top:2px">${date}</div></div><span class="order-status-badge ${o.status}">${o.status==='active'?'● Active':'● Cancelled'}</span></div><div class="order-details"><div class="order-detail-item">Product<strong>${o.productName}</strong></div><div class="order-detail-item">Size<strong>${o.size}</strong></div><div class="order-detail-item">Qty<strong>${o.qty}</strong></div><div class="order-detail-item">Total<strong>₹${o.total.toLocaleString('en-IN')}</strong></div></div><div style="display:flex;justify-content:flex-end">${cancelBtn}</div></div>`;
  }).join('');
}

// ─── CANCEL ORDER ───
async function cancelOrder(orderId){
  if(!confirm('Are you sure you want to cancel this order?'))return;
  try{
    const orders=await getOrders();const order=orders.find(o=>o.id===orderId);
    if(!order||order.status!=='active')return;
    await updateOrderAPI(orderId,{status:'cancelled'});
    const products=await getProducts();const product=products.find(p=>p.id===order.productId);
    if(product&&typeof product.stock==='number'){
      await updateProductAPI(product.id,{stock:product.stock+order.qty,soldOut:false});
    }
    await renderOrders();await renderHome();await renderShop();
    showToast('Order cancelled. Stock restored ✓');
  }catch(e){console.error(e);showToast('Error cancelling order');}
}

// ─── ADMIN ───
async function initAdmin(){
  const isLoggedIn=sessionStorage.getItem('dsw_admin')==='true';
  document.getElementById('admin-login-section').style.display=isLoggedIn?'none':'flex';
  document.getElementById('admin-panel-section').style.display=isLoggedIn?'block':'none';
  if(isLoggedIn){document.getElementById('wa-number-input').value=WA_NUMBER;await renderAdminProducts();}
}
function adminLogin(){
  const pwd=document.getElementById('admin-pwd').value;
  if(pwd===ADMIN_PASSWORD){
    sessionStorage.setItem('dsw_admin','true');
    document.getElementById('admin-login-section').style.display='none';
    document.getElementById('admin-panel-section').style.display='block';
    document.getElementById('wa-number-input').value=WA_NUMBER;
    renderAdminProducts();
  }else{document.getElementById('login-error').style.display='block';document.getElementById('admin-pwd').value='';setTimeout(()=>document.getElementById('login-error').style.display='none',3000);}
}
function adminLogout(){sessionStorage.removeItem('dsw_admin');initAdmin();showToast('Logged out successfully');}
function saveWaNumber(){const num=document.getElementById('wa-number-input').value.replace(/\D/g,'');if(!num||num.length<10){showToast('Enter valid number with country code');return;}WA_NUMBER=num;localStorage.setItem('ds_wa_number',num);document.querySelectorAll('#footer-wa,#contact-wa').forEach(el=>el.href=`https://wa.me/${num}`);showToast('WhatsApp number saved ✓');}
function switchAdminTab(tab){document.querySelectorAll('.admin-tab').forEach((t,i)=>{const tabs=['add','manage'];t.classList.toggle('active',tabs[i]===tab);});document.querySelectorAll('.admin-section').forEach(s=>s.classList.remove('active'));document.getElementById('admin-tab-'+tab).classList.add('active');if(tab==='manage')renderAdminProducts();}
function toggleSizeCheck(el,size){el.classList.toggle('checked');el.dataset.size=size;}
function toggleFeatured(val){isFeatured=val==='yes';document.getElementById('feat-yes').classList.toggle('checked',val==='yes');document.getElementById('feat-no').classList.toggle('checked',val==='no');}
function previewImage(input){if(!input.files[0])return;const reader=new FileReader();reader.onload=e=>{currentImageData=e.target.result;const area=document.getElementById('upload-area');let img=area.querySelector('img.preview-img');if(!img){img=document.createElement('img');img.className='preview-img';area.appendChild(img);}img.src=currentImageData;area.querySelector('.upload-icon').style.display='none';area.querySelector('.upload-hint').style.display='none';};reader.readAsDataURL(input.files[0]);}

// ─── ADD PRODUCT ───
async function addProduct(){
  const name=document.getElementById('prod-name').value.trim();
  const price=document.getElementById('prod-price').value.trim();
  const badge=document.getElementById('prod-badge').value;
  const desc=document.getElementById('prod-desc').value.trim();
  const stockVal=document.getElementById('prod-stock').value.trim();
  const sizes=Array.from(document.querySelectorAll('#size-checkboxes .size-check-label.checked')).map(l=>l.dataset.size);
  if(!name){showToast('Product name is required');return;}
  if(!price||isNaN(price)||Number(price)<=0){showToast('Enter a valid price');return;}
  if(!sizes.length){showToast('Select at least one size');return;}
  if(!stockVal||isNaN(stockVal)||Number(stockVal)<0){showToast('Enter valid stock quantity');return;}
  const stock=Number(stockVal);const id=editingProductId||'p_'+Date.now();
  const productData={id,name,price:Number(price),badge,desc,sizes,stock,featured:isFeatured,image:currentImageData,soldOut:stock<=0,addedAt:Date.now()};
  try{
    if(editingProductId){await updateProductAPI(id,productData);editingProductId=null;}
    else{await createProductAPI(productData);}
    clearProductForm();showToast('Product saved ✓');await renderHome();
  }catch(e){console.error(e);showToast('Error saving product');}
}

function clearProductForm(){
  document.getElementById('prod-name').value='';document.getElementById('prod-price').value='';document.getElementById('prod-badge').value='';document.getElementById('prod-desc').value='';document.getElementById('prod-stock').value='';
  document.querySelectorAll('#size-checkboxes .size-check-label').forEach(l=>l.classList.remove('checked'));
  document.getElementById('feat-yes').classList.remove('checked');document.getElementById('feat-no').classList.remove('checked');
  currentImageData='';editingProductId=null;
  const area=document.getElementById('upload-area');const img=area.querySelector('.preview-img');if(img)img.remove();
  area.querySelector('.upload-icon').style.display='';area.querySelector('.upload-hint').style.display='';
  document.getElementById('img-file').value='';isFeatured=false;
}

// ─── ADMIN PRODUCT LIST ───
async function renderAdminProducts(){
  const products=await getProducts();
  const list=document.getElementById('admin-product-list');const empty=document.getElementById('admin-empty');const count=document.getElementById('product-count');
  count.textContent=`${products.length} product${products.length!==1?'s':''} total`;
  if(!products.length){list.innerHTML='';empty.style.display='block';return;}
  empty.style.display='none';
  list.innerHTML=products.map(p=>`<div class="admin-product-card"><div class="admin-product-img">${p.image?`<img src="${p.image}" alt="${p.name}" loading="lazy"/>`:`<div class="no-img">No Image</div>`}</div><div class="admin-product-info"><div class="ap-name">${p.name}</div><div class="ap-price">₹${Number(p.price).toLocaleString('en-IN')}</div><div class="ap-status ${p.soldOut||p.stock<=0?'status-sold':'status-available'}">${p.soldOut||p.stock<=0?'● Out of Stock':'● Available'} · Stock: ${typeof p.stock==='number'?p.stock:'N/A'}${p.featured?' · Featured':''}${p.badge?' · '+p.badge.toUpperCase():''}</div><div style="font-size:9px;color:var(--muted);margin-bottom:10px;letter-spacing:1px">Sizes: ${(p.sizes||[]).join(', ')}</div><div class="admin-actions"><button class="admin-btn admin-btn-warn" onclick="toggleSoldOut('${p.id}')">${p.soldOut?'Restock':'Sold Out'}</button><button class="admin-btn admin-btn-neutral" onclick="editProduct('${p.id}')">Edit</button><button class="admin-btn admin-btn-danger" onclick="deleteProduct('${p.id}')">Delete</button></div></div></div>`).join('');
}

async function toggleSoldOut(id){
  try{
    const products=await getProducts();const p=products.find(x=>x.id===id);if(!p)return;
    const newSold=!p.soldOut;
    await updateProductAPI(id,{soldOut:newSold,stock:newSold?0:p.stock});
    await renderAdminProducts();await renderHome();
    showToast(`Marked as ${newSold?'Sold Out':'Available'} ✓`);
  }catch(e){console.error(e);showToast('Error updating product');}
}

async function deleteProduct(id){
  if(!confirm('Delete this product permanently?'))return;
  try{await deleteProductAPI(id);await renderAdminProducts();await renderHome();showToast('Product deleted');}
  catch(e){console.error(e);showToast('Error deleting product');}
}

async function editProduct(id){
  const products=await getProducts();const p=products.find(x=>x.id===id);if(!p)return;
  switchAdminTab('add');editingProductId=id;
  document.getElementById('prod-name').value=p.name;document.getElementById('prod-price').value=p.price;
  document.getElementById('prod-badge').value=p.badge||'';document.getElementById('prod-desc').value=p.desc||'';
  document.getElementById('prod-stock').value=typeof p.stock==='number'?p.stock:'';
  document.querySelectorAll('#size-checkboxes .size-check-label').forEach(l=>{l.classList.toggle('checked',(p.sizes||[]).includes(l.dataset.size));});
  isFeatured=p.featured||false;
  document.getElementById('feat-yes').classList.toggle('checked',isFeatured);document.getElementById('feat-no').classList.toggle('checked',!isFeatured);
  if(p.image){currentImageData=p.image;const area=document.getElementById('upload-area');let img=area.querySelector('.preview-img');if(!img){img=document.createElement('img');img.className='preview-img';area.appendChild(img);}img.src=p.image;area.querySelector('.upload-icon').style.display='none';area.querySelector('.upload-hint').style.display='none';}
  window.scrollTo(0,0);showToast('Editing product — make changes and save');
}

// ─── TOAST ───
function showToast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),3000);}

// ─── MODAL CLOSE ON BG ───
document.getElementById('order-modal').addEventListener('click',function(e){if(e.target===this)closeOrderModal();});

// ─── INIT ───
document.addEventListener('DOMContentLoaded',async()=>{
  await renderHome();initReveal();
  if(WA_NUMBER){document.querySelectorAll('#footer-wa,#contact-wa').forEach(el=>el.href=`https://wa.me/${WA_NUMBER}`);document.querySelector('#contact-wa .contact-link-value').textContent=`+${WA_NUMBER.slice(0,2)} ${WA_NUMBER.slice(2,7)} ${WA_NUMBER.slice(7)}`;}
});
"""

final = before + '<script>' + NEW_JS + '\n</script>' + after

with open(SRC, 'w') as f:
    f.write(final)

print("✅ Supabase backend applied to v3 file!")
