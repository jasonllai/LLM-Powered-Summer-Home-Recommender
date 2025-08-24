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
function capWords(s){ return String(s||"").split(/\s+/).map(w=> w.split("-").map(p=> p ? (p[0].toUpperCase()+p.slice(1)) : "").join("-")).join(" "); }
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


// --- Home ---
function initHome(){
  const el = document.getElementById("hero");
  if(!el) return;

  const imgs = [
    "assets/img/img1.png",
    "assets/img/img2.png",
    "assets/img/img3.png",
    "assets/img/img4.png",
    "assets/img/img5.png"
  ];

  const nodes = imgs.map(src=>{
    const img = new Image();
    img.src = src; img.alt = "SummerStay";
    el.appendChild(img);
    return img;
  });

  let i = 0;
  if(nodes.length){ nodes[0].classList.add("active"); }
  setInterval(()=>{
    if(!nodes.length) return;
    const cur = nodes[i]; i = (i+1) % nodes.length; const nxt = nodes[i];
    if(cur) cur.classList.remove("active");
    if(nxt) nxt.classList.add("active");
  }, 5000);
}


// --- Login Page ---
function initLogin(isAdmin=false){
  const form = qs("#login-form"); const err = qs("#login-error");
  const prevErr = urlParam("error"); if(prevErr) { err.textContent = isAdmin ? "Admin ID or password is incorrect, please try again." : "User ID or password is incorrect, please try again."; err.classList.remove("hidden"); }
  form?.addEventListener("submit", async (e)=>{
    e.preventDefault();
    const userid = qs("[name=userid]").value.trim();
    const password = qs("[name=password]").value;

    // per-field required prompts (only present on admin page)
    const errId = qs("#err-admin-id");
    const errPw = qs("#err-admin-pass");
    errId?.classList.add("hidden"); errPw?.classList.add("hidden"); err?.classList.add("hidden");

    if(isAdmin){
      if(!userid){ if(errId){ errId.textContent = "Admin ID is required."; errId.classList.remove("hidden"); } return; }
      if(!password){ if(errPw){ errPw.textContent = "Password is required."; errPw.classList.remove("hidden"); } return; }
    }else{
      if(!userid || !password) return;
    }

    if(!USE_LOCAL){
      try{
        const endpoint = isAdmin ? "/admin/login" : "/login";
        const r = await fetch(`${API_BASE}${endpoint}`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ userId: userid, password })
        });
        if(!r.ok){
          err.textContent = isAdmin ? "Admin ID or password is incorrect, please try again." : "User ID or password is incorrect, please try again.";
          err.classList.remove("hidden");
          return;
        }
        sessionStorage.setItem(isAdmin ? "adminId" : "userId", userid);
        location.href = isAdmin ? `admin.html?admin=${encodeURIComponent(userid)}` : `dashboard.html?user=${encodeURIComponent(userid)}`;
      }catch{
        err.textContent = "Unable to log in. Please try again.";
        err.classList.remove("hidden");
      }
      return;
    }
  });
}

