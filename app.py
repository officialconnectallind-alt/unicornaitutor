import streamlit as st
import google.generativeai as genai
import os

# --- PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Startup-to-Unicorn AI Tutor",
    page_icon="🦄",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SECRETS & API SETUP ---
# Streamlit secrets manage API keys securely
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input("Enter Google Gemini API Key:", type="password")

if api_key:
    genai.configure(api_key=api_key)
    # Using gemini-2.5-flash (active model)
   model = genai.GenerativeModel('gemini-3.8-flash')
else:
    st.warning(".")

# --- SIDEBAR: CURRICULUM NAVIGATION ---
st.sidebar.title("🦄 Unicorn Blueprint")
st.sidebar.markdown("**Day-by-Day Masterclass**")

phase = st.sidebar.radio(
    "Select Program Phase:",
    [
        "Phase 1: Ideation & Validation (Days 1–30)",
        "Phase 2: MVP & Product-Market Fit (Days 31–90)",
        "Phase 3: Growth & Venture Funding (Days 91–180)",
        "Phase 4: Scaling & Global Dominance (Days 181–365)"
    ]
)

st.sidebar.divider()
st.sidebar.markdown("### 📚 Free Resource Library")
st.sidebar.markdown("- [Y Combinator Startup Library](https://www.ycombinator.com/library)")
st.sidebar.markdown("- [Stripe Atlas Legal Guides](https://stripe.com/atlas)")
st.sidebar.markdown("- [YC Standard SAFE Agreements](https://www.ycombinator.com/documents)")

# --- MAIN CONTENT AREA ---
st.title("🦄 Startup-to-Unicorn AI Tutor")
st.caption("All business knowledge, tycoon principles, market strategy, and legal processes—day by day.")

st.subheader(f"Current Focus: {phase}")

# Phase Overview & Daily Schedule Tabs
tab1, tab2, tab3 = st.tabs(["💬 Ask AI Tutor", "📅 Daily Action Roadmap", "📄 Templates & Legal"])

with tab1:
    st.markdown("#### Converse with your Personal Unicorn Coach")
    st.info("Ask anything regarding business models, SAFEs, unit economics ($CAC$/$LTV$), user interviews, or pitching.")
    
    # Session state to retain chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [
            {"role": "assistant", "content": f"Welcome founder! We are currently looking at **{phase}**. What specific challenge or lesson do you want to tackle today?"}
        ]

    for msg in st.session_state.messages:
        st.chat_message(msg["role"]).write(msg["content"])

    if user_prompt := st.chat_input("Ask your AI Tutor a question..."):
        st.session_state.messages.append({"role": "user", "content": user_prompt})
        st.chat_message("user").write(user_prompt)

        if api_key:
            with st.spinner("AI Tutor is analyzing venture frameworks..."):
                system_instruction = (
                    f"You are a world-class Startup & Unicorn Coach (ex-Y Combinator Partner & Venture Investor). "
                    f"The founder is currently in {phase}. Answer their question with highly tactical, first-principles business advice, "
                    f" citing real frameworks, books, or legal steps where appropriate."
                )
                full_prompt = f"{system_instruction}\n\nFounder Question: {user_prompt}"
                response = model.generate_content(full_prompt)
                
                st.session_state.messages.append({"role": "assistant", "content": response.text})
                st.chat_message("assistant").write(response.text)
        else:
            st.error("Please add your Gemini API key to get an answer.")

with tab2:
    st.markdown("#### Day-by-Day Execution Plan")
    if "Phase 1" in phase:
        st.markdown("""
        * **Day 1:** Problem Identification & First-Principles Deconstruction.
        * **Day 2:** Conducting 10 'Mom Test' style non-leading customer interviews.
        * **Day 3:** Filling out the 1-Page Lean Canvas.
        * **Day 4:** Competitor research using Crunchbase, Similarweb, and G2.
        * **Day 5:** Drafting your PRFAQ (Amazon method press release).
        """)
    elif "Phase 2" in phase:
        st.markdown("""
        * **Day 31:** Scoping the absolute minimum feature set for MVP.
        * **Day 45:** Setting up product analytics (Mixpanel / Amplitude tracking).
        * **Day 60:** Running the 40% Sean Ellis Product-Market Fit survey.
        """)
    else:
        st.markdown("Select a phase to view detailed daily tasks.")

with tab3:
    st.markdown("#### Downloadable Templates & Documents")
    st.download_button(
        label="📄 Download YC Standard SAFE Template (Pre-Money)",
        data="Y Combinator SAFE Agreement Standard Content...",
        file_name="YC_SAFE_Agreement.txt",
        mime="text/plain"
    )
