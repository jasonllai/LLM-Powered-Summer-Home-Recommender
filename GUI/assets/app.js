/* SummerStay HTML Frontend (no framework)
   - USE_LOCAL = true => mock backend with localStorage.
   - Switch to server endpoints later by setting USE_LOCAL = false.
*/
const USE_LOCAL = true;
const API_BASE = ""; // e.g., "/api"
const ASSIST_API = "http://127.0.0.1:5050";

// --- Local demo DB ---
function seedDb() {
  return {
    users: [{
      id:"jason", name:"Jason L", password:"test123",
      bookingHistory:[], groupSize:2, preferredEnv:"beach", budgetRange:[150,300]
    }],
    admin: { id:"admin", password:"admin123" },
    properties: [
      { id: rnd(), location:"Tofino, BC", type:"Beach House", pricePerNight:280,
        features:["Ocean view","Fire pit","Kayaks"], tags:["beach","quiet","family"], guestCapacity:6, unavailable:[] },
      { id: rnd(), location:"Kelowna, BC", type:"Lake Cabin", pricePerNight:210,
        features:["Dock","BBQ","Canoe"], tags:["lake","sunset"], guestCapacity:4, unavailable:[{start:"2025-08-25", end:"2025-08-30"}] },
      { id: rnd(), location:"Prince Edward County, ON", type:"Country Cottage", pricePerNight:190,
        features:["Vineyard nearby","Fireplace","Bikes"], tags:["countryside","wineries"], guestCapacity:5, unavailable:[] },
      { id: rnd(), location:"Muskoka, ON", type:"Forest Chalet", pricePerNight:320,
        features:["Hot tub","Sauna","Hiking trails"], tags:["forest","luxury"], guestCapacity:8, unavailable:[] },
    ],
    session: { userId:null, isAdmin:false }
  };
}
function loadDb(){
  const raw = localStorage.getItem("summerstay-db");
  if(!raw){ const db = seedDb(); localStorage.setItem("summerstay-db", JSON.stringify(db)); return db; }
  try { return JSON.parse(raw); } catch { const db = seedDb(); localStorage.setItem("summerstay-db", JSON.stringify(db)); return db; }
}
function saveDb(db){ localStorage.setItem("summerstay-db", JSON.stringify(db)); }
let DB = USE_LOCAL ? loadDb() : null;
function rnd(){ return (self.crypto?.randomUUID?.() || Math.random().toString(36).slice(2)); }

// --- Helpers ---
function qs(sel,root=document){ return root.querySelector(sel); }
function qsa(sel,root=document){ return Array.from(root.querySelectorAll(sel)); }
function toast(msg, ok=true){ const el=qs("#toast"); if(!el) return;
  el.textContent = msg; el.classList.remove("hidden","err"); if(!ok) el.classList.add("err");
  el.classList.remove("hidden"); setTimeout(()=> el.classList.add("hidden"), 2600);
}
function urlParam(key){ const u=new URL(location.href); return u.searchParams.get(key); }
function logoutAll(){ if(USE_LOCAL){ DB.session={userId:null,isAdmin:false}; saveDb(DB); } location.href="index.html"; }
function requireUser(){ if(USE_LOCAL){ if(!DB.session.userId) location.href="login.html"; } }
function requireAdmin(){ if(USE_LOCAL){ if(!DB.session.isAdmin) location.href="admin-login.html"; } }
function money(n){ return "$"+Number(n).toLocaleString(); }
function dateOverlap(a,b){ return !(b.end < a.start || b.start > a.end); }
function isAvailable(prop,start,end){ const req={start,end}; return !prop.unavailable?.some(r=>dateOverlap(r,req)); }

