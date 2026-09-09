import base64
import html
import random
from datetime import datetime

import streamlit as st


st.set_page_config(
    page_title="わたくし柴原と申します。",
    page_icon="㊞",
    layout="centered",
    initial_sidebar_state="collapsed",
)

CSS = r"""
<style>
:root {
  --paper:#fbfaf6; --ink:#2d2a26; --muted:#777067; --vermilion:#a93b32;
  --line:#ded8ce; --note:#fff5b8;
}
html, body, [data-testid="stAppViewContainer"] { background:var(--paper); color:var(--ink); }
html { color-scheme:light !important; }
[data-testid="stAppViewContainer"], [data-testid="stAppViewContainer"] * { color-scheme:light; }
[data-testid="stHeader"] { background:rgba(251,250,246,.95); }
.block-container { max-width:720px; padding-top:2.4rem; padding-bottom:6rem; }
#MainMenu, footer { visibility:hidden; }
.app-title { text-align:center; color:#2d2a26 !important; font-weight:800; font-size:1.35rem; line-height:1.5;
  letter-spacing:.05em; margin:0 0 .15rem; padding-top:.35rem; opacity:1 !important; }
.app-sub { text-align:center; color:#665f57 !important; font-size:.82rem; margin-bottom:1.2rem; opacity:1 !important; }
.attendance { width:max-content; max-width:100%; margin:-.65rem auto 1rem; padding:5px 11px; border:1px solid #ded8ce;
  border-radius:999px; background:#fff; color:#6f675e; font-size:.74rem; font-weight:700; letter-spacing:.04em; }
.section-title { font-weight:800; font-size:1.25rem; margin:.25rem 0 .7rem; }
.muted { color:var(--muted); font-size:.9rem; }
.callout { border-left:4px solid var(--vermilion); background:#fff; padding:10px 13px; border-radius:8px; margin:10px 0 14px; }
.hero-copy { font-size:1.05rem; line-height:1.7; text-align:center; margin:.5rem 0 1rem; }
[data-testid="stForm"] [data-testid="stCheckbox"] label { display:flex; align-items:center; gap:11px; margin:5px 0 9px; cursor:pointer; }
[data-testid="stForm"] [data-testid="stCheckbox"] label > div:first-child,
[data-testid="stForm"] [data-testid="stCheckbox"] label > span:first-child { position:absolute; opacity:0; pointer-events:none; }
[data-testid="stForm"] [data-testid="stCheckbox"] input[type="checkbox"] { position:absolute !important; width:0 !important;
  height:0 !important; margin:0 !important; opacity:0 !important; pointer-events:none !important; }
[data-testid="stForm"] [data-testid="stCheckbox"] input[type="checkbox"] + div { display:none !important; }
[data-testid="stForm"] [data-testid="stCheckbox"] label > span:has(input[type="checkbox"]),
[data-testid="stForm"] [data-testid="stCheckbox"] label > div:has(input[type="checkbox"]) { position:absolute !important;
  width:0 !important; height:0 !important; margin:0 !important; overflow:hidden !important; opacity:0 !important; pointer-events:none !important; }
[data-testid="stForm"] [data-testid="stCheckbox"] label::before { content:""; display:inline-flex; align-items:center; justify-content:center;
  flex:0 0 42px; width:42px; height:42px; box-sizing:border-box; border:3px solid #c8bbb5; border-radius:50%;
  color:var(--vermilion); background:#fff; font-family:"Yu Mincho","Hiragino Mincho ProN",serif; font-size:1.05rem; font-weight:800;
  transform:rotate(-4deg); transition:border-color .15s ease, color .15s ease, transform .15s ease; }
[data-testid="stForm"] [data-testid="stCheckbox"] label:has(input:checked)::before { content:"済"; border-color:var(--vermilion);
  box-shadow:inset 0 0 0 1px rgba(169,59,50,.18); animation:sealPop .34s cubic-bezier(.2,.85,.3,1.2) both; }
@keyframes sealPop { 0%{opacity:.15;transform:rotate(-4deg) scale(1.35)} 55%{opacity:1;transform:rotate(-4deg) scale(.9)} 100%{transform:rotate(-4deg) scale(1.04)} }

.stamp { display:inline-flex; align-items:center; justify-content:center; width:54px; height:54px;
  border:3px solid var(--stamp-color,#a93b32); color:var(--stamp-color,#a93b32); border-radius:50%;
  font-weight:800; line-height:1; text-align:center; font-size:16px; letter-spacing:-1px; transform:rotate(-3deg);
  background:rgba(255,255,255,.25); box-shadow:inset 0 0 0 1px rgba(169,59,50,.18); }
.stamp.small { width:32px; height:32px; border-width:2px; font-size:11px; }
.stamps-line .stamp:last-child { animation:stampArrive .34s cubic-bezier(.2,.82,.28,1.18) both; }
@keyframes stampArrive { 0%{opacity:0;transform:rotate(-8deg) scale(1.4)} 65%{opacity:1;transform:rotate(-2deg) scale(.9)} 100%{transform:rotate(-3deg) scale(1)} }
.stamp.square { border-radius:7px; }

.business-card { position:relative; overflow:hidden; aspect-ratio:1.72/1; min-height:250px; border:1px solid #d8d0c4;
  border-radius:10px; padding:28px 30px; background:#fffefb; box-shadow:0 10px 28px rgba(45,42,38,.09);
  margin:8px 0 18px; display:flex; flex-direction:column; justify-content:space-between; }
.presented-card { width:100%; max-width:680px; min-height:350px; margin:8px auto 18px;
  animation:handOverCard .52s cubic-bezier(.2,.82,.25,1) both; transform-origin:50% 100%; }
@keyframes handOverCard {
  0% { opacity:0; transform:translateY(48px) scale(.92) rotate(1.5deg); filter:blur(2px); }
  72% { opacity:1; transform:translateY(-3px) scale(1.012) rotate(-.25deg); filter:blur(0); }
  100% { opacity:1; transform:translateY(0) scale(1) rotate(0); }
}
.profile-prompt { text-align:center; color:var(--muted); font-size:.8rem; margin:-2px 0 10px; letter-spacing:.04em; }
.business-card.theme-white { background:#fffefb; border-color:#d8d0c4; }
.business-card.theme-washi { background:linear-gradient(135deg,#fbf7ec 0%,#f6f0df 100%); border-color:#d3c6aa; }
.business-card.theme-retro { background:#f1eadb; border-color:#b7a78b; box-shadow:0 10px 28px rgba(82,67,45,.12); }
.business-card.theme-modern { background:#f7f7f5; border-color:#cfcfc9; border-radius:4px; }
.business-card.theme-sakura { background:linear-gradient(145deg,#fffafb 0%,#fbeef1 100%); border-color:#e8cfd6; }
.business-card.theme-black { background:linear-gradient(145deg,#272624 0%,#171716 100%); border-color:#44413d; color:#f5f1e8;
  box-shadow:0 12px 30px rgba(0,0,0,.20); }
.business-card::before { content:""; position:absolute; inset:0; pointer-events:none; opacity:.24;
  background-image:radial-gradient(rgba(96,82,63,.12) .65px, transparent .65px); background-size:6px 6px; }
.business-card::after { content:""; position:absolute; width:210px; height:210px; border:1px solid rgba(169,59,50,.08);
  border-radius:50%; right:-95px; bottom:-115px; }
.business-card.theme-black .card-label,.business-card.theme-black .card-honorific,.business-card.theme-black .card-meta-item,
.business-card.theme-black .card-signoff { color:#bcb5aa; }
.business-card.theme-black .surname,.business-card.theme-black .card-meta-item b { color:#f8f4ec; }
.business-card.theme-black .card-bio { color:#ddd6ca; }
.business-card.theme-black .card-bottom { border-top-color:#48443f; }
.business-card.theme-black .status-badge { background:rgba(255,255,255,.07); color:#d8d1c6; border-color:#514c46; }
.business-card.theme-modern .surname { font-family:system-ui,-apple-system,"Hiragino Sans",sans-serif; letter-spacing:.08em; }
.business-card.theme-retro .card-label { color:#7e684b; }
.business-card.theme-sakura::after { border-color:rgba(190,100,125,.16); }
.card-topline { position:relative; z-index:1; display:flex; justify-content:space-between; align-items:flex-start; gap:18px; }
.card-label { font-size:.68rem; letter-spacing:.18em; color:#91877b; text-transform:uppercase; margin-bottom:12px; }
.card-honorific { font-size:.77rem; color:#81786e; letter-spacing:.12em; margin-bottom:4px; }
.surname { font-family:"Yu Mincho","Hiragino Mincho ProN",serif; font-size:2.05rem; line-height:1.15; font-weight:700; letter-spacing:.13em; }
.card-bio { margin-top:12px; color:#5d574f; font-size:.9rem; line-height:1.65; max-width:72%; }
.card-interests { margin-top:7px; color:#7b7168; font-size:.72rem; letter-spacing:.03em; }
.card-bottom { position:relative; z-index:1; border-top:1px solid #e8e1d7; padding-top:13px; display:flex; justify-content:space-between; gap:12px; align-items:flex-end; }
.card-meta { display:flex; gap:18px; flex-wrap:wrap; }
.card-meta-item { font-size:.69rem; letter-spacing:.06em; color:#8a8177; }
.card-meta-item b { display:block; margin-top:3px; font-size:.92rem; letter-spacing:0; color:#403b35; }
.card-signoff { font-size:.66rem; letter-spacing:.14em; color:#a39a8f; white-space:nowrap; }
.card-stamp-wrap { flex:0 0 auto; padding-top:2px; transform:scale(1.08); transform-origin:top right; }
.status-badge { display:inline-flex; align-items:center; gap:7px; margin-top:10px; padding:5px 9px; border:1px solid rgba(120,110,100,.22);
  border-radius:999px; background:rgba(255,255,255,.62); color:#675f56; font-size:.74rem; font-weight:700; }
.status-dot { width:7px; height:7px; border-radius:50%; background:var(--status-color,#7d8f74); box-shadow:0 0 0 3px rgba(125,143,116,.10); }
.card-theme-chip { display:inline-block; font-size:.72rem; font-weight:700; padding:3px 8px; border-radius:999px; border:1px solid #d8d0c4;
  margin-left:6px; color:#6e655b; background:#fff; }
.card-theme-preview { border:1px solid var(--line); border-radius:12px; padding:12px 13px; background:#fff; margin:6px 0 10px; }

.ringi { border:1px solid var(--line); border-radius:14px; background:#fff; padding:16px 16px 14px; margin:10px 0 16px;
  box-shadow:0 5px 18px rgba(45,42,38,.045); }
.ringi-head { display:flex; justify-content:space-between; gap:12px; align-items:flex-start; }
.ringi-kicker { color:var(--vermilion); font-weight:800; font-size:.76rem; letter-spacing:.08em; }
.ringi-title { font-weight:800; font-size:1.05rem; margin:8px 0 10px; }
.ringi-body { white-space:pre-wrap; line-height:1.75; font-size:.96rem; }
.ringi-meta { color:var(--muted); font-size:.78rem; margin-top:2px; }
.stamps-line { margin-top:12px; padding-top:10px; border-top:1px dashed var(--line); display:flex; align-items:center; gap:7px; flex-wrap:wrap; }
.note { background:var(--note); padding:9px 11px; border-radius:3px; margin:7px 0; box-shadow:1px 2px 4px rgba(0,0,0,.06); transform:rotate(-.25deg); }
.note-name { font-weight:700; font-size:.78rem; color:#665f45; }
.note-body { font-size:.9rem; margin-top:2px; }

.courtesy-wait { display:flex; align-items:center; gap:18px; padding:16px 18px; margin:10px 0; border:1px solid #ead8d2;
  border-radius:14px; background:#fffdf9; color:var(--ink); box-shadow:0 6px 20px rgba(67,52,45,.06); }
.card-clerk { position:relative; width:82px; height:68px; flex:0 0 82px; }
.clerk-head { position:absolute; width:24px; height:24px; left:29px; top:1px; border:2px solid #5b554f; border-radius:50%; background:#f7ddc7; }
.clerk-body { position:absolute; width:42px; height:39px; left:20px; top:25px; border-radius:12px 12px 5px 5px; background:#e7e3dc; border:2px solid #777067; }
.clerk-card { position:absolute; width:30px; height:18px; left:49px; top:37px; border:2px solid var(--vermilion); border-radius:2px;
  background:#fff; animation:offerCard 1.25s ease-in-out infinite; }
.clerk-hands::before,.clerk-hands::after { content:""; position:absolute; width:28px; height:3px; top:46px; background:#777067; border-radius:4px; }
.clerk-hands::before { left:27px; transform:rotate(13deg); }.clerk-hands::after { left:34px; transform:rotate(-10deg); }
@keyframes offerCard { 0%,18%{transform:translateX(-15px) scale(.88);opacity:.35} 48%,72%{transform:translateX(0) scale(1);opacity:1} 100%{transform:translateX(-15px) scale(.88);opacity:.35} }
.wait-copy b { display:block; font-size:.9rem; margin-bottom:3px; }.wait-copy span { color:var(--muted); font-size:.78rem; }

[data-testid="stForm"] { border:1px solid var(--line); border-radius:14px; padding:16px; background:#fff; }
.stButton > button, .stFormSubmitButton > button { border-radius:999px; font-weight:700; background:#fff !important; color:#403b35 !important;
  border:1px solid #d9d3ca !important; box-shadow:none !important; }
.stButton > button:hover, .stFormSubmitButton > button:hover { color:var(--vermilion) !important; border-color:#c77b72 !important; background:#fffaf8 !important; }
.stButton > button:active, .stFormSubmitButton > button:active { transform:translateY(1px); }
.stButton > button[kind="primary"], .stFormSubmitButton > button[kind="primary"] { background:var(--vermilion) !important;
  color:#fff !important; border-color:var(--vermilion) !important; }
.stButton > button[kind="primary"]:hover, .stFormSubmitButton > button[kind="primary"]:hover { background:#913128 !important; color:#fff !important; }
[data-baseweb="input"] > div, [data-baseweb="base-input"], [data-baseweb="textarea"] > div,
[data-baseweb="select"] > div, [data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea { background:#fff !important;
  color:#2d2a26 !important; border-color:#d8d2ca !important; -webkit-text-fill-color:#2d2a26 !important; }
[data-testid="stTextInput"] input::placeholder, [data-testid="stTextArea"] textarea::placeholder { color:#817970 !important; opacity:1 !important; }
[data-baseweb="input"]:focus-within, [data-baseweb="textarea"]:focus-within, [data-baseweb="select"]:focus-within { border-color:var(--vermilion) !important;
  box-shadow:0 0 0 3px rgba(169,59,50,.12) !important; }
[role="listbox"], [role="option"], [data-baseweb="popover"] { background:#fff !important; color:#2d2a26 !important; }
[role="option"]:hover, [role="option"][aria-selected="true"] { background:#faece8 !important; color:#2d2a26 !important; }
[class*="st-key-stamp-"] button { background:#fff !important; color:var(--vermilion) !important; border-color:var(--vermilion) !important; }
[class*="st-key-stamp-"][class*="-done"] button { background:#fae9e5 !important; color:#8f2f27 !important; box-shadow:inset 0 0 0 1px rgba(169,59,50,.08) !important; }
[class*="st-key-note-"] button { background:#fff8d8 !important; color:#635a3c !important; border-color:#eadb94 !important; }
[class*="st-key-save-"] button { background:#fff !important; color:#5f5952 !important; border-color:#d8d2ca !important; }
[class*="st-key-profile-"] button, [class*="st-key-related-"] button, [class*="st-key-person-"] button,
[class*="st-key-notice-person-"] button { background:#fffdf9 !important; color:#413a34 !important; border-color:#e3d8ce !important;
  border-radius:9px !important; box-shadow:0 2px 7px rgba(69,53,45,.05) !important; }
[data-testid="stRadio"] > div { gap:.2rem; }
[data-testid="stRadio"] label { padding:.35rem .55rem; border-radius:10px; }
[data-testid="stRadio"] label:has(input:checked) { background:#fae9e5 !important; color:#8f2f27 !important; box-shadow:inset 0 0 0 1px #dfaaa2; }
[data-testid="stRadio"] label p { color:#403b35 !important; }
[data-testid="stRadio"] label:has(input:checked) p { color:#8f2f27 !important; font-weight:700 !important; }
[data-testid="stFileUploader"] button { background:#fff !important; color:#403b35 !important; border:1px solid #d8d2ca !important; }
[data-testid="stExpander"] { background:#fffdf9; border-color:#ded8ce !important; }
@media (max-width:640px) {
  /* Streamlitのスマホ用ツールバーと重ならないよう、本文の開始位置を下げる */
  .block-container { padding:4.6rem .75rem 6.5rem; }
  .app-title { font-size:1.22rem; padding-top:.25rem; }
  /* 主ナビは端末幅いっぱいの5等分。内容幅による横はみ出しを防ぐ */
  div[class*="st-key-nav"] [data-testid="stRadio"] > div {
    display:grid !important; grid-template-columns:repeat(5,minmax(0,1fr)) !important;
    width:100% !important; gap:.2rem !important;
  }
  div[class*="st-key-nav"] [data-testid="stRadio"] label {
    width:100% !important; min-width:0 !important; justify-content:center !important;
    padding:.42rem .14rem !important; font-size:.79rem !important; white-space:nowrap !important;
  }
  div[class*="st-key-nav"] [data-testid="stRadio"] label > div:last-child {
    min-width:0 !important; white-space:nowrap !important;
  }
  /* スマホでは環境依存の黒い標準ラジオ印を隠し、文字タブとして表示する */
  div[class*="st-key-nav"] [data-testid="stRadio"] label > div:first-child,
  div[class*="st-key-circulation_filter"] [data-testid="stRadio"] label > div:first-child {
    display:none !important;
  }
  div[class*="st-key-nav"] [data-testid="stRadio"] label p,
  div[class*="st-key-circulation_filter"] [data-testid="stRadio"] label p {
    display:block !important; visibility:visible !important; opacity:1 !important;
    color:#403b35 !important; margin:0 !important; white-space:nowrap !important;
  }
  div[class*="st-key-nav"] [data-testid="stRadio"] label:has(input:checked) p,
  div[class*="st-key-circulation_filter"] [data-testid="stRadio"] label:has(input:checked) p {
    color:#8f2f27 !important; font-weight:800 !important;
  }
  div[class*="st-key-circulation_filter"] [data-testid="stRadio"] > div {
    display:grid !important; grid-template-columns:repeat(4,minmax(0,1fr)) !important;
    width:100% !important; gap:.25rem !important;
  }
  div[class*="st-key-circulation_filter"] [data-testid="stRadio"] label {
    width:100% !important; min-width:0 !important; justify-content:center !important;
    padding:.42rem .18rem !important; font-size:.82rem !important; white-space:nowrap !important;
  }
  .business-card { aspect-ratio:auto; min-height:220px; padding:21px 19px; border-radius:9px; }
  .presented-card { min-height:220px; }
  .surname { font-size:1.65rem; }
  .card-bio { max-width:100%; font-size:.84rem; }
  .card-meta { gap:11px; }
  .card-signoff { display:none; }
  .card-stamp-wrap { transform:scale(.9); transform-origin:top right; }
  [data-testid="stHorizontalBlock"] { gap:.38rem; }
  .stButton > button { min-height:2.65rem; padding-left:.55rem; padding-right:.55rem; }
  .courtesy-wait { padding:12px; gap:10px; }.card-clerk { transform:scale(.85); transform-origin:left center; margin-right:-9px; }
}
@media (prefers-reduced-motion:reduce) { .presented-card,.stamps-line .stamp:last-child,.clerk-card,
  [data-testid="stForm"] [data-testid="stCheckbox"] label:has(input:checked)::before { animation:none; } }
</style>
"""
st.markdown(CSS, unsafe_allow_html=True)

