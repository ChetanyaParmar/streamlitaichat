import streamlit as st
import google.generativeai as genai
import datetime
import os

# Configure Gemini API
def configure_gemini():
    if 'GOOGLE_API_KEY' not in st.session_state:
        st.session_state['GOOGLE_API_KEY'] = "YOUR_API_KEY"
    
    genai.configure(api_key=st.session_state['GOOGLE_API_KEY'])
    return genai.GenerativeModel('gemini-1.0-pro')

# Fitness context prompt
FITNESS_CONTEXT = """
You are a professional fitness assistant. Provide helpful and accurate responses to fitness-related queries.
Keep responses concise and professional. Offer actionable advice, but remind users to consult fitness professionals
for personalized plans.

You can help with:
1. General fitness advice
2. Workout suggestions
3. Diet tips
4. Information about fitness trends and equipment

Do not:
1. Provide medical advice
2. Create detailed fitness plans for specific medical conditions
3. Suggest extreme diets or unverified fitness methods
4. Diagnose any conditions
"""

def get_gemini_response(model, user_input):
    try:
        response = model.generate_content(
            f"{FITNESS_CONTEXT}\n\nUser: {user_input}\nAssistant:"
        )
        return response.text
    except Exception as e:
        return f"I apologize, but I encountered an error. Please try again or contact support. Error: {str(e)}"

def main():
    st.set_page_config(
        page_title="AI Fitness Assistant",
        page_icon="🏃",
        layout="centered"
    )

    # Header
    st.markdown("""
        <div style='text-align: center;'>
            <h1>🏃 AI Fitness Assistant</h1>
            <p>Powered by Google Gemini</p>
        </div>
    """, unsafe_allow_html=True)

    # API Key Input in Sidebar
    with st.sidebar:
        st.markdown("### Configuration")
        api_key = st.text_input("Enter Gemini API Key", type="password")
        if api_key:
            st.session_state['GOOGLE_API_KEY'] = api_key
            
        st.markdown("### Quick Links")
        st.markdown("- [Popular Workouts]()")
        st.markdown("- [Dietary Guidelines]()")
        st.markdown("- [Consult a Trainer]()")
        
        st.markdown("### Fitness Center Hours")
        st.markdown("Monday-Friday: 6:00 AM - 10:00 PM")
        st.markdown("Saturday-Sunday: 7:00 AM - 8:00 PM")
        
        st.markdown(f"Current Time: {datetime.datetime.now().strftime('%I:%M %p')}")

    # Initialize session state for messages
    if 'messages' not in st.session_state:
        st.session_state.messages = []

    # Display chat messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Initial greeting
    if not st.session_state.messages:
        with st.chat_message("assistant"):
            welcome_msg = """
                👋 Welcome! I'm your AI fitness assistant powered by Google Gemini.
                I can help you with general fitness advice and queries.
                How can I assist you today?
            """
            st.markdown(welcome_msg)
            st.session_state.messages.append({
                "role": "assistant",
                "content": welcome_msg
            })

    # Chat input
    if prompt := st.chat_input("Type your fitness query here..."):
        if not st.session_state['GOOGLE_API_KEY']:
            st.error("Please enter your Gemini API key in the sidebar first.")
            return

        # Display user message
        with st.chat_message("user"):
            st.markdown(prompt)
        st.session_state.messages.append({"role": "user", "content": prompt})

        # Get Gemini response
        try:
            model = configure_gemini()
            response = get_gemini_response(model, prompt)
            
            # Display assistant response
            with st.chat_message("assistant"):
                st.markdown(response)
            st.session_state.messages.append({"role": "assistant", "content": response})
            
        except Exception as e:
            st.error(f"Error: {str(e)}")

    # Footer
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #666;'>
            <small>This is an AI assistant for general fitness information only. 
            For personalized fitness plans or medical advice, consult a professional.</small>
        </div>
        """, 
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()
