document.getElementById('run-btn').addEventListener('click', () => {
  /* ───────── 1.  PARSE SOURCE ───────── */
  const lines = document.getElementById('editor').innerText.split('\n');
  const segs  = Object.create(null);   // # segment → []
  const macros= Object.create(null);   // & name   → {params, body}
  let mode = null;                     // 'seg' | 'mac'
  let cur  = '';                       // segment / macro name
  let macBody = [], macParams = [];

  for (let raw of lines) {
    const L = raw.trimEnd();
    if (L.startsWith('&') && L.trim() !== '&') {
      mode='mac';
      const [, ...rest] = L.slice(1).trim().split(/\s+/);
      cur       = rest[0];
      macParams = rest.slice(1);
      macBody   = [];
    } else if (L === '&' && mode==='mac') {
      macros[cur] = {params: macParams, body: macBody.slice()};
      mode = null;
    } else if (L.startsWith('#')) { 
      mode='seg'; cur = L.slice(1).trim(); segs[cur]=[];
    } else if (mode==='mac') macBody.push(L);
    else if (mode==='seg')  segs[cur].push(L);
  }

  /* ───────── 2.  RUNTIME STATE ───────── */
  const out  = document.getElementById('output');
  const hud  = document.getElementById('hud');
  const vars = Object.create(null);
  const hudMap = Object.create(null);
  const COLORS = {black:'#000',red:'red',green:'green',yellow:'goldenrod',
                  blue:'blue',purple:'purple',cyan:'cyan',white:'#fff'};

  const fmt = t => t.replace(/\[([a-zA-Z0-9_.]+)\]/g,(_,k)=>
      COLORS[k] ? `<span style="color:${COLORS[k]}">`
     : k==='reset'?'</span>'
     : k==='end'  ?'\n'
     : vars[k]!==undefined ? String(vars[k]) : `[${k}]`);

  /* quick typewriter w/ skip */
  const type = html => new Promise(res=>{
    const d=document.createElement('div'); out.appendChild(d);
    let i=0,skip=false;
    const press=()=>skip=true;
    const done =()=>{d.innerHTML=html;off();res();};
    const off  =()=>{document.removeEventListener('keydown',press);
                     document.removeEventListener('mousedown',press);};
    document.addEventListener('keydown',press);
    document.addEventListener('mousedown',press);
    (function tick(){ if(skip){done();return;}
      d.innerHTML=html.slice(0,++i);
      if(i<html.length) setTimeout(tick,20); else done();
    })();
  });

  const sub = v => (v.startsWith('[')&&v.endsWith(']')) ? vars[v.slice(1,-1)] : v;

  /* ───────── 3.  MAIN ENGINE ───────── */
  const run = async (seg, clearOut = false) => {
    if (clearOut) out.innerHTML='';
    purgeChoices();                                 // remove old buttons

    let i=0, list=segs[seg]||[], concat='', collectingHUD=false, hudName='';
    let softJump='';

    const flush = async ()=>{ if(!concat) return; await type(concat); concat=''; };

    const updateHUD = () =>{
      hud.innerHTML='';
      Object.values(hudMap).forEach(arr=>{
        arr.forEach(l=>hud.insertAdjacentHTML('beforeend', fmt(l.replace('[noend]',''))+'\n'));
      });
      hud.style.display = hud.textContent.trim() ? '' : 'none';
    };

    const applyMacro = async (name,args)=>{
      const m=macros[name]; if(!m) return;
      const rep = ln=>{ m.params.forEach((p,j)=> ln=ln.replaceAll(`[${p}]`,args[j]||''));return ln;};
      for (const ln of m.body) await exec(rep(ln));
    };

    async function exec(raw){
      let line=raw.trim();
      if(!line){ concat+='\n'; return; }

      /* HUD MODE ------------------------------------------------------------ */
      if(line.startsWith('%')){
        if(!collectingHUD){             // opening
          collectingHUD=true; hudName=line.slice(1).trim()||'__DEFAULT__';
          hudMap[hudName]=[];
        } else {                        // closing %
          collectingHUD=false; updateHUD();
        }
        return;
      }
      if(collectingHUD){ hudMap[hudName].push(line); return; }

      /* MACROS -------------------------------------------------------------- */
      if(line.startsWith('\\\\')){
        const rest=line.slice(2).trim(); const sp=rest.indexOf(' ');
        const mName = sp===-1?rest:rest.slice(0,sp);
        const argStr= sp===-1?'':rest.slice(sp+1);
        await applyMacro(mName,argStr?argStr.split(',').map(s=>s.trim()):[]);
        return;
      }

      /* WAIT PROMPT --------------------------------------------------------- */
      if(line.startsWith('`')){
        await flush();
        const lbl = fmt(line.slice(1).trim()).replace(/<\/?span[^>]*>/g,'');
        await new Promise(r=>{
          const b=document.createElement('button'); b.textContent=lbl;
          b.onclick=()=>{b.remove();r();}; out.appendChild(b);
        });
        return;
      }

      /* MENUS --------------------------------------------------------------- */
      if(line.startsWith('>>>')||line.startsWith('<<<')){
        const hard = line[2]==='>';
        const opts = fmt(line.slice(3)).split(',').map(s=>s.trim()).filter(Boolean);
        await flush();
        const choice = await new Promise(r=>{
          opts.forEach(o=>{
            const b=document.createElement('button'); b.className='choice';
            b.textContent=o; b.onclick=()=>{purgeChoices();r(o);};
            out.appendChild(b);
          });
        });
        if(hard) { await run(choice,false); return; }  // keep history
        softJump = choice; return;
      }

      /* CONDITIONS ---------------------------------------------------------- */
      if(/^[@!<>]/.test(line)){
        const tk=line.split(/\s+/);
        while(/^[@!<>]/.test(tk[0])){
          const op=tk.shift(), A=sub(tk.shift()), B=sub(tk.shift());
          if( (op==='@'&&A!=B)||(op==='!'&&A==B)||(op==='<'&&+A>=+B)||(op==='>'&&+A<=+B) ) return;
        }
        line=tk.join(' '); if(!line) return;
      }

      /* VARIABLE OPS -------------------------------------------------------- */
      if(line.startsWith('=')){const[v,k]=line.slice(1).trim().split(/\s+/);
        vars[k]=isNaN(+v)?v.replace(/^"|"$/g,''):+v; return;}
      if(line.startsWith('?')){const[m,k]=line.slice(1).trim().split(/\s+/);
        vars[k]=Math.floor(Math.random()*(+sub(m)+1)); return;}
      const math=(f)=>{const[v,k]=line.slice(1).trim().split(/\s+/);
        vars[k]=f(vars[k]??0,+sub(v));};
      if(line.startsWith('+')){math((a,b)=>a+b); return;}
      if(line.startsWith('-')){math((a,b)=>a-b); return;}
      if(line.startsWith('*')){math((a,b)=>a*b); return;}
      if(line.startsWith('/')){math((a,b)=>Math.floor(a/(b||1))); return;}

      /* REPEAT ^ ------------------------------------------------------------ */
      if(line.startsWith('^')){
        const [cnt,...txt]=line.slice(1).trim().split(/\s+/);
        concat+=fmt(txt.join(' ').repeat(+sub(cnt)||0)); return;
      }

      /* STANDARD TEXT ------------------------------------------------------- */
      const cont=line.endsWith('[noend]');
      concat+=fmt(line.replace('[noend]',''))+(cont?'':'\n');
      if(!cont) await flush();
    }

    while(i<list.length){ await exec(list[i++]); if(softJump){await run(softJump,true); return;} }
  };

  const purgeChoices = ()=> out.querySelectorAll('button.choice').forEach(b=>b.remove());

  run('start',true);           // first segment, clear screen
});
