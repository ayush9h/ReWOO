import asyncio

import streamlit as st
from langchain_core.messages import HumanMessage

from ag_workflows.nodes import app
from schemas.agent_schema import AgentState


async def run_agent(query: str):
    initial_state: AgentState = {
        "query": [HumanMessage(content=query)],
    }  # type: ignore

    result = await app.ainvoke(initial_state)
    return result


def main():
    st.set_page_config(page_title="ReWOO Agent", layout="wide")

    st.title("ReWOO Agent")

    query = st.text_input("Enter your query")

    if st.button("Run") and query:
        with st.spinner("Running agent..."):
            result = asyncio.run(run_agent(query))

        plan = result.get("plan")
        final_response = result.get("final_response", "")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Execution Steps")
            if plan and plan.steps:
                for step in sorted(plan.steps, key=lambda x: x.step_id):
                    with st.expander(f"Step {step.step_id}"):
                        st.write("Plan:", step.plan)
                        st.write("Tool:", step.evidence.tool_name)
                        st.write("Input:", step.evidence.tool_input)
                        st.write("Status:", step.status)
                        st.write("Output:", step.evidence.content)
            else:
                st.write("No steps available")

        with col2:
            st.subheader("Final Response")
            st.write(final_response)


if __name__ == "__main__":
    main()
