import json

# Read the prompts data
with open(r'D:\Personal\Downloads\robot-memory-git\prompts_data.js', 'r', encoding='utf-8') as f:
    js_data = f.read()

# Extract the JSON data part
data_json = js_data.replace('const PROMPTS_DATA=', '')

# HTML template
html_template = '''<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Robot Memory - AI Prompt Collection</title>
    <style>
        :root { --bg-primary: #ffffff; --bg-secondary: #f5f5f7; --text-primary: #1d1d1f; --text-secondary: #86868b; --accent: #0071e3; --border: rgba(0,0,0,0.1); }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { font-family: -apple-system, BlinkMacSystemFont, "SF Pro Text", sans-serif; background: var(--bg-primary); color: var(--text-primary); line-height: 1.5; -webkit-font-smoothing: antialiased; padding: 20px; }
        .container { max-width: 1080px; margin: 0 auto; }
        header { padding: 40px 0; text-align: center; }
        .logo { font-size: 14px; font-weight: 600; color: var(--text-secondary); margin-bottom: 8px; }
        h1 { font-size: 36px; font-weight: 700; margin-bottom: 12px; }
        .subtitle { font-size: 18px; color: var(--text-secondary); margin-bottom: 20px; }
        .stats { display: flex; justify-content: center; gap: 30px; margin-bottom: 20px; flex-wrap: wrap; }
        .stat-item { text-align: center; }
        .stat-number { font-size: 24px; font-weight: 700; }
        .stat-label { font-size: 12px; color: var(--text-secondary); }
        .search-section { padding: 20px 0; border-bottom: 1px solid var(--border); }
        .search-box input { width: 100%; max-width: 400px; padding: 12px 16px; font-size: 14px; border: 1px solid var(--border); border-radius: 10px; background: var(--bg-secondary); }
        .filters { display: flex; justify-content: center; gap: 8px; padding: 16px 0; flex-wrap: wrap; }
        .filter-btn { padding: 6px 14px; font-size: 13px; border: none; border-radius: 16px; background: transparent; color: var(--text-secondary); cursor: pointer; }
        .filter-btn:hover { background: var(--bg-secondary); }
        .filter-btn.active { background: var(--text-primary); color: var(--bg-primary); }
        .cards { display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 16px; padding-bottom: 40px; }
        .card { background: var(--bg-primary); border: 1px solid var(--border); border-radius: 14px; padding: 16px; cursor: pointer; transition: all 0.2s; }
        .card:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
        .card-header { display: flex; justify-content: space-between; gap: 8px; margin-bottom: 10px; }
        .card-title { font-size: 15px; font-weight: 600; }
        .card-badge { padding: 3px 8px; font-size: 11px; border-radius: 4px; white-space: nowrap; }
        .badge-tool { background: #e8f4fd; color: #0071e3; }
        .badge-general { background: #f2e8fd; color: #7c3aed; }
        .badge-draw { background: #fff4e8; color: #f59e0b; }
        .badge-write { background: #e8f9ed; color: #10b981; }
        .card-preview { font-size: 13px; color: var(--text-secondary); line-height: 1.5; margin-bottom: 10px; display: -webkit-box; -webkit-line-clamp: 3; -webkit-box-orient: vertical; overflow: hidden; }
        .card-footer { display: flex; justify-content: space-between; align-items: center; padding-top: 10px; border-top: 1px solid var(--border); font-size: 12px; color: var(--text-secondary); }
        .modal { display: none; position: fixed; inset: 0; background: rgba(0,0,0,0.5); z-index: 1000; align-items: center; justify-content: center; padding: 20px; }
        .modal.active { display: flex; }
        .modal-content { background: var(--bg-primary); border-radius: 16px; max-width: 600px; width: 100%; max-height: 80vh; overflow: hidden; display: flex; flex-direction: column; }
        .modal-header { padding: 20px; border-bottom: 1px solid var(--border); display: flex; justify-content: space-between; align-items: center; }
        .modal-close-btn { width: 28px; height: 28px; border: none; border-radius: 50%; background: var(--bg-secondary); cursor: pointer; font-size: 18px; }
        .modal-title { font-size: 18px; font-weight: 700; }
        .modal-body { padding: 20px; overflow-y: auto; flex: 1; }
        .section-label { font-size: 12px; font-weight: 600; color: var(--text-secondary); margin-bottom: 6px; text-transform: uppercase; }
        .section-content { font-size: 13px; line-height: 1.6; white-space: pre-wrap; background: var(--bg-secondary); padding: 12px; border-radius: 8px; max-height: 200px; overflow-y: auto; }
        .modal-footer { padding: 16px 20px; border-top: 1px solid var(--border); display: flex; gap: 10px; }
        .modal-btn { flex: 1; padding: 12px; border: none; border-radius: 8px; cursor: pointer; font-size: 14px; }
        .modal-btn-secondary { background: var(--bg-secondary); }
        .modal-btn-primary { background: var(--accent); color: white; }
        .toast { position: fixed; bottom: 20px; left: 50%; transform: translateX(-50%) translateY(100px); background: var(--text-primary); color: white; padding: 10px 20px; border-radius: 8px; opacity: 0; transition: all 0.3s; z-index: 2000; font-size: 14px; }
        .toast.show { transform: translateX(-50%) translateY(0); opacity: 1; }
    </style>
</head>
<body>
    <div class="container">
        <header>
            <div class="logo">Robot Memory</div>
            <h1>AI Prompt Collection</h1>
            <p class="subtitle">31 个精心策划的提示词</p>
            <div class="stats">
                <div class="stat-item"><div class="stat-number">31</div><div class="stat-label">总计</div></div>
                <div class="stat-item"><div class="stat-number">20</div><div class="stat-label">工具</div></div>
                <div class="stat-item"><div class="stat-number">10</div><div class="stat-label">通用</div></div>
                <div class="stat-item"><div class="stat-number">1</div><div class="stat-label">创作</div></div>
            </div>
        </header>
        <div class="search-section">
            <div style="display:flex;justify-content:center;">
                <div class="search-box">
                    <input type="text" id="searchInput" placeholder="搜索提示词...">
                </div>
            </div>
        </div>
        <div class="filters" id="filters"></div>
        <div class="cards" id="cardsContainer"></div>
    </div>
    <div class="modal" id="modal">
        <div class="modal-content">
            <div class="modal-header">
                <div class="modal-title" id="modalTitle"></div>
                <button class="modal-close-btn" onclick="closeModal()">&times;</button>
            </div>
            <div class="modal-body">
                <div class="section-label">系统指令</div>
                <div class="section-content" id="modalSystemPrompt"></div>
                <div class="section-label" style="margin-top:16px;">用户指令</div>
                <div class="section-content" id="modalUserPrompt"></div>
                <div class="section-label" style="margin-top:16px;">添加时间</div>
                <div class="section-content" id="modalDate"></div>
            </div>
            <div class="modal-footer">
                <button class="modal-btn modal-btn-secondary" onclick="closeModal()">关闭</button>
                <button class="modal-btn modal-btn-primary" onclick="copyPrompt()">复制</button>
            </div>
        </div>
    </div>
    <div class="toast" id="toast">已复制</div>
    <script>
''' + js_data + '''
let currentPrompt=null,activeFilter="all";
function getBadgeClass(e){return e.includes("工具")?"badge-tool":e.includes("通用")?"badge-general":e.includes("绘图")?"badge-draw":e.includes("写作")?"badge-write":"badge-general"}
function renderCards(e){const t=document.getElementById("cardsContainer");if(0===e.length){t.innerHTML='<div style="text-align:center;padding:40px;color:#888;">没有找到匹配的提示词</div>';return}t.innerHTML=e.map((e,n)=>`<div class="card" onclick="openModal(${n})"><div class="card-header"><div class="card-title">${e.title}</div><span class="card-badge ${getBadgeClass(e.category)}">${e.category.replace("芯片","")}</span></div><div class="card-preview">${(e.systemPrompt||e.userPrompt||"").substring(0,100)}...</div><div class="card-footer"><span>${e.date}</span><span>查看详情</span></div></div>`).join("")}
function openModal(e){currentPrompt=PROMPTS_DATA[e],document.getElementById("modalTitle").textContent=currentPrompt.title,document.getElementById("modalSystemPrompt").textContent=currentPrompt.systemPrompt||"无",document.getElementById("modalUserPrompt").textContent=currentPrompt.userPrompt||"无",document.getElementById("modalDate").textContent=currentPrompt.date,document.getElementById("modal").classList.add("active"),document.body.style.overflow="hidden"}
function closeModal(){document.getElementById("modal").classList.remove("active"),document.body.style.overflow=""}
function copyPrompt(){if(!currentPrompt)return;let e=`【${currentPrompt.title}】\\n分类：${currentPrompt.category}\\n\\n系统指令：\\n${currentPrompt.systemPrompt||"无"}\\n\\n用户指令：\\n${currentPrompt.userPrompt||"无"}\\n\\n添加时间：${currentPrompt.date}`;navigator.clipboard.writeText(e).then(()=>{const e=document.getElementById("toast");e.classList.add("show"),setTimeout(()=>e.classList.remove("show"),2000)})}
function applyFilters(){const e=document.getElementById("searchInput").value.toLowerCase(),n=PROMPTS_DATA.filter(t=>("all"===activeFilter||t.category===activeFilter)&&(!e||t.title.toLowerCase().includes(e)||(t.systemPrompt||"").toLowerCase().includes(e)||(t.userPrompt||"").toLowerCase().includes(e)));renderCards(n)}document.querySelectorAll(".filter-btn").forEach(e=>{e.addEventListener("click",()=>{document.querySelectorAll(".filter-btn").forEach(e=>e.classList.remove("active")),e.classList.add("active"),activeFilter=e.dataset.filter,applyFilters()})}),document.getElementById("searchInput").addEventListener("input",applyFilters);const categories=[...new Set(PROMPTS_DATA.map(e=>e.category))];document.getElementById("filters").innerHTML=`<button class="filter-btn active" data-filter="all">全部</button>`+categories.map(e=>`<button class="filter-btn" data-filter="${e}">${e}</button>`).join("");document.getElementById("modal").addEventListener("click",e=>{"modal"===e.target.id&&closeModal()}),document.addEventListener("keydown",e=>{"Escape"===e.key&&closeModal()});renderCards(PROMPTS_DATA);
    </script>
</body>
</html>'''

# Write the final HTML
with open(r'D:\Personal\Downloads\robot-memory-git\index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

print("HTML file generated successfully!")
