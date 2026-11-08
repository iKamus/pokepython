/* ═══════════════════════════════════════════════════
   PokéPython — Curso interactivo de Python con Pokémon
   SPA con routing hash, Pyodide para ejecución local
   ═══════════════════════════════════════════════════ */

console.info('PokéPython build: 2026-11-08-a');

// ── Estado global ──────────────────────────────
let LESSONS = [];       // flat array [lesson, ...]
let MODULES = {};       // grouped by moduleId

const state = {
  currentLessonId: null,
  completedLessons: new Set(JSON.parse(localStorage.getItem('pokpy_completed') || '[]')),
  pyodideReady: false,
  pyodide: null,
};

// Tipos Pokémon → colores hex
const TYPE_COLORS = {
  electric:'#ffcb05',fire:'#f08030',water:'#6890f0',grass:'#78c850',
  psychic:'#f46d44',ghost:'#705596',dragon:'#6f35fc',dark:'#705746',
  fairy:'#d877d8',normal:'#a8a878',steel:'#b8b8d0',ice:'#96d9d8',
  fighting:'#c22e28',poison:'#a33ea1',ground:'#e2b630',flying:'#a98ff3',
  bug:'#a6b91a',rock:'#ba7744',
};

// ── Utilidades DOM ──────────────────────────────
const $ = s => document.querySelector(s);
const $$ = s => document.querySelectorAll(s);

function formatNumber(n) { return String(n).padStart(2,'0'); }
function capitalize(s) { return s.charAt(0).toUpperCase()+s.slice(1); }

