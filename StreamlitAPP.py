import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv
from src.mcqgenerator.utils import read_file, get_table_data
import streamlit as st 
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

#load_dotenv()
# Loading json file from local
with open(r"C:\Users\mayur\MCQGen\response.json", "r") as f:
    RESPONSE_JSON = json.load(f)

# Creating titel for app
st.title = ("MCQ creator application with LangChain")

# creating a form using stramlit
with st.form("user_inputs"):
    # File Upload
    uploaded_file = st.file_uploader("Upload a pdf or text file")

    # Input field
    mcq_count = st.number_input("No. of MCQ's: ", min_value=3, max_value=50)

    # subject field
    subject = st.text_input("Insert Subject: ", max_chars=30)

    # Quiz Tone
    tone = st.text_input("Complexity level of questions: ", max_chars=30, placeholder = "Simple")

    # Add Button
    button = st.form_submit_button("Create MCQ's")


# Checked if button is clicked and all inputs are filled
    if button and uploaded_file is not None and mcq_count and subject and tone:
        with st.spinner("loading..."):
            try:
                text = read_file(uploaded_file)
                response = generate_evaluate_chain(
               {"text": text,
                "number": mcq_count,
                "subject": subject,
                "tone": tone,
                "response_json": json.dumps(RESPONSE_JSON)
               }
                )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
        
            else:
                if isinstance(response,dict):
                    quiz = response.get("quiz", None)

                    if quiz is not None:
                        table_data = get_table_data(quiz)

                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index + 1
                            st.table(df)
                            st.text_area("Review", value = response["review"])
                        else:
                            st.error("Error in the table data")
                
                else:
                    st.write(response)




