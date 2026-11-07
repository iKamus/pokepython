/* ═══════════════════════════════════════════════════
   PokéPython — Curso interactivo de Python con Pokémon
   SPA con routing hash, Pyodide para ejecución local
   ═══════════════════════════════════════════════════ */

console.info('PokéPython build: 2026-11-07-md');

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
// Bloques primero: fences, tablas y listas. Si las reglas inline corren antes, el
// fence ```python se lo come el regex de `código` (quedaba un <code> gigante y un
// backtick huérfano) y las tablas y listas salían con barras y guiones literales.
function renderMarkdown(t){
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
      guardar(`<pre><code>${escapeHtml(codigo.replace(/\n$/,''))}</code></pre>`))
    .replace(/(?:^\|.*\|[ \t]*\n?){2,}/gm,bloque=>guardar(tabla(bloque.trim().split('\n'))))
    .replace(/(?:^[ \t]*[-*] .*\n?)+/gm,bloque=>guardar(`<ul>${items(bloque,/^[ \t]*[-*] /)}</ul>`))
    .replace(/(?:^\d+\. .*\n?)+/gm,bloque=>guardar(`<ol>${items(bloque,/^\d+\. /)}</ol>`));

  out=out
    .replace(/^(#{1,6}) (.+)$/gm,(_,nivel,titulo)=>`<${nivel.length<=2?'h2':'h3'}>${titulo}</${nivel.length<=2?'h2':'h3'}>`);
  out=inline(out).replace(/\n/g,'<br>');

  // Los <br> de alrededor eran los saltos que el texto tenía antes del bloque.
  const B='(?:pre|ul|ol|table|div)';
  return out
    .replace(/\u0000(\d+)\u0000/g,(_,i)=>bloques[Number(i)])
    .replace(new RegExp(`(?:<br>\\s*)+(</?${B}[^>]*>)`,'g'),'$1')
    .replace(new RegExp(`(</?${B}[^>]*>)\\s*(?:<br>)+`,'g'),'$1');
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
  if(lesson.keyConcept) theoryHTML+=`<div class="concept-box"><strong>Concepto clave:</strong> ${renderMarkdown(lesson.keyConcept)}</div>`;
  if(lesson.theory) theoryHTML+=`<h2>Teoría</h2>${renderMarkdown(lesson.theory)}`;
  if(lesson.example) theoryHTML+=`<h2>Ejemplo Pokémon</h2><pre>${escapeHtml(lesson.example)}</pre>`;
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
  
  // Tests panel
  const tests=lesson.tests||[];
  $('#testsPanel').innerHTML=tests.length>0
    ?tests.map(t=>`
      <div class="test-item" data-test-id="${t.id}">
        <span class="test-status test-pending" id="ts-${t.id}">?</span>
        <div>
          <strong>${t.name}</strong>
          <p style="font-size:.8rem;color:var(--text-muted);margin-top:2px;">${t.description||''}</p>
          ${t.expect?`<code style="font-size:.75rem;background:var(--bg-deep);padding:1px 6px;border-radius:3px;margin-top:4px;display:inline-block;">${escapeHtml(t.expect)}</code>`:''}
        </div>
      </div>`).join('')
    :`<div class="concept-box">No hay tests obligatorios. Explorá libremente y experimentá con el código.</div>`;
  
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
  const val=$('#codeEditor').value;
  const lines=val.match(/\n/g);
  const n=(lines?lines.length:0)+1;
  $('#lineNumbers').textContent=Array.from({length:n},(_,i)=>i+1).join('\n');
}

// ── CodeMirror 6 (vendorizado) ───────────────────
// El textarea #codeEditor sigue siendo la única fuente de verdad: la app y la
// suite leen .value. CodeMirror es solo la vista. Si el bundle no carga, no se
// monta nada (sin body.has-cm) y el textarea queda visible y usable.
let cmView=null;
let cmAPI=null;
let cmExtensions=null;

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
    const cm=await import('./vendor/codemirror.bundle.js?v=2026-11-07-md');
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
  if(!state.pyodideReady){
    const listo=await initPyodide();
    if(!listo) return;   // initPyodide ya explicó el motivo en la consola
  }
  
  const code=$('#codeEditor').value;
  consoleClear();
  $('#consoleStatus').textContent='Ejecutando...';
  
  try{
    const output=await state.pyodide.runPythonAsync(code);
    if(output!==undefined&&output!==null){
      consoleLog(String(output),'success');
    }
    consoleLog('— Código ejecutado sin errores.','info');
    $('#consoleStatus').textContent='Listo';

    // Auto-run tests
    if(state.currentLessonId){
      const lesson=LESSONS.find(l=>l.id===state.currentLessonId);
      if(lesson?.tests?.length>0){
        setTimeout(()=>runTests(lesson,code),500);
      }
    }
  }catch(err){
    // Antes se mostraba solo la primera línea, que en un traceback de Python
    // es "PythonError: Traceback (most recent call last):" y no dice nada.
    const lineas=String(err).split('\n').filter(l=>l.trim());
    const detalle=lineas.length>1?lineas.slice(0,4).join('\n'):lineas[0]||String(err);
    consoleLog(detalle,'error');
    $('#consoleStatus').textContent='Error';
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

async function runTests(lesson, code){
  if(!state.pyodideReady) return;
  
  for(const test of lesson.tests){
    try{
      let passed=false;
      
      if(test.validate){
        passed=test.validate(code);
      } else if(test.pythonTest){
        // Run a python assertion
        const result=await state.pyodide.runPythonAsync(test.pythonTest(code));
        passed=result===true||String(result)==='True';
      } else if(test.expect){
        // Código REAL, en minúsculas, sin comentarios ni docstrings
        // (espejo en tests/py_matcher.py).
        const normalized=stripPythonNoise(code).toLowerCase();
        const expected=test.expect.toLowerCase();
        
        if(expected.includes('assert ')||expected.includes('==')||expected.includes('!=')){
          // Correrlo como Python es un intento OPCIONAL: solo puede mejorar el
          // resultado (L28). SyntaxError o False → comparación normalizada.
          try{
            const res=await state.pyodide.runPythonAsync(test.expect);
            if(res===true) passed=true;
          }catch(e){ /* esperado: el expect es un fragmento, no un programa */ }
          if(!passed){
            passed=matcherClean(normalized).includes(matcherClean(expected));
          }
        } else {
          passed=normalized.includes(expected);
        }
      }
      
      const statusEl=$(`#ts-${test.id}`);
      if(statusEl){
        statusEl.className=`test-status ${passed?'test-pass':'test-fail'}`;
        statusEl.textContent=passed?'✓':'✗';
      }
      
      if(passed) markCompleted(lesson.id);
    }catch(e){
      const statusEl=$(`#ts-${test.id}`);
      if(statusEl){
        statusEl.className='test-status test-fail';
        statusEl.textContent='✗';
      }
    }
  }
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
