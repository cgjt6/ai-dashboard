
# AI Assistant Dashboard (Streamlit Prototype)
# Agents: Steve (Job Search) and Wendy (CV & Cover Letter)

import streamlit as st
import openai
import os
import json

# --- Set up API Key ---
openai.api_key = st.secrets["OPENAI_API_KEY"]

# --- Load or Initialize Job Database ---
if "jobs" not in st.session_state:
    st.session_state.jobs = []

# --- Sidebar: Agent Selector ---
agent = st.sidebar.selectbox("Talk to:", ["Steve (Job Search)", "Wendy (CV & Cover Letter)"])

st.title("🧠 John's AI Assistant Dashboard")
st.markdown("Talk to your AI agents, review job leads, and get application drafts.")

# --- Steve: Job Finder ---
if agent.startswith("Steve"):
    st.header("📌 Jobs Steve Has Found")
    if st.button("Add Trojan Technologies Job"):
        job = {
            "title": "Research Scientist, UV AOP",
            "company": "Trojan Technologies",
            "location": "London, ON",
            "source": "Trabajo.org",
            "description": "Perform chemical and photochemical experiments for advanced oxidation processes...",
            "link": "https://www.trabajo.org/job/"
        }
        st.session_state.jobs.append(job)

    if st.session_state.jobs:
        for i, job in enumerate(st.session_state.jobs):
            with st.expander(f"{job['title']} at {job['company']}"):
                st.write(f"Location: {job['location']}")
                st.write(f"Source: {job['source']}")
                st.write(job['description'])
                st.markdown(f"[Apply Here]({job['link']})")
    else:
        st.info("No jobs yet. Click the button above to add an example.")

# --- Wendy: CV and Cover Letter Assistant ---
elif agent.startswith("Wendy"):
    st.header("📝 CV and Cover Letter Drafts")

    uploaded_cv = st.file_uploader("Upload your CV (DOCX or TXT)", type=["docx", "txt"])
    selected_job = st.selectbox("Select a job to tailor your application:", [j["title"] for j in st.session_state.jobs] if st.session_state.jobs else [])

    if uploaded_cv and selected_job:
        job = next(j for j in st.session_state.jobs if j["title"] == selected_job)
        job_desc = job["description"]
        cv_text = uploaded_cv.read().decode("utf-8") if uploaded_cv.type == "text/plain" else "Uploaded CV content here."

        prompt = f"You are Wendy, a job application assistant. Here is my CV:\n{cv_text}\n\nAnd here is the job description:\n{job_desc}\n\nWrite a tailored cover letter for me and suggest CV edits."

        if st.button("Generate Application Draft"):
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are Wendy, an expert job application writer."},
                    {"role": "user", "content": prompt}
                ]
            )
            result = response.choices[0].message.content
            st.markdown("---")
            st.subheader("Draft Output")
            st.write(result)
    else:
        st.info("Please upload your CV and select a job.")