const LEVEL_LABELS={beginner:'Básico',intermediate:'Intermedio',advanced:'Avanzado'};
const TYPE_LABELS={electric:'Eléctrico',fire:'Fuego',water:'Agua',grass:'Planta',psychic:'Psíquico',ghost:'Fantasma',dragon:'Dragón',dark:'Siniestro',fairy:'Hada',normal:'Normal',steel:'Acero',ice:'Hielo',fighting:'Lucha',poison:'Veneno',ground:'Tierra',flying:'Volador',bug:'Bicho',rock:'Roca'};
function typeLabel(type){ return TYPE_LABELS[type]||capitalize(type||''); }
function levelLabel(level){ return LEVEL_LABELS[level]||capitalize(level||''); }
function plural(n,singular,pluralForm){ return n===1?singular:pluralForm; }
function escapeHtml(s){return s.replace(/&/g,'&amp;').replace(/</g,'&lt;').replace(/>/g,'&gt;').replace(/"/g,'&quot;');}
// Resalta sintaxis Python en los bloques de teoría (fences ```python y ejemplo).
// Tokeniza el código crudo y escapa cada fragmento por separado: escapar antes
// destruiría la detección de strings (las comillas se vuelven &quot;).
const PY_KW_SET=new Set(['def','class','return','if','elif','else','for','while','in','not','and','or','is','import','from','as','with','try','except','finally','pass','break','continue','lambda','None','True','False','global','yield','assert','raise','del']);
const PY_BI_SET=new Set(['print','len','range','int','str','float','bool','list','dict','set','tuple','sum','min','max','sorted','enumerate','zip','open','input','abs','round','type','isinstance','super','format','map','filter','any','all','self']);
function highlightPython(code){
  const n=code.length; let i=0; let out=''; let buf='';
  const flush=()=>{ if(buf){ out+=escapeHtml(buf); buf=''; } };
  while(i<n){
    const c=code[i];
    if(c==='#'){ flush(); let j=i; while(j<n && code[j]!=='\n') j++; out+=`<span class="tok-comentario">${escapeHtml(code.slice(i,j))}</span>`; i=j; continue; }
    if(c==='"' || c==="'"){
      flush();
      const triple=code.startsWith(c+c+c,i);
      let j=i;
      if(triple){ j=i+3; while(j<n){ if(code.startsWith(c+c+c,j)){ j+=3; break;} j++; } }
      else { j=i+1; while(j<n && code[j]!==c && code[j]!=='\n') j++; if(j<n && code[j]===c) j++; }
      out+=`<span class="tok-texto">${escapeHtml(code.slice(i,j))}</span>`;
      i=j; continue;
    }
    if(/[0-9]/.test(c)){
      const prev=i>0?code[i-1]:'';
      if(!/[A-Za-z_]/.test(prev)){
        flush(); let j=i;
        while(j<n && /[0-9]/.test(code[j])) j++;
        if(j<n && code[j]==='.'){ j++; while(j<n && /[0-9]/.test(code[j])) j++; }
        if(j<n && (code[j]==='e'||code[j]==='E')){ j++; if(j<n && (code[j]==='+'||code[j]==='-')) j++; while(j<n && /[0-9]/.test(code[j])) j++; }
        out+=`<span class="tok-numero">${escapeHtml(code.slice(i,j))}</span>`;
        i=j; continue;
      }
    }
    if(/[A-Za-z_]/.test(c)){
      flush(); let j=i; while(j<n && /[A-Za-z0-9_]/.test(code[j])) j++;
      const word=code.slice(i,j);
      if(PY_KW_SET.has(word)) out+=`<span class="tok-clave">${escapeHtml(word)}</span>`;
      else if(PY_BI_SET.has(word)) out+=`<span class="tok-builtin">${escapeHtml(word)}</span>`;
      else out+=escapeHtml(word);
      i=j; continue;
    }
    buf+=c; i++;
  }
  flush();
  return out;
}
// Bloques primero: fences, tablas y listas. Si las reglas inline corren antes, el
// fence ```python se lo come el regex de `código` (quedaba un <code> gigante y un
// backtick huérfano) y las tablas y listas salían con barras y guiones literales.
function renderMarkdown(t,enLinea=false){
  const bloques=[];
  const guardar=html=>{bloques.push(html);return `\u0000${bloques.length-1}\u0000`; };
  // Lo que va dentro de un bloque también lleva énfasis y código inline.
  const inline=s=>s
    .replace(/\*\*(.+?)\*\*/g,'<strong>$1</strong>')
    .replace(/\*(.+?)\*/g,'<em>$1</em>')
    .replace(/`([^`]+)`/g,'<code>$1</code>');
  const celdas=fila=>fila.replace(/^\||\|$/g,'').split('|').map(c=>inline(c.trim()));
  const esSeparador=fila=>/^\|[\s:|-]+\|$/.test(fila);
  const tabla=filas=>{
    const [cabecera,...resto]=filas;
    const cuerpo=resto.filter(f=>!esSeparador(f));
    const th=celdas(cabecera).map(c=>`<th>${c}</th>`).join('');
    const tr=cuerpo.map(f=>`<tr>${celdas(f).map(c=>`<td>${c}</td>`).join('')}</tr>`).join('');
    return `<div class="md-table"><table><thead><tr>${th}</tr></thead><tbody>${tr}</tbody></table></div>`;
  };
  const items=(bloque,prefijo)=>bloque.trim().split('\n')
    .map(l=>`<li>${inline(l.replace(prefijo,'').trim())}</li>`).join('');

  let out=String(t)
    .replace(/```[a-z]*\n([\s\S]*?)```/g,(_,codigo)=>
      guardar(`<pre><code>${highlightPython(codigo.replace(/\n$/,''))}</code></pre>`))
    .replace(/(?:^\|.*\|[ \t]*\n?){2,}/gm,bloque=>guardar(tabla(bloque.trim().split('\n'))))
    .replace(/(?:^[ \t]*[-*] .*\n?)+/gm,bloque=>guardar(`<ul>${items(bloque,/^[ \t]*[-*] /)}</ul>`))
    .replace(/(?:^\d+\. .*\n?)+/gm,bloque=>guardar(`<ol>${items(bloque,/^\d+\. /)}</ol>`));

  out=out
    .replace(/^(#{1,6}) (.+)$/gm,(_,nivel,titulo)=>`<${nivel.length<=2?'h2':'h3'}>${titulo}</${nivel.length<=2?'h2':'h3'}>`);

  // Énfasis inline (también para párrafos, items y celdas: los bloques ya lo
  // aplicaron por su cuenta; aquí cubre el texto suelto y los encabezados).
  out=inline(out);

  // Párrafos reales: el texto suelto se parte en líneas vacías. Un salto
  // simple dentro de un párrafo sigue siendo <br>; una línea vacía corta el
  // párrafo. Los encabezados y los placeholders de bloque son bloques propios:
  // nunca se envuelven en <p> y no llevan <br> pegado.
  // En modo en línea (concepto clave: va dentro de un <div> que ya tiene texto)
  // no corresponde <p>, porque partiría el rótulo "Concepto clave:" de su contenido.
  if(enLinea) return out
    .replace(/\u0000(\d+)\u0000/g,(_,i)=>bloques[Number(i)])
    .replace(/\n/g,'<br>').trim();

  const lineas=out.split('\n');
  const bloquesFinales=[];
  let parrafo=[];
  const vaciarParrafo=()=>{
    if(parrafo.length){
      const texto=parrafo.join('\n').trim();
      if(texto) bloquesFinales.push(`<p>${texto.replace(/\n/g,'<br>')}</p>`);
      parrafo=[];
    }
  };
  const esBloque=t=>/^<h[23]>/.test(t)||/^\u0000\d+\u0000$/.test(t);
  for(const linea of lineas){
    const t=linea.trim();
    if(t===''){ vaciarParrafo(); continue; }
    if(esBloque(t)){ vaciarParrafo(); bloquesFinales.push(t); }
    else parrafo.push(linea);
  }
  vaciarParrafo();
  out=bloquesFinales.join('\n');

  // Restaurar los bloques: ya son elementos de bloque, sin <br> pegado.
  return bloquesFinales.join('\n').replace(/\u0000(\d+)\u0000/g,(_,i)=>bloques[Number(i)]);
}

// Orden de módulos explícito. JavaScript emite primero las claves que parecen
// enteros ("10","11","12") y después las que no ("01"…"09","proyecto"), así que
// confiar en el orden del objeto listaba los módulos empezando por el 10.
function moduleEntries(){
  const rank=k=>/^\d+$/.test(k)?Number(k):Number.POSITIVE_INFINITY;
  return Object.entries(MODULES).sort(([a],[b])=>{
    const ra=rank(a), rb=rank(b);
    if(ra!==rb) return ra<rb?-1:1;
    return a.localeCompare(b);
  });
}

function updateHeroStats(){
  const set=(sel,value)=>{const el=$(sel); if(el) el.textContent=value;};
  set('#statLessons', LESSONS.length);
  set('#statModules', Object.keys(MODULES).length);
  set('#statTests', LESSONS.reduce((n,l)=>n+((l.tests||[]).length),0));
}

// ── Tema claro / oscuro ─────────────────────────
const THEME_KEY='pokpy_theme';

function currentTheme(){
  return document.documentElement.getAttribute('data-theme')==='light'?'light':'dark';
}

function applyTheme(theme){
  document.documentElement.setAttribute('data-theme',theme);
  const btn=$('#themeToggle');
  if(btn) btn.setAttribute('aria-pressed',String(theme==='light'));
}

function storedTheme(){
  try{
    const saved=localStorage.getItem(THEME_KEY);
    return saved==='light'||saved==='dark'?saved:null;
  }catch(e){ return null; }
}

function initTheme(){
  const prefersLight=window.matchMedia('(prefers-color-scheme: light)').matches;
  applyTheme(storedTheme()||(prefersLight?'light':'dark'));

  const btn=$('#themeToggle');
  if(btn) btn.onclick=()=>{
    const next=currentTheme()==='light'?'dark':'light';
    applyTheme(next);
    try{ localStorage.setItem(THEME_KEY,next); }catch(e){}
  };

  // Sin elección guardada, el tema sigue la preferencia del sistema.
  const mq=window.matchMedia('(prefers-color-scheme: light)');
  const onSystem=m=>{ if(!storedTheme()) applyTheme(m.matches?'light':'dark'); };
  if(mq.addEventListener) mq.addEventListener('change',onSystem);
  else if(mq.addListener) mq.addListener(onSystem);
}

// ── Cargar datos ────────────────────────────────
async function loadData(){
  try{
    const res = await fetch('lessons.json');
    const json = await res.json();
    // Flatten nested modules into one array + keep groups
    LESSONS = [];
    MODULES = {};
    for(const [modId, mod] of Object.entries(json.modules)){
      MODULES[modId] = {title:mod.title, description:mod.description, lessons:[]};
      for(const lesson of mod.lessons){
        LESSONS.push({...lesson});
        MODULES[modId].lessons.push(LESSONS[LESSONS.length-1]);
      }
    }
    LESSONS.sort((a,b)=>a.id-b.id);
  } catch(e){
    console.error('No se pudo cargar lessons.json:', e);
    alert('Error cargando las lecciones. Asegurate de que lessons.json esté en la misma carpeta.');
  }
}

// ── Progreso ───────────────────────────────────
function saveProgress(){
  localStorage.setItem('pokpy_completed',JSON.stringify([...state.completedLessons]));
}

function updateProgress(){
  const total=LESSONS.length, done=state.completedLessons.size;
  const pct=total?Math.round(done/total*100):0;
  const pill=$('#progressPill');
  if(pill){
    pill.querySelector('.progress-count').textContent=`${done}/${total}`;
    pill.querySelector('.fill').style.width=`${pct}%`;
  }
}

function markCompleted(id){
  state.completedLessons.add(id);
  saveProgress();
  updateProgress();
  updateSidebar(state.currentLessonId);
}

// ── Routing ─────────────────────────────────────
function parseHash(){
  const h=location.hash.slice(1)||'/';
  if(h.startsWith('/lesson/') && h.split('/').length===3){
    const id=parseInt(h.split('/').pop(),10);
    return {view:'lesson', lessonId:isNaN(id)?null:id};
  }
  return {view:'index'};
}

function navigate(){
  if(!LESSONS.length) return; // wait for data
  const route=parseHash();
  $('#indexView').classList.toggle('active',route.view==='index');
  $('#lessonView').classList.toggle('active',route.view==='lesson' && !!route.lessonId);
  if(route.view==='lesson' && route.lessonId){
    renderLesson(route.lessonId);
  } else {
    renderIndex();
  }
  updateSidebar(route.lessonId);
  window.scrollTo({top:0,behavior:'smooth'});
}

// ── Index View ──────────────────────────────────
function renderIndex(){
  const grid=$('#modulesGrid');
  const mode=getCurrentMode();

  const cards=moduleEntries().map(([modId,mod])=>({
    modId,
    mod,
    lessons:mode==='all'?mod.lessons:mod.lessons.filter(l=>l.level===mode),
  })).filter(c=>c.lessons.length);

  grid.innerHTML=cards.map(({modId,mod,lessons})=>{
    const first=lessons[0];
    const level=first.level||'beginner';
    const badge=/^\d+$/.test(modId)?modId.padStart(2,'0'):'PY';
    const title=mod.title||first.title.replace(/^[0-9]+\.\s*/, '');
    return `<article class="module-card" data-module="${modId}" data-level="${level}" data-first="${first.id}" role="link" tabindex="0" aria-label="Módulo ${badge}: ${escapeHtml(title)}">
      <div class="module-card-head">
        <span class="module-badge" aria-hidden="true">${badge}</span>
        <div>
          <h3>${title}</h3>
          <p class="card-meta">
            <span class="level-chip ${level}">${levelLabel(level)}</span>
            <span>${lessons.length} ${plural(lessons.length,'lección','lecciones')}</span>
          </p>
        </div>
      </div>
      <p class="card-desc">${mod.description||''}</p>
      <div class="card-lessons">
        ${lessons.map(l=>`<a class="card-lesson-tag" href="#/lesson/${l.id}" data-lesson-link="${l.id}">${formatNumber(l.id)} · ${escapeHtml(l.shortTitle||'')}</a>`).join('')}
      </div>
    </article>`;
  }).join('');

  // Clic o Enter sobre una tarjeta -> primera lección del módulo (respetando el filtro de nivel)
  grid.querySelectorAll('.module-card').forEach(card=>{
    const go=()=>{ location.hash=`/lesson/${card.dataset.first}`; };
    card.addEventListener('click',e=>{
      if(e.target.closest('a')) return;   // el link de la lección manda
      go();
    });
    card.addEventListener('keydown',e=>{
      if(e.key==='Enter'||e.key===' '){ e.preventDefault(); go(); }
    });
  });
}

// ── Sidebar Navigation ──────────────────────────
let collapsedModules=new Set();

function updateSidebar(activeLessonId){
  const nav=$('#moduleNav');
  const mode=getCurrentMode();
  if(!nav) return;
  
  let html='<p class="sidebar-title">MÓDULOS</p>';
  for(const [modId,mod] of moduleEntries()){
    const activeMods=mode==='all'||mod.lessons.some(l=>l.level===mode);
    if(!activeMods) continue;
    
    const visibleLessons=mode==='all'?mod.lessons:mod.lessons.filter(l=>l.level===mode);
    if(!visibleLessons.length) continue;
    
    const isActive=mod.lessons.some(l=>l.id===activeLessonId);
    const isCollapsed=collapsedModules.has(modId);
    
    html+=`<div class="module-group">
      <div class="module-header ${isCollapsed?'collapsed':''}" data-module="${modId}">
        <span class="arrow">▾</span>
        <span class="module-num">${modId.padStart(2,'0')}</span>
        <span>${mod.title}</span>
      </div>
      <ul class="lesson-list" style="display:${isCollapsed?'none':''}">
        ${visibleLessons.map(l=>`
          <li class="lesson-item ${state.completedLessons.has(l.id)?'completed':''} ${l.id===activeLessonId?'active':''}" 
              data-lesson="${l.id}" data-level="${l.level}">
            <span class="status-check"></span>
            <span class="lesson-num level-badge-${l.level}">${formatNumber(l.id)}</span>
            <span>${l.shortTitle||l.title.replace(/^[0-9]+\.\s*/,'')}</span>
          </li>`).join('')}
      </ul>
    </div>`;
  }
  nav.innerHTML=html;
  
  // Header click -> toggle
  nav.querySelectorAll('.module-header').forEach(h=>{
    h.onclick=()=>{
      const mid=h.dataset.module;
      if(collapsedModules.has(mid)) collapsedModules.delete(mid);
      else collapsedModules.add(mid);
      const list=h.nextElementSibling;
      h.classList.toggle('collapsed');
      list.style.display=collapsedModules.has(mid)?'none':'';
    };
  });
  
  // Lesson item click
  nav.querySelectorAll('.lesson-item').forEach(item=>{
    item.onclick=()=>{
      location.hash=`/lesson/${item.dataset.lesson}`;
    };
  });
}

function getCurrentMode(){
  const btn=document.querySelector('.mode-btn.active');
  return btn?.dataset.mode||'all';
}

initTheme();

// Mode filter buttons
$$('.mode-btn').forEach(btn=>{
  btn.addEventListener('click',()=>{
    $$('.mode-btn').forEach(b=>{b.classList.remove('active');b.setAttribute('aria-selected','false')});
    btn.classList.add('active');
    btn.setAttribute('aria-selected','true');
    const r=parseHash();
    updateSidebar(r.lessonId);
    if($('#indexView').classList.contains('active')) renderIndex();
  });
});

// ── Lesson View ─────────────────────────────────
async function renderLesson(id){
  const lesson=LESSONS.find(l=>l.id===id);
  if(!lesson){alert(`Lección ${id} no encontrada.`);return;}
  
  // Title & meta
  $('#lessonTitle').innerHTML=lesson.title;
  const typeInfo=lesson.type?`<span class="type-badge type-${lesson.type}" style="color:#fff;background:${TYPE_COLORS[lesson.type]}">${typeLabel(lesson.type)}</span> · `:'';
  $('#lessonMeta').innerHTML=`${typeInfo}${levelLabel(lesson.level)} · Módulo ${String(lesson.module).padStart(2,'0')}`;
  
  // Theory panel
  let theoryHTML=`<h2>Objetivo de la lección</h2><p>${lesson.objective||''}</p>`;
  // El concepto clave es prosa con markdown (`código` inline): crudo mostraba los backticks.
  if(lesson.keyConcept) theoryHTML+=`<div class="concept-box"><strong>Concepto clave:</strong> ${renderMarkdown(lesson.keyConcept,true)}</div>`;
  if(lesson.theory) theoryHTML+=`<h2>Teoría</h2>${renderMarkdown(lesson.theory)}`;
  if(lesson.example) theoryHTML+=`<h2>Ejemplo Pokémon</h2><pre class="ejemplo"><code>${highlightPython(lesson.example)}</code></pre>`;
  if(lesson.extraTheory) theoryHTML+=`<h2>Profundizando</h2>${renderMarkdown(lesson.extraTheory)}`;
  $('#theoryPanel').innerHTML=theoryHTML;
  
  // Exercise panel
  // El enunciado es prosa con markdown (**negrita**, `código`, saltos de línea):
  // inyectarlo crudo mostraba los asteriscos y colapsaba los saltos.
  const promptHTML=renderMarkdown(lesson.exercisePrompt||'Escribí el código necesario para completar cada ejercicio.');
  $('#exerciseDesc').innerHTML=`<strong>Tu turno.</strong> ${promptHTML}<br><em>Podés correr tu código con el botón <b>▶ Correr</b> o presionando <b>Ctrl+Enter</b>.</em>`;
  $('#editorLabel').textContent=lesson.codeFile||`lecci\u00f3n_${formatNumber(id)}.py`;
  
  // Load code template
  let codeTemplate='';
  try{
    const url=lesson.codeFile||`./lessons/${formatNumber(id)}.py`;
    const resp=await fetch(url);
    if(resp.ok) codeTemplate=await resp.text();
  }catch(e){}
  if(!codeTemplate && !lesson.codeTemplate){
    codeTemplate='# Escribí tu código aquí...\nprint("¡Empezando!")\n';
  }
  codeTemplate=codeTemplate||lesson.codeTemplate||'# Completá los ejercicios\nprint("Hello World")\n';
  
  clearErrorLine();
  setEditorText(codeTemplate);
  
  // Solution — only fetch a file the lesson declares, so lessons without one
  // don't fire a 404 in the console.
  let solution='';
  const surl=lesson.solutionFile;
  if(surl){
    try{
      const resp=await fetch(surl);
      if(resp.ok) solution=await resp.text();
    }catch(e){}
  }
  $('#solutionPanel').innerHTML=solution
    ?`<p>Solución completa:</p><div class="solution-code">${escapeHtml(solution)}</div>`
    :lesson.solution?`<p>Solución:</p><div class="solution-code">${escapeHtml(lesson.solution)}</div>`
    :'<p>Solución disponible cuando completes todos los tests.</p>';
  
  // Tests panel: vive abajo de la consola (pestaña Ejercicio), no en otra pestaña.
  renderTestsPanel(lesson);
  
  // Tab switching
  $$('.tab').forEach(tab=>{
    tab.onclick=()=>switchTab(tab.dataset.tab);
  });
  
  // Code editor events
  const editor=$('#codeEditor');
  editor.onkeydown=handleEditorKeydown;
  editor.oninput=()=>updateLineNumbers();
  
  // Run button
  $('#runBtn').onclick=handleRunCode;
  $('#resetBtn').onclick=()=>{
    setEditorText(codeTemplate);
    consoleClear();
    clearErrorLine();
    const actual=LESSONS.find(l=>l.id===state.currentLessonId)||lesson;
    resetTestStatuses(actual);
    updateTestsSummary(actual,0,(actual.tests||[]).length,'idle');
  };
  
  // Prev/Next
  const prev=LESSONS.find(l=>l.id===id-1);
  const next=LESSONS.find(l=>l.id===id+1);
  const prevBtn=$('#prevBtn');
  const nextBtn=$('#nextBtn');
  if(prev){prevBtn.disabled=false;prevBtn.onclick=()=>location.hash=`/lesson/${prev.id}`;}else{prevBtn.disabled=true;}
  if(next){nextBtn.disabled=false;nextBtn.onclick=()=>location.hash=`/lesson/${next.id}`;}else{nextBtn.disabled=true;}
  
  switchTab('teoria');
  state.currentLessonId=id;
}

function switchTab(tabName){
  $$('.tab').forEach(t=>{
    t.classList.toggle('active',t.dataset.tab===tabName);
    t.setAttribute('aria-selected',t.dataset.tab===tabName);
  });
  $$('.panel').forEach(p=>p.classList.toggle('active',p.dataset.panel===tabName));
}

// ── Editor helpers ──────────────────────────────
function handleEditorKeydown(e){
  if(e.key==='Tab'){
    e.preventDefault();
    const ed=e.target;
    const s=ed.selectionStart, en=ed.selectionEnd;
    ed.value=ed.value.substring(0,s)+'    '+ed.value.substring(en);
    ed.selectionStart=ed.selectionEnd=s+4;
    updateLineNumbers();
  }
  if((e.ctrlKey||e.metaKey)&&e.key==='Enter'){
    e.preventDefault();
    handleRunCode();
  }
}

function updateLineNumbers(){
  const editor=$('#codeEditor');
  if(!editor) return;
  const lines=editor.value.match(/\n/g);
  const n=(lines?lines.length:0)+1;
  // Cada número es un span: así se puede pintar en rojo SOLO la línea del error
  // (la gutter del textarea simple no admite decoraciones como CodeMirror).
  $('#lineNumbers').innerHTML=Array.from({length:n},(_,i)=>{
    const num=i+1;
    return `<span class="ln${num===errorLine?' ln-error':''}" data-line="${num}">${num}</span>`;
  }).join('\n');
}

// Línea marcada por el último error de ejecución (null = sin error).
let errorLine=null;

function markErrorLine(n){
  errorLine=Number.isInteger(n)&&n>0?n:null;
  updateLineNumbers();
  if(cmSetErrorLine) cmSetErrorLine(errorLine);
}

function clearErrorLine(){
  errorLine=null;
  updateLineNumbers();
  if(cmSetErrorLine) cmSetErrorLine(null);
}

// ── CodeMirror 6 (vendorizado) ───────────────────
// El textarea #codeEditor sigue siendo la única fuente de verdad: la app y la
// suite leen .value. CodeMirror es solo la vista. Si el bundle no carga, no se
// monta nada (sin body.has-cm) y el textarea queda visible y usable.
let cmView=null;
let cmAPI=null;
let cmExtensions=null;
let cmSetErrorLine=null;   // lo define buildCMExtensions: pinta la línea del error

// Seteo programático (carga de lección y botón Reset): cambia el textarea Y el
// documento del editor. setState además limpia el historial para que Ctrl+Z no
// traiga código de otra lección.
function setEditorText(text){
  const ta=$('#codeEditor');
  ta.value=text;
  if(cmView&&cmAPI){
    cmView.setState(cmAPI.EditorState.create({doc:text,extensions:cmExtensions}));
  }
  updateLineNumbers();
}

// textarea -> editor (los tests setean .value y disparan input). La app no
// necesita el evento inverso: lee .value bajo demanda.
function syncTextareaToEditor(){
  if(!cmView) return;
  const ta=$('#codeEditor');
  const doc=cmView.state.doc.toString();
  if(doc!==ta.value) cmView.dispatch({changes:{from:0,to:doc.length,insert:ta.value}});
}

// ── Autocompletado ───────────────────────────────
// Mismos nodos que lang-python excluye: nada de completar dentro de cadenas,
// comentarios ni propiedades (las fuentes propias también se envuelven con
// ifNotIn para no disparar en contextos que rompen la escritura).
const DONT_COMPLETE=['String','FormatString','Comment','PropertyName'];
const NO_STRINGS_COMMENTS=['String','FormatString','Comment'];

const PY_BUILTIN_FUNCS=['print','len','range','enumerate','zip','sorted','sum','min','max',
  'input','abs','round','isinstance','type','open','super','format','all','any','map','filter',
  'reversed','iter','next','hash','id','getattr','setattr','hasattr','bytes','bytearray',
  'frozenset','staticmethod','classmethod','property','dir','repr','hex','bin','ord'];
const PY_BUILTIN_CLASSES=['str','int','float','list','dict','set','tuple','object',
  'Exception','ValueError','TypeError','KeyError'];
const PY_METHOD_NAMES=['upper','lower','title','capitalize','strip','split','join','replace',
  'startswith','endswith','find','index','count','format','encode','decode','isdigit','isalpha',
  'isspace','islower','isupper','istitle','append','extend','insert','remove','pop','clear',
  'sort','reverse','copy','update','keys','values','items','get','add','discard','union','intersection'];
const PY_BUILTINS=PY_BUILTIN_FUNCS.map(label=>({label,type:'function',detail:'integrada'}))
  .concat(PY_BUILTIN_CLASSES.map(label=>({label,type:'class',detail:'clase'})));
const PY_METHOD_OPTIONS=PY_METHOD_NAMES.map(label=>({label,type:'method',detail:'método'}));

// (b) builtins curados. (a) los nombres del documento y los builtins de
// lang-python ya vienen con python() (localCompletionSource + globalCompletion).
function builtinSource(context){
  try{
    if(context.matchBefore(/\.\w*$/)) return null; // tras un punto: métodos / Pyodide
    const word=context.matchBefore(/\w+/);
    if(!word&&!context.explicit) return null;
    return {options:PY_BUILTINS,from:word?word.from:context.pos,validFor:/^[\w]*$/};
  }catch(e){ return null; }
}

// Métodos tras un punto (lista estática). Los flotantes (3.14) no son objetos.
function methodSource(context){
  try{
    const m=context.matchBefore(/\.\w*/);
    if(!m) return null;
    const dot=m.text.indexOf('.');
    if(/^\d/.test(m.text.slice(dot+1))) return null;
    return {options:PY_METHOD_OPTIONS,from:m.from+dot+1,validFor:/^[\w]*$/};
  }catch(e){ return null; }
}

// Código Python para dir(): resultado en _pokpy_result (no dependemos del
// valor de retorno de runPythonAsync) y firmas solo cuando son baratas.
function pyodideDirCode(expr){
  return [
    '_pokpy_result = None',
    'import json, inspect',
    'def _pokpy_dir(expr):',
    '    try:',
    '        obj = eval(expr, globals())',
    '    except Exception:',
    '        return None',
    '    out = []',
    '    for name in dir(obj):',
    "        if name.startswith('_'):",
    '            continue',
    "        detail, typ = '', 'property'",
    '        try:',
    '            member = getattr(obj, name)',
    '            if callable(member):',
    "                typ = 'method'",
    '                try:',
    '                    detail = str(inspect.signature(member))',
    '                except (ValueError, TypeError):',
    "                    detail = ''",
    '        except Exception:',
    '            pass',
    "        out.append({'label': name, 'type': typ, 'detail': detail})",
    '    return json.dumps(out)',
    '_pokpy_result = _pokpy_dir(' + JSON.stringify(expr) + ')',
  ].join('\n');
}

function parseMemberOptions(raw){
  if(typeof raw!=='string') return null;
  try{
    const arr=JSON.parse(raw);
    if(!Array.isArray(arr)) return null;
    return arr.filter(m=>m&&typeof m.label==='string').map(m=>({
      label:m.label,
      type:m.type==='method'?'method':'property',
      detail:m.detail?String(m.detail):undefined,
    }));
  }catch(e){ return null; }
}

// (c) Pyodide: dir() real sobre la expresión antes del cursor. Fuente async con
// timeout: si Pyodide no está listo, la expresión es desconocida o la llamada
// falla, devuelve null rápido y nunca lanza (un throw cerraría el popup).
function pyodideMemberSource(context){
  try{
    if(!state.pyodideReady||!state.pyodide) return null;
    const before=context.matchBefore(/[\w.]+/);
    if(!before) return null;
    const dot=before.text.lastIndexOf('.');
    if(dot<1) return null; // solo expresiones con punto (obj.miembro)
    const obj=before.text.slice(0,dot);
    if(!/^[A-Za-z_]\w*(\.[A-Za-z_]\w*)*$/.test(obj)) return null;
    let pending;
    try{
      pending=Promise.resolve(state.pyodide.runPythonAsync(pyodideDirCode(obj)))
        .then(()=>true,()=>false);
    }catch(e){ return null; }
    const slow=new Promise(resolve=>{setTimeout(()=>resolve('timeout'),1500);});
    return Promise.race([pending,slow]).then(status=>{
      if(status!==true) return null; // timeout o error: no completar
      let raw;
      try{ raw=state.pyodide.globals.get('_pokpy_result'); }catch(e){ return null; }
      const options=parseMemberOptions(raw);
      if(!options||!options.length) return null;
      return {from:before.from+dot+1,options,validFor:/^[\w]*$/};
    }).catch(()=>null);
  }catch(e){ return null; }
}

// Tema: SOLO var(--token) — cero hex en JS. El paleta --syn-* vive en
// styles.css en ambos temas, así el toggle de tema repinta sin JS ni remount.
function cmEditorTheme(cm){
  const {EditorView,HighlightStyle,tags:t}=cm;
  const highlight=HighlightStyle.define([
    {tag:t.comment,color:'var(--syn-comment)'},
    {tag:t.string,color:'var(--syn-string)'},
    {tag:t.escape,color:'var(--syn-string)'},
    {tag:t.number,color:'var(--syn-number)'},
    {tag:t.bool,color:'var(--syn-number)'},
    {tag:t.keyword,color:'var(--syn-keyword)'},
    {tag:t.operator,color:'var(--syn-operator)'},
    {tag:t.punctuation,color:'var(--syn-operator)'},
    {tag:t.bracket,color:'var(--syn-operator)'},
    {tag:t.variableName,color:'var(--text-primary)'},
    {tag:t.propertyName,color:'var(--text-primary)'},
    {tag:t.typeName,color:'var(--syn-function)'},
    {tag:t.className,color:'var(--syn-function)'},
    {tag:t.function(t.variableName),color:'var(--syn-function)'},
    {tag:t.function(t.definition(t.variableName)),color:'var(--syn-function)'},
    {tag:t.function(t.propertyName),color:'var(--syn-function)'},
    {tag:t.definition(t.className),color:'var(--syn-function)'},
    {tag:t.meta,color:'var(--text-muted)'},
    {tag:t.invalid,color:'var(--accent-red)'},
  ]);
  const theme=EditorView.theme({
    '&':{
      height:'100%',
      background:'var(--bg-code)',
      color:'var(--text-primary)',
      fontFamily:'var(--font-mono)',
      fontSize:'.8rem',
      borderRadius:'var(--radius-sm)',
      overflow:'hidden',
    },
    '.cm-scroller':{
      fontFamily:'var(--font-mono)',
      lineHeight:'1.75',
      scrollbarColor:'var(--border-accent) transparent',
      scrollbarWidth:'thin',
    },
    '.cm-scroller::-webkit-scrollbar':{width:'8px',height:'8px'},
    '.cm-scroller::-webkit-scrollbar-thumb':{
      background:'var(--border-accent)',
      borderRadius:'999px',
    },
    '.cm-scroller::-webkit-scrollbar-track':{background:'transparent'},
    '.cm-content':{
      fontFamily:'var(--font-mono)',
      lineHeight:'1.75',
      color:'var(--text-primary)',
      background:'var(--bg-code)',
      caretColor:'var(--accent-strong)',
    },
    '.cm-gutters':{
      background:'var(--bg-code)',
      borderRight:'1px solid var(--border-subtle)',
      color:'var(--text-muted)',
      fontFamily:'var(--font-mono)',
      lineHeight:'1.75',
    },
    '.cm-lineNumbers .cm-gutterElement':{color:'var(--text-muted)'},
    '.cm-activeLine':{background:'var(--bg-raised)'},
    '.cm-activeLineGutter':{background:'var(--bg-raised)'},
    '.cm-selectionBackground, .cm-content ::selection':{background:'var(--accent-line)'},
    '&.cm-focused > .cm-scroller > .cm-selectionLayer .cm-selectionBackground':{
      background:'var(--accent-line)',
    },
    '.cm-cursor, .cm-dropCursor':{borderLeftColor:'var(--accent-strong)'},
    '.cm-matchingBracket, &.cm-focused .cm-matchingBracket':{
      background:'var(--accent-soft)',
      outline:'1px solid var(--accent-line)',
    },
    '&.cm-focused':{outline:'none',boxShadow:'var(--ring)'},
    '.cm-tooltip':{
      background:'var(--bg-raised)',
      border:'1px solid var(--border-subtle)',
      boxShadow:'var(--shadow-md)',
      color:'var(--text-primary)',
      fontFamily:'var(--font-mono)',
      fontSize:'.78rem',
    },
    '.cm-tooltip.cm-tooltip-autocomplete > ul':{fontFamily:'var(--font-mono)'},
    '.cm-tooltip.cm-tooltip-autocomplete ul li[aria-selected]':{
      background:'var(--accent-soft)',
      color:'var(--text-primary)',
    },
  });
  return {theme,highlight};
}

function buildCMExtensions(cm){
  const {EditorView,EditorState,keymap,lineNumbers,highlightActiveLine,highlightActiveLineGutter,
    drawSelection,history,bracketMatching,indentOnInput,indentUnit,syntaxHighlighting,
    defaultKeymap,historyKeymap,indentMore,indentLess,autocompletion,ifNotIn,
    acceptCompletion,completionStatus,python,pythonLanguage}=cm;
  const {theme,highlight}=cmEditorTheme(cm);

  // La gutter de CodeMirror reemplaza a la del textarea cuando el bundle carga:
  // el resaltado de la línea con error tiene que existir también acá.
  const {StateField,StateEffect,Decoration}=cm;
  const setErrorLine=StateEffect.define();
  const errorLineField=StateField.define({
    create:()=>Decoration.none,
    update(deco,tr){
      let next=deco.map(tr.changes);
      for(const effect of tr.effects){
        if(!effect.is(setErrorLine)) continue;
        if(effect.value==null){ next=Decoration.none; continue; }
        const lineNumber=Math.min(Math.max(1,Number(effect.value)||1),tr.state.doc.lines);
        next=Decoration.set([
          Decoration.line({class:'cm-error-line'}).range(tr.state.doc.line(lineNumber).from),
        ]);
      }
      return next;
    },
    provide:field=>EditorView.decorations.from(field),
  });
  cmSetErrorLine=n=>{
    try{
      if(cmView) cmView.dispatch({effects:setErrorLine.of(n==null?null:n)});
    }catch(e){}
  };

  const editorKeymap=[
    // Ctrl/Cmd+Enter corre el código: mismo handler que el botón ▶ Correr.
    {key:'Mod-Enter',run:()=>{handleRunCode();return true;}},
    // Tab indenta; con el popup abierto lo acepta en vez de salir del editor.
    {key:'Tab',run:view=>{
      const s=completionStatus(view.state);
      if(s==='active') return acceptCompletion(view);
      if(s==='pending') return true;
      return indentMore(view);
    },shift:indentLess},
    ...defaultKeymap,
    ...historyKeymap,
  ];

  return [
    python(),
    lineNumbers(),
    highlightActiveLineGutter(),
    highlightActiveLine(),
    drawSelection(),
    history(),
    bracketMatching(),
    indentOnInput(),
    EditorState.tabSize.of(4),
    indentUnit.of('    '),
    theme,
    errorLineField,
    syntaxHighlighting(highlight),
    autocompletion({icons:false}),
    pythonLanguage.data.of({autocomplete:ifNotIn(DONT_COMPLETE,builtinSource)}),
    pythonLanguage.data.of({autocomplete:ifNotIn(NO_STRINGS_COMMENTS,methodSource)}),
    pythonLanguage.data.of({autocomplete:ifNotIn(NO_STRINGS_COMMENTS,pyodideMemberSource)}),
    keymap.of(editorKeymap),
    EditorView.contentAttributes.of({'aria-label':'Editor de código'}),
    EditorView.updateListener.of(update=>{
      if(update.docChanged){
        $('#codeEditor').value=update.state.doc.toString();
        updateLineNumbers();
      }
    }),
  ];
}

// Montaje progresivo: si el import o la construcción fallan, no se agrega
// body.has-cm y el textarea queda visible y usable como siempre.
async function initCodeMirror(){
  const ta=$('#codeEditor');
  const host=$('#editorHost');
  if(!ta||!host) return;
  try{
    const cm=await import('./vendor/codemirror.bundle.js?v=2026-11-08-a');
    cmAPI=cm;
    cmExtensions=buildCMExtensions(cm);
    ta.addEventListener('input',syncTextareaToEditor);
    cmView=new cm.EditorView({
      state:cm.EditorState.create({doc:ta.value,extensions:cmExtensions}),
      parent:host,
    });
    document.body.classList.add('has-cm');
  }catch(err){
    console.warn('CodeMirror no disponible; se usa el textarea simple.',err);
  }
}

function consoleLog(msg,cls=''){
  const out=$('#consoleOutput');
  const line=document.createElement('div');
  if(cls) line.className=cls;
  line.textContent=msg;
  out.appendChild(line);
  out.scrollTop=out.scrollHeight;
}

function consoleClear(){
  // Vaciar, no volver a poner el placeholder: si se inyecta, queda arriba de la
  // salida real y parece que el programa no imprimió nada.
  $('#consoleOutput').innerHTML='';
}

function firstLine(text){
  return String(text||'').split('\n').map(l=>l.trim()).filter(Boolean)[0]||'';
}

// El traceback de Pyodide trae frames internos (_base.py) que no dicen nada: el
// frame real es `<exec>`. Extraemos línea, tipo y mensaje para que la consola
// responda "dónde" y "qué", en vez de mostrar solo el encabezado del traceback.
function parsePythonError(err, code){
  let raw;
  try{ raw=String(err); }catch(e){ raw='Error desconocido'; }
  const rawLines=raw.split('\n');
  const codeLines=String(code||'').split('\n');
  const execFrame=/File "<(?:exec|string|console)>", line (\d+)(.*)$/;
  let lineNo=null;
  let sourceLine='';
  let column=null;
  for(let i=0;i<rawLines.length;i++){
    const match=execFrame.exec(rawLines[i]);
    if(!match) continue;
    lineNo=Number(match[1]);
    // Sin ", in ..." el frame es de compilación: la línea siguiente es el
    // código culpable y la próxima, el caret que marca la columna.
    if(!/,\s*in\s+/.test(match[2])){
      const next=rawLines[i+1]||'';
      if(next.trim()) sourceLine=next.replace(/^ {0,4}/,'');
      const caret=rawLines[i+2]||'';
      if(/^\s*\^+\s*$/.test(caret)) column=caret.indexOf('^')+1;
    }
  }
  if(!sourceLine&&lineNo&&codeLines[lineNo-1]!==undefined) sourceLine=codeLines[lineNo-1];

  // La última línea con forma "TipoError: mensaje" es la excepción real (el
  // resto del traceback son frames internos).
  let kind='Error';
  let message='';
  for(let i=rawLines.length-1;i>=0;i--){
    const text=rawLines[i].trim();
    const match=/^([A-Za-z_][\w.]*(?:Error|Exception|Interrupt|Exit|Warning))(?::\s*([\s\S]*))?$/.exec(text);
    if(!match) continue;
    const continuacion=rawLines.slice(i+1).map(l=>l.trim()).filter(Boolean);
    kind=match[1];
    message=[(match[2]||'').trim(),...continuacion].filter(Boolean).join(' ');
    break;
  }
  if(!message&&rawLines.length) message=rawLines[rawLines.length-1].trim();
  return {raw,lineNo,sourceLine,column,kind,message};
}

function showRunError(err, code){
  const info=parsePythonError(err, code);
  // Hook de diagnóstico: la suite de navegador lee el traceback crudo sin
  // depender del texto formateado de la consola.
  window.__lastRunError={raw:info.raw,line:info.lineNo,kind:info.kind,message:info.message};

  const donde=info.lineNo?`la línea ${info.lineNo}`:'una línea desconocida';
  const detalle=info.message?`${info.kind}: ${info.message}`:info.kind;
  consoleLog(`✗ Error en ${donde} — ${detalle}`,'error');
  if(info.sourceLine) consoleLog(`${info.lineNo||''} │ ${info.sourceLine}`,'error-source');
  if(info.column) consoleLog(`  ↳ columna ${info.column}`,'error-meta');

  const out=$('#consoleOutput');
  const details=document.createElement('details');
  details.className='console-details';
  const summary=document.createElement('summary');
  summary.textContent='Ver traceback completo';
  const pre=document.createElement('pre');
  pre.textContent=info.raw;
  details.appendChild(summary);
  details.appendChild(pre);
  out.appendChild(details);
  out.scrollTop=out.scrollHeight;

  markErrorLine(info.lineNo);
}

// ── Code Execution (Pyodide) ────────────────────
// stdout/stderr de Pyodide → consola de la página. Sin esto, print() solo
// llega a la consola del navegador (F12) y #consoleOutput queda vacío.
// Cada chunk se parte por línea para que cada línea de Python sea un div.
function routePyodideOutput(py){
  if(!py) return;
  const emit=(chunk,cls)=>{
    String(chunk).split('\n').forEach(line=>{
      if(line.length) consoleLog(line,cls);
    });
  };
  if(typeof py.setStdout==='function') py.setStdout({batched:s=>emit(s,'')});
  if(typeof py.setStderr==='function') py.setStderr({batched:s=>emit(s,'error')});
}

// Carga Pyodide una sola vez y ESPERA a que esté listo. Antes devolvía al
// instante cuando había que inyectar el <script>, así que la primera corrida
// seguía de largo sin runtime y los tests quedaban en "?" para siempre.
let pyodideLoading=null;
// La corrida y la evaluación de tests son una sola operación: si el botón se
// clickea dos veces, la segunda no pisa el estado de la primera.
let runInFlight=false;

function initPyodide(){
  if(state.pyodideReady) return Promise.resolve(true);
  if(pyodideLoading) return pyodideLoading;

  pyodideLoading=(async()=>{
    consoleLog('· Cargando Python en tu navegador…','info');
    $('#consoleStatus').textContent='Cargando...';
    try{
      if(!window.loadPyodide){
        await new Promise((resolve,reject)=>{
          const script=document.createElement('script');
          // Local, no CDN: funciona offline y el navegador no bloquea storage
          // de terceros (los avisos de "Tracking Prevention" en Edge).
          script.src='./vendor/pyodide/pyodide.js';
          script.onload=resolve;
          script.onerror=()=>reject(new Error('no se pudo descargar Pyodide'));
          document.head.appendChild(script);
        });
      }
      state.pyodide=await window.loadPyodide({ indexURL: './vendor/pyodide/' });
      routePyodideOutput(state.pyodide);
      state.pyodideReady=true;
      consoleLog('✓ Python listo. Ya podés ejecutar código.','success');
      $('#consoleStatus').textContent='Listo';
      return true;
    }catch(err){
      const motivo=(err&&err.message)||String(err);
      consoleLog(`✗ No se pudo iniciar Python (${motivo}). Revisá la conexión y volvé a intentar con ▶ Correr.`,'error');
      $('#consoleStatus').textContent='Sin conexión';
      return false;
    }finally{
      pyodideLoading=null;
    }
  })();

  return pyodideLoading;
}

async function handleRunCode(){
  if(runInFlight) return;   // una corrida a la vez: nada de estados cruzados
  runInFlight=true;
  const runBtn=$('#runBtn');
  if(runBtn){ runBtn.disabled=true; runBtn.classList.add('is-running'); }
  const lesson=LESSONS.find(l=>l.id===state.currentLessonId)||null;

  clearErrorLine();
  resetTestStatuses(lesson);
  window.__lastRunError=null;
  try{
    if(!state.pyodideReady){
      const listo=await initPyodide();
      if(!listo){
        updateTestsSummary(lesson,0,(lesson?.tests||[]).length,'idle');
        return;   // initPyodide ya explicó el motivo en la consola
      }
    }

    // Re-enganchar stdout/stderr en cada corrida: si una corrida anterior dejó
    // el runtime en un estado raro, la consola vuelve a recibir la salida.
    routePyodideOutput(state.pyodide);

    const code=$('#codeEditor').value;
    consoleClear();
    $('#consoleStatus').textContent='Ejecutando…';
    let failed=false;

    try{
      const output=await state.pyodide.runPythonAsync(code);
      if(output!==undefined&&output!==null){
        consoleLog(String(output),'success');
      }
      consoleLog('— Código ejecutado sin errores.','info');
    }catch(err){
      failed=true;
      showRunError(err, code);
    }

    // Los tests se evalúan SIEMPRE, también cuando el código lanzó: antes un
    // error de Python dejaba el panel en "?" para siempre y parecía muerto.
    if(lesson&&(lesson.tests||[]).length){
      const resultado=await runTests(lesson, code);
      if(resultado){
        const fallan=resultado.total-resultado.passed;
        if(fallan===0&&!failed) consoleLog(`✓ ${resultado.passed}/${resultado.total} retos cumplidos.`,'success');
        else if(fallan===0) consoleLog(`✓ ${resultado.passed}/${resultado.total} retos cumplidos (aunque el código lanzó un error).`,'info');
        else consoleLog(`✗ ${fallan} de ${resultado.total} retos sin cumplir: revisá la tabla de tests.`,'error');
      }
    }
    $('#consoleStatus').textContent=failed?'Error':'Listo';
  }catch(err){
    // Fallo inesperado del arnés (no de Python): la consola nunca queda muerta.
    consoleLog(`✗ Falló la ejecución: ${firstLine(err)||String(err)}`,'error');
    $('#consoleStatus').textContent='Error';
  }finally{
    runInFlight=false;
    if(runBtn){ runBtn.disabled=false; runBtn.classList.remove('is-running'); }
  }
}

// ── Test Runner ───────────────────────────────────────────────
// Quita comentarios (# …) y docstrings (triple comilla que abre una sentencia)
// antes de matchear: las consignas citan la salida esperada en comentarios y,
// sin este paso, un starter intacto aprueba sus propios tests (L14 / L26).
// ESPEJO EXACTO de tests/py_matcher.py::strip_python_noise — cambiar juntos.
function stripPythonNoise(src){
  let out='';
  let i=0;
  const n=src.length;
  let prev='';   // último código no vacío visto (los comentarios no lo tocan)
  let depth=0;   // profundidad de ( [ { — dentro de un paréntesis no hay docstring
  while(i<n){
    const c=src[i];
    // Triple comilla: docstring (se descarta) o cadena multilinea (se conserva)
    if(src.startsWith('"""',i)||src.startsWith("'''",i)){
      const q=src.substr(i,3);
      const isDoc=depth===0&&(prev===''||prev===':');
      let j=i+3;
      let closed=false;
      while(j<n){
        if(src[j]==='\\'){j+=2;continue;}
        if(src.startsWith(q,j)){j+=3;closed=true;break;}
        j++;
      }
      if(!closed) j=n; // sin cierre: se lleva el resto
      if(!isDoc){ out+=src.slice(i,j); prev='"'; }
      i=j;
      continue;
    }
    // Cadena de una línea (con escapes; corta en fin de línea si no cierra)
    if(c==='"'||c==="'"){
      let j=i+1;
      while(j<n){
        if(src[j]==='\\'){j+=2;continue;}
        if(src[j]===c){j++;break;}
        if(src[j]==='\n') break;
        j++;
      }
      out+=src.slice(i,j);
      prev='"';
      i=j;
      continue;
    }
    // Comentario hasta fin de línea (solo fuera de cadenas: print("#") conserva el #)
    if(c==='#'){
      while(i<n&&src[i]!=='\n') i++;
      continue;
    }
    out+=c;
    if(c==='('||c==='['||c==='{') depth++;
    else if(c===')'||c===']'||c==='}') depth=Math.max(0,depth-1);
    if(!/\s/.test(c)) prev=c;
    i++;
  }
  return out;
}

// Expect y código a solo minúsculas alfanuméricas: el fallback de los expects
// con == quitaba puntuación SOLO del expect y nunca matcheaba (L28).
function matcherClean(s){
  return s.toLowerCase().replace(/[^a-z0-9]/g,'');
}

// ── Panel de tests ────────────────────────────────────────────
// Tabla siempre visible abajo de la consola: estado, reto y qué se espera.
// Conserva #testsPanel, .test-item, .test-status y #ts-<id> (contratos de la
// suite) pero deja de ser una pestaña aparte.
function renderTestsPanel(lesson){
  const panel=$('#testsPanel');
  if(!panel) return;
  const tests=lesson.tests||[];
  if(!tests.length){
    panel.innerHTML='<div class="concept-box">No hay tests obligatorios. Explorá libremente y experimentá con el código.</div>';
    updateTestsSummary(lesson,0,0,'idle');
    return;
  }
  panel.innerHTML=`<table class="tests-table" aria-label="Tests del ejercicio">
    <thead><tr><th class="col-status" scope="col">Estado</th><th scope="col">Reto</th><th scope="col">Qué se espera</th></tr></thead>
    <tbody>${tests.map(t=>`
      <tr class="test-item" data-test-id="${escapeHtml(String(t.id))}">
        <td class="col-status"><span class="test-status test-pending" id="ts-${escapeHtml(String(t.id))}" role="img" aria-label="Pendiente">?</span></td>
        <td><strong>${escapeHtml(String(t.name||'Reto'))}</strong>${t.description?`<p class="test-desc">${escapeHtml(String(t.description))}</p>`:''}</td>
        <td>${t.expect?`<code class="test-expect">${escapeHtml(String(t.expect))}</code>`:''}<p class="test-fail-detail" id="td-${escapeHtml(String(t.id))}"></p></td>
      </tr>`).join('')}</tbody></table>`;
  updateTestsSummary(lesson,0,tests.length,'idle');
}

// Repone todos los retos a "?" antes de cada corrida y durante Reset: sin esto
// los estados del run anterior quedaban pegados y la tabla mentía.
function resetTestStatuses(lesson){
  const tests=(lesson&&lesson.tests)||[];
  for(const test of tests){
    const status=$(`#ts-${test.id}`);
    if(status){
      status.className='test-status test-pending';
      status.textContent='?';
      status.setAttribute('aria-label','Pendiente');
    }
    const detail=$(`#td-${test.id}`);
    if(detail) detail.textContent='';
  }
  updateTestsSummary(lesson,0,tests.length,'running');
  const wrap=$('#testsWrap');
  if(wrap) wrap.classList.remove('has-failure');
}

