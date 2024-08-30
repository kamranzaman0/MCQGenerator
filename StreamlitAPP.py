import os
import json
import traceback
import pandas as pd
from dotenv import load_dotenv

from io import BytesIO
from PyPDF2 import PdfWriter
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch


     
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

                            # Display DataFrame
                            st.table(df)
                            st.text_area(label="Review", value=response["review"])

                            # Generate PDF
                            buffer = BytesIO()
                            c = canvas.Canvas(buffer, pagesize=letter)
                            width, height = letter
                            margin = 1 * inch
                            y_position = height - margin
                            line_height = 14  # Adjust line height to fit more lines
                            max_width = width - 2 * margin

                            # Add main header to the PDF
                            c.setFont("Helvetica-Bold", 16)
                            c.drawCentredString(width / 2, y_position, f"MCQs List of {subject}")
                            y_position -= 30
                            c.setFont("Helvetica", 12)


                            def draw_text(text, x, y):
                                c.setFont("Helvetica", 12)
                                lines = []
                                words = text.split(' ')
                                line = ''
                                for word in words:
                                    test_line = f"{line} {word}".strip()
                                    text_width = c.stringWidth(test_line, "Helvetica", 12)
                                    if text_width < max_width:
                                        line = test_line
                                    else:
                                        lines.append(line)
                                        line = word
                                lines.append(line)
                                
                                for line in lines:
                                    if y < margin:
                                        c.showPage()
                                        c.setFont("Helvetica", 12)
                                        y = height - margin
                                    c.drawString(x, y, line)
                                    y -= line_height
                                return y

                            # Add content to the PDF
                            for index, row in df.iterrows():
                                question = row.get('MCQ', 'No Question')
                                choices = row.get('Choices', 'No Choices')
                                correct = row.get('Correct', 'No Correct Answer')

                                y_position = draw_text(f"Q{index}: {question}", margin, y_position)
                                y_position -= 10

                                choices_list = choices.split(' || ')
                                for opt in choices_list:
                                    y_position = draw_text(f"- {opt.strip()}", margin + 0.5 * inch, y_position)
                                    y_position -= 10

                                y_position = draw_text(f"Correct Answer: {correct}", margin + 0.5 * inch, y_position)
                                y_position -= 20

                            c.save()
                            buffer.seek(0)

                            # Store PDF buffer in session state
                            st.session_state.pdf_buffer = buffer.getvalue()
                            st.success("MCQs created successfully!")


                        else:
                            st.error("Error in the table data")
                    else: 
                        st.error("Quiz in not found")
                else:
                    st.write(response)   

#  Provide download button outside the form
if 'pdf_buffer' in st.session_state:
    st.download_button(
        label="Download PDF",
        data=st.session_state.pdf_buffer,
        file_name="MCQs.pdf",
        mime="application/pdf"
    )
    # Set a query parameter to trigger a page reload
    st.query_params["reload"] = "true"
    st.query_params.from_dict({"reload": "true"})




