import html
import os
import uuid

import requests
import streamlit as st

API_URL = os.getenv("MOVIE_AGENT_API_URL", "http://127.0.0.1:8000").rstrip("/")
TIMEOUT = 120

st.set_page_config(page_title="CineMind", page_icon="🎬", layout="wide")

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;700&family=Fraunces:opsz,wght@9..144,600;9..144,800&display=swap');
:root{--bg:#0e1020;--surface:#171a2e;--line:#2a2e4a;--text:#ecebf4;--muted:#9a9cb8;--amber:#f2b84b;--teal:#5ad1c4}
.stApp{background:radial-gradient(1200px 500px at 70% -10%,#1d2145 0%,var(--bg) 60%);color:var(--text);font-family:'DM Sans',sans-serif}
header[data-testid="stHeader"]{background:transparent}
.block-container{max-width:1150px;padding-top:2.2rem}
[data-testid="stSidebar"]{background:#0b0d1a;border-right:1px solid var(--line)}
h1,h2,h3,.hero-title{font-family:'Fraunces',serif!important}
.hero-title{font-size:3rem;font-weight:800;line-height:1.1;letter-spacing:-1px;margin:.4rem 0}
.hero-sub{color:var(--muted);font-size:1.08rem;max-width:560px;line-height:1.7}
.brand{font-family:'Fraunces',serif;font-size:1.6rem;font-weight:800}
.brand span{color:var(--amber)}
.stButton>button{border-radius:12px;border:1px solid var(--line);background:var(--surface);color:var(--text);transition:.15s}
.stButton>button:hover{border-color:var(--amber);color:var(--amber)}
.stButton>button:focus-visible{outline:2px solid var(--amber)}
[data-testid="stChatMessage"]{background:transparent;padding:.4rem 0}
[data-testid="stChatInput"]{border-radius:16px}
.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(190px,1fr));gap:16px;margin:.8rem 0 1.4rem}
.card{background:var(--surface);border:1px solid var(--line);border-radius:16px;overflow:hidden}
.card img,.ph{width:100%;aspect-ratio:2/3;object-fit:cover;display:block}
.ph{display:flex;align-items:center;justify-content:center;font-family:'Fraunces',serif;font-size:3.4rem;color:var(--amber);background:linear-gradient(160deg,#252a52,#141730)}
.body{padding:12px 14px 14px}
.t{font-weight:700;line-height:1.3;margin-bottom:4px}
.meta{color:var(--muted);font-size:.85rem}
.rate{color:var(--amber);margin-left:6px}
.chips{display:flex;flex-wrap:wrap;gap:5px;margin:8px 0}
.chip{font-size:.72rem;padding:2px 9px;border-radius:99px;border:1px solid var(--line);color:var(--muted)}
.bar{height:5px;border-radius:9px;background:var(--line);overflow:hidden}
.bar i{display:block;height:100%;background:linear-gradient(90deg,var(--teal),var(--amber))}
.pct{font-size:.76rem;color:var(--muted);margin-top:5px}
.status{font-size:.82rem;color:var(--muted)}
.dot{display:inline-block;width:8px;height:8px;border-radius:50%;margin-right:6px}
@media (prefers-reduced-motion:reduce){*{transition:none!important}}
</style>
""",
    unsafe_allow_html=True,
)

ss = st.session_state
ss.setdefault("messages", [])
ss.setdefault("conversation_id", str(uuid.uuid4()))


@st.cache_data(ttl=15)
def api_online() -> bool:
    try:
        return requests.get(f"{API_URL}/health", timeout=2).ok
    except requests.RequestException:
        return False


def match_pct(movie: dict) -> int:
    scores = [movie.get(k) or 0 for k in ("similarity_score", "semantic_score", "cf_score")]
    return int(round(min(max(scores), 1) * 100))


def movie_card(m: dict) -> str:
    e = lambda v: html.escape(str(v))
    title = e(m.get("title", "Untitled"))
    poster = m.get("poster_url")
    art = f'<img src="{e(poster)}" alt="{title} poster">' if poster else f'<div class="ph">{title[:1]}</div>'
    year = e(m.get("year") or m.get("release_year") or "")
    rating = f'<span class="rate">★ {e(m["rating"])}</span>' if m.get("rating") else ""
    chips = "".join(f'<span class="chip">{e(g)}</span>' for g in (m.get("genres") or [])[:3])
    pct = match_pct(m)
    return (
        f'<div class="card">{art}<div class="body"><div class="t">{title}</div>'
        f'<div class="meta">{year}{rating}</div><div class="chips">{chips}</div>'
        f'<div class="bar"><i style="width:{pct}%"></i></div><div class="pct">{pct}% match</div></div></div>'
    )


def render(msg: dict) -> None:
    with st.chat_message(msg["role"], avatar="🎬" if msg["role"] == "assistant" else None):
        if msg.get("is_error"):
            st.error(msg["content"])
            return
        results = msg.get("results")
        if results:
            st.markdown(
                '<div class="grid">' + "".join(movie_card(m) for m in results) + "</div>",
                unsafe_allow_html=True,
            )
        st.markdown(msg["content"])


def ask(prompt: str) -> None:
    ss.messages.append({"role": "user", "content": prompt})
    try:
        r = requests.post(
            f"{API_URL}/chat",
            json={"conversation_id": ss.conversation_id, "message": prompt},
            timeout=TIMEOUT,
        )
        r.raise_for_status()
        data = r.json()
        text = (data.get("response") or "").strip()
        if not text:
            raise ValueError("empty response")
        ss.messages.append({"role": "assistant", "content": text, "results": data.get("results")})

    except requests.exceptions.HTTPError as exc:
        status = exc.response.status_code if exc.response is not None else "unknown"
        fail(f"Backend returned HTTP {status}. Check the FastAPI terminal for the actual error.")

    except requests.exceptions.ConnectionError:
        fail("Cannot connect to FastAPI. Check that the backend is running.")

    except requests.exceptions.Timeout:
        fail("The request timed out. The backend may still be processing it.")

    except (ValueError, requests.exceptions.RequestException):
        fail("The response could not be processed. Please try again.")

    except Exception:
        fail("An unexpected error occurred. Check the application logs.")

def fail(text: str) -> None:
    ss.messages.append({"role": "assistant", "content": text, "is_error": True})


# ---------------- Sidebar ----------------
with st.sidebar:
    st.markdown('<div class="brand">Cine<span>Mind</span></div>', unsafe_allow_html=True)
    online = api_online()
    color = "#5ad1c4" if online else "#e5605a"
    st.markdown(
        f'<div class="status"><span class="dot" style="background:{color}"></span>'
        f'{"Backend online" if online else "Backend offline"}</div>',
        unsafe_allow_html=True,
    )
    if st.button("New chat", use_container_width=True, type="primary"):
        ss.messages, ss.conversation_id = [], str(uuid.uuid4())
        st.rerun()

    st.markdown("### Your profile")
    user = st.text_input("Username", value="shiva", label_visibility="collapsed")
    if st.button("Picks for me", use_container_width=True):
        ss.pending = f"Give me personalized movie recommendations for user {user}"
    if st.button("Picks tuned to my genres", use_container_width=True):
        ss.pending = f"Give me genre-based personalized movie recommendations for user {user}"

    st.markdown("### Find similar films")
    movie = st.text_input("Movie", placeholder="Interstellar", label_visibility="collapsed")
    c1, c2 = st.columns(2)
    if c1.button("By story", use_container_width=True, disabled=not movie):
        ss.pending = f"Recommend movies similar to {movie}"
    if c2.button("By viewers", use_container_width=True, disabled=not movie):
        ss.pending = f"Recommend movies using collaborative filtering for {movie}"

# ---------------- Main ----------------
prompt = st.chat_input("Describe a movie, a mood, or name a film you loved") or ss.pop("pending", None)
if prompt:
    with st.spinner("Finding your next watch..."):
        ask(prompt.strip())

if not ss.messages:
    st.markdown(
        '<div class="hero-title">Find the film you<br>didn\'t know you wanted.</div>'
        '<div class="hero-sub">CineMind blends what a story is about with what viewers like you '
        "rated highly, then explains every pick.</div>",
        unsafe_allow_html=True,
    )
    st.write("")
    starters = [
        ("Space epics like Interstellar", "Recommend movies similar to Interstellar"),
        ("Great science fiction", "Recommend some great science fiction movies"),
        ("Picks based on my taste", f"Give me personalized movie recommendations for user {user}"),
    ]
    for col, (label, text) in zip(st.columns(3), starters):
        if col.button(label, use_container_width=True, key=label):
            ss.pending = text
            st.rerun()

for message in ss.messages:
    render(message)