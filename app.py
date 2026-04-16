# """
# EventForge AI — Streamlit Demo UI
# Chatbot-style input collection → live agent progress → rich output display.
# Run: streamlit run app.py
# """

# import asyncio
# import streamlit as st
# import time
# import sys
# import os

# # ── Page config ────────────────────────────────────────────────────────────────
# st.set_page_config(
#     page_title="EventForge AI",
#     page_icon="⚡",
#     layout="wide",
#     initial_sidebar_state="collapsed",
# )

# # ── Custom CSS ─────────────────────────────────────────────────────────────────
# st.markdown("""
# <style>
# @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Mono:wght@300;400;500&display=swap');

# html, body, [class*="css"] {
#     font-family: 'DM Mono', monospace;
#     background-color: #0a0a0f;
#     color: #e8e4d9;
# }

# .stApp {
#     background: #0a0a0f;
# }

# /* Hide default streamlit stuff */
# #MainMenu, footer, header { visibility: hidden; }

# /* Title */
# .ef-title {
#     font-family: 'Syne', sans-serif;
#     font-weight: 800;
#     font-size: 2.8rem;
#     letter-spacing: -0.03em;
#     background: linear-gradient(135deg, #f0e6c8 0%, #d4a853 50%, #e8c87a 100%);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
#     margin-bottom: 0;
#     line-height: 1.1;
# }

# .ef-subtitle {
#     font-family: 'DM Mono', monospace;
#     font-size: 0.75rem;
#     color: #5a5a6e;
#     letter-spacing: 0.15em;
#     text-transform: uppercase;
#     margin-top: 0.3rem;
#     margin-bottom: 2rem;
# }

# /* Chat bubble - bot */
# .chat-bot {
#     background: #141420;
#     border: 1px solid #2a2a3e;
#     border-left: 3px solid #d4a853;
#     border-radius: 0 12px 12px 12px;
#     padding: 0.9rem 1.2rem;
#     margin: 0.6rem 0;
#     font-size: 0.88rem;
#     max-width: 72%;
#     color: #c8c4b8;
#     position: relative;
# }

# .chat-bot::before {
#     content: '⚡ EventForge';
#     display: block;
#     font-size: 0.65rem;
#     color: #d4a853;
#     letter-spacing: 0.12em;
#     text-transform: uppercase;
#     margin-bottom: 0.4rem;
#     font-weight: 500;
# }

# /* Chat bubble - user */
# .chat-user {
#     background: #1a1a2e;
#     border: 1px solid #3a3a52;
#     border-right: 3px solid #7c6aff;
#     border-radius: 12px 0 12px 12px;
#     padding: 0.9rem 1.2rem;
#     margin: 0.6rem 0 0.6rem auto;
#     font-size: 0.88rem;
#     max-width: 60%;
#     color: #c8c4b8;
#     text-align: right;
#     position: relative;
# }

# .chat-user::after {
#     content: 'You';
#     display: block;
#     font-size: 0.65rem;
#     color: #7c6aff;
#     letter-spacing: 0.12em;
#     text-transform: uppercase;
#     margin-top: 0.4rem;
#     font-weight: 500;
# }

# /* Agent status cards */
# .agent-card {
#     background: #0f0f1a;
#     border: 1px solid #2a2a3e;
#     border-radius: 8px;
#     padding: 0.7rem 1rem;
#     margin: 0.3rem 0;
#     display: flex;
#     align-items: center;
#     gap: 0.8rem;
#     font-size: 0.82rem;
#     transition: all 0.3s ease;
# }

# .agent-card.running {
#     border-color: #d4a853;
#     background: #141410;
#     box-shadow: 0 0 12px rgba(212, 168, 83, 0.1);
# }

# .agent-card.done {
#     border-color: #3a7a4a;
#     background: #0f140f;
# }

# .agent-card.pending {
#     opacity: 0.4;
# }

# .status-dot {
#     width: 8px;
#     height: 8px;
#     border-radius: 50%;
#     flex-shrink: 0;
# }

# .dot-pending { background: #444; }
# .dot-running { background: #d4a853; animation: pulse 1s infinite; }
# .dot-done    { background: #4caf50; }
# .dot-failed  { background: #e05252; }

# @keyframes pulse {
#     0%, 100% { opacity: 1; transform: scale(1); }
#     50%       { opacity: 0.5; transform: scale(0.7); }
# }

# /* Output cards */
# .output-section {
#     background: #0f0f1a;
#     border: 1px solid #2a2a3e;
#     border-radius: 10px;
#     padding: 1.2rem 1.4rem;
#     margin-bottom: 1rem;
# }

# .output-section-title {
#     font-family: 'Syne', sans-serif;
#     font-size: 0.72rem;
#     letter-spacing: 0.2em;
#     text-transform: uppercase;
#     color: #d4a853;
#     margin-bottom: 0.8rem;
#     border-bottom: 1px solid #2a2a3e;
#     padding-bottom: 0.5rem;
# }

# .item-card {
#     background: #141420;
#     border: 1px solid #222235;
#     border-radius: 6px;
#     padding: 0.8rem 1rem;
#     margin-bottom: 0.6rem;
#     font-size: 0.8rem;
# }

# .item-name {
#     font-family: 'Syne', sans-serif;
#     font-weight: 600;
#     font-size: 0.9rem;
#     color: #e8e4d9;
#     margin-bottom: 0.3rem;
# }

# .item-meta {
#     color: #6a6a80;
#     font-size: 0.75rem;
#     margin-bottom: 0.2rem;
# }

# .score-badge {
#     display: inline-block;
#     background: #1e1e0a;
#     border: 1px solid #d4a853;
#     color: #d4a853;
#     border-radius: 4px;
#     padding: 0.1rem 0.4rem;
#     font-size: 0.7rem;
#     margin-right: 0.4rem;
# }

# .price-badge {
#     display: inline-block;
#     background: #0a1e0a;
#     border: 1px solid #4caf50;
#     color: #4caf50;
#     border-radius: 4px;
#     padding: 0.1rem 0.4rem;
#     font-size: 0.7rem;
# }

# /* Divider */
# .ef-divider {
#     border: none;
#     border-top: 1px solid #1e1e2e;
#     margin: 1.5rem 0;
# }

# /* Email block */
# .email-block {
#     background: #0a0a14;
#     border: 1px solid #1e1e35;
#     border-radius: 4px;
#     padding: 0.6rem 0.8rem;
#     font-size: 0.72rem;
#     color: #7a7a9a;
#     margin-top: 0.4rem;
#     font-style: italic;
#     line-height: 1.5;
# }

# /* Revenue highlight */
# .revenue-highlight {
#     font-family: 'Syne', sans-serif;
#     font-size: 2rem;
#     font-weight: 800;
#     background: linear-gradient(135deg, #4caf50, #8bc34a);
#     -webkit-background-clip: text;
#     -webkit-text-fill-color: transparent;
#     background-clip: text;
# }

# /* Input area styling */
# .stTextInput > div > div > input {
#     background: #141420 !important;
#     border: 1px solid #2a2a3e !important;
#     border-radius: 8px !important;
#     color: #e8e4d9 !important;
#     font-family: 'DM Mono', monospace !important;
#     font-size: 0.88rem !important;
# }

# .stNumberInput > div > div > input {
#     background: #141420 !important;
#     border: 1px solid #2a2a3e !important;
#     color: #e8e4d9 !important;
#     font-family: 'DM Mono', monospace !important;
# }

# .stSelectbox > div > div {
#     background: #141420 !important;
#     border: 1px solid #2a2a3e !important;
#     color: #e8e4d9 !important;
# }

# .stButton > button {
#     background: linear-gradient(135deg, #d4a853, #b8872a) !important;
#     color: #0a0a0f !important;
#     border: none !important;
#     border-radius: 6px !important;
#     font-family: 'Syne', sans-serif !important;
#     font-weight: 700 !important;
#     letter-spacing: 0.08em !important;
#     text-transform: uppercase !important;
#     font-size: 0.8rem !important;
#     padding: 0.5rem 1.5rem !important;
# }