STAMP_COLORS = {"朱色":"#a93b32", "藍色":"#315b75", "紫":"#6f5378", "桃":"#a75c76", "深緑":"#496b57", "墨":"#343434"}
CARD_THEMES = {
    "白無地":{"class":"theme-white","price":"無料","desc":"いちばん素直な、白い名刺。"},
    "和紙":{"class":"theme-washi","price":"有料","desc":"やわらかな生成りの和紙風。"},
    "レトロ事務":{"class":"theme-retro","price":"有料","desc":"昔の事務用品を思わせる落ち着いた紙色。"},
    "モダン":{"class":"theme-modern","price":"有料","desc":"余白を広く取った、すっきり現代的な名刺。"},
    "桜":{"class":"theme-sakura","price":"有料","desc":"ごく淡い桜色。季節限定にも向くデザイン。"},
    "黒名刺":{"class":"theme-black","price":"有料","desc":"墨色ベースの引き締まった特別仕様。"},
}
PRESENCE_STATUSES = {
    "在席しております":{"color":"#6f8a67","quiet":False,"desc":"通常の状態です。"},
    "離席中です":{"color":"#b08a4a","quiet":False,"desc":"少し席を外しているときに。"},
    "別件打ち合わせ中です":{"color":"#667e9a","quiet":True,"desc":"今は反応しづらい、というやわらかな意思表示。"},
    "ただいま取り込み中です":{"color":"#8a6d8f","quiet":True,"desc":"しばらく静かにしておきたいときに。"},
    "外出しております":{"color":"#7f857e","quiet":True,"desc":"少し長めの不在に。"},
    "本日は退勤しました":{"color":"#6f7276","quiet":True,"desc":"今日はもうSNSを見ない、という合図。"},
    "休暇をいただいております":{"color":"#8c7b6d","quiet":True,"desc":"数日ほどゆっくり離れるときに。"},
    "しばらく席を外しております":{"color":"#857d76","quiet":True,"desc":"長めのお休み・休会代わりに。"},
}
WAITING_MESSAGES = {
    "short":["書類を確認しております","ただいま資料をそろえております","少々、朱肉をなじませております","ただいま付箋を探しております"],
    "medium":["ただいま会議室へ移動中です","エレベーターを待っております","ただいま回覧中です","ただいま席に戻るところです"],
    "long":["担当の者が向かっております","印鑑を取りに戻っております","少々、机の上を整えております","ただいま稟議書を運んでおります"],
}
DEMO_PROFILES = {
    "佐藤":{"bio":"甘いものの案件を多めに扱っております。","interests":["プリン","喫茶店"],"theme":"和紙","color":"朱色","shape":"丸印","presence":"在席しております"},
    "田中":{"bio":"洗濯と散歩についてご報告します。","interests":["散歩","洗濯"],"theme":"モダン","color":"藍色","shape":"角印","presence":"離席中です"},
    "鈴木":{"bio":"だいたい承知しております。","interests":["読書","おやつ"],"theme":"桜","color":"紫","shape":"丸印","presence":"別件打ち合わせ中です"},
    "山田":{"bio":"お茶と読書を担当しております。","interests":["お茶","読書"],"theme":"レトロ事務","color":"深緑","shape":"丸印","presence":"在席しております"},
    "高橋":{"bio":"ときどき重要案件を回覧します。","interests":["日常","散策"],"theme":"白無地","color":"墨","shape":"角印","presence":"外出しております"},
}


