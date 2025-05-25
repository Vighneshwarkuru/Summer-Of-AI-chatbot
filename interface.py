import streamlit as st
from streamlit_chat import message
import requests
from datetime import datetime, timedelta
import json
from PIL import Image
import pandas as pd

# App configuration
st.set_page_config(
    page_title="Open-Source Internship Assistant",
    page_icon="👩‍💻",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Load assets (replace with your actual assets)
def load_assets():
    try:
        logo = Image.open("assets/logo.png")
        emergency_icon = Image.open("assets/emergency.png")
        return logo, emergency_icon
    except:
        return None, None

logo, emergency_icon = load_assets()

# Initialize session state
if 'generated' not in st.session_state:
    st.session_state['generated'] = []
if 'past' not in st.session_state:
    st.session_state['past'] = []
if 'messages' not in st.session_state:
    st.session_state['messages'] = [
        {"role": "system", "content": "You are a helpful assistant for open-source contribution interns."}
    ]
if 'leave_submitted' not in st.session_state:
    st.session_state['leave_submitted'] = False

# RAG backend integration (mock function)
def rag_query(query, context=None):
    # In a real implementation, this would connect to your RAG backend
    mock_responses = {
        "duration": "The internship program runs for 12 weeks.",
        "curriculum": "Weeks 1-2: Onboarding, Weeks 3-6: Core contributions, Weeks 7-10: Advanced projects, Weeks 11-12: Wrap-up and evaluation.",
        "requirements": "Completion requires: 80% task completion, 4 merged PRs, final presentation, and mentor evaluation.",
        "emergency": "For emergencies, contact: Campus Security: 911, Program Manager: (555) 123-4567, Mental Health Support: (555) 987-6543"
    }
    
    query_lower = query.lower()
    for key in mock_responses:
        if key in query_lower:
            return mock_responses[key]
    return "I'm sorry, I don't have information on that. Please contact the program administrator for assistance."

# UI Components
def emergency_section():
    with st.expander("🚨 Emergency Contacts", expanded=False):
        st.markdown("""
        ### Immediate Assistance
        - **Campus Security**: 911
        - **Program Manager**: (555) 123-4567
        - **Mental Health Support**: (555) 987-6543
        
        *Available 24/7*
        """)
        
        if st.button("📞 Connect to Emergency Helpline Now", 
                    help="Click to initiate emergency call",
                    type="primary",
                    use_container_width=True):
            st.warning("In a real implementation, this would initiate a phone call")
            # JavaScript injection for actual calling functionality
            # components.html("""<script>window.location.href='tel:911';</script>""")

def leave_application_section():
    st.subheader("Leave Application")
    
    if st.session_state['leave_submitted']:
        st.success("Your leave application has been submitted successfully!")
        if st.button("Submit another request"):
            st.session_state['leave_submitted'] = False
        return
    
    with st.form("leave_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            intern_id = st.text_input("Intern ID*", placeholder="OSI-2023-XXX")
            leave_type = st.selectbox("Leave Type*", 
                                     ["", "Medical", "Personal", "Academic", "Other"])
        
        with col2:
            start_date = st.date_input("Start Date*", min_value=datetime.today())
            end_date = st.date_input("End Date*", min_value=datetime.today())
        
        reason = st.text_area("Reason for Leave*", 
                             placeholder="Please provide details about your leave request",
                             height=100)
        
        docs = st.file_uploader("Supporting Documents (if any)", 
                               type=['pdf', 'docx', 'png', 'jpg'],
                               accept_multiple_files=True)
        
        submitted = st.form_submit_button("Submit Application", type="primary")
        
        if submitted:
            if not all([intern_id, leave_type, start_date, end_date, reason]):
                st.error("Please fill all required fields (*)")
            elif end_date < start_date:
                st.error("End date must be after start date")
            else:
                # In a real implementation, this would submit to a backend
                st.session_state['leave_submitted'] = True
                st.rerun()

def internship_info_section():
    st.subheader("Internship Program Information")
    
    tab1, tab2, tab3 = st.tabs(["Program Overview", "Curriculum Timeline", "Completion Requirements"])
    
    with tab1:
        st.markdown("""
        ### 12-Week Open-Source Contribution Program
        
        - **Duration**: 12 weeks full-time
        - **Format**: Hybrid (remote + optional in-person)
        - **Stipend**: $1000/month
        - **Mentorship**: Weekly 1:1 sessions
        """)
        
        st.image("https://via.placeholder.com/800x300?text=Program+Overview", 
                caption="Program Structure Overview")
    
    with tab2:
        weeks = []
        for i in range(1, 13):
            if i <= 2:
                phase = "Onboarding"
            elif i <= 6:
                phase = "Core Contributions"
            elif i <= 10:
                phase = "Advanced Projects"
            else:
                phase = "Wrap-up"
            weeks.append({
                "Week": i,
                "Phase": phase,
                "Milestones": "Orientation" if i == 1 else 
                            "First PR" if i == 3 else 
                            "Midpoint Review" if i == 6 else 
                            "Final Presentation" if i == 12 else "-"
            })
        
        st.dataframe(pd.DataFrame(weeks), hide_index=True, use_container_width=True)
        
        st.progress(0.25, text="Example progress at Week 3")
    
    with tab3:
        st.markdown("""
        ### Completion Requirements
        
        ✅ **Code Contributions**
        - Minimum 4 merged pull requests
        - At least 2 significant feature implementations
        
        ✅ **Documentation**
        - Contribute to project documentation
        - Create at least 1 tutorial/guide
        
        ✅ **Community Engagement**
        - Participate in weekly standups
        - Help other interns with 2+ issues
        
        ✅ **Final Evaluation**
        - Present your work to the community
        - Receive positive mentor evaluation
        """)

def faq_section():
    st.subheader("Frequently Asked Questions")
    
    categories = {
        "General": [
            "What are the program hours?",
            "Is the internship paid?",
            "Can I work remotely?"
        ],
        "Technical": [
            "What tech stack will I use?",
            "How are projects assigned?",
            "What if I get stuck on a problem?"
        ],
        "Logistics": [
            "How do I request time off?",
            "What's the dress code?",
            "Where do I report issues with my stipend?"
        ]
    }
    
    selected_category = st.selectbox("Browse by category", list(categories.keys()))
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        search_query = st.text_input("Search FAQs", placeholder="Type your question...")
    
    with col2:
        st.write("")
        st.write("")
        if st.button("🔍 Search", use_container_width=True):
            pass  # Search functionality would be implemented here
    
    st.divider()
    
    # Display FAQs
    for question in categories[selected_category]:
        with st.expander(question):
            # In a real implementation, this would pull from your knowledge base
            st.write(rag_query(question))
            st.write("")
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button(f"👍 Helpful", key=f"helpful_{question}", use_container_width=True):
                    st.toast("Thanks for your feedback!")
            with col2:
                if st.button(f"👎 Not Helpful", key=f"nothelpful_{question}", use_container_width=True):
                    st.toast("We'll improve this answer. Thanks!")

# Chat interface
def chat_interface():
    st.subheader("Internship Assistant Chat")
    
    # Chat history
    reply_container = st.container()
    input_container = st.container()
    
    with input_container:
        with st.form(key='chat_form', clear_on_submit=True):
            user_input = st.text_input("Ask your question:", key='input', placeholder="Type your message here...")
            submit_button = st.form_submit_button(label='Send')
    
    if submit_button and user_input:
        # Add user message to chat history
        st.session_state['past'].append(user_input)
        
        # Get RAG response
        response = rag_query(user_input)
        
        # Add assistant response to chat history
        st.session_state['generated'].append(response)
    
    # Display chat history
    if st.session_state['generated']:
        with reply_container:
            for i in range(len(st.session_state['generated'])):
                message(st.session_state['past'][i], is_user=True, key=f"{i}_user")
                message(st.session_state['generated'][i], key=str(i))

# Main app layout
def main():
    # Sidebar
    with st.sidebar:
        if logo:
            st.image(logo, use_column_width=True)
        else:
            st.title("Open-Source Internship")
        
        st.markdown("""
        ### Navigation
        """)
        
        app_mode = st.radio(
            "Go to",
            ["Chat Assistant", "Leave Application", "Program Info", "FAQs"],
            index=0
        )
        
        emergency_section()
        
        st.markdown("---")
        st.markdown("""
        ### Quick Links
        - [Code of Conduct](#)
        - [Mentor Directory](#)
        - [Project Repositories](#)
        - [Community Forum](#)
        """)
        
        st.markdown("""
        ---
        *v1.0.0 | [Report Issue](#)*
        """)
    
    # Main content
    if app_mode == "Chat Assistant":
        chat_interface()
    elif app_mode == "Leave Application":
        leave_application_section()
    elif app_mode == "Program Info":
        internship_info_section()
    elif app_mode == "FAQs":
        faq_section()

if __name__ == "__main__":
    main()