function updateTestsSummary(lesson, passed, total, mode){
  const el=$('#testsSummary');
  if(!el) return;
  el.classList.remove('is-ok','is-fail');
  const n=Number(total)||0;
  if(!lesson||!n){ el.textContent='Sin retos'; return; }
  if(mode==='running'){ el.textContent=`Corriendo… 0/${n}`; return; }
  if(mode==='idle'){ el.textContent=`Sin correr · ${n} retos`; return; }
  const fallan=n-passed;
  // La cruz roja con el resumen es la señal de "ejercicio mal hecho" (S5).
  el.textContent=fallan===0?`✓ ${passed}/${n} retos OK`:`✗ ${fallan} de ${n} retos fallan`;
  el.classList.add(fallan===0?'is-ok':'is-fail');
  const wrap=$('#testsWrap');
  if(wrap) wrap.classList.toggle('has-failure',fallan>0);
}

async function evaluateTest(test, code){
  if(test.validate){
    return {passed:Boolean(test.validate(code))};
  }
  if(test.pythonTest){
    try{
      const result=await state.pyodide.runPythonAsync(test.pythonTest(code));
      return {passed:result===true||String(result)==='True'};
    }catch(e){
      return {passed:false,detalle:`El test no se pudo ejecutar: ${firstLine(e)||'error de Python'}`};
    }
  }
  if(test.expect){
    // Código REAL, en minúsculas, sin comentarios ni docstrings
    // (espejo en tests/py_matcher.py).
    const normalized=stripPythonNoise(code).toLowerCase();
    const expected=test.expect.toLowerCase();

    if(expected.includes('assert ')||expected.includes('==')||expected.includes('!=')){
      // Correrlo como Python es un intento OPCIONAL: solo puede mejorar el
      // resultado (L28). SyntaxError o False → comparación normalizada.
      try{
        const res=await state.pyodide.runPythonAsync(test.expect);
        if(res===true) return {passed:true};
      }catch(e){ /* esperado: el expect es un fragmento, no un programa */ }
      if(matcherClean(normalized).includes(matcherClean(expected))) return {passed:true};
      return {passed:false,detalle:`Falta en tu código: ${test.expect}`};
    }
    if(normalized.includes(expected)) return {passed:true};
    return {passed:false,detalle:`Falta en tu código: ${test.expect}`};
  }
  return {passed:false,detalle:'El reto no tiene criterio de evaluación.'};
}