def waiting_message(kind="short"):
    key = kind if kind in WAITING_MESSAGES else "short"
    previous = st.session_state.get("last_waiting_message")
    choices = [m for m in WAITING_MESSAGES[key] if m != previous] or WAITING_MESSAGES[key]
    picked = random.choice(choices)
    st.session_state.last_waiting_message = picked
    return picked


def courtesy_wait_html(message="名刺をお渡ししております。", detail="少々お待ちくださいませ。"):
    return f'''<div class="courtesy-wait"><div class="card-clerk" aria-hidden="true">
      <span class="clerk-head"></span><span class="clerk-body"></span><span class="clerk-hands"></span><span class="clerk-card"></span>
      </div><div class="wait-copy"><b>{esc(message)}</b><span>{esc(detail)}</span></div></div>'''


def esc(value):
    return html.escape(str(value))


def stamp_html(surname, small=False, color="#a93b32", square=False):
    classes = "stamp" + (" small" if small else "") + (" square" if square else "")
    display = "<br>".join([esc(surname[:2]), esc(surname[2:])]) if len(surname) > 2 else esc(surname)
    return f'<span class="{classes}" style="--stamp-color:{color}">{display}</span>'


def image_data_uri(image_bytes, mime):
    if not image_bytes:
        return None
    return f"data:{mime};base64,{base64.b64encode(image_bytes).decode('ascii')}"


