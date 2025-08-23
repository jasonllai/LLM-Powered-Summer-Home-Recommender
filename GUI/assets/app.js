/* SummerStay HTML Frontend (no framework)
   - USE_LOCAL = true => mock backend with localStorage.
   - Switch to server endpoints later by setting USE_LOCAL = false.
*/
const USE_LOCAL = false;       // switch to backend
const API_BASE = "http://127.0.0.1:5050";  // reuse your Flask host
const ASSIST_API = "http://127.0.0.1:5050";

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
function normalizeIsoDate(s){
  const m = String(s||"").trim().match(/^(\d{4})[-/](\d{1,2})[-/](\d{1,2})$/);
  if(!m) return null;
  const y = +m[1], mo = +m[2], d = +m[3];
  const dt = new Date(Date.UTC(y, mo-1, d));
  if (dt.getUTCFullYear()!==y || (dt.getUTCMonth()+1)!==mo || dt.getUTCDate()!==d) return null;
  const pad = n => String(n).padStart(2,'0');
  return `${y}-${pad(mo)}-${pad(d)}`;
}

// --- Login Page ---
function initLogin(isAdmin=false){
  const form = qs("#login-form"); const err = qs("#login-error");
  const prevErr = urlParam("error"); if(prevErr) { err.textContent = isAdmin ? "Admin ID or password is incorrect, please try again." : "User ID or password is incorrect, please try again."; err.classList.remove("hidden"); }
  form?.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const userid = qs("[name=userid]").value.trim();
    const password = qs("[name=password]").value;
    if(!userid || !password) return;
  
    if(!USE_LOCAL){
      try{
        const r = await fetch(`${API_BASE}/login`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId: userid, password })
        });
        if(!r.ok){
          err.textContent = "User ID or password is incorrect, please try again.";
          err.classList.remove("hidden");
          return;
        }
        sessionStorage.setItem("userId", userid);
        location.href = `dashboard.html?user=${encodeURIComponent(userid)}`;
      }catch{
        err.textContent = "Unable to log in. Please try again.";
        err.classList.remove("hidden");
      }
      return;
    }
  
    // LOCAL MODE ONLY (keep this; remove any redirect before checks)
    const ok = DB.users.some(u=>u.id===userid && u.password===password);
    if(!ok){
      err.textContent="User ID or password is incorrect, please try again.";
      err.classList.remove("hidden");
      return;
    }
    DB.session.userId = userid; saveDb(DB); location.href="dashboard.html";
  });
}

