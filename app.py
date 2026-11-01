import os
import streamlit as st
import google.generativeai as genai

# 1. Title & Header
st.title("Unicorn AI Tutor")
st.write("Welcome! Ask your question below:")

# 2. Configure Gemini API Key securely from Streamlit Secrets
api_key = st.secrets.get("GEMINI_API_KEY") or os.environ.get("GEMINI_API_KEY")

if not api_key:
    st.error("Missing Gemini API Key! Please set GEMINI_API_KEY in your Streamlit Secrets.")
else:
    genai.configure(api_key=api_key)

    # 3. Initialize the Model (PUT IT HERE)
    model = genai.GenerativeModel('gemini-1.5-flash')
    # Alternatively, you can use:
    # model = genai.GenerativeModel('gemini-1.5-pro')

    # 4. User Input Interface
    user_query = st.text_input("Enter your question for the AI Tutor:")

    # 5. Handle the "Ask AI Tutor" Button Click
    if st.button("Ask AI Tutor"):
        if user_query:
            try:
                with st.spinner("AI Tutor is thinking..."):
                    response = model.generate_content(user_query)
                    st.success("Response:")
                    st.write(response.text)
            except Exception as e:
                st.error(f"Error generating response: {str(e)}")
        else:
            st.warning("Please type a question before clicking the button.")