// --- Login Page ---
function initLogin(isAdmin=false){
  const form = qs("#login-form"); const err = qs("#login-error");
  const prevErr = urlParam("error"); if(prevErr) { err.textContent = isAdmin ? "Admin ID or password is incorrect, please try again." : "User ID or password is incorrect, please try again."; err.classList.remove("hidden"); }
  form?.addEventListener("submit", (e)=>{
    if(!USE_LOCAL) return; // let the server handle
    e.preventDefault();
    const userid = qs("[name=userid]").value.trim();
    const password = qs("[name=password]").value;
    if(isAdmin){
      const ok = (userid===DB.admin.id && password===DB.admin.password);
      if(!ok){ err.textContent="Admin ID or password is incorrect, please try again."; err.classList.remove("hidden"); return; }
      DB.session.isAdmin = true; saveDb(DB); location.href="admin.html";
    }else{
      const ok = DB.users.some(u=>u.id===userid && u.password===password);
      if(!ok){ err.textContent="User ID or password is incorrect, please try again."; err.classList.remove("hidden"); return; }
      DB.session.userId = userid; saveDb(DB); location.href="dashboard.html";
    }
  });
}

// --- Register Page ---
function initRegister(){
  const form = qs("#register-form"); const idErr = qs("#id-error");
  form?.addEventListener("submit",(e)=>{
    if(!USE_LOCAL) return;
    e.preventDefault();
    const id = qs("[name=userid]").value.trim();
    const name = qs("[name=name]").value.trim();
    const password = qs("[name=password]").value;
    if(DB.users.some(u=>u.id===id)){ idErr.textContent="This ID has already been used by another user."; idErr.classList.remove("hidden"); return; }
    DB.users.push({ id, name, password, bookingHistory:[], groupSize:2, preferredEnv:"beach", budgetRange:[150,300] });
    DB.session.userId = id; saveDb(DB); location.href="dashboard.html";
  });
}

// --- Dashboard ---
function initDashboard(){
  requireUser();
  const user = DB.users.find(u=>u.id===DB.session.userId);
  qs("#hello").textContent = `Welcome, ${user?.name || ""}`;
  qs("#logout")?.addEventListener("click", logoutAll);
}

// --- Profile ---
function initProfile(){
  requireUser();
  const user = DB.users.find(u=>u.id===DB.session.userId);
  const map = {
    id: user.id, name: user.name, password: user.password,
    groupSize: user.groupSize, preferredEnv: user.preferredEnv, budgetRange: user.budgetRange?.join("–")
  };
  for(const [k,v] of Object.entries(map)){ const el = qs(`[data-val='${k}']`); if(el) el.textContent = v; }
  // booking history
  const list = qs("#bookings");
  if(user.bookingHistory?.length){
    list.innerHTML = user.bookingHistory.map(b => {
      const p = (DB.properties||[]).find(x=>x.id===b.propertyId);
      const name = p ? `${p.type} in ${p.location}` : "Property";
      return `<div class="booking-item">
        <div class="left">
          <div class="name"><strong>${name}</strong></div>
          <div class="kbd small">${b.propertyId.slice(0,8)}</div>
        </div>
        <div class="right small">${b.start} → ${b.end} · ${money(b.price)}/night</div>
      </div>`;
    }).join("");
  } else list.innerHTML = `<div class="small">No bookings yet.</div>`;
  qsa("[data-edit]").forEach(btn => {
    btn.addEventListener("click", ()=>{
      const key = btn.getAttribute("data-edit");
      const row = btn.closest(".rowline"); row.querySelector(".view").classList.add("hidden"); row.querySelector(".edit").classList.remove("hidden");
      if(key==="budgetRange"){
        const [min,max] = user.budgetRange;
        row.querySelector("[name=budgetMin]").value = min;
        row.querySelector("[name=budgetMax]").value = max;
      }else if(key==="preferredEnv"){
        const sel = row.querySelector("select");
        if(sel) sel.value = user.preferredEnv || "";
      }else{
        row.querySelector("input").value = user[key];
      }
    });
  });
  qsa("[data-save]").forEach(btn => {
    btn.addEventListener("click", ()=>{
      const key = btn.getAttribute("data-save");
      if(key==="budgetRange"){
        const min = Number(qs("[name=budgetMin]").value);
        const max = Number(qs("[name=budgetMax]").value);
        user.budgetRange = [min,max];
        qs("[data-val='budgetRange']").textContent = `${min}–${max}`;
      }else if(key==="preferredEnv"){
        const val = btn.closest(".rowline").querySelector("select").value;
        user.preferredEnv = val;
        qs(`[data-val='preferredEnv']`).textContent = val;
      }else{
        const val = btn.closest(".rowline").querySelector("input").value;
        user[key] = (key==="groupSize") ? Number(val) : val;
        qs(`[data-val='${key}']`).textContent = user[key];
      }
      saveDb(DB);
      const row = btn.closest(".rowline"); row.querySelector(".edit").classList.add("hidden"); row.querySelector(".view").classList.remove("hidden");
      toast("Saved", true);
    });
  });
  qsa("[data-cancel]").forEach(btn => {
    btn.addEventListener("click", ()=>{
      const row = btn.closest(".rowline"); row.querySelector(".edit").classList.add("hidden"); row.querySelector(".view").classList.remove("hidden");
    });
  });
  qs("#logout")?.addEventListener("click", logoutAll);
}

