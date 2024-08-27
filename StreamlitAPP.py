import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv

import streamlit as st
from langchain.callbacks import get_openai_callback

from src.mcqgenerator.utils import read_file, get_table_data
from src.mcqgenerator.MCQGenerator import generate_evaluate_chain
from src.mcqgenerator.logger import logging

with open('C:\\Users\\USER\\Generative AI Course\\Projects\MCQGenerator\\Response.json', 'r') as file:
    RESPONSE_JSON = json.load(file)


#creating the title of the app
st.title("MCQs Creator Application with Langchain")

#creating the form using st.form
with st.form("user_input"):
    #File upload
    upload_file = st.file_uploader("Upload a pdf or txt file")

    #input fields
    mcq_count = st.number_input("NO of MCQs", min_value=3, max_value = 50)

    #Subject
    subject = st.text_input("Insert Subject", max_chars=20)

    #Quiz Tone
    tone = st.text_input("Complexity Levels of Questions", max_chars=20, placeholder="Simple")

    #Add Button
    button = st.form_submit_button("Create MCQs")

    if button and upload_file is not None and mcq_count and subject and tone:
        with st.spinner("loading......"):
            try:
                text = read_file(upload_file)
                with get_openai_callback() as cb:
                    response = generate_evaluate_chain(
                        {
                            "text" : text,
                            "number" : mcq_count,
                            "subject" : subject, 
                            "tone" : tone, 
                            "response_json" : json.dumps(RESPONSE_JSON)
                        }
                    )
            except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
            else:
                print(f"Total Tokans: {cb.total_tokens}")
                print(f"Prompt Tokans: {cb.prompt_tokens}")
                print(f"Completion Tokans: {cb.completion_tokens}")
                print(f"Total Cost: {cb.total_cost}")
                if isinstance(response, dict):
                    quiz = response.get("quiz", None)
                    if quiz is not None:
                        table_data = get_table_data(quiz)
                        if table_data is not None:
                            df = pd.DataFrame(table_data)
                            df.index = df.index+1
                            st.table(df)

                            st.text_area(label="Review", value=response["review"])
                        else:
                            st.error("Error in the table data")
                    else: 
                        st.error("Quiz in not found")
                else:
                    st.write(response)   

