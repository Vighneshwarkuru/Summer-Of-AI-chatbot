# interface.py
import streamlit as st
from streamlit_chat import message
from datetime import datetime
import pandas as pd
import logging

# Import RAG system
from main import rag_system

# Streamlit configuration
st.set_page_config(page_title="Internship Assistant", layout="wide")

# Logging
logging.basicConfig(filename='interface.log', level=logging.INFO)

# Session state init
def init_state():
    for key in ["generated", "past", "leave_submitted", "messages"]:
        if key not in st.session_state:
            st.session_state[key] = [] if key != "leave_submitted" else False
init_state()

# Sections
def emergency_section():
    with st.expander("🚨 Emergency Contacts"):
        st.markdown("""
        - *Security*: 911
        - *Manager*: (555) 123-4567
        - *Mental Health*: (555) 987-6543
        """)
        if st.button("📞 Call Emergency"):
            st.warning("Would initiate a call (simulated)")

def leave_application_section():
    st.subheader("Leave Application")
    if st.session_state['leave_submitted']:
        st.success("Leave application submitted!")
        if st.button("Submit another"):
            st.session_state['leave_submitted'] = False
            st.rerun()
        return

    with st.form("leave_form"):
        col1, col2 = st.columns(2)
        with col1:
            intern_id = st.text_input("Intern ID")
            leave_type = st.selectbox("Type", ["Medical", "Personal", "Academic", "Other"])
        with col2:
            start = st.date_input("Start Date", min_value=datetime.today())
            end = st.date_input("End Date", min_value=datetime.today())
        reason = st.text_area("Reason")
        st.file_uploader("Docs (optional)", type=["pdf", "png", "jpg", "docx"])
        submit = st.form_submit_button("Submit", type="primary")

        if submit:
            if not intern_id or not leave_type or not reason:
                st.error("All fields required")
            elif end < start:
                st.error("End must be after start")
            else:
                st.session_state['leave_submitted'] = True
                logging.info(f"Leave submitted by {intern_id}")

def chat_interface():
    st.subheader("Chat Assistant")
    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("Ask your question")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.session_state['past'].append(user_input)
        try:
            answer = rag_system.query(user_input)
        except Exception as e:
            answer = "Error processing your request."
            logging.error(f"Chat error: {e}")
        st.session_state['generated'].append(answer)

    for i in range(len(st.session_state['generated'])):
        message(st.session_state['past'][i], is_user=True, key=f"user_{i}")
        message(st.session_state['generated'][i], key=f"bot_{i}")

def internship_info():
    st.subheader("Program Info")
    try:
        response = rag_system.query("What is the internship structure?")
        st.markdown(response)
    except Exception as e:
        st.error("Could not load program info.")

def faq_section():
    st.subheader("FAQs")
    faqs = [
        "What is the duration?",
        "Can I work remotely?",
        "Is it paid?",
        "How do I apply for leave?"
    ]
    for q in faqs:
        with st.expander(q):
            st.write(rag_system.query(q))

def main():
    with st.sidebar:
        st.title("Internship Portal")
        option = st.radio("Navigate", ["Chat", "Leave", "Info", "FAQ"])
        emergency_section()

    if option == "Chat":
        chat_interface()
    elif option == "Leave":
        leave_application_section()
    elif option == "Info":
        internship_info()
    elif option == "FAQ":
        faq_section()

if _name_ == "_main_":
    main()
