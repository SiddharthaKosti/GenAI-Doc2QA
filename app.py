import streamlit as st
import os
import shutil
import dotenv
import asyncio
import aiofiles
from src.helper import async_llm_pipeline

dotenv.load_dotenv()

# Set up OpenAI model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

st.set_page_config(layout="wide", page_title="GenAI-Doc2QA")

async def run_temp_dir():
    temp_dir = "temp_files"
    if os.path.exists(temp_dir):
        await asyncio.to_thread(shutil.rmtree, temp_dir)
    await asyncio.to_thread(os.makedirs, "temp_files", exist_ok=True)

def check_if_pdf(uploaded_file):
    if uploaded_file.name.endswith('.pdf'):
        st.write("PDF file uploaded successfully")
    else:
        st.write("Uploaded file is not a PDF. Please choose a PDF file.")

async def main():
    st.title("GenAI-Doc2QA")
    st.divider()
    uploaded_file = st.file_uploader("Upload a file here: ", type=["pdf"])
    st.sidebar.image("data/Designer.png", width=285, caption="GenAI-Doc2QA")
    n = st.sidebar.text_input("Enter the number of Q/A pairs required")
    
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            left: 0;
            bottom: 0;
            width: 100%;
            background-color: #ffe5ec;
            color: black;
            text-align: center;
        }
        </style>
        <div class="footer">
            <p>Made with ❤️ by Siddhartha Kosti</p>
        </div>
        """,
        unsafe_allow_html=True
    )

    if uploaded_file is not None:
        st.subheader(""":blue[File is uploaded successfully] :blossom:""")
        await run_temp_dir()

        # Save the uploaded file temporarily
        file_path = os.path.join("temp_files", uploaded_file.name)
        await asyncio.to_thread(uploaded_file.getbuffer().tobytes)
        async with aiofiles.open(file_path, "wb") as f:
            await f.write(uploaded_file.getbuffer())

        st.divider()
        if n:
            answer_generation_chain, ques_list = await async_llm_pipeline(file_path, n)
            st.header("Question-Answer:")
            for question in ques_list:
                answer = await answer_generation_chain.arun(question)
                st.info(f"Question: {question}\n\n Answer: {answer}")

if __name__ == "__main__":
    asyncio.run(main())