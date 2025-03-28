import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import google.generativeai as genai

# Initialize Gemini API Key
genai.configure(api_key="AIzaSyA1GyCtWcJGfYGGoR-E2DvdWeXRsKskisE")  # Directly include the API key

# Function to query Google Gemini API
def query_gemini(prompt):
    try:
        model = genai.GenerativeModel("gemini-2.0-flash")
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"

# Streamlit Page Configuration
st.set_page_config(page_title="AI Financial Story Analyzer", layout="wide")

# Title and Description
st.title("📊 AI-Powered Financial Statement Analyzer")
st.markdown("Gain meaningful insights from financial data with AI-powered analysis and interactive visualizations.")

# File Upload Section
st.subheader("📂 Upload a Financial Statement (CSV/XLSX)")
uploaded_file = st.file_uploader("Upload a file", type=["csv", "xlsx"], help="Supports CSV and Excel formats")

if uploaded_file:
    try:
        # Read the uploaded file
        df = pd.read_excel(uploaded_file) if uploaded_file.name.endswith('.xlsx') else pd.read_csv(uploaded_file)
        st.success("✅ File uploaded successfully!")

        # Display Data Preview
        with st.expander("🔍 Preview Financial Data"):
            st.dataframe(df.head())
        
        # AI Analysis
        st.subheader("📢 AI-Generated Financial Insights")
        with st.spinner("Analyzing financial data..."):
            prompt = f"""Given a financial dataset, generate the following:

1. A technical analysis summarizing key financial indicators and trends.

2. A simplified, narrative-style explanation that translates financial jargon into a compelling story, comparing the company’s actual performance with its public messaging.

3. A final conclusion and recommendation, highlighting whether the financial data aligns with the company's projected image and what this means for stakeholders.

4. Ensure the explanation is clear, engaging, and avoids unnecessary technical complexity while retaining accuracy.

The dataset is as follows:
{df.to_csv(index=False)}
"""
            ai_response = query_gemini(prompt)
            st.markdown(f"📊 AI Insights:** {ai_response}")
        
        # Data Visualization
        if 'Total Revenue' in df.columns and 'Gross Profit' in df.columns:
            revenue = df['Total Revenue']
            profit = df['Gross Profit']
            
            st.markdown("### 📈 Revenue vs Profit")
            fig, ax = plt.subplots()
            ax.plot(revenue, label="Revenue", marker='o', color="blue")
            ax.plot(profit, label="Profit", marker='o', color="green")
            ax.set_title("Revenue vs Profit")
            ax.set_xlabel("Time Period")
            ax.set_ylabel("Amount")
            ax.legend()
            st.pyplot(fig)
        else:
            st.warning("⚠ The dataset does not contain 'Total Revenue' or 'Gross Profit' columns.")

    except Exception as e:
        st.error(f"❌ Error processing file: {e}")
        st.stop()

# Interactive Q&A Section
st.subheader("💡 Ask the AI a Financial Question")
question = st.text_input("Enter a financial query...", help="Example: 'What are the key financial trends in this data?'")

if st.button("Analyze"):
    if question:
        with st.spinner("Generating response..."):
            prompt2 = f"Provide an easy-to-understand response for the following question based on financial data:\n{question}"
            ai_response2 = query_gemini(prompt2)
        st.success("✅ Response Generated Successfully!")
        st.markdown(f"📢 Response: \n{ai_response2}")
    else:
        st.warning("⚠ Please enter a question before submitting.")