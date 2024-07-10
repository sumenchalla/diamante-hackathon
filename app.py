import streamlit as st
from support import retriever,model,tokenizer
import traceback
import torch


st.title("Diamante chatbot")



with st.form("user input"):
    question=st.text_input("Insert your question",max_chars=200)
    button=st.form_submit_button("Generate answer")

if button and question:
    with st.spinner("Loading...."):
        try:
            docs = retriever.invoke(question)
            content =""
            for i in docs:
                 content+=i.page_content
            content = content.replace("\n","").replace("\xa0","")
            input_text = f"""
            Based on the below data,
            answer this question {question}.
            and the data is {content}"""
            inputs = tokenizer(input_text, max_length=1024, return_tensors="pt", truncation=True)
                 
            # Get the input IDs and attention mask
            summary_ids = model.generate(inputs["input_ids"], max_length=150, min_length=40, num_beams=4, early_stopping=True)
            summary = tokenizer.decode(summary_ids[0], skip_special_tokens=True)



        except Exception as e:
                traceback.print_exception(type(e), e, e.__traceback__)
                st.error("Error")
        else:
             if summary is not None:
                   st.text_area(label="Answer", value=summary)



elif button and not question:
     st.write("Please enter the question and then submit")