// --- Register Page ---
function initRegister(){
  const form = qs("#register-form");
  const errUser = qs("#err-userid");
  const errName = qs("#err-name");
  const errPass = qs("#err-password");
  const errBmin = qs("#err-bmin");
  const errBmax = qs("#err-bmax");
  const errG    = qs("#err-gsize");

  function hide(el){ el?.classList.add("hidden"); }
  function show(el,msg){ if(!el) return; el.textContent = msg; el.classList.remove("hidden"); }
  function clearErrs(){ [errUser,errName,errPass,errBmin,errBmax,errG].forEach(hide); }

  form?.addEventListener("submit", async (e)=>{
    e.preventDefault();
    clearErrs();

    const userid = qs("[name=userid]")?.value.trim();
    const name = qs("[name=name]")?.value.trim();
    const password = qs("[name=password]")?.value;
    const preferredEnv = qs("#reg-preferred-env")?.value;
    const bminStr = qs("#reg-budget-min")?.value;
    const bmaxStr = qs("#reg-budget-max")?.value;
    const gsizeStr = qs("#reg-group-size")?.value;

    if(!userid){ show(errUser,"Username is required."); return; }
    if(!name){ show(errName,"Name is required."); return; }
    if(!password){ show(errPass,"Password is required."); return; }
    if(!bminStr){ show(errBmin,"Budget min is required."); return; }
    if(!bmaxStr){ show(errBmax,"Budget max is required."); return; }
    if(!gsizeStr){ show(errG,"Group size is required."); return; }

    const budgetMin = parseInt(bminStr,10);
    const budgetMax = parseInt(bmaxStr,10);
    const groupSize = parseInt(gsizeStr,10);

    if(!Number.isInteger(groupSize) || groupSize < 1 || groupSize > 10){
      show(errG,"Group size must be an integer between 1 and 10."); return;
    }
    if(!Number.isInteger(budgetMin)){ show(errBmin,"Budget min must be an integer > 0."); return; }
    if(!Number.isInteger(budgetMax)){ show(errBmax,"Budget max must be an integer >= min."); return; }
    if(budgetMin <= 0 || budgetMax < budgetMin){
      if(budgetMin <= 0) show(errBmin,"Min must be > 0.");
      if(budgetMax < budgetMin) show(errBmax,"Max must be >= Min.");
      return;
    }

    if(!USE_LOCAL){
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
          const msg = data?.error || "Failed to sign up.";
          if(r.status === 409) show(errUser, msg); else toast(msg, false);
          return;
        }
        sessionStorage.setItem("userId", userid);
        location.href = `dashboard.html?user=${encodeURIComponent(userid)}`;
      }catch(err){
        console.error(err);
        toast("Failed to sign up. Please try again.", false);
      }
      return;
    }
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
    let propById = {};

    async function loadPropsMap(){
      try{
        const r = await fetch(`${API_BASE}/admin/properties`, {
          method: "POST",
          headers: { "Content-Type": "application/json" }
        });
        if(!r.ok) return;
        const data = await r.json();
        (data.properties || []).forEach(x=>{
          if(x && x.property_id){
            propById[x.property_id] = { type: x.type, location: x.location };
          }
        });
      }catch(e){}
    }

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
        ? hist.map(b => {
            const info = propById[b.propertyId];
            const title = info ? `${capWords(info.type)} · ${info.location}` : "Property";
            return `
            <div class="booking-item">
              <div class="left">
                <div class="name"><strong>${title}</strong></div>
                <div class="kbd small">${(b.propertyId||"").slice(0,8)}</div>
              </div>
              <div class="right small">
                ${b.start} → ${b.end}
                <button class="btn danger small" data-del data-prop="${b.propertyId}" data-start="${b.start}" data-end="${b.end}" style="margin-left:8px">Delete</button>
              </div>
            </div>`;
          }).join("")
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
        await loadPropsMap();  // ensure propById is ready for renderProfile
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
              <strong>${capWords(p.type)} in ${p.location}</strong>
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
      const title = qs("#list-title"); if(title) title.textContent = "Recommended for you (Top 20)";
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
    const lines = String(text||"").split(/\r?\n/);
    let html = "";
    let depth = 0;
  
    const open = (n)=>{ for(let i=0;i<n;i++){ html += `<ul class="ai-list">`; depth++; } };
    const close = (n)=>{ for(let i=0;i<n;i++){ html += `</ul>`; depth--; } };
    const closeAll = ()=>{ if(depth>0) close(depth); };
  
    for(const raw of lines){
      const line = raw.replace(/\u00A0/g," ").trimEnd();
      if(!line.trim()){ continue; }
  
      // Headings: #, ##, ### …
      const h = line.match(/^#{1,6}\s+(.*)$/);
      if(h){ closeAll(); html += `<div class="ai-h">${escapeHtml(h[1])}</div>`; continue; }
  
      // Hyphen bullets with nesting by indentation (2 spaces per level)
      const b = line.match(/^(\s*)-\s+(.*)$/);
      if(b){
        const indent = b[1].length;
        const target = Math.min(4, Math.floor(indent/2)); // 0,1,2,...
        if(target > depth) open(target - depth);
        else if(target < depth) close(depth - target);
  
        let content = escapeHtml(b[2]).replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>");
        html += `<li>${content}</li>`;
        continue;
      }
  
      // Paragraph line; close any open lists
      closeAll();
      let safe = escapeHtml(line).replace(/\*\*(.+?)\*\*/g,"<strong>$1</strong>");
      html += `<p>${safe}</p>`;
    }
    closeAll();
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

  // Users (backend mode)
  async function fetchUsers(){
    try{
      const r = await fetch(`${API_BASE}/admin/users`, { method: "POST", headers: { "Content-Type": "application/json" }});
      if(!r.ok) throw new Error(await r.text());
      const data = await r.json();
      renderUsers(Array.isArray(data.users) ? data.users : []);
    }catch(err){
      console.error(err);
      qs("#users-body").innerHTML = `<tr><td colspan="4" class="small">Failed to load users.</td></tr>`;
    }
  }

  function renderUsers(list){
    const tb = qs("#users-body");
    tb.innerHTML = list.map(u => `
      <tr data-u="${u.id}">
        <td class="kbd">${u.id}</td>
        <td>${u.name || ""}</td>
        <td>${(u.bookingHistory||[]).length}</td>
        <td><span class="pill">${u.preferredEnv || ""}</span>
            <span class="pill">${u.groupSize || 0} guests</span>
            ${Array.isArray(u.budgetRange) ? `<span class="pill">$${u.budgetRange[0]}–$${u.budgetRange[1]}</span>` : ""}
        </td>
      </tr>
    `).join("");

    // click to expand bookings for that user
    tb.querySelectorAll("tr[data-u]").forEach(tr=>{
      tr.addEventListener("click", ()=>{
        const next = tr.nextElementSibling;
        if(next && next.classList.contains("subrow")){ next.remove(); return; }
        const id = tr.getAttribute("data-u");
        const u = list.find(x=>x.id===id) || { bookingHistory: [] };
        const rows = (u.bookingHistory||[]).map(b => {
          const pname = String(b.propertyName || "");
          const i = pname.indexOf(" in ");
          const pretty = i >= 0 ? capWords(pname.slice(0, i)) + pname.slice(i) : capWords(pname);
          return `
            <div class="booking-item">
              <div class="left"><div class="name"><strong>${pretty}</strong></div><div class="kbd small">${(b.propertyId||"").slice(0,8)}</div></div>
              <div class="right small">${b.start} → ${b.end}</div>
            </div>`;
        }).join("") || `<div class="small">No bookings.</div>`;
        const tr2 = document.createElement("tr");
        tr2.className = "subrow";
        tr2.innerHTML = `<td colspan="4"><div style="padding:8px 6px">${rows}</div></td>`;
        tr.after(tr2);
      });
    });
  }


  // default: show users pane and load
  qs("[data-tab='users']")?.addEventListener("click", fetchUsers);
  qs("[data-tab='users']")?.click();


  // Properties
  function optionsHtml(arr, selected){
    return arr.map(v=>`<option value="${v}" ${v===selected?"selected":""}>${v}</option>`).join("");
  }
  function checkListHtml(arr, selected){
    const sel = new Set(selected||[]);
    return arr.map(v=>`<label class="option"><input type="checkbox" value="${v}" ${sel.has(v)?"checked":""}><span>${v}</span></label>`).join("");
  }
  function capWords(s){
    return String(s||"").split(/\s+/).map(w=> w.split("-").map(p=> p ? (p[0].toUpperCase()+p.slice(1)) : "").join("-")).join(" ");
  }
  const LOCATIONS_ADM = ["Vancouver","Toronto","Montreal","Calgary","Edmonton","Winnipeg","Halifax","Victoria","Quebec City","Fredericton"];
  const TYPES_ADM = ["cabin","apartment","cottage","loft","villa","tiny house","studio"];
  const FEATURES_ADM = ["mountain view","city skyline view","lakefront","riverfront","oceanfront","beach access","balcony or patio","rooftop terrace","private hot tub","sauna","private pool","fireplace","houskeeper service","BBQ grill","full kitchen","chef's kitchen","EV charger","free parking","garage","air conditioning","heating","washer and dryer","fast wifi","dedicated workspace","smart TV with streaming","game room","fitness room","ski-in/ski-out","wheelchair accessible","pet-friendly"];
  const TAGS_ADM = ["mountains","remote","adventure","beach","city","lake","river","ocean","forest","park","national park","state park","national forest","state forest","modern","rustic","historic","family-friendly","kid-friendly","pet-friendly","romantic","business-travel","nightlife","eco-friendly","spa","golf","foodie","farm-stay","glamping","long-term"];

  async function fetchProps(){
    try{
      const r = await fetch(`${API_BASE}/admin/properties`, { method:"POST", headers:{ "Content-Type":"application/json" }});
      if(!r.ok) throw new Error(await r.text());
      const data = await r.json();
      renderProps(data.properties || []);
    }catch(e){
      console.error(e);
      qs("#props-list").innerHTML = `<div class="small">Failed to load properties.</div>`;
    }
  }

  function renderProps(props){
    const list = qs("#props-list");
    list.innerHTML = (props||[]).map(p => `
      <div class="card pad">
        <div class="flex-between">
          <div>
            <div class="kbd small">${(p.property_id||"").slice(0,8)}</div>
            <strong>${capWords(p.type)}</strong> · ${p.location}
            <div class="small">${money(p.price_per_night)}/night · ${p.guest_capacity} guests</div>
            <div class="pills" style="margin-top:6px">${(p.tags||[]).map(t=>`<span class="pill">${t}</span>`).join("")}</div>
          </div>
          <div class="buttons">
            <button class="btn outline" data-edit="${p.property_id}">Update</button>
            <button class="btn danger" data-del="${p.property_id}">Delete</button>
          </div>
        </div>
        <div class="hidden" id="edit-${p.property_id}" style="margin-top:10px">
          <div class="grid grid-2">
            <div class="field"><label>Location</label>
              <select data-k="location">${optionsHtml(LOCATIONS_ADM, p.location)}</select>
              <div class="error hidden" data-err="location"></div>
            </div>
            <div class="field"><label>Type</label>
              <select data-k="type">${optionsHtml(TYPES_ADM, p.type)}</select>
              <div class="error hidden" data-err="type"></div>
            </div>
            <div class="field"><label>Price per night ($)</label>
              <input type="number" min="1" step="1" value="${p.price_per_night}" data-k="price_per_night">
              <div class="error hidden" data-err="price_per_night"></div>
            </div>
            <div class="field"><label>Guest capacity</label>
              <input type="number" min="1" max="10" step="1" value="${p.guest_capacity}" data-k="guest_capacity">
              <div class="error hidden" data-err="guest_capacity"></div>
            </div>
            <div class="field" style="grid-column:1/-1"><label>Features</label>
              <div class="multi" data-k="features">
                <button class="btn outline sm" id="btn-feat-${p.property_id}" type="button">Any features</button>
                <div class="menu hidden list" id="dd-feat-${p.property_id}">${checkListHtml(FEATURES_ADM, p.features||[])}</div>
              </div>
              <div class="error hidden" data-err="features"></div>
            </div>
            <div class="field" style="grid-column:1/-1"><label>Tags</label>
              <div class="multi" data-k="tags">
                <button class="btn outline sm" id="btn-tags-${p.property_id}" type="button">Any tags</button>
                <div class="menu hidden list" id="dd-tags-${p.property_id}">${checkListHtml(TAGS_ADM, p.tags||[])}</div>
              </div>
              <div class="error hidden" data-err="tags"></div>
            </div>
          </div>
          <div class="row">
            <button class="btn" data-save="${p.property_id}">Save</button>
            <button class="btn outline" data-cancel="${p.property_id}">Cancel</button>
          </div>
        </div>
      </div>
    `).join("");

    // init per-card multi-selects
    (props||[]).forEach(p=>{
      const btnF = qs(`#btn-feat-${p.property_id}`), ddF = qs(`#dd-feat-${p.property_id}`);
      const btnT = qs(`#btn-tags-${p.property_id}`), ddT = qs(`#dd-tags-${p.property_id}`);
      const updF = ()=>{ const sel = Array.from(ddF?.querySelectorAll("input:checked")||[]).length; if(btnF) btnF.textContent = sel ? `${sel} selected` : "Any features"; };
      const updT = ()=>{ const sel = Array.from(ddT?.querySelectorAll("input:checked")||[]).length; if(btnT) btnT.textContent = sel ? `${sel} selected` : "Any tags"; };
      btnF?.addEventListener("click", ()=> ddF?.classList.toggle("hidden"));
      btnT?.addEventListener("click", ()=> ddT?.classList.toggle("hidden"));
      ddF?.addEventListener("change", updF); ddT?.addEventListener("change", updT);
      document.addEventListener("click", (e)=>{ if(btnF && ddF && !btnF.contains(e.target) && !ddF.contains(e.target)) ddF.classList.add("hidden"); });
      document.addEventListener("click", (e)=>{ if(btnT && ddT && !btnT.contains(e.target) && !ddT.contains(e.target)) ddT.classList.add("hidden"); });
      updF(); updT();
    });

    // Events
    qsa("[data-edit]").forEach(b => b.addEventListener("click", ()=>{
      const id=b.getAttribute("data-edit");
      qsa("[id^='edit-']").forEach(x=>x.classList.add("hidden"));
      qs("#edit-"+id).classList.toggle("hidden");
    }));

    qsa("[data-cancel]").forEach(b => b.addEventListener("click", ()=>{
      const id=b.getAttribute("data-cancel"); qs("#edit-"+id).classList.add("hidden");
    }));

    qsa("[data-del]").forEach(b => b.addEventListener("click", async ()=>{
      const id=b.getAttribute("data-del");
      if(!confirm("Delete this property?")) return;
      try{
        const r = await fetch(`${API_BASE}/admin/property/delete`, { method:"POST", headers:{ "Content-Type":"application/json" }, body: JSON.stringify({ propertyId: id }) });
        if(!r.ok) throw new Error(await r.text());
        toast("Property deleted", true);
        fetchProps();
      }catch(e){ console.error(e); toast("Failed to delete", false); }
    }));

    qsa("[data-save]").forEach(b => b.addEventListener("click", async ()=>{
      const id=b.getAttribute("data-save");
      const box = qs("#edit-"+id);
      const getVal = (k)=> box.querySelector(`[data-k='${k}']`);
      const hide = el => el?.classList.add("hidden"); const show = (k,msg)=>{ const el=box.querySelector(`[data-err='${k}']`); if(el){ el.textContent=msg; el.classList.remove("hidden"); } };
      ["location","type","price_per_night","guest_capacity","features","tags"].forEach(k=>hide(box.querySelector(`[data-err='${k}']`)));

      const location = getVal("location").value;
      const type = getVal("type").value;
      const price = parseInt(getVal("price_per_night").value,10);
      const cap = parseInt(getVal("guest_capacity").value,10);
      const features = Array.from(getVal("features").querySelectorAll("input:checked")).map(i=>i.value);
      const tags = Array.from(getVal("tags").querySelectorAll("input:checked")).map(i=>i.value);

      // client validations
      if(!LOCATIONS_ADM.includes(location)){ show("location","Pick a valid location."); return; }
      if(!TYPES_ADM.includes(type)){ show("type","Pick a valid type."); return; }
      if(!Number.isInteger(price) || price<=0){ show("price_per_night","Positive integer required."); return; }
      if(!Number.isInteger(cap) || cap<1 || cap>10){ show("guest_capacity","Must be 1–10."); return; }
      if(!features.every(f=>FEATURES_ADM.includes(f))){ show("features","Invalid feature selected."); return; }
      if(!tags.every(t=>TAGS_ADM.includes(t))){ show("tags","Invalid tag selected."); return; }

      // send to backend
      const payload = { property_id:id, location, type, price_per_night:price, features, tags, guest_capacity:cap };
      try{
        const r = await fetch(`${API_BASE}/admin/property/update`, { method:"POST", headers:{ "Content-Type":"application/json" }, body: JSON.stringify(payload) });
        if(!r.ok){ const msg = await r.text().catch(()=> ""); toast(msg || "Failed to save", false); return; }
        toast("Saved", true);
        fetchProps();
      }catch(e){ console.error(e); toast("Failed to save", false); }
    }));
  }

  // Load properties when the tab is opened and on page load
  qs("[data-tab='props']")?.addEventListener("click", fetchProps);

  // Add property (backend)
  (function setupAddForm(){
    // Replace location/type inputs with selects
    const locEl = qs("#ap-location");
    if (locEl && locEl.tagName !== "SELECT"){
      const sel = document.createElement("select"); sel.id = "ap-location"; sel.innerHTML = `<option value="">Select…</option>` + LOCATIONS_ADM.map(v=>`<option>${v}</option>`).join("");
      locEl.replaceWith(sel);
      const err = document.createElement("div"); err.id="ap-location-err"; err.className="error hidden"; sel.parentElement.appendChild(err);
    }
    const typEl = qs("#ap-type");
    if (typEl && typEl.tagName !== "SELECT"){
      const sel = document.createElement("select"); sel.id = "ap-type"; sel.innerHTML = `<option value="">Select…</option>` + TYPES_ADM.map(v=>`<option>${v}</option>`).join("");
      typEl.replaceWith(sel);
      const err = document.createElement("div"); err.id="ap-type-err"; err.className="error hidden"; sel.parentElement.appendChild(err);
    }
    // Constrain price/capacity and add error holders
    const price = qs("#ap-price"); const cap = qs("#ap-capacity");
    if (price){ price.type="number"; price.min="2"; price.step="1"; price.placeholder="e.g., 150"; price.insertAdjacentHTML("afterend", `<div id="ap-price-err" class="error hidden"></div>`); }
    if (cap){ cap.type="number"; cap.min="1"; cap.max="10"; cap.step="1"; cap.placeholder="1–10"; cap.insertAdjacentHTML("afterend", `<div id="ap-cap-err" class="error hidden"></div>`); }

    // Replace features/tags inputs with multiselect dropdowns
    function buildMulti(hostId, btnId, ddId, items, anyLabel){
      const host = qs(hostId);
      if (!host) return { get: ()=>[], label:()=>{} };
      const wrap = document.createElement("div");
      wrap.className = "multi";
      wrap.innerHTML = `
        <button class="btn outline sm" id="${btnId}" type="button">${anyLabel}</button>
        <div class="menu hidden list" id="${ddId}">
          ${items.map(v=>`<label class="option"><input type="checkbox" value="${v}"><span>${v}</span></label>`).join("")}
        </div>
        <div id="${btnId}-err" class="error hidden"></div>`;
      host.replaceWith(wrap);
      const btn = qs("#"+btnId), dd = qs("#"+ddId), err = qs("#"+btnId+"-err");
      const update = ()=>{ const n = dd.querySelectorAll("input:checked").length; btn.textContent = n ? `${n} selected` : anyLabel; };
      btn.addEventListener("click", ()=> dd.classList.toggle("hidden"));
      dd.addEventListener("change", update);
      document.addEventListener("click", (e)=>{ if(!btn.contains(e.target) && !dd.contains(e.target)) dd.classList.add("hidden"); });
      update();
      return {
        get: ()=> Array.from(dd.querySelectorAll("input:checked")).map(i=>i.value),
        showErr: (msg)=>{ err.textContent=msg; err.classList.remove("hidden"); },
        clearErr: ()=> err.classList.add("hidden"),
      };
    }
    const mFeat = buildMulti("#ap-features", "ap-feat-btn", "ap-feat-dd", FEATURES_ADM, "Any features");
    const mTags = buildMulti("#ap-tags", "ap-tags-btn", "ap-tags-dd", TAGS_ADM, "Any tags");

    // Create click
    qs("#ap-create")?.addEventListener("click", async ()=>{
      // clear errors
      const hide = id => qs(id)?.classList.add("hidden");
      hide("#ap-location-err"); hide("#ap-type-err"); hide("#ap-price-err"); hide("#ap-cap-err"); mFeat.clearErr(); mTags.clearErr();

      const location = qs("#ap-location")?.value || "";
      const ptype    = qs("#ap-type")?.value || "";
      const priceVal = parseInt(qs("#ap-price")?.value || "", 10);
      const capVal   = parseInt(qs("#ap-capacity")?.value || "", 10);
      const features = mFeat.get();
      const tags     = mTags.get();

      let invalid = false;
      if(!location){ const el=qs("#ap-location-err"); el.textContent="Location is required."; el.classList.remove("hidden"); invalid = true; }
      if(!ptype){ const el=qs("#ap-type-err"); el.textContent="Type is required."; el.classList.remove("hidden"); invalid = true; }
      if(!Number.isInteger(priceVal) || priceVal <= 1){ const el=qs("#ap-price-err"); el.textContent="Price must be an integer > 1."; el.classList.remove("hidden"); invalid = true; }
      if(!Number.isInteger(capVal) || capVal < 1 || capVal > 10){ const el=qs("#ap-cap-err"); el.textContent="Capacity must be 1–10."; el.classList.remove("hidden"); invalid = true; }
      if(!features.length){ mFeat.showErr("Select at least one feature."); invalid = true; }
      if(!tags.length){ mTags.showErr("Select at least one tag."); invalid = true; }
      if(invalid) return;

      try{
        const r = await fetch(`${API_BASE}/admin/property/create`, {
          method:"POST",
          headers:{ "Content-Type":"application/json" },
          body: JSON.stringify({
            location, type: ptype,
            price_per_night: priceVal,
            guest_capacity: capVal,
            features, tags
          })
        });
        if(!r.ok){
          const data = await r.json().catch(()=> ({}));
          const msg = data?.error || "Failed to create property.";
          toast(msg, false);
          return;
        }
        toast("Successfully create property!", true);
        // optional: reset minimal fields
        qs("#ap-price").value = ""; qs("#ap-capacity").value = "";
        document.querySelectorAll("#ap-feat-dd input:checked").forEach(i=> i.checked=false);
        document.querySelectorAll("#ap-tags-dd input:checked").forEach(i=> i.checked=false);
        qs("#ap-feat-btn").textContent = "Any features";
        qs("#ap-tags-btn").textContent = "Any tags";
        fetchProps();
      }catch(e){
        console.error(e); toast("Failed to create property.", false);
      }
    });
  })();

  // Generate properties using LLM
  qs("#gen-btn")?.addEventListener("click", async ()=>{
    const inputEl = qs("#gen-n");
    const err = qs("#gen-err");
    const status = qs("#gen-status");
    err?.classList.add("hidden"); if(status) status.textContent = "";

    const raw = inputEl?.value || "";
    const n = parseInt(raw, 10);
    if(!Number.isInteger(n) || n < 1){
      if(err){ err.textContent = "Enter a positive integer (>= 1)."; err.classList.remove("hidden"); }
      return;
    }

    const btn = qs("#gen-btn");
    btn.disabled = true; if(inputEl) inputEl.disabled = true;

    let dots = 0, tmr = null;
    if(status){
      status.textContent = "Generating properties...";
      tmr = setInterval(()=>{ dots = (dots+1)%4; status.textContent = "Generating properties" + ".".repeat(dots); }, 700);
    }

    try{
      if(!USE_LOCAL){
        const r = await fetch(`${API_BASE}/admin/properties/generate`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ n })
        });
        if(!r.ok){
          const data = await r.json().catch(()=> ({}));
          throw new Error(data?.error || "Generation failed");
        }
      }else{
        const list = generateProperties(n);
        DB.properties = [...list, ...DB.properties]; saveDb(DB);
      }
      if(status) status.textContent = `Successfully generated ${n} properties!`;
      fetchProps();
    }catch(e){
      if(status) status.textContent = e?.message || "Generation failed";
    }finally{
      if(tmr) clearInterval(tmr);
      btn.disabled = false; if(inputEl) inputEl.disabled = false;
    }
  });
}

// Expose initializers globally
window.SummerStay = { initLogin, initRegister, initDashboard, initProfile, initSearch, initAdmin, logoutAll, initHome };
