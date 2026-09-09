'use strict';
(() => {
  const people = window.NORSE_PEOPLE, stops = window.NORSE_STOPS, sources = window.NORSE_SOURCES;
  const byId = new Map(stops.map(s => [s.id,s]));
  const personById = new Map(people.map(p => [p.id,p]));
  const $ = id => document.getElementById(id);
  const esc = value => String(value).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));
  const key = 'escape-backpack-norse-routes-v1';
  const fresh = () => ({version:1,active:'leif',routes:Object.fromEntries(people.map(p=>[p.id,[]]))});
  let state = fresh(), history = [];
  // Validate saved and imported state against the trusted catalogue. Never render imported HTML or coordinates.
  function validate(value) {
    if (!value || value.version !== 1 || !personById.has(value.active) || !value.routes || typeof value.routes !== 'object') throw Error('This is not a compatible Norse route plan.');
    const result = fresh(); result.active = value.active;
    for (const p of people) {
      const route = value.routes[p.id];
      if (!Array.isArray(route) || route.length > 100 || route.some(id => typeof id !== 'string' || byId.get(id)?.person !== p.id)) throw Error('The plan contains an unknown place, a wrong-person stop, or more than 100 visits per trip.');
      result.routes[p.id] = [...route];
    }
    return result;
  }
  try { const saved = localStorage.getItem(key); if (saved) { state = validate(JSON.parse(saved)); $('save-status').textContent = 'Restored from this browser'; } }
  catch { $('save-status').textContent = 'Saved plan unavailable. Export to keep your work.'; }
  const current = () => personById.get(state.active);
  const route = () => state.routes[state.active];
  function status(message) { $('save-status').textContent = message; }
  function save() {
    try { localStorage.setItem(key,JSON.stringify(state)); status('Saved in this browser · export for a backup'); }
    catch { status('Browser saving unavailable · export to keep your work'); }
  }
  function change(fn) {
    history.push(JSON.stringify(state)); if (history.length>50) history.shift();
    fn(); save(); render();
  }
  function add(id) {
    const stop = byId.get(id); if (!stop) return;
    if (state.routes[stop.person].length>=100) {status('Maximum 100 visits per trip.');return;}
    change(()=>{state.active=stop.person;state.routes[stop.person].push(id);});
  }
  function selectPerson(id,fit=true) {
    if (!personById.has(id)) return;
    state.active=id; $('search').value=''; $('evidence').value='all'; save(); render();
    if(fit) fitPerson();
  }
  const map = L.map('map',{minZoom:2,maxZoom:16,worldCopyJump:false,zoomControl:true,attributionControl:true});
  map.attributionControl.setPrefix('<a href="https://leafletjs.com" target="_blank" rel="noopener">Leaflet</a>');
  map.setView([56,-15],3);
  map.createPane('coast');map.getPane('coast').style.zIndex='150';
  L.geoJSON(window.NORSE_LAND,{pane:'coast',style:{fillColor:'#e7e5d6',fillOpacity:1,color:'#b7c4b4',weight:1},interactive:false,attribution:'<a href="https://www.naturalearthdata.com/" target="_blank" rel="noopener">Natural Earth</a>'}).addTo(map);
  const tiles = L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png',{maxZoom:19,attribution:'&copy; <a href="https://www.openstreetmap.org/copyright" target="_blank" rel="noopener">OpenStreetMap contributors</a>'});
  let tileFailed = false;
  tiles.on('tileerror',()=>{tileFailed=true;$('tile-status').textContent='Some street tiles unavailable · coast map remains usable';});
  tiles.on('loading',()=>{tileFailed=false;$('tile-status').textContent='Loading street detail…';});
  tiles.on('load',()=>{if(!tileFailed && $('tiles').checked)$('tile-status').textContent='Online street detail';});
  const regions=L.layerGroup().addTo(map), paths=L.layerGroup().addTo(map), markers=L.layerGroup().addTo(map);
  [['GREENLAND',70,-44],['ICELAND',65,-19],['SCANDINAVIA',65,15],['NORTH ATLANTIC',49,-32],['LABRADOR',56,-66],['BRITAIN',54,-5],['FRANCE',46,2],['MEDITERRANEAN',35,17]].forEach(([name,lat,lng])=>L.marker([lat,lng],{interactive:false,icon:L.divIcon({className:'region-label',html:esc(name),iconSize:[130,18]})}).addTo(regions));
  const coordinates = ids => ids.map(id=>{const s=byId.get(id);return [s.lat,s.lng];});
  function fitStops(list) {
    if(!list.length)return;
    map.fitBounds(L.latLngBounds(list.map(s=>[s.lat,s.lng])),{padding:[45,45],maxZoom:10,animate:false});
  }
  function fitPerson(){fitStops(stops.filter(s=>s.person===state.active));}
  function sourceLink(s) {const source=sources[s.source];return `<a href="${source[1]}" target="_blank" rel="noopener">${esc(source[0])} ↗</a>`;}
  const evidenceNames = {supported:'Supported',saga:'Saga account',uncertain:'Uncertain / disputed',context:'Context / memorial'};
  function showStop(s) {
    const box=document.createElement('div');
    box.innerHTML=`<h3>${esc(s.name)}</h3><p><b>${evidenceNames[s.evidence]}</b> · ${esc(s.precision)}</p><p>${esc(s.note)}</p><p>${sourceLink(s)}</p><p>Approximate anchor: ${s.lat.toFixed(3)}, ${s.lng.toFixed(3)}</p>`;
    const button=document.createElement('button');
    button.textContent=state.routes[s.person].includes(s.id)?'Add another visit':'Add to aunt’s trip';
    button.onclick=()=>{add(s.id);map.closePopup();}; box.append(button);
    L.popup({maxWidth:280}).setLatLng([s.lat,s.lng]).setContent(box).openOn(map);
  }
  function drawMap() {
    paths.clearLayers();markers.clearLayers();
    const all=$('show-all').checked;
    const visiblePeople=all?people:[current()];
    for(const p of visiblePeople){
      const line=coordinates(state.routes[p.id]);
      if(line.length>1){
        L.polyline(line,{color:'#fffdf4',weight:7,opacity:.85,interactive:false}).addTo(paths);
        L.polyline(line,{color:p.color,weight:p.id===state.active?3.5:2.5,opacity:p.id===state.active?1:.65,interactive:false}).addTo(paths);
      }
    }
    // Other people's pins remain selectable in overview; shared sites can also be reached from the catalogue.
    const priority=s=>(state.routes[s.person].includes(s.id)?2:0)+(s.person===state.active?1:0);
    const visible=stops.filter(s=>all||s.person===state.active).sort((a,b)=>priority(b)-priority(a));
    const labelBoxes=[];
    for(const s of visible){
      const p=personById.get(s.person), visits=state.routes[s.person].flatMap((id,i)=>id===s.id?[i+1]:[]),selected=visits.length>0;
      const icon=L.divIcon({className:'pin-wrapper',html:`<span class="pin ${s.evidence} ${selected?'selected':''}" style="--person:${p.color}">${selected?visits[0]:p.short[0]}</span>`,iconSize:[28,28],iconAnchor:[14,14]});
      const marker=L.marker([s.lat,s.lng],{icon,title:`${p.short}: ${s.name}${selected?' · visits '+visits.join(', '):''}`,keyboard:true,zIndexOffset:(s.person===state.active?200:0)+(selected?500:0)}).addTo(markers);
      const label=`${all?p.short+': ':''}${esc(s.name.split(' · ')[0])}${selected?' · '+visits.join(', '):''}`;
      const pos=map.latLngToContainerPoint([s.lat,s.lng]);
      const box={left:pos.x+18,right:pos.x+18+Math.min(310,s.name.length*6+30),top:pos.y-13,bottom:pos.y+13};
      const clear=!labelBoxes.some(b=>box.left<b.right&&box.right>b.left&&box.top<b.bottom&&box.bottom>b.top);
      const permanent=$('labels').checked&&(selected||map.getZoom()>=5)&&clear;
      if(permanent)labelBoxes.push(box);
      marker.bindTooltip(label,{permanent,direction:'right',offset:[11,0],className:'place-label'});
      marker.on('click',()=>showStop(s));
    }
  }
  map.on('zoomend',()=>{ if(document.readyState!=='loading')drawMap(); });
  function renderPeople(){
    $('people').innerHTML=people.map(p=>`<button data-person="${p.id}" style="--person:${p.color}" aria-pressed="${p.id===state.active}"><strong>${p.name}</strong><span>${p.theme} · ${state.routes[p.id].length} visits</span></button>`).join('');
  }
  function renderRoute(){
    $('route-count').textContent=`${route().length} visits`;
    $('route').innerHTML=route().map((id,i)=>{const s=byId.get(id);return `<li><input type="number" min="1" max="${route().length}" value="${i+1}" data-position="${i}" aria-label="Position of visit ${i+1}, ${esc(s.name)}"><span class="route-name">${esc(s.name)}</span><button data-up="${i}" aria-label="Move visit ${i+1} up" ${i===0?'disabled':''}>↑</button><button data-down="${i}" aria-label="Move visit ${i+1} down" ${i===route().length-1?'disabled':''}>↓</button><button data-remove="${i}" aria-label="Remove visit ${i+1}">×</button></li>`;}).join('');
    $('reverse').disabled=route().length<2;$('clear').disabled=!route().length;$('fit-route').disabled=!route().length;
    $('undo').disabled=!history.length;
  }
  function renderCatalog(){
    const q=$('search').value.toLocaleLowerCase().trim(),evidence=$('evidence').value;
    const personal=stops.filter(s=>s.person===state.active);
    const list=personal.filter(s=>(evidence==='all'||s.evidence===evidence)&&`${s.name} ${s.note}`.toLocaleLowerCase().includes(q));
    $('stop-count').textContent=`${list.length} / ${personal.length}`;
    $('catalog').innerHTML=list.length?list.map(s=>{const chosen=route().includes(s.id);return `<article class="stop-card"><div class="stop-head"><h3>${esc(s.name)}</h3><button data-add="${s.id}" class="${chosen?'selected-action':''}" aria-label="${chosen?'Add another visit to':'Add'} ${esc(s.name)}">${chosen?'Add again':'+ Add'}</button></div><div class="meta">${evidenceNames[s.evidence]} · ${esc(s.precision)}</div><p>${esc(s.note)}</p>${sourceLink(s)} <button class="locate" data-locate="${s.id}" aria-label="Locate ${esc(s.name)} on map">Locate</button></article>`;}).join(''):'<p class="small">No matching places. Try a different name or evidence filter.</p>';
  }
  // Match Web Mercator used by the map. Uniform scaling preserves shape; never stretch x and y separately.
  function shape(id,w=220,h=125,numbers=false){
    const pts=state.routes[id].map(stopId=>{const s=byId.get(stopId);return [s.lng,180/Math.PI*Math.log(Math.tan(Math.PI/4+s.lat*Math.PI/360))];});
    if(!pts.length)return `<text x="${w/2}" y="${h/2}" text-anchor="middle" font-family="Segoe UI,sans-serif" font-size="12" fill="#7c8072">Choose stops to draw</text>`;
    const xs=pts.map(p=>p[0]),ys=pts.map(p=>p[1]),minX=Math.min(...xs),maxX=Math.max(...xs),minY=Math.min(...ys),maxY=Math.max(...ys);
    const scale=Math.min((w-36)/Math.max(maxX-minX,0.001),(h-36)/Math.max(maxY-minY,0.001));
    const plot=pts.map(([x,y])=>[w/2+(x-(minX+maxX)/2)*scale,h/2-(y-(minY+maxY)/2)*scale]);
    const color=personById.get(id).color;
    let out=`<polyline points="${plot.map(p=>p.map(n=>n.toFixed(2)).join(',')).join(' ')}" fill="none" stroke="${color}" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/>`;
    if(numbers)out+=plot.map(([x,y],i)=>`<circle cx="${x}" cy="${y}" r="8" fill="#fffcf5" stroke="${color}"/><text x="${x}" y="${y+3}" text-anchor="middle" fill="${color}" font-size="9" font-family="Segoe UI,sans-serif">${i+1}</text>`).join('');
    else if(plot.length===1)out+=`<circle cx="${plot[0][0]}" cy="${plot[0][1]}" r="3" fill="${color}"/>`;
    return out;
  }
  function renderPreviews(){
    $('previews').innerHTML=people.map(p=>`<button class="preview ${p.id===state.active?'active':''}" data-person="${p.id}" style="--person:${p.color}" aria-label="Edit ${p.name} route"><b>${p.name}</b><svg viewBox="0 0 220 125" role="img" aria-label="${p.short} route shape">${shape(p.id,220,125,$('preview-points').checked)}</svg><span>${state.routes[p.id].length} visits · north ↑</span></button>`).join('');
  }
  function render(){
    document.documentElement.style.setProperty('--active',current().color);
    $('map-person').textContent=current().name;$('person-note').textContent=current().note;
    renderPeople();renderRoute();renderCatalog();renderPreviews();drawMap();
  }
  function download(filename,content,type){
    const url=URL.createObjectURL(new Blob([content],{type})),a=document.createElement('a');
    a.href=url;a.download=filename;document.body.append(a);a.click();a.remove();setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  $('people').onclick=e=>{const b=e.target.closest('[data-person]');if(b)selectPerson(b.dataset.person);};
  $('previews').onclick=e=>{const b=e.target.closest('[data-person]');if(b)selectPerson(b.dataset.person);};
  $('catalog').onclick=e=>{
    const addButton=e.target.closest('[data-add]');if(addButton){add(addButton.dataset.add);return;}
    const locate=e.target.closest('[data-locate]');if(locate){const s=byId.get(locate.dataset.locate);map.setView([s.lat,s.lng],Math.max(map.getZoom(),7),{animate:false});showStop(s);$('map').scrollIntoView({behavior:'smooth',block:'center'});}
  };
  function move(from,to){if(from===to||to<0||to>=route().length)return;change(()=>{const [id]=route().splice(from,1);route().splice(to,0,id);});}
  $('route').onclick=e=>{
    const b=e.target.closest('button');if(!b)return;
    if('up' in b.dataset){const i=+b.dataset.up;move(i,i-1);$('route').querySelector(`[data-down="${i-1}"]`)?.focus();}
    if('down' in b.dataset){const i=+b.dataset.down;move(i,i+1);$('route').querySelector(`[data-up="${i+1}"]`)?.focus();}
    if('remove' in b.dataset)change(()=>route().splice(+b.dataset.remove,1));
  };
  $('route').onchange=e=>{
    if(!('position' in e.target.dataset))return;
    const from=+e.target.dataset.position,to=Number(e.target.value)-1;
    if(Number.isInteger(to)&&to>=0&&to<route().length)move(from,to);else renderRoute();
  };
  $('search').oninput=renderCatalog;$('evidence').onchange=renderCatalog;
  $('fit-person').onclick=fitPerson;
  $('fit-route').onclick=()=>fitStops(route().map(id=>byId.get(id)));
  $('fit-all').onclick=()=>{$('show-all').checked=true;drawMap();fitStops(stops);};
  $('show-all').onchange=drawMap;$('labels').onchange=drawMap;
  $('tiles').onchange=()=>{if($('tiles').checked)tiles.addTo(map);else{tiles.remove();$('tile-status').textContent='Offline coast map';}};
  $('preview-points').onchange=renderPreviews;
  $('reverse').onclick=()=>change(()=>route().reverse());
  $('clear').onclick=()=>change(()=>{state.routes[state.active]=[];});
  $('undo').onclick=()=>{if(!history.length)return;state=validate(JSON.parse(history.pop()));save();render();};
  $('export').onclick=()=>{
    const plan={...state,exportedAt:new Date().toISOString(),description:'The aunt’s fictional research itinerary. Catalogue associations are not verified visit logs.',visits:Object.fromEntries(people.map(p=>[p.id,state.routes[p.id].map((id,i)=>({order:i+1,...byId.get(id),sourceUrl:sources[byId.get(id).source][1]}))]))};
    download('Norse_Aunt_Route_Plan.json',JSON.stringify(plan,null,2),'application/json');status('Plan exported · keep this file to restore or share');
  };
  $('import').onclick=()=>$('import-file').click();
  $('import-file').onchange=async e=>{
    const file=e.target.files[0];if(!file)return;
    try{
      if(file.size>1000000)throw Error('Plan is too large. Choose an exported route plan under 1 MB.');
      const next=validate(JSON.parse(await file.text()));change(()=>{state=next;});fitPerson();status('Imported all four trips · Undo restores the previous plan');
    }catch(error){status(`Import failed: ${error instanceof SyntaxError?'The file is not valid JSON.':error.message}`);}
    finally{e.target.value='';}
  };
  $('export-shapes').onclick=()=>{
    const body=people.map((p,i)=>`<g transform="translate(${i*280},0)"><text x="140" y="30" text-anchor="middle" font-size="16" font-family="Segoe UI,sans-serif" fill="${p.color}">${esc(p.name)}</text><g transform="translate(0,45)">${shape(p.id,280,260,$('preview-points').checked)}</g><text x="140" y="327" text-anchor="middle" font-size="12" font-family="Segoe UI,sans-serif" fill="#586454">${state.routes[p.id].length} visits · north ↑</text></g>`).join('');
    download('Norse_Route_Shapes.svg',`<svg xmlns="http://www.w3.org/2000/svg" width="1120" height="350" viewBox="0 0 1120 350"><rect width="1120" height="350" fill="#fffcf5"/>${body}</svg>`,'image/svg+xml');
    status('Route shapes exported');
  };
  $('sources').innerHTML=people.map(p=>`<section><h3>${p.name}</h3><ul>${[...new Set(stops.filter(s=>s.person===p.id).map(s=>s.source))].map(id=>`<li><a href="${sources[id][1]}" target="_blank" rel="noopener">${esc(sources[id][0])}</a></li>`).join('')}</ul></section>`).join('');
  render();fitPerson();
})();
