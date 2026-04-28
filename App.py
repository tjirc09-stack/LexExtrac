import streamlit as st
from openai import OpenAI

# Page configuration for a professional look
st.set_page_config(page_title="LexExtract AI", layout="wide", page_icon="⚖️")
st.title("⚖️ LexExtract: Smart Legal Assistant")

# Sidebar for configuration
api_key = st.sidebar.text_input("OpenAI API Key", type="password", help="Enter your API key to enable analysis.")

if api_key:
    client = OpenAI(api_key=api_key)
    
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Document Input")
        action = st.radio("Select Action:", ["Full Legal Analysis", "Executive Summary Only"])
        input_text = st.text_area("Paste your contract or legal document here:", height=450, placeholder="Enter text...")

    if st.button("Analyze Document"):
        if input_text:
            # Specialized prompt for the English legal niche
            legal_prompt = (
                f"Act as an expert attorney. Analyze the following legal text and extract: "
                f"1. A concise executive summary. "
                f"2. All key dates, deadlines, and milestones. "
                f"3. All parties involved (individuals and entities). "
                f"4. Penalty clauses, liabilities, or detected legal risks. "
                f"\n\nDocument Text: {input_text}"
            )
            
            with st.spinner("Analyzing legal structure..."):
                try:
                    response = client.chat.completions.create(
                        model="gpt-4", # GPT-4 is highly recommended for legal accuracy
                        messages=[
                            {"role": "system", "content": "You are a specialized assistant for contract law and legal auditing."},
                            {"role": "user", "content": legal_prompt}
                        ]
                    )
                    
                    result = response.choices[0].message.content

                    with col2:
                        st.subheader("Risk Analysis & Key Data")
                        st.markdown(result)
                        
                except Exception as e:
                    st.error(f"An error occurred: {e}")
        else:
            st.error("Please paste a text to analyze.")
else:
    st.info("Please enter your OpenAI API Key in the sidebar to begin.")
