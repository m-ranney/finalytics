import streamlit as st 
from pandasai.llm.openai import OpenAI
from dotenv import load_dotenv
import os
import pandas as pd
from pandasai import PandasAI

load_dotenv()

openai_api_key = os.getenv("OPENAI_API_KEY")

def chat_with_csv(df,prompt):
    try:
        llm = OpenAI(api_token=openai_api_key)
        pandas_ai = PandasAI(llm)
        
        # Construct the prompt with additional information
        full_prompt = f"You are a personal banking assistant. You have been provided with a banking statement for a middle class family of four with the following columns: Store Name, Date of purchase/expense, Amount of purchase/expense, Category of purchase/expense (ie. mortagage, utility bill, restaurant, etc.), Remaining balance of the bank account. The owner of the bank account is asking: {prompt}, please provide them with as accurate and concise information as possible."

        result = pandas_ai.run(df, full_prompt)
        print(result)
        return result
    except Exception as e:
        st.write(f"Exception occurred: {e}")
        return None

st.set_page_config(layout='wide')

st.title("Budget Buddy")

input_csv = st.file_uploader("Upload your CSV file", type=['csv'])

if input_csv is not None:

        col1, col2 = st.columns([1,1])

        with col1:
            st.info("CSV Uploaded Successfully")
            data = pd.read_csv(input_csv)
            st.dataframe(data, use_container_width=True)

        with col2:

            st.info("Chat Below")
            
            input_text = st.text_area("Enter your query")

            if input_text is not None:
                if st.button("Chat with CSV"):
                    st.info("Your Query: "+input_text)
                    result = chat_with_csv(data, input_text)
                    if result is not None:
                        st.success(result)
                    else:
                        st.error("There was a problem generating a response")