# .stButton > button:hover {
#     background: linear-gradient(135deg, #e8c87a, #d4a853) !important;
#     transform: translateY(-1px);
# }
# </style>
# """, unsafe_allow_html=True)

# # ── State init ─────────────────────────────────────────────────────────────────
# def init_state():
#     defaults = {
#         "step": 0,            # which question we're on
#         "answers": {},        # collected answers
#         "chat_log": [],       # list of (role, text)
#         "pipeline_done": False,
#         "result": None,
#         "agent_statuses": {},
#         "pipeline_started": False,
#     }
#     for k, v in defaults.items():
#         if k not in st.session_state:
#             st.session_state[k] = v

# init_state()

# # ── Questions config ───────────────────────────────────────────────────────────
# QUESTIONS = [
#     {
#         "key": "category",
#         "bot": "👋 Welcome to **EventForge AI**! Let's plan your conference.\n\nFirst — what's the **category or theme** of your event?",
#         "placeholder": "e.g. AI & Machine Learning, FinTech, SaaS, Healthcare...",
#         "type": "text",
#     },
#     {
#         "key": "geography",
#         "bot": "Great choice! Now, what **geography** are you targeting — where will attendees primarily be from?",
#         "placeholder": "e.g. San Francisco, India, Europe, Global...",
#         "type": "text",
#     },
#     {
#         "key": "audience_size",
#         "bot": "Perfect. What's the **expected audience size** for your event?",
#         "placeholder": "e.g. 500",
#         "type": "number",
#     },
#     {
#         "key": "duration_days",
#         "bot": "How many **days** will the conference run?",
#         "type": "select",
#         "options": [1, 2, 3, 4, 5],
#     },
#     {
#         "key": "budget_usd",
#         "bot": "Finally — what's your **budget** (USD)? Enter 0 to skip.",
#         "placeholder": "e.g. 50000",
#         "type": "number",
#     },
# ]

# # ── Helpers ────────────────────────────────────────────────────────────────────
# def bot_bubble(text):
#     st.markdown(f'<div class="chat-bot">{text}</div>', unsafe_allow_html=True)

# def user_bubble(text):
#     col1, col2 = st.columns([1, 3])
#     with col2:
#         st.markdown(f'<div class="chat-user">{text}</div>', unsafe_allow_html=True)

# def render_chat_log():
#     for role, text in st.session_state.chat_log:
#         if role == "bot":
#             bot_bubble(text)
#         else:
#             user_bubble(text)

# def agent_status_html(name, status, elapsed=None):
#     dot_class = f"dot-{status}"
#     card_class = f"agent-card {status}"
#     label = {
#         "pending": "Waiting...",
#         "running": "Running" + (" · " + elapsed if elapsed else ""),
#         "done": "✓ Done" + (" · " + elapsed if elapsed else ""),
#         "failed": "✗ Failed",
#     }.get(status, status)
#     return f"""
#     <div class="{card_class}">
#         <span class="status-dot {dot_class}"></span>
#         <span style="font-family:'Syne',sans-serif;font-weight:600;color:#c8c4b8;">{name}</span>
#         <span style="color:#5a5a6e;margin-left:auto;font-size:0.75rem;">{label}</span>
#     </div>
#     """

# # ── Header ──────────────────────────────────────────────────────────────────────
# st.markdown('<div class="ef-title">⚡ EventForge AI</div>', unsafe_allow_html=True)
# st.markdown('<div class="ef-subtitle">Agentic Conference Intelligence Platform</div>', unsafe_allow_html=True)

# col_chat, col_status = st.columns([3, 2], gap="large")

# # ── LEFT: Chat ──────────────────────────────────────────────────────────────────
# with col_chat:

#     # If pipeline is done, show results
#     if st.session_state.pipeline_done and st.session_state.result:
#         render_chat_log()
#         st.markdown('<hr class="ef-divider">', unsafe_allow_html=True)

#         result = st.session_state.result
#         outputs = result.get("outputs", {})

#         final = outputs.get("final_agent")
#         if final is None:
#             st.error("Pipeline completed but no final output found. Check agent logs.")
#         else:
#             # ── Sponsors ──────────────────────────────────────────────────────
#             sponsors_out = final.sponsors
#             sponsors = sponsors_out.sponsors if hasattr(sponsors_out, "sponsors") else []
#             st.markdown('<div class="output-section">', unsafe_allow_html=True)
#             st.markdown('<div class="output-section-title">🤝 Recommended Sponsors</div>', unsafe_allow_html=True)
#             for s in sponsors:
#                 relevance = getattr(s, "relevance_score", 0)
#                 st.markdown(f"""
#                 <div class="item-card">
#                     <div class="item-name">{s.name}</div>
#                     <div class="item-meta">Industry: {s.industry}</div>
#                     <span class="score-badge">relevance {relevance:.0%}</span>
#                     <div style="color:#8a8a9a;font-size:0.78rem;margin-top:0.4rem;">{s.reason}</div>
#                     <div class="email-block">📧 {s.outreach_email[:280]}{'...' if len(s.outreach_email)>280 else ''}</div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#             # ── Speakers ──────────────────────────────────────────────────────
#             speakers_out = final.speakers
#             speakers = speakers_out.speakers if hasattr(speakers_out, "speakers") else []
#             st.markdown('<div class="output-section">', unsafe_allow_html=True)
#             st.markdown('<div class="output-section-title">🎤 Suggested Speakers</div>', unsafe_allow_html=True)
#             for sp in speakers:
#                 infl = getattr(sp, "influence_score", 0)
#                 st.markdown(f"""
#                 <div class="item-card">
#                     <div class="item-name">{sp.name}</div>
#                     <div class="item-meta">{sp.title} @ {sp.company}</div>
#                     <span class="score-badge">influence {infl:.0%}</span>
#                     <div style="color:#8a8a9a;font-size:0.78rem;margin-top:0.4rem;">Topic: <em>{sp.suggested_topic}</em></div>
#                     <div style="color:#6a6a80;font-size:0.75rem;margin-top:0.3rem;">{sp.bio_summary[:200]}{'...' if len(sp.bio_summary)>200 else ''}</div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#             # ── Venues ────────────────────────────────────────────────────────
#             venues_out = final.venues
#             venues = venues_out.venues if hasattr(venues_out, "venues") else []
#             st.markdown('<div class="output-section">', unsafe_allow_html=True)
#             st.markdown('<div class="output-section-title">🏛️ Venue Options</div>', unsafe_allow_html=True)
#             for v in venues:
#                 st.markdown(f"""
#                 <div class="item-card">
#                     <div class="item-name">{v.name}</div>
#                     <div class="item-meta">📍 {v.city} &nbsp;|&nbsp; 👥 Capacity: {v.capacity:,} &nbsp;|&nbsp; 💵 ${v.price_per_day_usd:,}/day</div>
#                     <div style="color:#8a8a9a;font-size:0.78rem;margin-top:0.3rem;">{v.notes}</div>
#                 </div>
#                 """, unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#             # ── Pricing ───────────────────────────────────────────────────────
#             pricing_out = final.pricing
#             tiers = pricing_out.tiers if hasattr(pricing_out, "tiers") else []
#             predicted_attendance = getattr(pricing_out, "predicted_attendance", "—")
#             predicted_revenue = getattr(pricing_out, "predicted_revenue_usd", 0)
#             st.markdown('<div class="output-section">', unsafe_allow_html=True)
#             st.markdown('<div class="output-section-title">💰 Ticket Pricing Strategy</div>', unsafe_allow_html=True)
#             st.markdown(f"""
#             <div style="display:flex;gap:2rem;margin-bottom:1rem;">
#                 <div>
#                     <div style="font-size:0.7rem;color:#5a5a6e;letter-spacing:0.1em;text-transform:uppercase;">Predicted Attendance</div>
#                     <div style="font-family:'Syne',sans-serif;font-size:1.5rem;font-weight:700;color:#c8c4b8;">{predicted_attendance:,}</div>
#                 </div>
#                 <div>
#                     <div style="font-size:0.7rem;color:#5a5a6e;letter-spacing:0.1em;text-transform:uppercase;">Predicted Revenue</div>
#                     <div class="revenue-highlight">${predicted_revenue:,}</div>
#                 </div>
#             </div>
#             """, unsafe_allow_html=True)
#             for t in tiers:
#                 st.markdown(f"""
#                 <div class="item-card" style="display:flex;justify-content:space-between;align-items:center;">
#                     <div>
#                         <div class="item-name">{t.name}</div>
#                         <div class="item-meta">Expected conversions: {t.expected_conversions}</div>
#                     </div>
#                     <span class="price-badge" style="font-size:0.9rem;padding:0.3rem 0.7rem;">${t.price_usd:,}</span>
#                 </div>
#                 """, unsafe_allow_html=True)
#             st.markdown('</div>', unsafe_allow_html=True)