// --- Search ---
function initSearch(){
  requireUser();
  const user = DB.users.find(u=>u.id===DB.session.userId);
  qs("#logout")?.addEventListener("click", logoutAll);
  // fill filters
  const props = DB.properties;
  const types = ["cabin", "apartment", "cottage", "loft", "villa", "tiny house", "studio"];
  const locations = ["Vancouver", "Toronto", "Montreal", "Calgary", "Edmonton", 
    "Winnipeg", "Halifax", "Victoria", "Quebec City", "Fredericton"];
  const tags = ["mountains", "remote", "adventure", "beach", "city", "lake", 
    "river", "ocean", "forest", "park", "national park", "state park", 
    "national forest", "state forest", "modern","rustic","historic",
    "family-friendly","kid-friendly","pet-friendly","romantic","business-travel",
    "nightlife","eco-friendly","spa","golf","foodie","farm-stay","glamping","long-term"];
  const features = ["mountain view", "city skyline view", "lakefront", "riverfront",
    "oceanfront", "beach access", "balcony or patio", "rooftop terrace",
    "private hot tub", "sauna", "private pool", "fireplace", "houskeeper service",
    "BBQ grill", "full kitchen", "chef's kitchen", "EV charger", "free parking",
    "garage", "air conditioning", "heating", "washer and dryer", "fast wifi",
    "dedicated workspace", "smart TV with streaming", "game room", "fitness room",
    "ski-in/ski-out", "wheelchair accessible", "pet-friendly"];

  const locSel = qs("#f-location"); locSel.innerHTML = `<option value="">Any</option>` + locations.map(l=>`<option>${l}</option>`).join("");
  const typeSel = qs("#f-type"); typeSel.innerHTML = `<option value="">Any</option>` + types.map(t=>`<option>${t}</option>`).join("");

  function buildMulti(btnSel, ddSel, items, anyLabel){
    const btn = qs(btnSel), dd = qs(ddSel);
    dd.innerHTML = items.map(v=>`<label class="option"><span>${v}</span><input type="checkbox" value="${v}"></label>`).join("");
    const update = ()=>{
      const sel = Array.from(dd.querySelectorAll("input:checked")).map(i=>i.value);
      btn.textContent = sel.length ? `${sel.length} selected` : anyLabel;
    };
    btn.addEventListener("click", ()=> dd.classList.toggle("hidden"));
    dd.addEventListener("change", update);
    document.addEventListener("click", (e)=>{ if(!btn.contains(e.target) && !dd.contains(e.target)) dd.classList.add("hidden"); });
    update();
    return { get: ()=>Array.from(dd.querySelectorAll("input:checked")).map(i=>i.value),
             clear: ()=>{ dd.querySelectorAll("input:checked").forEach(i=>i.checked=false); update(); } };
  }
  const msFeatures = buildMulti("#btn-features", "#dd-features", features, "Any features");
  const msTags = buildMulti("#btn-tags", "#dd-tags", tags, "Any tags");

  // recommendations
  function score(p){
    let s=0; if(p.tags.includes(user.preferredEnv)) s+=2;
    const [min,max] = user.budgetRange || [0,999999]; if(p.pricePerNight>=min && p.pricePerNight<=max) s+=1;
    if(p.guestCapacity >= (user.groupSize||1)) s+=1; return s;
  }
  let recs = props.slice().sort((a,b)=>score(b)-score(a));
  renderList(recs);

  function renderList(list){
    const wrap = qs("#results"); if(!wrap) return;
    qs("#count").textContent = list.length;
    wrap.innerHTML = list.map(p => `
      <div class="card pad prop-card" data-prop="${p.id}">
        <div class="flex-between prop-head">
          <div>
            <div class="kbd small">${p.id.slice(0,8)}</div>
            <div class="row" style="margin-top:6px">
              <strong>${p.type} in ${p.location}</strong>
            </div>
            <div class="small">${money(p.pricePerNight)}/night · ${p.guestCapacity} guests</div>
            <div class="pills" style="margin-top:8px">${p.tags.map(t=>`<span class="pill">${t}</span>`).join("")}</div>
          </div>
          <div><button class="btn" data-book="${p.id}">Book</button></div>
        </div>

        <div class="hidden featuresbox" id="feat-${p.id}" style="margin-top:10px">
          <div class="small" style="margin-bottom:6px;color:#334155">Features</div>
          <ul class="features-list">${p.features.map(f=>`<li>${f}</li>`).join("")}</ul>
        </div>

        <div class="hidden bookbox" id="book-${p.id}" style="margin-top:10px">
          <div class="row">
            <div class="field"><label>Start date</label><input type="date" id="start-${p.id}"></div>
            <div class="field"><label>End date</label><input type="date" id="end-${p.id}"></div>
            <div class="field"><label>&nbsp;</label><button class="btn" data-confirm="${p.id}">Confirm</button></div>
          </div>
          <div class="error hidden" id="err-${p.id}"></div>
        </div>
      </div>
    `).join("");

    // expand/collapse features when the card body is clicked
    qsa(".prop-card").forEach(card=>{
      card.addEventListener("click",(e)=>{
        // ignore clicks on buttons/inputs so Book flow still works
        if(e.target.closest("button, input, select, .bookbox")) return;
        const id = card.getAttribute("data-prop");
        qs("#feat-"+id)?.classList.toggle("hidden");
      });
    });


    // filter logic
    function buildFilters(){
      return {
        start: qs("#f-start").value,
        end: qs("#f-end").value,
        loc: qs("#f-location").value,
        typ: qs("#f-type").value,
        pmin: qs("#f-price-min").value,
        pmax: qs("#f-price-max").value,
        cap: qs("#f-capacity").value,
        features: msFeatures.get(),
        tags: msTags.get()
      };
    }
    
    async function runSearch(){
      const f = buildFilters();
      if(USE_LOCAL){
        let list = recs.filter(p=>{
          if(f.loc && !p.location.startsWith(f.loc)) return false;
          if(f.typ && p.type!==f.typ) return false;
          if(f.pmin && p.pricePerNight < Number(f.pmin)) return false;
          if(f.pmax && p.pricePerNight > Number(f.pmax)) return false;
          if(f.cap && p.guestCapacity < Number(f.cap)) return false;
          if(f.features.length && !f.features.every(x=>p.features.includes(x))) return false;
          if(f.tags.length && !f.tags.every(x=>p.tags.includes(x))) return false;
          if(f.start && f.end && !isAvailable(p, f.start, f.end)) return false;
          return true;
        });
        renderList(list);
      }else{
        // Hook for your Python backend:
        // const res = await fetch(`${API_BASE}/search`, { method:"POST", headers:{"Content-Type":"application/json"}, body: JSON.stringify(f) });
        // const list = await res.json();
        // renderList(list);
      }
    }
    
    qs("#search")?.addEventListener("click", runSearch);
    qs("#reset")?.addEventListener("click", ()=>{
      qsa(".filter").forEach(f=>{ if(f.type==="checkbox") f.checked=false; else f.value=""; });
      msFeatures.clear(); msTags.clear();
      renderList(recs);
    });

    // attach events
    qsa("[data-book]").forEach(b=>{
      b.addEventListener("click", ()=>{
        const id=b.getAttribute("data-book");
        qsa(".bookbox").forEach(x=>x.classList.add("hidden"));
        qs("#book-"+id).classList.toggle("hidden");
      });
    });
    qsa("[data-confirm]").forEach(btn=>{
      btn.addEventListener("click", ()=>{
        const id = btn.getAttribute("data-confirm");
        const start = qs("#start-"+id).value, end = qs("#end-"+id).value;
        const err = qs("#err-"+id);
        if(!start || !end){ err.textContent="Please select start and end dates."; err.classList.remove("hidden"); return; }
        // local booking
        const prop = DB.properties.find(p=>p.id===id);
        if(!isAvailable(prop, start, end)){ err.textContent="This property is not available for those dates. Try other dates or another property."; err.classList.remove("hidden"); return; }
        prop.unavailable.push({start,end});
        const user = DB.users.find(u=>u.id===DB.session.userId);
        user.bookingHistory.push({propertyId:id,start,end,price:prop.pricePerNight});
        saveDb(DB);
        toast("Booking confirmed!", true);
        qs("#book-"+id).classList.add("hidden");
      });
    });
  }

  // --- AI Assistant UI ---
  // Floating button
  const fab = document.createElement("button");
  fab.className = "ai-fab";
  fab.title = "AI Assistant";
  fab.textContent = "🤖";
  document.body.appendChild(fab);

  // Hint bubble (persistent))
  const hint = document.createElement("div");
  hint.className = "ai-hint";
  hint.textContent = "Ask our AI Assistant for travel blurbs & activity ideas!";
  hint.setAttribute("role","button");
  hint.tabIndex = 0;
  document.body.appendChild(hint);

  // clicking the hint also opens the assistant
  hint.addEventListener("click", openModal);
  hint.addEventListener("keypress", (e)=>{ if(e.key==="Enter" || e.key===" ") openModal(); });

  // Modal
  const overlay = document.createElement("div");
  overlay.className = "ai-overlay hidden";
  overlay.innerHTML = `
    <div class="ai-modal">
      <div class="ai-top">
        <button type="button" class="btn ghost ai-min">← Minimize</button>
        <div class="small">AI Travel Assistant</div>
        <div></div>
      </div>
      <div class="ai-chat"></div>
      <form class="ai-input">
        <input type="text" placeholder="Tell me your trip details..." autocomplete="off" />
        <button class="btn" type="submit">Send</button>
      </form>
    </div>
  `;
  document.body.appendChild(overlay);

  const chat = overlay.querySelector(".ai-chat");
  const form = overlay.querySelector("form");
  const input = overlay.querySelector("input");

  function escapeHtml(s){ const d=document.createElement("div"); d.textContent=s; return d.innerHTML; }

  const thread = [];

  function renderRich(text){
    const lines = String(text || "").split(/\r?\n/);
    let html = "", inList = false;
    const flush = ()=>{ if(inList){ html += "</ul>"; inList=false; } };
    for(const raw of lines){
      const line = raw.trimEnd();
      if(!line.trim()){ flush(); html += "<div style='height:6px'></div>"; continue; }
      const h = line.match(/^\*\*(.+?)\*\*:?$/); // full-line bold as a section title
      if(h){ flush(); html += `<div class="ai-h">${escapeHtml(h[1])}</div>`; continue; }
      const m = line.match(/^(?:\*|-)\s+(.*)$/); // bullet lines starting with * or -
      if(m){
        if(!inList){ html += `<ul class="ai-list">`; inList = true; }
        html += `<li>${escapeHtml(m[1])}</li>`;
        continue;
      }
      flush();
      html += `<p>${escapeHtml(line)}</p>`;
    }
    flush();
    return html;
  }
  
  function addMsg(who, text){
    const el = document.createElement("div");
    el.className = "ai-msg " + (who==="me" ? "me" : "ai");
    const content = (who==="ai") ? renderRich(text) : escapeHtml(text);
    el.innerHTML = `<div class="bubble">${content}</div>`;
    chat.appendChild(el);
    chat.scrollTop = chat.scrollHeight;
    thread.push({ role: who==="me" ? "user" : "assistant", content: text });
  }

  const initialMsg = "Tell me where you're going, when, and what you enjoy - I'll suggest activities tailored to you.\n\nExample input: 3 days in Kyoto in April, mid budget, love food + temples, slow pace.";
  let seeded = false;

  function openModal(){
    overlay.classList.remove("hidden");
    if(!seeded){ addMsg("ai", initialMsg); seeded = true; }
  }
  function closeModal(){ overlay.classList.add("hidden"); }

  fab.addEventListener("click", openModal);
  overlay.querySelector(".ai-min").addEventListener("click", closeModal);

  async function assistantReply(prompt){
    try{
      const r = await fetch(`${ASSIST_API}/assistant`, {
        method:"POST",
        headers:{ "Content-Type":"application/json" },
        body: JSON.stringify({ user_input: prompt, messages: thread })
      });
      if(!r.ok) throw new Error(await r.text());
      const data = await r.json();
      return data.text || "Sorry, I couldn't generate suggestions right now.";
    }catch(err){
      console.error(err);
      return localFallbackSuggestion(prompt, user);
    }
  }

  function localFallbackSuggestion(prompt, user){
    const days = /\b(\d+)\s*(day|days|night|nights)\b/i.test(prompt) ? Math.max(2, Math.min(5, Number(RegExp.$1))) : 3;
    const loc = (prompt.match(/\bin\s+([A-Za-z][A-Za-z\s,'-]+?)(?:\s+(in|on|during|for|from|by|at)\b|[.!?,;]|$)/i)?.[1] || "your destination").trim();
    const blurb = `Here’s a mini‑itinerary for ${days} days in ${loc}. Expect a mix of highlights with room to explore.`;
    const lines = Array.from({length:days}, (_,i)=>`Day ${i+1}: Neighborhood wander + local eats · Afternoon museum/park · Evening views.`);
    return `${blurb}\n\n${lines.join("\n")}`;
  }

  form.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const text = input.value.trim();
    if(!text) return;
    addMsg("me", text);
    input.value = "";
  
    // show immediate placeholder (not added to thread)
    const wrap = document.createElement("div");
    wrap.className = "ai-msg ai";
    wrap.innerHTML = `<div class="bubble">Generating… This may take a few minutes. Thank you for your patience.</div>`;
    chat.appendChild(wrap);
    chat.scrollTop = chat.scrollHeight;
    const bubble = wrap.querySelector(".bubble");
  
    // get real reply and swap the placeholder
    try{
      const reply = await assistantReply(text);
      bubble.innerHTML = renderRich(reply);
      thread.push({ role: "assistant", content: reply }); // keep conversation history
    }catch(err){
      console.error(err);
      bubble.textContent = "Sorry, something went wrong. Please try again.";
    }
  });
}

// --- Admin ---
function initAdmin(){
  requireAdmin();
  qs("#logout")?.addEventListener("click", logoutAll);
  // Tabs
  const tabs = qsa("[data-tab]"); const panes = qsa("[data-pane]");
  tabs.forEach(t => t.addEventListener("click", ()=>{
    const k=t.getAttribute("data-tab"); panes.forEach(p=>p.classList.add("hidden"));
    qs(`[data-pane='${k}']`).classList.remove("hidden");
    tabs.forEach(x=>x.classList.remove("active")); t.classList.add("active");
  }));
  qs("[data-tab='users']")?.click();

  // Users
  function renderUsers(){
    const tb = qs("#users-body");
    tb.innerHTML = DB.users.map(u => `
      <tr>
        <td class="kbd">${u.id}</td>
        <td>${u.name}</td>
        <td>${(u.bookingHistory||[]).length}</td>
        <td><span class="pill">${u.preferredEnv}</span> <span class="pill">${u.groupSize} guests</span> <span class="pill">$${u.budgetRange?.[0]}–$${u.budgetRange?.[1]}</span></td>
      </tr>
    `).join("");
  }
  renderUsers();

  // Properties
  function renderProps(){
    const list = qs("#props-list");
    list.innerHTML = DB.properties.map(p => `
      <div class="card pad">
        <div class="flex-between">
          <div>
            <strong>${p.type}</strong> · ${p.location}
            <div class="small">${money(p.pricePerNight)}/night · sleeps ${p.guestCapacity}</div>
            <div class="pills" style="margin-top:6px">${p.tags.map(t=>`<span class="pill">${t}</span>`).join("")}</div>
          </div>
          <div class="buttons">
            <button class="btn outline" data-edit="${p.id}">Update</button>
            <button class="btn danger" data-del="${p.id}">Delete</button>
          </div>
        </div>
        <div class="hidden" id="edit-${p.id}" style="margin-top:10px">
          <div class="grid grid-2">
            <div class="field"><label>Location</label><input value="${p.location}" data-k="location"></div>
            <div class="field"><label>Type</label><input value="${p.type}" data-k="type"></div>
            <div class="field"><label>Price per night ($)</label><input type="number" value="${p.pricePerNight}" data-k="pricePerNight"></div>
            <div class="field"><label>Guest capacity</label><input type="number" value="${p.guestCapacity}" data-k="guestCapacity"></div>
            <div class="field"><label>Features (comma-separated)</label><input value="${p.features.join(", ")}" data-k="features"></div>
            <div class="field"><label>Tags (comma-separated)</label><input value="${p.tags.join(", ")}" data-k="tags"></div>
            <div class="field" style="grid-column:1/-1"><label>Unavailable (YYYY-MM-DD..YYYY-MM-DD; ; separated)</label>
              <input value="${(p.unavailable||[]).map(r=>`${r.start}..${r.end}`).join("; ")}" data-k="unavailable">
            </div>
          </div>
          <div class="row">
            <button class="btn" data-save="${p.id}">Save</button>
            <button class="btn outline" data-cancel="${p.id}">Cancel</button>
          </div>
        </div>
      </div>
    `).join("");

    // Events
    qsa("[data-edit]").forEach(b => b.addEventListener("click", ()=>{
      const id=b.getAttribute("data-edit");
      qsa("[id^='edit-']").forEach(x=>x.classList.add("hidden"));
      qs("#edit-"+id).classList.toggle("hidden");
    }));
    qsa("[data-del]").forEach(b => b.addEventListener("click", ()=>{
      const id=b.getAttribute("data-del");
      DB.properties = DB.properties.filter(p=>p.id!==id);
      saveDb(DB); renderProps();
    }));
    qsa("[data-cancel]").forEach(b => b.addEventListener("click", ()=>{
      const id=b.getAttribute("data-cancel"); qs("#edit-"+id).classList.add("hidden");
    }));
    qsa("[data-save]").forEach(b => b.addEventListener("click", ()=>{
      const id=b.getAttribute("data-save");
      const box = qs("#edit-"+id);
      const get = (k)=> box.querySelector(`[data-k='${k}']`).value;
      const prop = DB.properties.find(p=>p.id===id);
      prop.location = get("location");
      prop.type = get("type");
      prop.pricePerNight = Number(get("pricePerNight"));
      prop.guestCapacity = Number(get("guestCapacity"));
      prop.features = get("features").split(",").map(s=>s.trim()).filter(Boolean);
      prop.tags = get("tags").split(",").map(s=>s.trim()).filter(Boolean);
      const raw = get("unavailable").trim();
      prop.unavailable = raw ? raw.split(";").map(seg=>seg.trim()).filter(Boolean).map(seg=>{
        const [start,end] = seg.split(".."); return {start,end};
      }) : [];
      saveDb(DB); renderProps(); toast("Property updated", true);
    }));
  }
  renderProps();

  // Add property
  qs("#ap-create")?.addEventListener("click", ()=>{
    const get=(id)=>qs("#"+id).value;
    const p = {
      id:rnd(),
      location:get("ap-location"),
      type:get("ap-type"),
      pricePerNight:Number(get("ap-price")),
      features:get("ap-features").split(",").map(s=>s.trim()).filter(Boolean),
      tags:get("ap-tags").split(",").map(s=>s.trim()).filter(Boolean),
      guestCapacity:Number(get("ap-capacity")),
      unavailable:[]
    };
    if(!p.location || !p.type){ toast("Location and Type are required", false); return; }
    DB.properties.unshift(p); saveDb(DB);
    // reset
    ["ap-location","ap-type","ap-price","ap-features","ap-tags","ap-capacity"].forEach(id=>qs("#"+id).value = (id in {"ap-price":1,"ap-capacity":1})? "": "");
    renderProps(); toast("New property created successfully.", true);
  });

  // Generate properties (simulated LLM)
  function generateProperties(n){
    const locations = ["Whistler, BC","Niagara-on-the-Lake, ON","Banff, AB","Cavendish, PEI","Lunenburg, NS","Wasaga Beach, ON","Tofino, BC","Jasper, AB"];
    const types = ["Beach House","Lake Cabin","Country Cottage","Forest Chalet","City Loft"];
    const features = ["Hot tub","Sauna","BBQ","Fire pit","Bikes","Canoe","Dock","Ocean view","Mountain view","Pet friendly"];
    const tags = ["beach","lake","forest","mountain","quiet","family","luxury","cozy"];
    const arr=[];
    for(let i=0;i<n;i++){
      const loc = locations[Math.floor(Math.random()*locations.length)];
      const typ = types[Math.floor(Math.random()*types.length)];
      const price = Math.floor(120 + Math.random()*300);
      const feat = features.sort(()=>0.5-Math.random()).slice(0,3+Math.floor(Math.random()*3));
      const tgs = tags.sort(()=>0.5-Math.random()).slice(0,2+Math.floor(Math.random()*2));
      const cap = 2 + Math.floor(Math.random()*7);
      arr.push({ id:rnd(), location:loc, type:typ, pricePerNight:price, features:feat, tags:tgs, guestCapacity:cap, unavailable:[] });
    }
    return arr;
  }
  qs("#gen-btn")?.addEventListener("click", ()=>{
    const n = Math.max(1, Math.min(50, Number(qs("#gen-n").value || 5)));
    const list = generateProperties(n);
    DB.properties = [...list, ...DB.properties]; saveDb(DB); renderProps(); toast(`Successfully generated ${n} properties.`, true);
  });
}

// Expose initializers globally
window.SummerStay = { initLogin, initRegister, initDashboard, initProfile, initSearch, initAdmin, logoutAll };