def init_state():
    defaults = {
        "registered":False, "surname":"", "bio":"", "interests":[], "stamp_color":"朱色", "stamp_shape":"丸印", "card_theme":"白無地",
        "presence_status":"在席しております", "follows":set(), "saved":set(), "blocked":set(), "reports":[], "flash":"",
        "view_profile":None, "editing_post":None,
        "posts":[
            {"id":"demo-1","surname":"佐藤","title":"午後のおやつ購入の件","body":"本日15時、プリンを購入いたしました。\n大変おいしく、再購入の可能性が高いことをご報告いたします。","created_at":"本日 15:42","stamps":["鈴木","高橋","山田"],"notes":[("鈴木","再購入を推奨いたします。"),("山田","重要案件ですね。")],"image_bytes":None,"image_mime":None},
            {"id":"demo-2","surname":"田中","title":"洗濯物の乾燥状況について","body":"想定より早く乾きました。\n以上、取り急ぎご報告まで。","created_at":"本日 13:10","stamps":["佐藤"],"notes":[],"image_bytes":None,"image_mime":None},
        ],
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


init_state()


def header():
    title = "わたくし柴原と申します。"
    st.markdown(f'<div class="app-title">{title}</div>', unsafe_allow_html=True)
    st.markdown('<div class="app-sub">承認するほどでもない日々を、承認しよう。</div>', unsafe_allow_html=True)
    if st.session_state.get("registered") and st.session_state.get("surname"):
        st.markdown(f'<div class="attendance">ただいま {esc(st.session_state.surname)} 出社中</div>', unsafe_allow_html=True)


def render_faq():
    faqs = [
        ("これは会社員専用のSNSですか？", "いいえ。どなたでも参加できます。事務的な言葉づかいを、少しかわいく楽しむSNSです。上司・部下・役職・社員ランクはありません。"),
        ("何を投稿すればよいですか？", "食べたもの、散歩、昼寝など、日常の小さな出来事で十分です。投稿を『今日の稟議書』、投稿することを『起案・提出』と呼びますが、誰かの承認は必要ありません。"),
        ("本当の名字を登録する必要がありますか？", "原則として、実際に使用している名字を登録してください。戸籍姓に限らず、旧姓や普段使用している通称も含みます。本人確認書類の提出は求めません。"),
        ("名字以外の個人情報も公開されますか？", "基本プロフィールは名字と短い一言だけです。年齢、性別、勤務先、学校、住所は登録項目にしていません。投稿にも個人を特定できる情報を書かないことをおすすめします。"),
        ("ハンコは何に使いますか？", "ハンコは、このSNSでのあなたのアイコンです。『捺印』すると相手の稟議書に自分の名字の印が表示されます。捺印は一般的なSNSの『いいね』に近い機能です。"),
        ("付箋・回覧・控えとは何ですか？", "付箋はコメント、回覧はシェア、控えはブックマークです。意味が分からなくなったときは、このご案内へお戻りください。"),
        ("ご縁とは何ですか？", "一般的なSNSのフォローです。『ご縁を結ぶ』と、その方の稟議書を見つけやすくなります。上下関係や承認関係は生まれません。"),
        ("嫌な投稿や利用者を見つけたら？", "投稿・名刺から通報できます。また、相手をブロックすると、その方の投稿は回覧に表示されなくなります。"),
        ("有料にすると投稿が目立ちますか？", "いいえ。課金はハンコや名刺の着せ替えだけを想定しています。投稿の表示順や影響力が有利になる仕組みにはしません。"),
    ]
    st.caption("形式は少々かしこまっておりますが、どうぞ気軽にお使いください。")
    for question, answer in faqs:
        st.markdown(f"**{question}**")
        st.write(answer)


def registration():
    header()
    st.markdown('<div class="hero-copy">名字だけで参加する、<br>ちょっと他人行儀な日常SNSです。</div>', unsafe_allow_html=True)
    st.markdown('<div class="callout"><b>お名前ではなく、名字をお聞かせください。</b><br><span class="muted">原則として、実際に使用している名字をご登録ください。</span></div>', unsafe_allow_html=True)
    with st.form("register_form"):
        surname = st.text_input("名字", placeholder="例：柴原", max_chars=12)
        agreed = st.checkbox("実際に使用している名字です")
        submitted = st.form_submit_button("ハンコを作る", type="primary", use_container_width=True)
    if submitted:
        cleaned = surname.strip().replace(" ", "").replace("　", "")
        if not cleaned:
            st.error("名字を入力してください。")
        elif not agreed:
            st.error("丸い確認欄を押して『済』にしてください。")
        else:
            st.session_state.surname = cleaned
            st.session_state.registered = True
            st.session_state.flash = f"お待たせいたしました。{cleaned}さんですね。こちらがあなたの印鑑です。"
            st.rerun()
    with st.expander("ご案内・よくあるご質問（FAQ）"):
        render_faq()


def get_profile(surname):
    if surname == st.session_state.surname:
        return {"bio":st.session_state.bio or "どうぞ、よしなに。", "theme":st.session_state.card_theme, "color":st.session_state.stamp_color,
                "shape":st.session_state.stamp_shape, "presence":st.session_state.presence_status, "interests":st.session_state.interests}
    return DEMO_PROFILES.get(surname, {"bio":"どうぞ、よしなに。","interests":[],"theme":"白無地","color":"朱色","shape":"丸印","presence":"在席しております"})


def business_card_html(surname, own=False, presented=False):
    profile = get_profile(surname)
    theme = CARD_THEMES[profile["theme"]]
    presence = PRESENCE_STATUSES[profile["presence"]]
    color = STAMP_COLORS[profile["color"]]
    square = profile["shape"] == "角印"
    post_count = sum(1 for p in st.session_state.posts if p["surname"] == surname)
    follows_count = len(st.session_state.follows) if own else "—"
    saved_count = len(st.session_state.saved) if own else "—"
    presented_class = " presented-card" if presented else ""
    return f'''<div class="business-card {theme["class"]}{presented_class}">
      <div class="card-topline"><div><div class="card-label">WATAKUSHI SHIBAHARA TO MOUSHIMASU.</div><div class="card-honorific">わたくし</div>
      <div class="surname">{esc(surname)}</div><div class="card-bio">{esc(profile["bio"])}</div>
      <div class="card-interests">{esc('・'.join(profile.get('interests', [])[:3]))}</div>
      <div class="status-badge" style="--status-color:{presence['color']}"><span class="status-dot"></span>{esc(profile['presence'])}</div></div>
      <div class="card-stamp-wrap">{stamp_html(surname, color=color, square=square)}</div></div>
      <div class="card-bottom"><div class="card-meta"><div class="card-meta-item">今日の稟議書<b>{post_count}件</b></div>
      <div class="card-meta-item">ご縁<b>{follows_count}</b></div><div class="card-meta-item">控え<b>{saved_count}</b></div></div>
      <div class="card-signoff">どうぞ よしなに</div></div></div>'''


def open_profile(surname):
    st.session_state.view_profile = surname


@st.dialog("名刺を拝見", width="medium")
def profile_dialog(surname):
    st.markdown('<div class="profile-prompt">名刺を一枚、お預かりしました。</div>', unsafe_allow_html=True)
    st.markdown(business_card_html(surname, own=(surname == st.session_state.surname), presented=True), unsafe_allow_html=True)
    if surname == st.session_state.surname:
        st.caption("こちらは、あなたの名刺です。")
    else:
        c1, c2 = st.columns(2)
        with c1:
            following = surname in st.session_state.follows
            if st.button("ご縁を外す" if following else "ご縁を結ぶ", key=f"dialog-follow-{surname}", type="primary" if not following else "secondary", use_container_width=True):
                st.session_state.follows.discard(surname) if following else st.session_state.follows.add(surname)
                st.rerun()
        with c2:
            blocked = surname in st.session_state.blocked
            if st.button("ブロック解除" if blocked else "この方をブロック", key=f"dialog-block-{surname}", use_container_width=True):
                if blocked:
                    st.session_state.blocked.discard(surname)
                    st.toast("ブロックを解除しました。")
                else:
                    st.session_state.blocked.add(surname)
                    st.session_state.follows.discard(surname)
                    st.toast(f"{surname}さんをブロックしました。")
                st.session_state.view_profile = None
                st.rerun()
    if st.button("名刺をお返しする", key=f"dialog-close-{surname}", use_container_width=True):
        st.session_state.view_profile = None
        st.rerun()


def render_post(post):
    if post["surname"] in st.session_state.blocked:
        return
    profile = get_profile(post["surname"])
    color = STAMP_COLORS[profile["color"]]
    square = profile["shape"] == "角印"
    stamp = stamp_html(post["surname"], color=color, square=square)
    stamp_line = "".join(stamp_html(s, small=True) for s in post["stamps"][-8:])
    notes_html = "".join(f'<div class="note"><div class="note-name">{esc(name)}さんの付箋</div><div class="note-body">{esc(body)}</div></div>' for name, body in post["notes"][-3:])
    st.markdown(f'''<div class="ringi"><div class="ringi-head"><div><div class="ringi-kicker">今日の稟議書</div>
      <div class="ringi-meta">{esc(post['surname'])}さん ・ {esc(post['created_at'])}</div></div>{stamp}</div>
      <div class="ringi-title">件名：{esc(post['title'])}</div><div class="ringi-body">{esc(post['body'])}</div>
      <div class="stamps-line"><span class="ringi-meta">捺印 {len(post['stamps'])}件</span>{stamp_line}</div>{notes_html}</div>''', unsafe_allow_html=True)
    if post.get("image_bytes"):
        st.image(post["image_bytes"], caption="添付資料", use_container_width=True)

    if st.button(f"{post['surname']}さん　{post['surname']}㊞", key=f"profile-{post['id']}", help="この方の名刺を拝見する", use_container_width=True):
        open_profile(post["surname"]); st.rerun()

    me = st.session_state.surname
    stamped = me in post["stamps"]
    c1, c2, c3 = st.columns(3)
    with c1:
        stamp_label = f"{me}㊞ 捺印済" if stamped else "㊞ 捺印"
        if st.button(stamp_label, key=f"stamp-{post['id']}-{'done' if stamped else 'ready'}", use_container_width=True):
            if me not in post["stamps"]:
                post["stamps"].append(me); st.toast("㊞ ポン。捺印しました。")
            else:
                st.toast("すでに捺印済みです。")
            st.rerun()
    with c2:
        if st.button("＋ 付箋", key=f"note-{post['id']}", use_container_width=True):
            st.session_state[f"note_open_{post['id']}"] = not st.session_state.get(f"note_open_{post['id']}", False); st.rerun()
    with c3:
        saved = post["id"] in st.session_state.saved
        if st.button("控え済" if saved else "控え", key=f"save-{post['id']}", use_container_width=True):
            st.session_state.saved.discard(post["id"]) if saved else st.session_state.saved.add(post["id"]); st.rerun()

    related_people = []
    for person in post["stamps"][-8:] + [name for name, _ in post["notes"][-3:]]:
        if person != st.session_state.surname and person not in related_people:
            related_people.append(person)
    if related_people:
        st.caption("名字を押すと、その方の名刺を拝見できます。")
        people_cols = st.columns(min(3, len(related_people)))
        for index, person in enumerate(related_people):
            with people_cols[index % len(people_cols)]:
                if st.button(f"{person}さん ㊞", key=f"related-{post['id']}-{index}-{person}", use_container_width=True):
                    open_profile(person); st.rerun()

    if post["surname"] == st.session_state.surname:
        e1, e2 = st.columns(2)
        with e1:
            if st.button("訂正する", key=f"edit-{post['id']}", use_container_width=True):
                st.session_state.editing_post = post["id"]; st.rerun()
        with e2:
            if st.button("取り下げる", key=f"delete-{post['id']}", use_container_width=True):
                st.session_state[f"confirm_delete_{post['id']}"] = True; st.rerun()
        if st.session_state.get(f"confirm_delete_{post['id']}"):
            st.warning("この稟議書を取り下げますか？")
            y, n = st.columns(2)
            with y:
                if st.button("取り下げを確定", key=f"delete-yes-{post['id']}", type="primary", use_container_width=True):
                    st.session_state.posts = [p for p in st.session_state.posts if p["id"] != post["id"]]
                    st.session_state.saved.discard(post["id"]); st.toast("稟議書を取り下げました。"); st.rerun()
            with n:
                if st.button("やめる", key=f"delete-no-{post['id']}", use_container_width=True):
                    st.session_state[f"confirm_delete_{post['id']}"] = False; st.rerun()
        if st.session_state.editing_post == post["id"]:
            with st.form(f"edit-form-{post['id']}"):
                title = st.text_input("件名を訂正", value=post["title"], max_chars=60)
                body = st.text_area("ご報告を訂正", value=post["body"], max_chars=1000, height=150)
                if st.form_submit_button("訂正版を保存", type="primary", use_container_width=True):
                    if title.strip() and body.strip():
                        post["title"] = title.strip(); post["body"] = body.strip(); post["created_at"] = "訂正済み"
                        st.session_state.editing_post = None; st.toast("訂正いたしました。"); st.rerun()
    else:
        with st.expander("この稟議書について"):
            if st.button("この投稿を通報", key=f"report-post-{post['id']}", use_container_width=True):
                st.session_state[f"report_open_{post['id']}"] = True
            if st.session_state.get(f"report_open_{post['id']}"):
                with st.form(f"report-form-{post['id']}"):
                    reason = st.selectbox("理由", ["迷惑行為・嫌がらせ","個人情報","不適切な内容","なりすましの疑い","その他"])
                    details = st.text_input("補足（任意）", max_chars=200)
                    if st.form_submit_button("通報を提出"):
                        st.session_state.reports.append({"post_id":post["id"],"surname":post["surname"],"reason":reason,"details":details})
                        st.session_state[f"report_open_{post['id']}"] = False; st.success("通報を受け付けました（デモ保存）。")

    if st.session_state.get(f"note_open_{post['id']}"):
        preset = st.selectbox(
            "付箋の内容",
            ["自由に書く","承知しました。","異議なし。","お疲れさまです。","大変よくできました。","重要案件ですね。","続報をお待ちしております。","私も同様です。","ご自愛ください。"],
            key=f"preset-{post['id']}",
        )
        if preset == "自由に書く":
            note_text = st.text_input("付箋", max_chars=120, key=f"note-text-{post['id']}", placeholder="ひとことお書きください")
        else:
            note_text = preset
            st.markdown(f'<div class="note"><div class="note-body">{esc(note_text)}</div></div>', unsafe_allow_html=True)
        if st.button("付箋を貼る", key=f"note-submit-{post['id']}", type="primary", use_container_width=True):
            if note_text.strip():
                post["notes"].append((st.session_state.surname, note_text.strip()))
                st.session_state[f"note_open_{post['id']}"] = False
                st.toast("付箋を貼りました。")
                st.rerun()
            else:
                st.warning("付箋の内容を入力してください。")


def page_circulation():
    st.markdown('<div class="section-title">本日の回覧</div>', unsafe_allow_html=True)
    filter_mode = st.radio("表示", ["おすすめ","ご縁","自分","控え"], horizontal=True, key="circulation_filter", label_visibility="collapsed")
    posts = [p for p in reversed(st.session_state.posts) if p["surname"] not in st.session_state.blocked]
    if filter_mode == "自分": posts = [p for p in posts if p["surname"] == st.session_state.surname]
    elif filter_mode == "ご縁": posts = [p for p in posts if p["surname"] in st.session_state.follows]
    elif filter_mode == "控え": posts = [p for p in posts if p["id"] in st.session_state.saved]
    if not posts: st.info("ただいま回覧する稟議書はありません。")
    for post in posts: render_post(post)


def page_draft():
    st.markdown('<div class="section-title">稟議書を起案する</div>', unsafe_allow_html=True)
    st.caption("内容は気軽で大丈夫です。形式だけ、少々かしこまっております。")
    with st.form("draft"):
        title = st.text_input("件名", placeholder="例：本日の昼寝について", max_chars=60)
        body = st.text_area("ご報告", placeholder="本日14時より休憩を開始したところ、想定を超えて眠ってしまいました。", height=170, max_chars=1000)
        photo = st.file_uploader("添付資料（写真・任意）", type=["jpg","jpeg","png","webp"])
        submitted = st.form_submit_button("提出する", type="primary", use_container_width=True)
    if submitted:
        if not title.strip() or not body.strip():
            st.error("件名とご報告を入力してください。")
        else:
            image_bytes = None; image_mime = None
            waiting_area = st.empty()
            if photo is not None:
                waiting_area.markdown(courtesy_wait_html("資料を整えております。", "ただいま回覧にお持ちしております。"), unsafe_allow_html=True)
                image_bytes = photo.getvalue(); image_mime = photo.type
            post = {"id":f"p-{datetime.now().timestamp()}-{random.randint(100,999)}","surname":st.session_state.surname,
                    "title":title.strip(),"body":body.strip(),"created_at":"たった今","stamps":[],"notes":[],
                    "image_bytes":image_bytes,"image_mime":image_mime}
            st.session_state.posts.append(post)
            waiting_area.empty()
            st.session_state.flash = "お待たせいたしました。稟議書を提出いたしました。お疲れさまでした。"
            st.session_state.nav_redirect = "回覧"; st.rerun()


def render_other_profile(surname):
    if not surname: return
    st.markdown("### 名刺を拝見")
    st.markdown(business_card_html(surname, own=(surname == st.session_state.surname)), unsafe_allow_html=True)
    if surname == st.session_state.surname:
        st.caption("こちらは、あなたの名刺です。")
    else:
        c1, c2 = st.columns(2)
        with c1:
            following = surname in st.session_state.follows
            if st.button("ご縁を外す" if following else "ご縁を結ぶ", key=f"follow-card-{surname}", type="primary" if not following else "secondary", use_container_width=True):
                st.session_state.follows.discard(surname) if following else st.session_state.follows.add(surname); st.rerun()
        with c2:
            blocked = surname in st.session_state.blocked
            if st.button("ブロック解除" if blocked else "この方をブロック", key=f"block-card-{surname}", use_container_width=True):
                if blocked: st.session_state.blocked.discard(surname); st.toast("ブロックを解除しました。")
                else:
                    st.session_state.blocked.add(surname); st.session_state.follows.discard(surname); st.toast(f"{surname}さんをブロックしました。")
                st.rerun()
        with st.expander("名刺を通報する"):
            with st.form(f"report-user-{surname}"):
                reason = st.selectbox("理由", ["なりすましの疑い","迷惑行為・嫌がらせ","個人情報","不適切なプロフィール","その他"])
                details = st.text_input("補足（任意）", max_chars=200)
                if st.form_submit_button("通報を提出"):
                    st.session_state.reports.append({"reported_user":surname,"reason":reason,"details":details}); st.success("通報を受け付けました（デモ保存）。")


def page_search():
    st.markdown('<div class="section-title">探す</div>', unsafe_allow_html=True)
    q = st.text_input("名字・件名・本文から探す", placeholder="例：佐藤 / プリン")
    surnames = sorted(({p["surname"] for p in st.session_state.posts} | {st.session_state.surname}) - st.session_state.blocked)
    st.markdown("**名字から探す**")
    cols = st.columns(3)
    for i, surname in enumerate(surnames):
        with cols[i % 3]:
            if st.button(f"{surname}さん", key=f"person-{surname}", use_container_width=True):
                st.session_state.view_profile = surname; st.rerun()
    if q.strip():
        query = q.strip().lower()
        matches = [p for p in reversed(st.session_state.posts) if p["surname"] not in st.session_state.blocked and (query in p["surname"].lower() or query in p["title"].lower() or query in p["body"].lower())]
        st.markdown(f"**検索結果：{len(matches)}件**")
        for post in matches: render_post(post)


def page_notices():
    st.markdown('<div class="section-title">お達し</div>', unsafe_allow_html=True)
    status_info = PRESENCE_STATUSES[st.session_state.presence_status]
    if status_info["quiet"]: st.info(f"現在『{st.session_state.presence_status}』。お達しは静かにしています。", icon="🔕")
    own = [p for p in st.session_state.posts if p["surname"] == st.session_state.surname]
    notices = []
    for p in reversed(own):
        for s in p["stamps"][-3:]:
            if s != st.session_state.surname: notices.append((s, f"{s}さんが『{p['title']}』に捺印しました。"))
        for name, _ in p["notes"][-3:]:
            if name != st.session_state.surname: notices.append((name, f"{name}さんが『{p['title']}』に付箋を貼りました。"))
    for surname in sorted(st.session_state.follows): notices.append((surname, f"{surname}さんとご縁があります。"))
    if notices:
        for index, (surname, message) in enumerate(notices[:15]):
            left, right = st.columns([4, 1.35])
            with left: st.info(message, icon="㊞")
            with right:
                if st.button(f"{surname}さん", key=f"notice-person-{index}-{surname}", help="名刺を拝見", use_container_width=True):
                    open_profile(surname); st.rerun()
    else: st.caption("新しいお達しはありません。")


def page_profile():
    st.markdown('<div class="section-title">わたくしの名刺</div>', unsafe_allow_html=True)
    st.caption("プロフィールは、名刺を一枚差し出すような見え方にしています。")
    st.markdown(business_card_html(st.session_state.surname, own=True), unsafe_allow_html=True)
    st.caption(f"現在の名刺：{st.session_state.card_theme} ・ {CARD_THEMES[st.session_state.card_theme]['price']}")

    st.markdown("### 在席札")
    status_names = list(PRESENCE_STATUSES)
    selected_status = st.selectbox("現在の状態", status_names, index=status_names.index(st.session_state.presence_status),
                                   format_func=lambda x: x + ("　🔕" if PRESENCE_STATUSES[x]["quiet"] else ""))
    info = PRESENCE_STATUSES[selected_status]
    st.caption(info["desc"] + ("　この状態では『お達し』を静かにする想定です。" if info["quiet"] else ""))
    if st.button("この在席札にする", use_container_width=True):
        st.session_state.presence_status = selected_status; st.toast(f"在席札を『{selected_status}』に掛け替えました。"); st.rerun()

    with st.expander("名刺を整える"):
        new_bio = st.text_input("一言", value=st.session_state.bio, max_chars=60, placeholder="例：だいたい眠いです。")
        interests_text = st.text_input("好きなもの・主な投稿ジャンル（3つまで）", value="、".join(st.session_state.interests),
                                       max_chars=60, placeholder="例：プリン、散歩、読書")
        st.caption("勤務先・住所・学校・年齢などは載せません。項目は読点「、」で区切ってください。")
        if st.button("名刺を更新", use_container_width=True):
            st.session_state.bio = new_bio.strip()
            st.session_state.interests = [item.strip() for item in interests_text.replace(",", "、").split("、") if item.strip()][:3]
            st.toast("名刺を更新しました。"); st.rerun()

    st.markdown("### 名刺屋")
    selected_theme = st.selectbox("名刺デザイン", list(CARD_THEMES), index=list(CARD_THEMES).index(st.session_state.card_theme),
                                  format_func=lambda x:f"{x}　（{CARD_THEMES[x]['price']}）")
    selected_info = CARD_THEMES[selected_theme]
    st.markdown(f'<div class="card-theme-preview"><b>{esc(selected_theme)}</b><span class="card-theme-chip">{esc(selected_info["price"])}</span><br><span class="muted">{esc(selected_info["desc"])}</span></div>', unsafe_allow_html=True)
    if st.button("この名刺にする", type="primary", use_container_width=True):
        st.session_state.card_theme = selected_theme; st.toast("名刺デザインを変更しました。試作版では有料デザインもお試しできます。" if selected_info["price"] == "有料" else "名刺デザインを変更しました。"); st.rerun()

    st.markdown("### はんこ屋")
    c1, c2 = st.columns(2)
    with c1: color_name = st.selectbox("印影カラー", list(STAMP_COLORS), index=list(STAMP_COLORS).index(st.session_state.stamp_color))
    with c2: shape = st.selectbox("印型", ["丸印","角印"], index=["丸印","角印"].index(st.session_state.stamp_shape))
    st.caption("朱色・丸印を無料基本デザインとし、その他は将来の課金対象を想定しています。MVPではすべてお試しできます。")
    if st.button("このハンコにする", type="primary", use_container_width=True):
        st.session_state.stamp_color = color_name; st.session_state.stamp_shape = shape; st.toast("㊞ 印鑑を変更しました。"); st.rerun()

    with st.expander("安全・管理"):
        st.write(f"ブロック中：{len(st.session_state.blocked)}名 / 通報記録：{len(st.session_state.reports)}件（このMVPではセッション内のみ）")
        if st.session_state.blocked:
            for surname in sorted(st.session_state.blocked):
                if st.button(f"{surname}さんのブロックを解除", key=f"unblock-{surname}"):
                    st.session_state.blocked.discard(surname); st.rerun()

    with st.expander("ご案内・よくあるご質問（FAQ）"):
        render_faq()


def main():
    if not st.session_state.registered:
        registration(); st.stop()
    header()
    if st.session_state.flash:
        st.success(st.session_state.flash); st.session_state.flash = ""
    if "nav_redirect" in st.session_state:
        st.session_state.nav = st.session_state.pop("nav_redirect")
    if "nav" not in st.session_state: st.session_state.nav = "回覧"
    nav = st.radio("メニュー", ["回覧","探す","起案","お達し","わたくし"], horizontal=True, key="nav", label_visibility="collapsed")
    st.divider()
    {"回覧":page_circulation,"探す":page_search,"起案":page_draft,"お達し":page_notices,"わたくし":page_profile}[nav]()
    if st.session_state.view_profile:
        profile_dialog(st.session_state.view_profile)


if __name__ == "__main__":
    main()
