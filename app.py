import streamlit as st
import os
import shutil
import dotenv

from src.helper import llm_pipeline

dotenv.load_dotenv()

# Set up OpenAI model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

st.set_page_config(layout="wide", page_title="GenAI-Doc2QA")

def run_temp_dir():
    temp_dir = "temp_files"
    if os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)
        os.makedirs("temp_files")
    else:
        os.makedirs("temp_files")

def check_if_pdf(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        st.write("PDF file uploaded successfully")
    else:
        st.write("Uploaded file is not a PDF. Please choose a PDF file.")

def main():
    uploaded_file = st.file_uploader("Choose a file", type=["pdf"])

    if uploaded_file is not None:
        #create a temporary dir
        run_temp_dir()

        # Save the uploaded file temporarily
        with open(os.path.join("temp_files", uploaded_file.name), "wb") as f:
            f.write(uploaded_file.getbuffer())
        # Get the file path
        file_path = os.path.join("temp_files", uploaded_file.name)

        answer_generation_chain, ques_list = llm_pipeline(file_path)

        # st.write(ques_list)
        for question in ques_list:
            st.write("Question: ", question)
            answer = answer_generation_chain.run(question)
            st.write("Answer: ", answer)
            st.write("--------------------------------------------------\\n\\n")

if __name__ == "__main__":
    main()