import streamlit as st
import re
from agents import build_search_agent, build_scrape_agent, writer_chain, critic_chain

st.set_page_config(
    page_title="ResearchAI",
    page_icon="🔬",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# Minimal safe CSS — no font imports, no html/body overrides
st.markdown("""
<style>
.main-title {
    font-size: 2.8rem;
    font-weight: 800;
    color: #7c3aed;
    margin-bottom: 0;
}
.sub-title {
    color: #888;
    font-size: 0.9rem;
    margin-top: 0.2rem;
    margin-bottom: 1.5rem;
}
.step-box {
    padding: 0.7rem 1rem;
    border-radius: 8px;
    margin-bottom: 0.5rem;
    font-size: 0.9rem;
    font-weight: 500;
}
.step-waiting { background: #f1f0f5; color: #888; }
.step-running { background: #fef3c7; color: #92400e; border-left: 4px solid #f59e0b; }
.step-done    { background: #d1fae5; color: #065f46; border-left: 4px solid #10b981; }
.score-display {
    font-size: 3.5rem;
    font-weight: 900;
    color: #7c3aed;
    line-height: 1;
}
.section-label {
    font-size: 0.7rem;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #aaa;
    margin-bottom: 0.5rem;
}
</style>
""", unsafe_allow_html=True)


# ── Header ────────────────────────────────────────────────────────────────────
st.markdown('<div class="main-title">🔬 ResearchAI</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-title">Search → Scrape → Write → Critique &nbsp;|&nbsp; Multi-Agent Pipeline</div>', unsafe_allow_html=True)
st.divider()

# ── Input ─────────────────────────────────────────────────────────────────────
col_input, col_btn = st.columns([5, 1])
with col_input:
    topic = st.text_input(
        label="Research Topic",
        placeholder="e.g. Impact of AI on healthcare in 2025",
        label_visibility="collapsed",
    )
with col_btn:
    run_btn = st.button("▶ Run", use_container_width=True, type="primary")


# ── Step renderer ─────────────────────────────────────────────────────────────
STEPS = [
    ("🔍", "Web Search Agent",   "Searching the web for relevant information…"),
    ("🌐", "Web Scrape Agent",   "Scraping top URLs for detailed content…"),
    ("✍️", "Report Writer",      "Drafting the research report…"),
    ("🎯", "Critic Reviewer",    "Reviewing and scoring the report…"),
]

def render_steps(active: int, done: list, placeholders: list):
    for i, (icon, title, _) in enumerate(STEPS):
        idx = i + 1
        if idx in done:
            css = "step-done"
            badge = "✓ Done"
        elif idx == active:
            css = "step-running"
            badge = "⏳ Running…"
        else:
            css = "step-waiting"
            badge = "Waiting"

        with placeholders[i]:
            st.markdown(
                f'<div class="step-box {css}">{icon} &nbsp; <b>{title}</b> &nbsp;'
                f'<span style="float:right;font-size:0.8rem">{badge}</span></div>',
                unsafe_allow_html=True,
            )


# ── Pipeline runner ───────────────────────────────────────────────────────────
def run_pipeline(topic: str):
    state = {}

    st.markdown('<div class="section-label">Pipeline Progress</div>', unsafe_allow_html=True)
    placeholders = [st.empty() for _ in STEPS]
    render_steps(active=1, done=[], placeholders=placeholders)

    # Step 1 — Search
    with st.spinner("🔍 Searching the web…"):
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user",
                f"Conduct a web search to gather recent and reliable information on: {topic}.")]
        })
    state["search_results"] = search_result["messages"][-1].content
    render_steps(active=2, done=[1], placeholders=placeholders)

    # Step 2 — Scrape
    with st.spinner("🌐 Scraping relevant pages…"):
        scrape_agent = build_scrape_agent()
        scrape_result = scrape_agent.invoke({
            "messages": [("user",
                f"Scrape the most relevant URLs for detailed info on: {topic}.\n\n"
                f"Search Results:\n{state['search_results'][:800]}")]
        })
    state["scrape_results"] = scrape_result["messages"][-1].content
    render_steps(active=3, done=[1, 2], placeholders=placeholders)

    # Step 3 — Writer
    with st.spinner("✍️ Writing the report…"):
        research_combined = (
            f"Search Results:\n{state['search_results']}\n\n"
            f"Detailed Scraped Content:\n{state['scrape_results']}"
        )
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined,
        })
    render_steps(active=4, done=[1, 2, 3], placeholders=placeholders)

    # Step 4 — Critic
    with st.spinner("🎯 Critiquing the report…"):
        state["feedback"] = critic_chain.invoke({
            "report": state["report"]
        })
    render_steps(active=0, done=[1, 2, 3, 4], placeholders=placeholders)

    st.success("✅ Research complete!")
    return state


# ── Trigger ───────────────────────────────────────────────────────────────────
if run_btn:
    if not topic.strip():
        st.warning("⚠️ Please enter a research topic first.")
    else:
        st.divider()
        results = run_pipeline(topic.strip())

        st.divider()

        # Raw data expanders
        st.markdown('<div class="section-label">Raw Agent Data</div>', unsafe_allow_html=True)
        with st.expander("🔍 Search Results"):
            st.text(results["search_results"])
        with st.expander("🌐 Scraped Content"):
            st.text(results["scrape_results"])

        st.divider()

        # Report + Feedback
        col_r, col_f = st.columns([3, 2], gap="large")

        with col_r:
            st.markdown('<div class="section-label">📄 Generated Report</div>', unsafe_allow_html=True)
            st.markdown(results["report"])
            st.download_button(
                label="⬇ Download Report (.txt)",
                data=results["report"],
                file_name=f"report_{topic[:30].replace(' ', '_')}.txt",
                mime="text/plain",
                use_container_width=True,
            )

        with col_f:
            st.markdown('<div class="section-label">🎯 Critic Feedback</div>', unsafe_allow_html=True)

            # Extract and display score
            score_match = re.search(r'Score[:\s]+(\d+(?:\.\d+)?)\s*/\s*10', results["feedback"], re.IGNORECASE)
            if score_match:
                st.markdown(
                    f'<div class="score-display">{score_match.group(1)}'
                    f'<span style="font-size:1.2rem;color:#aaa"> / 10</span></div>',
                    unsafe_allow_html=True,
                )
                st.caption("Critic Score")
                st.divider()

            st.markdown(results["feedback"])

else:
    # Empty state
    st.markdown(
        """
        <div style="text-align:center; padding: 5rem 0; color: #ccc;">
            <div style="font-size: 4rem;">🔬</div>
            <div style="font-size: 0.85rem; letter-spacing: 0.12em; margin-top: 1rem;">
                ENTER A TOPIC ABOVE AND CLICK RUN
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )
