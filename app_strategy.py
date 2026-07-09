import streamlit as st
from schemas import GraphState
from engine import analyst_node, auditor_node, judge_node, run_credit_shield

st.set_page_config(page_title="Credit Shield Orchestrator", layout="wide")
st.title("Credit Shield — Multi-Agent Orchestrator")

with st.sidebar:
    st.header("Controls")
    user_query = st.text_area("User query", value="Analizza il rischio di Amaris per l'anno 2026", height=120)
    run_btn = st.button("Run Workflow")
    max_retries = st.slider("Max Reflexion Retries", 0, 3, 2)

# Containers for agents
col1, col2, col3 = st.columns(3)
agent1_box = col1.container()
agent2_box = col2.container()
agent3_box = col3.container()

output_box = st.expander("Final State & Report", expanded=True)

def render_agent_box(container, title, content_lines):
    container.markdown(f"**{title}**")
    for line in content_lines:
        container.write(line)

if run_btn:
    state = GraphState(query=user_query)

    # Visual progress bar across nodes
    progress = st.progress(0)
    attempt = 0
    while not state.judge_approved and attempt <= max_retries:
        # Analyst
        agent1_box.markdown("---")
        agent1_box.write(f"Run: {attempt+1}")
        agent1_box.info("Analyst Agent: running semantic retrieval...")
        state = analyst_node(state)
        progress.progress(10)
        render_agent_box(agent1_box, "Analyst Output", [f"PII violation: {state.analyst_output.has_pii_violation}", f"Parent Doc ID: {state.analyst_output.parent_document_id}", f"Snippets: {state.analyst_output.detected_clausole_rischio}"])

        # Auditor
        agent2_box.markdown("---")
        agent2_box.info("Auditor Agent: fetching financial metrics...")
        state = auditor_node(state)
        progress.progress(55)
        render_agent_box(agent2_box, "Auditor Output", [f"Company: {state.auditor_output.company_name}", f"Revenue: {state.auditor_output.mrr_or_revenue}", f"Compliance: {state.auditor_output.compliance_score}"])

        # Judge
        agent3_box.markdown("---")
        agent3_box.info("Judge Agent: running quality & safety checks...")
        state = judge_node(state)
        progress.progress(90)

        # Visual judge outcome
        if state.judge_approved:
            agent3_box.success(f"Judge Result: APPROVED (attempt {state.retry_count})")
        else:
            agent3_box.error(f"Judge Result: REJECTED (attempt {attempt})")
            st.warning(f"Judge rejected output. Performing reflexion sanitization (attempt {attempt+1}).")

        render_agent_box(agent3_box, "Judge Result", [f"Approved: {state.judge_approved}", f"Retry Count: {state.retry_count}"])

        if not state.judge_approved:
            attempt += 1
            state.retry_count = attempt
            # simple reflexion sanitation as in engine
            state.query = state.query.lower().replace("mario rossi", "[REDACTED_USER]")
        else:
            break

    with output_box:
        st.subheader("GraphState")
        st.json(state.model_dump())
        if state.judge_approved:
            st.success("Workflow approved — final report below")
            st.code(state.final_report)
        else:
            st.error("Workflow blocked by Judge after reflexion attempts")

    st.balloons()

else:
    st.info("Fill the query in the sidebar and press 'Run Workflow' to start the multi-agent flow.")