// --- Register Page ---
function initRegister(){
  const form = qs("#register-form"); const idErr = qs("#id-error");
  form?.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const userid = qs("[name=userid]")?.value.trim();
    const name = qs("[name=name]")?.value.trim();
    const password = qs("[name=password]")?.value;
    const preferredEnv = qs("#reg-preferred-env")?.value;
    const budgetMin = parseInt(qs("#reg-budget-min")?.value, 10);
    const budgetMax = parseInt(qs("#reg-budget-max")?.value, 10);
    const groupSize = parseInt(qs("#reg-group-size")?.value, 10);

    if(!userid || !name || !password){ idErr.textContent="Please fill all required fields."; idErr.classList.remove("hidden"); return; }
    if(!Number.isInteger(groupSize) || groupSize < 1 || groupSize > 10){
      idErr.textContent="Group size must be an integer between 1 and 10.";
      idErr.classList.remove("hidden"); return;
    }
    if(!Number.isInteger(budgetMin) || !Number.isInteger(budgetMax) || budgetMin <= 0 || budgetMax < budgetMin){
      idErr.textContent="Budget must be integers; min > 0 and max >= min.";
      idErr.classList.remove("hidden"); return;
    }

    if(!USE_LOCAL){
      idErr.classList.add("hidden");
      try{
        const r = await fetch(`${API_BASE}/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            userId: userid, name, password,
            preferredEnv, budgetRange: [budgetMin, budgetMax],
            groupSize
          })
        });
        if(!r.ok){
          const data = await r.json().catch(()=> ({}));
          idErr.textContent = data?.error || "Failed to sign up.";
          idErr.classList.remove("hidden");
          return;
        }
        sessionStorage.setItem("userId", userid);
        location.href = `dashboard.html?user=${encodeURIComponent(userid)}`;
      }catch(err){
        console.error(err);
        idErr.textContent = "Failed to sign up. Please try again.";
        idErr.classList.remove("hidden");
      }
      return;
    }

    // Local mock mode (optional – keep or remove)
    if(DB.users.some(u=>u.id===userid)){ idErr.textContent="This username has been used."; idErr.classList.remove("hidden"); return; }
    DB.users.push({
      id: userid, name, password,
      bookingHistory: [], groupSize, preferredEnv,
      budgetRange: [budgetMin, budgetMax]
    });
    DB.session.userId = userid; saveDb(DB); location.href="dashboard.html";
  });
}

// --- Dashboard ---
function initDashboard(){
  if (USE_LOCAL){
    requireUser();
    const user = DB.users.find(u=>u.id===DB.session.userId);
    qs("#hello").textContent = `Welcome, ${user?.name || ""}`;
    qs("#logout")?.addEventListener("click", logoutAll);
    return;
  }
  const userId = urlParam("user") || sessionStorage.getItem("userId") || "";
  qs("#hello").textContent = `Welcome, ${userId || ""}`;
  qs("#logout")?.addEventListener("click", logoutAll);
  const searchLink = qs("a[href$='search.html']") || qs("#open-search");
  if (searchLink) searchLink.href = `search.html?user=${encodeURIComponent(userId)}`;
  const profileLink = qs("a[href$='profile.html']") || qs("#open-profile");
  if (profileLink) profileLink.href = `profile.html?user=${encodeURIComponent(userId)}`;
}

// --- Profile ---
function initProfile(){
  if (!USE_LOCAL){
    const userId = urlParam("user") || sessionStorage.getItem("userId") || "";
    qs("#logout")?.addEventListener("click", logoutAll);
    if(!userId){ toast("Missing user id", false); return; }

    let p = null; // current profile model shared by handlers

    function setVal(k,v){
      const el = qs(`[data-val='${k}']`);
      if(el) el.textContent = (v ?? "");
    }

    function renderProfile(profile){
      setVal("id", profile.id);
      setVal("name", profile.name);
      setVal("password", profile.password);
      setVal("groupSize", profile.groupSize);
      setVal("preferredEnv", profile.preferredEnv);
      setVal("budgetRange", Array.isArray(profile.budgetRange) ? `${profile.budgetRange[0]}–${profile.budgetRange[1]}` : "");
      const list = qs("#bookings");
      const hist = Array.isArray(profile.bookingHistory) ? profile.bookingHistory : [];
      list.innerHTML = hist.length
        ? hist.map(b => `
            <div class="booking-item">
              <div class="left">
                <div class="name"><strong>Property</strong></div>
                <div class="kbd small">${(b.propertyId||"").slice(0,8)}</div>
              </div>
              <div class="right small">
                ${b.start} → ${b.end}
                <button class="btn danger small" data-del data-prop="${b.propertyId}" data-start="${b.start}" data-end="${b.end}" style="margin-left:8px">Delete</button>
              </div>
            </div>`).join("")
        : `<div class="small">No bookings yet.</div>`;
    }

    qs("#bookings")?.addEventListener("click", async (e)=>{
      const btn = e.target.closest("[data-del]");
      if(!btn) return;
      const propertyId = btn.getAttribute("data-prop");
      const start = btn.getAttribute("data-start");
      const end = btn.getAttribute("data-end");
      btn.disabled = true;
      try{
        const r = await fetch(`${API_BASE}/booking/delete`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId, propertyId, start, end })
        });
        if(!r.ok){ toast("Failed to delete booking", false); btn.disabled = false; return; }
        const { bookingHistory } = await r.json();
        p.bookingHistory = bookingHistory || [];
        renderProfile(p);
        toast("Booking deleted", true);
      }catch(err){
        console.error(err);
        toast("Failed to delete booking", false);
        btn.disabled = false;
      }
    });

    const delBtn = qs("#delete-account");
    delBtn?.addEventListener("click", async ()=>{
      const userId = urlParam("user") || sessionStorage.getItem("userId") || "";
      if(!userId) { toast("Missing user id", false); return; }

      // Optional confirm
      if(!confirm("Are you sure you want to delete your account? This cannot be undone.")) return;

      try{
        const r = await fetch(`${API_BASE}/account/delete`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId })
        });
        if(!r.ok){ toast("Failed to delete account", false); return; }

        // Clear client session and inform user
        sessionStorage.removeItem("userId");
        toast("Your account has been deleted. You will be redirected to the main page in 5 seconds…", true);
        setTimeout(()=> { location.href = "index.html"; }, 5000);
      }catch(e){
        console.error(e);
        toast("Failed to delete account", false);
      }
    });

    (async ()=>{
      try{
        const r = await fetch(`${API_BASE}/profile`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId })
        });
        if(!r.ok){ toast("Unable to load profile", false); return; }
        const { profile } = await r.json();
        if(!profile){ toast("Profile not found", false); return; }
        p = profile;
        renderProfile(p);
      }catch(e){
        console.error(e);
        toast("Unable to load profile", false);
      }
    })();

    // Edit: show current values in inputs
    qsa("[data-edit]").forEach(btn => {
      btn.addEventListener("click", ()=>{
        const key = btn.getAttribute("data-edit");
        const row = btn.closest(".rowline");
        row.querySelector(".view").classList.add("hidden");
        row.querySelector(".edit").classList.remove("hidden");
        if(key==="budgetRange"){
          const [min,max] = (p?.budgetRange || []);
          row.querySelector("[name=budgetMin]").value = (min ?? "");
          row.querySelector("[name=budgetMax]").value = (max ?? "");
        }else if(key==="preferredEnv"){
          const sel = row.querySelector("select"); if(sel) sel.value = p?.preferredEnv || "";
        }else{
          const inp = row.querySelector("input"); if(inp) {
            const cur = key==="groupSize" ? (p?.groupSize ?? "") : (p?.[key] ?? "");
            inp.value = cur;
          }
        }
      });
    });

    // Cancel
    qsa("[data-cancel]").forEach(btn => {
      btn.addEventListener("click", ()=>{
        const row = btn.closest(".rowline");
        row.querySelector(".edit").classList.add("hidden");
        row.querySelector(".view").classList.remove("hidden");
      });
    });

    // Save -> backend update, then re-render immediately
    qsa("[data-save]").forEach(btn => {
      btn.addEventListener("click", async ()=>{
        const key = btn.getAttribute("data-save");
        const row = btn.closest(".rowline");
        const payload = { userId };

        if(key==="name") payload.name = row.querySelector("input").value.trim();
        else if(key==="password") payload.password = row.querySelector("input").value;
        else if(key==="groupSize") payload.groupSize = Number(row.querySelector("input").value);
        else if(key==="preferredEnv") payload.preferredEnv = row.querySelector("select").value;
        else if(key==="budgetRange"){
          const min = Number(row.querySelector("[name=budgetMin]").value);
          const max = Number(row.querySelector("[name=budgetMax]").value);
          payload.budgetRange = [min, max];
        }

        try{
          const r = await fetch(`${API_BASE}/profile/update`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });
          if(!r.ok){
            const errText = await r.text().catch(()=> "");
            console.error("update failed", errText);
            toast("Failed to update profile", false);
            return;
          }
          const { profile: np } = await r.json();
          p = np;                // keep local model in sync
          renderProfile(np);     // update UI immediately
          row.querySelector(".edit").classList.add("hidden");
          row.querySelector(".view").classList.remove("hidden");
          toast("Saved", true);
        }catch(e){
          console.error(e);
          toast("Failed to update profile", false);
        }
      });
    });
    return;
  }
}

// --- Search ---
function initSearch(){
  requireUser();
  let userId = urlParam("user") || sessionStorage.getItem("userId") || "";
  if(!userId){ console.error("Missing userId for recommendations"); return; }

  let recs = [];
  async function fetchRecs(){
    try{
      const r = await fetch(`${API_BASE}/recommend`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ userId })
      });
      if(!r.ok) throw new Error(await r.text());
      const data = await r.json();
      recs = Array.isArray(data.properties) ? data.properties : [];
      renderList(recs);
    }catch(err){
      console.error(err);
      renderList([]);
    }
  }

  fetchRecs();

  qs("#logout")?.addEventListener("click", logoutAll);

  // fill filters
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
      const title = qs("#list-title"); if(title) title.textContent = "Search Results";
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
        let pmin = f.pmin !== "" ? parseInt(f.pmin, 10) : null;
        let pmax = f.pmax !== "" ? parseInt(f.pmax, 10) : null;
        let cap  = f.cap  !== "" ? parseInt(f.cap, 10)  : null;

        // Basic client checks
        if(pmin !== null && (!Number.isInteger(pmin) || pmin < 0)){ toast("Min price must be an integer greater or equal to 0", false); return; }
        if(pmax !== null && (!Number.isInteger(pmax) || pmax < 0)){ toast("Max price must be an integer greater or equal to 0", false); return; }
        if(pmin !== null && pmax !== null && pmax < pmin){ toast("Max price must be greater or equal to min price", false); return; }
        if(cap !== null && (!Number.isInteger(cap) || cap < 1 || cap > 10)){ toast("Guest capacity must be an integer 1–10", false); return; }

        // Normalize dates
        const start = f.start ? normalizeIsoDate(f.start) : null;
        const end   = f.end   ? normalizeIsoDate(f.end)   : null;
        if(f.start && !start){ toast("Invalid start date (use YYYY-MM-DD)", false); return; }
        if(f.end   && !end)  { toast("Invalid end date (use YYYY-MM-DD)", false); return; }
        if(start && end && new Date(start) > new Date(end)){ toast("End date must be on or after start date", false); return; }

        const payload = {
          location: f.loc || null,
          propType: f.typ || null,
          minPrice: pmin,
          maxPrice: pmax,
          groupSize: cap,
          features: f.features.length ? f.features : null,
          tags: f.tags.length ? f.tags : null,
          startDate: start,
          endDate: end
        };

        try{
          const r = await fetch(`${API_BASE}/search`, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify(payload)
          });
          if(!r.ok){
            const data = await r.json().catch(()=> ({}));
            toast(data?.error || "Search failed", false);
            return;
          }
          const data = await r.json();
          const list = Array.isArray(data.properties) ? data.properties : [];
          const title = qs("#list-title"); if(title) title.textContent = "Search Results";
          renderList(list);
        } catch(err){
          console.error(err);
          toast("Search failed", false);
        }
      }
    }
    
    qs("#search")?.addEventListener("click", runSearch);
    qs("#reset")?.addEventListener("click", ()=>{
      qsa(".filter").forEach(f=>{ if(f.type==="checkbox") f.checked=false; else f.value=""; });
      msFeatures.clear(); msTags.clear();
      const title = qs("#list-title"); if(title) title.textContent = "Recommended for you";
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
      btn.addEventListener("click", async ()=>{
        const id = btn.getAttribute("data-confirm");
        const startRaw = qs("#start-"+id).value, endRaw = qs("#end-"+id).value;
        const err = qs("#err-"+id);
        if(!startRaw || !endRaw){ err.textContent="Please select start and end dates."; err.classList.remove("hidden"); return; }

        const start = normalizeIsoDate(startRaw);
        const end = normalizeIsoDate(endRaw);
        if(!start || !end){ err.textContent="Invalid date format. Use YYYY-MM-DD."; err.classList.remove("hidden"); return; }

        // frontend order check for fast UX
        if(new Date(start) > new Date(end)){ err.textContent="End date cannot be before the start date."; err.classList.remove("hidden"); return; }

        if(!USE_LOCAL){
          err.classList.add("hidden");
          try{
            const userId = urlParam("user") || sessionStorage.getItem("userId") || "";
            const r = await fetch(`${API_BASE}/booking/create`, {
              method: "POST",
              headers: { "Content-Type": "application/json" },
              body: JSON.stringify({ userId, propertyId: id, start, end })
            });
            if(!r.ok){
              const data = await r.json().catch(()=> ({}));
              err.textContent = data?.error || "Failed to create booking.";
              err.classList.remove("hidden");
              return;
            }
            toast("Booking successful!", true);
            qs("#book-"+id).classList.add("hidden");
          }catch(e){
            console.error(e);
            err.textContent = "Failed to create booking."; err.classList.remove("hidden");
          }
          return;
        }
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