async function runTests(lesson, code){
  if(!state.pyodideReady) return null;
  const tests=lesson.tests||[];
  let passed=0;
  for(const test of tests){
    let resultado;
    try{
      resultado=await evaluateTest(test, code);
    }catch(e){
      resultado={passed:false,detalle:`No se pudo evaluar: ${firstLine(e)||'error inesperado'}`};
    }

    const statusEl=$(`#ts-${test.id}`);
    if(statusEl){
      statusEl.className=`test-status ${resultado.passed?'test-pass':'test-fail'}`;
      statusEl.textContent=resultado.passed?'✓':'✗';
      statusEl.setAttribute('aria-label',resultado.passed?'Cumplido':'Falló');
    }
    const detailEl=$(`#td-${test.id}`);
    if(detailEl) detailEl.textContent=resultado.passed?'':(resultado.detalle||'No cumple lo que pide el reto.');

    if(resultado.passed){
      passed++;
      markCompleted(lesson.id);
    }
  }
  updateTestsSummary(lesson,passed,tests.length,'done');
  return {passed,total:tests.length};
}

// ── Init ────────────────────────────────────────
document.addEventListener('DOMContentLoaded', async()=>{
  await loadData();
  updateHeroStats();
  updateProgress();
  navigate();
  window.addEventListener('hashchange',navigate);
  
  // Keyboard shortcuts
  document.addEventListener('keydown',(e)=>{
    if((e.ctrlKey||e.metaKey)&&e.key==='ArrowLeft'){
      const r=parseHash();
      if(r.lessonId){
        const prev=LESSONS.find(l=>l.id===r.lessonId-1);
        if(prev) location.hash=`/lesson/${prev.id}`;
      }
    }
    if((e.ctrlKey||e.metaKey)&&e.key==='ArrowRight'){
      const r=parseHash();
      if(r.lessonId){
        const next=LESSONS.find(l=>l.id===r.lessonId+1);
        if(next) location.hash=`/lesson/${next.id}`;
      }
    }
  });
});

// Arranque del editor (al final del módulo: todo ya está definido).
initCodeMirror();