#         if st.button("🔄 Plan Another Event"):
#             for k in list(st.session_state.keys()):
#                 del st.session_state[k]
#             st.rerun()

#     # If pipeline is running, show chat log + spinner
#     elif st.session_state.pipeline_started:
#         render_chat_log()
#         bot_bubble("🔍 Agents are working on your conference plan. Check the live status →")

#     # Otherwise, show chat + input form
#     else:
#         render_chat_log()

#         step = st.session_state.step
#         if step < len(QUESTIONS):
#             q = QUESTIONS[step]

#             # Show bot question if not already in chat_log
#             if not st.session_state.chat_log or st.session_state.chat_log[-1] != ("bot", q["bot"]):
#                 st.session_state.chat_log.append(("bot", q["bot"]))
#                 st.rerun()

#             # Input widget
#             with st.form(key=f"form_{step}", clear_on_submit=True):
#                 if q["type"] == "text":
#                     val = st.text_input("", placeholder=q.get("placeholder", ""), label_visibility="collapsed")
#                 elif q["type"] == "number":
#                     val = st.number_input("", min_value=0, value=0, label_visibility="collapsed")
#                 elif q["type"] == "select":
#                     val = st.selectbox("", q["options"], label_visibility="collapsed")

#                 submitted = st.form_submit_button("→ Send")
#                 if submitted:
#                     if q["type"] == "text" and not str(val).strip():
#                         st.warning("Please enter a value.")
#                     else:
#                         display_val = str(val) if q["type"] != "number" else f"{int(val):,}"
#                         st.session_state.chat_log.append(("user", display_val))
#                         st.session_state.answers[q["key"]] = val
#                         st.session_state.step += 1
#                         st.rerun()

#         else:
#             # All questions answered — show summary and launch button
#             a = st.session_state.answers
#             bot_bubble(f"""
#             ✅ Got everything! Here's your event summary:<br><br>
#             <strong>Category:</strong> {a['category']}<br>
#             <strong>Geography:</strong> {a['geography']}<br>
#             <strong>Audience Size:</strong> {int(a['audience_size']):,}<br>
#             <strong>Duration:</strong> {a['duration_days']} day(s)<br>
#             <strong>Budget:</strong> {'$' + f"{int(a['budget_usd']):,}" if a['budget_usd'] else 'Not specified'}
#             """)

#             if st.button("⚡ Launch EventForge Agents"):
#                 st.session_state.pipeline_started = True
#                 st.rerun()

# # ── RIGHT: Agent Live Status + Pipeline ────────────────────────────────────────
# with col_status:
#     st.markdown('<div style="font-family:\'Syne\',sans-serif;font-size:0.72rem;letter-spacing:0.2em;text-transform:uppercase;color:#5a5a6e;margin-bottom:0.8rem;">Agent Pipeline</div>', unsafe_allow_html=True)

#     AGENTS = [
#         ("sponsor_agent",  "Sponsor Agent"),
#         ("speaker_agent",  "Speaker Agent"),
#         ("venue_agent",    "Venue Agent"),
#         ("pricing_agent",  "Pricing Agent"),
#         ("final_agent",    "Final Synthesis"),
#     ]

#     agent_statuses = st.session_state.agent_statuses
#     agent_placeholders = {}
#     for key, label in AGENTS:
#         status = agent_statuses.get(key, "pending")
#         ph = st.empty()
#         ph.markdown(agent_status_html(label, status), unsafe_allow_html=True)
#         agent_placeholders[key] = (ph, label)

#     # ── Run the pipeline ONCE ─────────────────────────────────────────────────
#     if st.session_state.pipeline_started and not st.session_state.pipeline_done:
#         # Guard: don't re-run if already done
#         import threading

#         a = st.session_state.answers
#         state_input = {
#             "input": {
#                 "category": a["category"],
#                 "geography": a["geography"],
#                 "audience_size": int(a["audience_size"]),
#                 "duration_days": int(a["duration_days"]),
#                 "budget_usd": int(a["budget_usd"]) if a.get("budget_usd") else None,
#             },
#             "outputs": {},
#             "agent_meta": {},
#             "shared_memory": {},
#             "logs": [],
#             "errors": [],
#         }

#         # ── Async runner with live status updates ─────────────────────────────
#         async def run_pipeline_with_status():
#             # Import here to avoid issues if path not set
#             try:
#                 from eventforge.graph.builder import build_graph
#             except ImportError as e:
#                 return {"_error": str(e)}

#             graph = build_graph()

#             # We'll stream events from the graph
#             start_times = {}
#             finished_agents = set()

#             # Update statuses via session state
#             def set_status(agent_key, status, elapsed=None):
#                 st.session_state.agent_statuses[agent_key] = status

#             # Use astream_events for live updates
#             try:
#                 async for event in graph.astream_events(state_input, version="v2"):
#                     kind = event.get("event")
#                     name = event.get("name", "")

#                     # Map node names to our agent keys
#                     agent_key = name if name in dict(AGENTS) else None

#                     if kind == "on_chain_start" and agent_key:
#                         start_times[agent_key] = time.time()
#                         st.session_state.agent_statuses[agent_key] = "running"

#                     elif kind == "on_chain_end" and agent_key:
#                         elapsed = time.time() - start_times.get(agent_key, time.time())
#                         st.session_state.agent_statuses[agent_key] = "done"
#                         finished_agents.add(agent_key)

#                 # After stream ends, get the final result by re-invoking (same graph, same state)
#                 # Actually astream_events doesn't return the final state easily.
#                 # So we invoke separately, but ONLY after streaming is done.
#                 result = await graph.ainvoke(state_input)
#                 return result

#             except Exception as e:
#                 return {"_error": str(e)}

#         # We need a different approach: use astream to get state updates + final result
#         # to avoid double LLM calls. Let's use astream with stream_mode="updates".
#         async def run_pipeline_streaming():
#             try:
#                 from eventforge.graph.builder import build_graph
#             except ImportError as e:
#                 return None, str(e)

#             graph = build_graph()
#             start_times = {}
#             final_state = {}

#             try:
#                 # Mark parallel starters as running immediately
#                 for ak in ["sponsor_agent", "speaker_agent", "venue_agent"]:
#                     st.session_state.agent_statuses[ak] = "running"
#                     start_times[ak] = time.time()

#                 async for chunk in graph.astream(state_input, stream_mode="updates"):
#                     # chunk is {node_name: node_output_dict}
#                     for node_name, node_output in chunk.items():
#                         if node_name in dict(AGENTS):
#                             elapsed = time.time() - start_times.get(node_name, time.time())
#                             st.session_state.agent_statuses[node_name] = "done"
#                             # Mark next agents as running based on graph topology
#                             if node_name == "venue_agent":
#                                 st.session_state.agent_statuses["pricing_agent"] = "running"
#                                 start_times["pricing_agent"] = time.time()
#                             if node_name == "pricing_agent":
#                                 st.session_state.agent_statuses["final_agent"] = "running"
#                                 start_times["final_agent"] = time.time()
#                         # Accumulate state
#                         final_state.update(node_output)

#                 return final_state, None

#             except Exception as e:
#                 import traceback
#                 return None, traceback.format_exc()

#         # Run the async pipeline
#         loop = asyncio.new_event_loop()
#         asyncio.set_event_loop(loop)

#         status_text = st.empty()
#         status_text.markdown('<div style="color:#d4a853;font-size:0.8rem;margin-top:1rem;">⏳ Pipeline running...</div>', unsafe_allow_html=True)

#         final_state, error = loop.run_until_complete(run_pipeline_streaming())
#         loop.close()

#         if error:
#             st.session_state.pipeline_done = True
#             st.session_state.result = {"_error": error}
#             status_text.markdown(f'<div style="color:#e05252;font-size:0.8rem;margin-top:1rem;">❌ Pipeline failed</div>', unsafe_allow_html=True)
#         else:
#             st.session_state.pipeline_done = True
#             st.session_state.result = {"outputs": final_state.get("outputs", {})}
#             status_text.markdown('<div style="color:#4caf50;font-size:0.8rem;margin-top:1rem;">✅ Pipeline complete!</div>', unsafe_allow_html=True)

#         # Update all agent placeholders to final statuses
#         for key, (ph, label) in agent_placeholders.items():
#             status = st.session_state.agent_statuses.get(key, "done")
#             ph.markdown(agent_status_html(label, status), unsafe_allow_html=True)

#         time.sleep(0.5)
#         st.rerun()

#     # Show graph topology hint
#     if not st.session_state.pipeline_started:
#         st.markdown("""
#         <div style="margin-top:2rem;padding:1rem;background:#0f0f1a;border:1px solid #1e1e2e;border-radius:8px;font-size:0.75rem;color:#4a4a60;line-height:1.8;">
#         <div style="color:#3a3a50;margin-bottom:0.5rem;font-family:'Syne',sans-serif;font-size:0.65rem;letter-spacing:0.15em;text-transform:uppercase;">Execution Graph</div>
#         START<br>
#         ├── Sponsor Agent ─────┐<br>
#         ├── Speaker Agent ─────┤→ Final Synthesis → END<br>
#         └── Venue Agent → Pricing Agent ──┘<br>
#         <br>
#         <div style="color:#3a3a50;">Parallel execution with dependency resolution</div>
#         </div>
#         """, unsafe_allow_html=True)

#     # Error display
#     if st.session_state.pipeline_done and st.session_state.result and st.session_state.result.get("_error"):
#         st.markdown(f"""
#         <div style="background:#1a0a0a;border:1px solid #e05252;border-radius:8px;padding:1rem;margin-top:1rem;font-size:0.75rem;color:#e05252;font-family:'DM Mono',monospace;white-space:pre-wrap;">
# {st.session_state.result['_error']}
#         </div>
#         """, unsafe_allow_html=True)








#----------------------------------------------------#







"""
EventForge AI — Streamlit Frontend
====================================
Run:  streamlit run app.py
"""

import streamlit as st
import asyncio
import json
import time
import random
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime

# ── Page config (must be first Streamlit call) ──────────────────────────────
st.set_page_config(
    page_title="EventForge AI",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ── Custom CSS ───────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;500;600;700;800&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,300&display=swap');

/* ── Global reset ── */
*, *::before, *::after { box-sizing: border-box; }

html, body, [data-testid="stAppViewContainer"] {
    font-family: 'DM Sans', sans-serif;
    background: #0A0A0F !important;
    color: #E8E6F0;
}

[data-testid="stAppViewContainer"] > .main {
    background: #0A0A0F;
}

[data-testid="block-container"] {
    padding: 2rem 3rem 4rem;
    max-width: 1400px;
}

/* ── Sidebar ── */
[data-testid="stSidebar"] {
    background: #111118 !important;
    border-right: 1px solid #1E1E2E;
}

/* ── Headers ── */
h1, h2, h3, h4 {
    font-family: 'Syne', sans-serif !important;
    letter-spacing: -0.02em;
}

/* ── Hero section ── */
.hero-title {
    font-family: 'Syne', sans-serif;
    font-size: clamp(2.8rem, 6vw, 5rem);
    font-weight: 800;
    line-height: 1.0;
    letter-spacing: -0.04em;
    color: #F5F3FF;
    margin: 0 0 0.5rem;
}

.hero-accent {
    background: linear-gradient(135deg, #7C6AFA 0%, #C471ED 50%, #F64F59 100%);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
}

.hero-sub {
    font-family: 'DM Sans', sans-serif;
    font-size: 1.15rem;
    font-weight: 300;
    color: #8A88A0;
    letter-spacing: 0.01em;
    margin-bottom: 2.5rem;
    line-height: 1.6;
}

.badge-row {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 2rem;
}

.badge {
    font-family: 'DM Sans', sans-serif;
    font-size: 0.72rem;
    font-weight: 500;
    padding: 5px 12px;
    border-radius: 100px;
    letter-spacing: 0.08em;
    text-transform: uppercase;
}
.badge-purple { background: #1E1833; color: #9B8FFF; border: 1px solid #2D2550; }
.badge-teal   { background: #0D201A; color: #4ECDC4; border: 1px solid #164035; }
.badge-amber  { background: #201A0D; color: #F6AE2D; border: 1px solid #3D3318; }

/* ── Input card ── */
.input-card {
    background: #111118;
    border: 1px solid #1E1E2E;
    border-radius: 16px;
    padding: 2rem;
    margin-bottom: 1.5rem;
}

.section-label {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #5A58A0;
    margin-bottom: 1.2rem;
}

/* ── Streamlit input overrides ── */
.stTextInput > div > div > input,
.stNumberInput > div > div > input,
.stSelectbox > div > div {
    background: #0D0D14 !important;
    border: 1px solid #1E1E2E !important;
    border-radius: 10px !important;
    color: #E8E6F0 !important;
    font-family: 'DM Sans', sans-serif !important;
}

.stTextInput > div > div > input:focus,
.stNumberInput > div > div > input:focus {
    border-color: #7C6AFA !important;
    box-shadow: 0 0 0 3px rgba(124, 106, 250, 0.12) !important;
}

.stSlider > div > div > div > div {
    background: #7C6AFA !important;
}

/* Labels */
.stTextInput label, .stNumberInput label,
.stSelectbox label, .stSlider label,
.stDateInput label, .stTextArea label {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.82rem !important;
    font-weight: 500 !important;
    color: #8A88A0 !important;
    letter-spacing: 0.02em !important;
}

/* ── Run button ── */
div.stButton > button {
    font-family: 'Syne', sans-serif !important;
    font-weight: 700 !important;
    font-size: 0.95rem !important;
    letter-spacing: 0.05em !important;
    background: linear-gradient(135deg, #7C6AFA 0%, #C471ED 100%) !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    padding: 0.65rem 2rem !important;
    width: 100% !important;
    transition: opacity 0.2s, transform 0.1s !important;
    cursor: pointer !important;
}
div.stButton > button:hover {
    opacity: 0.88 !important;
    transform: translateY(-1px) !important;
}
div.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Metric cards ── */
.metric-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    gap: 12px;
    margin-bottom: 1.5rem;
}

.metric-card {
    background: #111118;
    border: 1px solid #1E1E2E;
    border-radius: 12px;
    padding: 1.1rem 1.2rem;
}

.metric-label {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.1em;
    text-transform: uppercase;
    color: #5A58A0;
    margin-bottom: 6px;
}

.metric-value {
    font-family: 'Syne', sans-serif;
    font-size: 1.7rem;
    font-weight: 700;
    color: #F5F3FF;
    line-height: 1;
}

.metric-delta {
    font-size: 0.75rem;
    color: #4ECDC4;
    margin-top: 4px;
}

/* ── Agent pipeline ── */
.pipeline-wrap {
    background: #0D0D14;
    border: 1px solid #1E1E2E;
    border-radius: 14px;
    padding: 1.5rem;
    margin-bottom: 1.5rem;
}

.agent-row {
    display: flex;
    align-items: center;
    gap: 12px;
    padding: 10px 14px;
    border-radius: 10px;
    margin-bottom: 8px;
    transition: background 0.2s;
}

.agent-row.running  { background: #1A1535; border: 1px solid #2D2550; }
.agent-row.done     { background: #0D1E19; border: 1px solid #164035; }
.agent-row.waiting  { background: #111118; border: 1px solid #1E1E2E; }
.agent-row.error    { background: #1E0D0D; border: 1px solid #3D1818; }

.agent-icon { font-size: 18px; width: 28px; text-align: center; }
.agent-name { font-family: 'Syne', sans-serif; font-size: 0.85rem; font-weight: 600; flex: 1; }
.agent-name.running  { color: #9B8FFF; }
.agent-name.done     { color: #4ECDC4; }
.agent-name.waiting  { color: #3E3C5A; }
.agent-name.error    { color: #F64F59; }

.agent-status {
    font-size: 0.72rem;
    font-weight: 500;
    letter-spacing: 0.06em;
    text-transform: uppercase;
}
.status-running { color: #7C6AFA; }
.status-done    { color: #4ECDC4; }
.status-waiting { color: #3E3C5A; }
.status-error   { color: #F64F59; }

/* pulse animation for running */
@keyframes pulse { 0%, 100% { opacity: 1; } 50% { opacity: 0.4; } }
.pulse { animation: pulse 1.4s ease-in-out infinite; }

/* ── Result tabs ── */
.stTabs [data-baseweb="tab-list"] {
    background: #111118 !important;
    border-radius: 10px !important;
    padding: 4px !important;
    border: 1px solid #1E1E2E !important;
    gap: 2px !important;
}

.stTabs [data-baseweb="tab"] {
    font-family: 'DM Sans', sans-serif !important;
    font-size: 0.83rem !important;
    font-weight: 500 !important;
    color: #5A58A0 !important;
    border-radius: 8px !important;
    padding: 6px 16px !important;
}

.stTabs [aria-selected="true"] {
    background: #1E1833 !important;
    color: #9B8FFF !important;
}

/* ── Result cards ── */
.result-card {
    background: #111118;
    border: 1px solid #1E1E2E;
    border-radius: 14px;
    padding: 1.4rem 1.6rem;
    margin-bottom: 12px;
    transition: border-color 0.2s;
}
.result-card:hover { border-color: #2D2550; }

.result-card-header {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 10px;
}

.result-card-name {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #F5F3FF;
}

.score-pill {
    font-size: 0.72rem;
    font-weight: 600;
    padding: 3px 10px;
    border-radius: 100px;
    letter-spacing: 0.05em;
}
.score-high   { background: #0D2420; color: #4ECDC4; border: 1px solid #164035; }
.score-medium { background: #20180D; color: #F6AE2D; border: 1px solid #3D3318; }
.score-low    { background: #200D0D; color: #F64F59; border: 1px solid #3D1818; }

.result-meta {
    font-size: 0.8rem;
    color: #5A58A0;
    margin-bottom: 8px;
}

.result-body {
    font-size: 0.88rem;
    color: #A09EB8;
    line-height: 1.6;
}

/* ── Agenda ── */
.agenda-day-header {
    font-family: 'Syne', sans-serif;
    font-size: 0.7rem;
    font-weight: 700;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #5A58A0;
    padding: 6px 0;
    border-bottom: 1px solid #1E1E2E;
    margin: 1.2rem 0 0.8rem;
}

.session-row {
    display: grid;
    grid-template-columns: 90px 1fr auto;
    gap: 16px;
    align-items: center;
    padding: 12px 14px;
    border-radius: 10px;
    margin-bottom: 6px;
    border: 1px solid #1E1E2E;
}

.session-time {
    font-family: 'Syne', sans-serif;
    font-size: 0.82rem;
    font-weight: 600;
    color: #7C6AFA;
}

.session-title {
    font-weight: 500;
    font-size: 0.9rem;
    color: #E8E6F0;
}

.session-speaker {
    font-size: 0.78rem;
    color: #5A58A0;
    margin-top: 2px;
}

.session-type {
    font-size: 0.68rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 100px;
    text-transform: uppercase;
    letter-spacing: 0.07em;
    white-space: nowrap;
}

.type-keynote   { background: #1E1833; color: #9B8FFF; }
.type-panel     { background: #0D1E20; color: #4ECDC4; }
.type-workshop  { background: #20180D; color: #F6AE2D; }
.type-break     { background: #141414; color: #3E3C5A; }
.type-ceremony  { background: #200D18; color: #C471ED; }
.type-networking { background: #0D1820; color: #57B8FF; }

/* ── Community cards ── */
.community-card {
    background: #111118;
    border: 1px solid #1E1E2E;
    border-radius: 12px;
    padding: 1.1rem 1.3rem;
    margin-bottom: 10px;
}

.community-platform {
    display: inline-block;
    font-size: 0.68rem;
    font-weight: 600;
    padding: 2px 8px;
    border-radius: 100px;
    text-transform: uppercase;
    letter-spacing: 0.08em;
    margin-bottom: 6px;
}
.platform-discord  { background: #1A1535; color: #9B8FFF; }
.platform-slack    { background: #1A200D; color: #7CC84B; }
.platform-linkedin { background: #0D1820; color: #57B8FF; }
.platform-facebook { background: #0D1420; color: #4A8FFF; }

/* ── Venue cards ── */
.venue-card {
    background: #111118;
    border: 1px solid #1E1E2E;
    border-radius: 14px;
    padding: 1.4rem;
    margin-bottom: 12px;
}
.venue-name {
    font-family: 'Syne', sans-serif;
    font-size: 1rem;
    font-weight: 700;
    color: #F5F3FF;
    margin-bottom: 4px;
}
.venue-location { font-size: 0.8rem; color: #5A58A0; margin-bottom: 10px; }
.venue-detail-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 8px;
}
.venue-detail { font-size: 0.8rem; color: #A09EB8; }
.venue-detail span { color: #E8E6F0; font-weight: 500; }

/* ── GTM timeline ── */
.gtm-step {
    display: flex;
    gap: 16px;
    margin-bottom: 16px;
    position: relative;
}
.gtm-step-num {
    width: 28px;
    height: 28px;
    border-radius: 50%;
    background: #1E1833;
    border: 1px solid #2D2550;
    display: flex;
    align-items: center;
    justify-content: center;
    font-family: 'Syne', sans-serif;
    font-size: 0.75rem;
    font-weight: 700;
    color: #9B8FFF;
    flex-shrink: 0;
    margin-top: 2px;
}
.gtm-step-content { flex: 1; }
.gtm-step-channel { font-weight: 600; font-size: 0.88rem; color: #E8E6F0; }
.gtm-step-timing  { font-size: 0.75rem; color: #5A58A0; margin-bottom: 4px; }
.gtm-step-msg     { font-size: 0.84rem; color: #8A88A0; line-height: 1.5; }

/* ── Error / info boxes ── */
.info-box {
    background: #0D1820;
    border: 1px solid #1A3040;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    color: #57B8FF;
    margin-bottom: 12px;
}

.warn-box {
    background: #20180D;
    border: 1px solid #3D3318;
    border-radius: 10px;
    padding: 1rem 1.2rem;
    font-size: 0.85rem;
    color: #F6AE2D;
    margin-bottom: 12px;
}

/* ── Divider ── */
hr { border: none; border-top: 1px solid #1E1E2E; margin: 2rem 0; }

/* ── Plotly chart background override ── */
.js-plotly-plot .plotly { background: transparent !important; }

/* ── Hide Streamlit branding ── */
#MainMenu, footer, header { visibility: hidden; }
.stDeployButton { display: none; }
</style>
""", unsafe_allow_html=True)


# ── Session state init ──────────────────────────────────────────────────────
if "results" not in st.session_state:
    st.session_state.results = None
if "running" not in st.session_state:
    st.session_state.running = False
if "agent_statuses" not in st.session_state:
    st.session_state.agent_statuses = {}


def generate_mock_results(inputs: dict) -> dict:
    import asyncio
    from eventforge.graph.builder import build_graph

    graph = build_graph()

    state = {
        "input": {
            "category":      inputs["category"],
            "geography":     inputs["geography"],
            "audience_size": inputs["audience_size"],
        },
        "outputs": {},
        "agent_meta": {},
        "shared_memory": {},
        "logs": [],
        "errors": [],
    }

    result = asyncio.run(graph.ainvoke(state))
    return result["outputs"]   # your agents write here


# ── Helper: score pill ───────────────────────────────────────────────────────
def score_pill(score: float) -> str:
    pct = int(score * 100)
    cls = "score-high" if pct >= 80 else "score-medium" if pct >= 60 else "score-low"
    return f'<span class="score-pill {cls}">{pct}% match</span>'


def platform_badge(platform: str) -> str:
    cls = f"platform-{platform.lower()}"
    return f'<span class="community-platform {cls}">{platform}</span>'


def session_type_badge(stype: str) -> str:
    return f'<span class="session-type type-{stype}">{stype}</span>'


# ─────────────────────────────────────────────────────────────────────────────
#  LAYOUT
# ─────────────────────────────────────────────────────────────────────────────

# ── Hero ─────────────────────────────────────────────────────────────────────
col_hero, col_graphic = st.columns([3, 2], gap="large")

with col_hero:
    st.markdown("""
    <p class="hero-sub">
    Plan your entire conference in one place.<br>
    Enter your event details, run the planner, and explore results across pricing, speakers, venue, and more.
    </p>

    <div class="info-box">
    Fill in the details below → click <b>Run Event Planner</b> → explore results in tabs.
    </div>
    """, unsafe_allow_html=True)

with col_graphic:
    # Agent pipeline mini-diagram
    st.markdown("""
    <div style="padding: 2.5rem 0 1rem;">
        <div style="display:flex; flex-direction:column; gap:6px;">
    """ + "".join([
        f"""<div style="background:#111118; border:1px solid #1E1E2E; border-radius:8px;
                       padding:8px 14px; display:flex; align-items:center; gap:10px;">
              <span style="font-size:14px;">{icon}</span>
              <span style="font-family:'Syne',sans-serif; font-size:0.78rem; font-weight:600;
                           color:#5A58A0; letter-spacing:0.04em;">{name}</span>
              <span style="margin-left:auto; width:6px; height:6px; border-radius:50%;
                           background:{color};"></span>
            </div>"""
        for icon, name, color in [
            ("🏢", "Sponsors", "#7C6AFA"),
            ("🎤", "Speakers", "#C471ED"),
            ("📍", "Venue", "#4ECDC4"),
            ("💰", "Pricing", "#F6AE2D"),
            ("🏪", "Exhibitors", "#F64F59"),
            ("📣", "Marketing", "#57B8FF"),
            ("📋", "Schedule", "#7CC84B"),
        ]
    ]) + """
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<hr>", unsafe_allow_html=True)


# ── Input Form ───────────────────────────────────────────────────────────────
st.markdown("""
<div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:700;
            color:#F5F3FF; margin-bottom:1.5rem; letter-spacing:-0.02em;">
    Enter your event details
</div>
""", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3, gap="medium")

with col1:
    st.markdown('<div class="section-label">Event details</div>', unsafe_allow_html=True)
    event_name = st.text_input("Event name", value="DevConf India 2025",
                                placeholder="e.g. DevConf India 2025")
    category = st.selectbox("Category / theme", [
        "AI/ML", "Web3 & Blockchain", "FinTech", "HealthTech",
        "DevOps & Cloud", "Cybersecurity", "Product & Design",
        "Data Engineering", "Gaming & AR/VR", "SaaS & B2B Tech"
    ])
    geography = st.text_input("Location", value="Bangalore, India",
                               placeholder="City, Country")

with col2:
    st.markdown('<div class="section-label">Scale & budget</div>', unsafe_allow_html=True)
    audience_size = st.number_input("Expected attendees", min_value=50, max_value=50000,
                                     value=1200, step=50)
    budget = st.number_input("Total budget (₹)", min_value=100000, max_value=50000000,
                               value=5000000, step=100000,
                               format="%d")
    num_days = st.slider("Conference duration (days)", 1, 5, 2)

with col3:
    st.markdown('<div class="section-label">Schedule</div>', unsafe_allow_html=True)
    event_date = st.date_input("Event start date",
                                value=datetime(2025, 11, 15))
    event_topic = st.text_area("Specific topic / focus",
                                value="Large Language Models, Agentic AI, and AI in India",
                                height=80,
                                placeholder="More detail = better agent outputs")
    run_btn = st.button("Generate Conference Plan", use_container_width=True)


# ── Agent progress tracker ────────────────────────────────────────────────────
AGENTS = [
    ("🏢", "sponsor_agent",   "Finding sponsors",   "Identifying relevant companies"),
    ("🎤", "speaker_agent",   "Selecting speakers", "Matching speakers to your theme"),
    ("📍", "venue_agent",     "Choosing venue",     "Finding suitable venues"),
    ("💰", "pricing_agent",   "Setting pricing",    "Estimating ticket pricing"),
    ("🏪", "exhibitor_agent", "Planning exhibitors","Selecting exhibitor categories"),
    ("📣", "gtm_agent",       "Marketing plan",     "Identifying communities & outreach"),
    ("📋", "ops_agent",       "Building schedule",  "Creating agenda and resolving conflicts"),
]


def render_pipeline(statuses: dict):
    html = '<div class="pipeline-wrap">'
    html += '<div class="section-label" style="margin-bottom:1rem;">Agent pipeline</div>'
    for icon, key, name, desc in AGENTS:
        s = statuses.get(key, "waiting")
        pulse = ' pulse' if s == "running" else ""
        html += f"""
        <div class="agent-row {s}">
            <span class="agent-icon">{icon}</span>
            <div style="flex:1;">
                <div class="agent-name {s}">{name}</div>
                <div style="font-size:0.73rem; color:#3E3C5A; margin-top:1px;">{desc}</div>
            </div>
            <span class="agent-status status-{s}{pulse}">
                {"● running" if s == "running" else "✓ done" if s == "done" else "✗ error" if s == "error" else "○ waiting"}
            </span>
        </div>"""
    html += "</div>"
    return html


# ── Run logic ─────────────────────────────────────────────────────────────────
if run_btn:
    st.session_state.running = True
    st.session_state.results = None

    inputs = {
        "event_name":    event_name,
        "category":      category,
        "geography":     geography,
        "audience_size": audience_size,
        "budget":        budget,
        "num_days":      num_days,
        "event_date":    event_date.strftime("%Y-%m-%d"),
        "event_topic":   event_topic,
    }

    pipeline_placeholder = st.empty()

    # Simulate parallel + sequential agent execution
    parallel_agents = ["sponsor_agent", "speaker_agent", "venue_agent",
                       "exhibitor_agent", "gtm_agent"]
    sequential_agents = [("pricing_agent", "venue_agent"), ("ops_agent", None)]

    statuses = {k: "waiting" for _, k, _, _ in AGENTS}

    # Start parallel agents
    for key in parallel_agents:
        statuses[key] = "running"
    pipeline_placeholder.markdown(render_pipeline(statuses), unsafe_allow_html=True)
    time.sleep(0.8)

    # Finish parallel agents one by one
    for key in parallel_agents:
        time.sleep(random.uniform(0.6, 1.2))
        statuses[key] = "done"
        pipeline_placeholder.markdown(render_pipeline(statuses), unsafe_allow_html=True)

    # Pricing (depends on venue)
    statuses["pricing_agent"] = "running"
    pipeline_placeholder.markdown(render_pipeline(statuses), unsafe_allow_html=True)
    time.sleep(1.0)
    statuses["pricing_agent"] = "done"
    pipeline_placeholder.markdown(render_pipeline(statuses), unsafe_allow_html=True)

    # Ops agent (final)
    statuses["ops_agent"] = "running"
    pipeline_placeholder.markdown(render_pipeline(statuses), unsafe_allow_html=True)
    time.sleep(1.2)
    statuses["ops_agent"] = "done"
    pipeline_placeholder.markdown(render_pipeline(statuses), unsafe_allow_html=True)

    st.session_state.agent_statuses = statuses
    st.session_state.results = generate_mock_results(inputs)
    st.session_state.running = False

elif st.session_state.agent_statuses:
    st.markdown(render_pipeline(st.session_state.agent_statuses), unsafe_allow_html=True)
else:
    init_statuses = {k: "waiting" for _, k, _, _ in AGENTS}
    st.markdown(render_pipeline(init_statuses), unsafe_allow_html=True)


# ── Results ───────────────────────────────────────────────────────────────────
if st.session_state.results:
    r = st.session_state.results
    summary = r["summary"]

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="font-family:'Syne',sans-serif; font-size:1.3rem; font-weight:700;
                color:#F5F3FF; margin-bottom:1.2rem; letter-spacing:-0.02em;">
        Your conference plan
    </div>
    """, unsafe_allow_html=True)

    # Summary metric cards
    st.markdown(f"""
    <div class="metric-grid">
        <div class="metric-card">
            <div class="metric-label">Sponsors found</div>
            <div class="metric-value">{summary["total_sponsors"]}</div>
            <div class="metric-delta">+ outreach drafts</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Speakers sourced</div>
            <div class="metric-value">{summary["total_speakers"]}</div>
            <div class="metric-delta">LinkedIn + web</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Sessions scheduled</div>
            <div class="metric-value">{summary["total_sessions"]}</div>
            <div class="metric-delta">Conflict-free ✓</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Communities found</div>
            <div class="metric-value">{summary["total_communities"]}</div>
            <div class="metric-delta">Discord + Slack + LinkedIn</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Optimal ticket price</div>
            <div class="metric-value">{summary["recommended_price"]}</div>
            <div class="metric-delta">ML regression model</div>
        </div>
        <div class="metric-card">
            <div class="metric-label">Projected revenue</div>
            <div class="metric-value" style="font-size:1.3rem;">{summary["projected_revenue"]}</div>
            <div class="metric-delta">tickets only</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # ── Tabs ─────────────────────────────────────────────────────────────────
    tabs = st.tabs([
        "🏢  Sponsors",
        "🎤  Speakers",
        "📍  Venues",
        "💰  Pricing",
        "🏪  Exhibitors",
        "📣  GTM Plan",
        "📋  Agenda",
    ])

    # ── Tab 1: Sponsors ───────────────────────────────────────────────────────
    with tabs[0]:
        st.markdown('<div class="section-label" style="margin-top:1rem;">Ranked sponsor recommendations</div>',
                    unsafe_allow_html=True)

        for sp in r["sponsors"]:
            name = sp["name"]
            industry = sp["industry"]
            score = sp["relevance_score"]
            proposal = sp["proposal_text"]
            pill = score_pill(score)

            st.markdown(f"""
            <div class="result-card">
                <div class="result-card-header">
                    <span class="result-card-name">{name}</span>
                    {pill}
                </div>
                <div class="result-meta">🏭 {industry}</div>
                <div class="result-body">{proposal}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 2: Speakers ───────────────────────────────────────────────────────
    with tabs[1]:
        st.markdown('<div class="section-label" style="margin-top:1rem;">Speaker recommendations + slot assignments</div>',
                    unsafe_allow_html=True)

        for spk in r["speakers"]:
            pill = score_pill(spk["relevance_score"])
            st.markdown(f"""
            <div class="result-card">
                <div class="result-card-header">
                    <span class="result-card-name">{spk["name"]}</span>
                    {pill}
                </div>
                <div class="result-meta">💼 {spk["title"]} &nbsp;·&nbsp; 🗓 {spk["suggested_slot"]}</div>
                <div class="result-body">{spk["bio_summary"]}</div>
                <div style="display:flex; gap:20px; margin-top:12px;">
                    <span style="font-size:0.78rem; color:#5A58A0;">
                        👥 <span style="color:#A09EB8;">{spk["follower_count"]:,} followers</span>
                    </span>
                    <span style="font-size:0.78rem; color:#5A58A0;">
                        📄 <span style="color:#A09EB8;">{spk["publications"]} publications</span>
                    </span>
                    <span style="font-size:0.78rem; color:#5A58A0;">
                        🎙 <span style="color:#A09EB8;">{spk["past_speaking"]} past talks</span>
                    </span>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 3: Venues ─────────────────────────────────────────────────────────
    with tabs[2]:
        st.markdown('<div class="section-label" style="margin-top:1rem;">Top venue recommendations</div>',
                    unsafe_allow_html=True)

        for i, v in enumerate(r["venues"]):
            stars = "★" * int(v["rating"]) + "☆" * (5 - int(v["rating"]))
            amenities_html = " &nbsp;·&nbsp; ".join(v["amenities"])
            badge = ""
            if i == 0:
                badge = '<span style="font-size:0.68rem; font-weight:600; padding:2px 8px; border-radius:100px; background:#1E1833; color:#9B8FFF; border:1px solid #2D2550; margin-left:10px;">Recommended</span>'

            st.markdown(f"""
            <div class="venue-card">
                <div class="venue-name">{v["name"]}{badge}</div>
                <div class="venue-location">📍 {v["location"]} &nbsp;·&nbsp; ⭐ {v["rating"]} {stars}</div>
                <div class="venue-detail-grid">
                    <div class="venue-detail">Capacity: <span>{v["capacity"]:,} pax</span></div>
                    <div class="venue-detail">Day rate: <span>₹{v["price_per_day"]:,.0f}</span></div>
                    <div class="venue-detail" style="grid-column:1/-1;">Amenities: <span>{amenities_html}</span></div>
                    <div class="venue-detail" style="grid-column:1/-1; margin-top:6px; font-style:italic;">
                        💬 {v["notes"]}
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 4: Pricing ────────────────────────────────────────────────────────
    with tabs[3]:
        pricing = r["pricing"]

        st.markdown('<div class="section-label" style="margin-top:1rem;">ML pricing model — attendance vs ticket price</div>',
                    unsafe_allow_html=True)

        col_chart, col_tiers = st.columns([3, 2], gap="large")

        with col_chart:
            curve = pricing["price_curve"]
            df_curve = pd.DataFrame(curve)

            fig = go.Figure()

            # Attendance curve
            fig.add_trace(go.Scatter(
                x=df_curve["price"], y=df_curve["predicted_attendance"],
                name="Predicted attendance",
                line=dict(color="#9B8FFF", width=2.5),
                fill="tozeroy",
                fillcolor="rgba(124,106,250,0.08)",
                hovertemplate="₹%{x:,}<br>%{y:,} attendees<extra></extra>"
            ))

            # Mark optimal price
            fig.add_vline(
                x=pricing["optimal_price"],
                line_dash="dot", line_color="#4ECDC4", line_width=1.5,
                annotation_text=f"Optimal ₹{pricing['optimal_price']:,}",
                annotation_font_color="#4ECDC4",
                annotation_font_size=11,
            )

            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#8A88A0"),
                xaxis=dict(
                    title="Ticket price (₹)",
                    gridcolor="#1E1E2E",
                    tickformat="₹,.0f",
                    color="#5A58A0",
                    titlefont=dict(color="#5A58A0"),
                ),
                yaxis=dict(
                    title="Predicted attendance",
                    gridcolor="#1E1E2E",
                    color="#5A58A0",
                    titlefont=dict(color="#5A58A0"),
                ),
                showlegend=False,
                margin=dict(l=10, r=10, t=20, b=10),
                height=280,
            )
            st.plotly_chart(fig, use_container_width=True)

            # Revenue curve
            st.markdown('<div class="section-label">Revenue curve</div>', unsafe_allow_html=True)

            fig2 = go.Figure()
            fig2.add_trace(go.Bar(
                x=df_curve["price"], y=df_curve["revenue"],
                marker_color=[
                    "#7C6AFA" if p == pricing["optimal_price"] else "#1E1E2E"
                    for p in df_curve["price"]
                ],
                hovertemplate="₹%{x:,}<br>Revenue ₹%{y:,.0f}<extra></extra>"
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                plot_bgcolor="rgba(0,0,0,0)",
                font=dict(family="DM Sans", color="#8A88A0"),
                xaxis=dict(gridcolor="#1E1E2E", color="#5A58A0", tickformat="₹,.0f",
                           titlefont=dict(color="#5A58A0")),
                yaxis=dict(gridcolor="#1E1E2E", color="#5A58A0",
                           titlefont=dict(color="#5A58A0")),
                showlegend=False,
                margin=dict(l=10, r=10, t=10, b=10),
                height=200,
            )
            st.plotly_chart(fig2, use_container_width=True)

        with col_tiers:
            st.markdown('<div class="section-label" style="margin-top:0.2rem;">Ticket tier simulation</div>',
                        unsafe_allow_html=True)

            total_projected = 0
            for tier in pricing["tiers"]:
                proj_sold = int(tier["available"] * tier["conversion"])
                proj_rev  = proj_sold * tier["price"]
                total_projected += proj_rev
                bar_width = int(tier["conversion"] * 100)
                is_optimal = tier["price"] == pricing["optimal_price"]
                border = "border: 1px solid #2D2550;" if is_optimal else "border: 1px solid #1E1E2E;"

                st.markdown(f"""
                <div style="background:#111118; {border} border-radius:10px;
                            padding:1rem 1.1rem; margin-bottom:8px;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:6px;">
                        <span style="font-family:'Syne',sans-serif; font-size:0.85rem;
                                     font-weight:600; color:#F5F3FF;">{tier["tier"]}</span>
                        <span style="font-family:'Syne',sans-serif; font-size:0.85rem;
                                     font-weight:700; color:#9B8FFF;">₹{tier["price"]:,}</span>
                    </div>
                    <div style="font-size:0.75rem; color:#5A58A0; margin-bottom:8px;">
                        {proj_sold} / {tier["available"]} sold &nbsp;·&nbsp;
                        Conv. {int(tier["conversion"]*100)}%
                    </div>
                    <div style="background:#1E1E2E; border-radius:4px; height:4px;">
                        <div style="background:#7C6AFA; width:{bar_width}%; height:4px;
                                    border-radius:4px;"></div>
                    </div>
                    <div style="font-size:0.72rem; color:#4ECDC4; margin-top:6px;">
                        ₹{proj_rev:,.0f} projected
                    </div>
                </div>
                """, unsafe_allow_html=True)

            st.markdown(f"""
            <div style="background:#0D1E19; border:1px solid #164035; border-radius:10px;
                        padding:1rem 1.1rem; margin-top:4px;">
                <div style="font-size:0.72rem; font-weight:600; letter-spacing:0.1em;
                            text-transform:uppercase; color:#164035; margin-bottom:4px;">Total projected</div>
                <div style="font-family:'Syne',sans-serif; font-size:1.5rem; font-weight:700;
                            color:#4ECDC4;">₹{total_projected:,.0f}</div>
            </div>
            """, unsafe_allow_html=True)

    # ── Tab 5: Exhibitors ─────────────────────────────────────────────────────
    with tabs[4]:
        st.markdown('<div class="section-label" style="margin-top:1rem;">Exhibitor categories</div>',
                    unsafe_allow_html=True)

        exhibitors = r["exhibitors"]
        cat_colors = {
            "Enterprise": ("#1A3040", "#57B8FF"),
            "Startup":    ("#1E1833", "#9B8FFF"),
            "Tools & Infra": ("#0D2420", "#4ECDC4"),
        }

        for cat_name, items in exhibitors.items():
            bg, fg = cat_colors.get(cat_name, ("#111118", "#8A88A0"))
            items_html = "".join([
                f"""<div style="background:#111118; border:1px solid #1E1E2E; border-radius:8px;
                               padding:10px 14px; margin-bottom:6px;">
                      <div style="font-weight:600; font-size:0.86rem; color:#E8E6F0;
                                  margin-bottom:3px;">{item["name"]}</div>
                      <div style="font-size:0.76rem; color:#5A58A0;">
                          {item["booth_size"]} booth &nbsp;·&nbsp; {item["products"]}
                      </div>
                    </div>"""
                for item in items
            ])
            st.markdown(f"""
            <div style="margin-bottom:1.2rem;">
                <div style="background:{bg}; border-radius:8px; padding:5px 12px;
                            display:inline-block; font-size:0.72rem; font-weight:600;
                            letter-spacing:0.1em; text-transform:uppercase; color:{fg};
                            margin-bottom:10px;">
                    {cat_name} — {len(items)} companies
                </div>
                {items_html}
            </div>
            """, unsafe_allow_html=True)

        # Pie chart
        pie_labels = list(exhibitors.keys())
        pie_values = [len(v) for v in exhibitors.values()]
        fig_pie = go.Figure(go.Pie(
            labels=pie_labels,
            values=pie_values,
            hole=0.55,
            marker_colors=["#57B8FF", "#9B8FFF", "#4ECDC4"],
            textfont_color=["#0C447C", "#26215C", "#04342C"],
        ))
        fig_pie.update_layout(
            paper_bgcolor="rgba(0,0,0,0)",
            plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="DM Sans", color="#8A88A0"),
            showlegend=True,
            legend=dict(font=dict(color="#8A88A0")),
            margin=dict(l=0, r=0, t=20, b=0),
            height=220,
        )
        st.plotly_chart(fig_pie, use_container_width=True)

    # ── Tab 6: GTM Plan ───────────────────────────────────────────────────────
    with tabs[5]:
        col_comm, col_gtm = st.columns([2, 3], gap="large")

        with col_comm:
            st.markdown('<div class="section-label" style="margin-top:1rem;">Top communities</div>',
                        unsafe_allow_html=True)

            for c in r["communities"]:
                pb = platform_badge(c["platform"])
                st.markdown(f"""
                <div class="community-card">
                    {pb}
                    <div style="font-family:'Syne',sans-serif; font-size:0.9rem;
                                font-weight:700; color:#F5F3FF; margin-bottom:3px;">{c["name"]}</div>
                    <div style="font-size:0.76rem; color:#5A58A0; margin-bottom:8px;">
                        {c["member_count"]:,} members &nbsp;·&nbsp; {c["niche"]}
                    </div>
                    <div style="font-size:0.82rem; color:#8A88A0; line-height:1.5;
                                border-top:1px solid #1E1E2E; padding-top:8px;">
                        {c["promotion_message"]}
                    </div>
                </div>
                """, unsafe_allow_html=True)

        with col_gtm:
            st.markdown('<div class="section-label" style="margin-top:1rem;">GTM action plan</div>',
                        unsafe_allow_html=True)

            for step in r["gtm_plan"]:
                st.markdown(f"""
                <div class="gtm-step">
                    <div class="gtm-step-num">{step["step"]}</div>
                    <div class="gtm-step-content">
                        <div class="gtm-step-channel">{step["channel"]}</div>
                        <div class="gtm-step-timing">⏱ {step["timing"]}</div>
                        <div class="gtm-step-msg">{step["message"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    # ── Tab 7: Agenda ─────────────────────────────────────────────────────────
    with tabs[6]:
        conflict = r["conflict_report"]
        if conflict["has_conflicts"]:
            st.markdown(f"""
            <div class="warn-box">⚠️ {len(conflict["conflicts"])} scheduling conflict(s) detected.
            {"Auto-resolved ✓" if conflict["resolved"] else "Manual review needed."}</div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(
                '<div class="info-box">✓ Agenda is fully conflict-free — no room collisions or speaker double-bookings.</div>',
                unsafe_allow_html=True
            )

        # Group by day
        sessions_by_day = {}
        for s in r["agenda"]:
            day = s["start_time"][:10]
            sessions_by_day.setdefault(day, []).append(s)

        for day_str, sessions in sorted(sessions_by_day.items()):
            day_label = datetime.strptime(day_str, "%Y-%m-%d").strftime("%A, %B %d %Y")
            st.markdown(f'<div class="agenda-day-header">{day_label}</div>', unsafe_allow_html=True)

            for s in sessions:
                start = datetime.fromisoformat(s["start_time"]).strftime("%H:%M")
                end   = datetime.fromisoformat(s["end_time"]).strftime("%H:%M")
                stype = s["session_type"]
                badge = session_type_badge(stype)

                st.markdown(f"""
                <div class="session-row">
                    <div class="session-time">{start}–{end}</div>
                    <div>
                        <div class="session-title">{s["title"]}</div>
                        <div class="session-speaker">
                            🎤 {s["speaker_name"]} &nbsp;·&nbsp; 📍 {s["room"]}
                        </div>
                    </div>
                    <div>{badge}</div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("""
    <div style="text-align:center; font-size:0.78rem; color:#3E3C5A;
            font-family:'DM Sans',sans-serif; padding-bottom:2rem;">
    Designed for planning smarter events
    </div>
    """, unsafe_allow_html=True)