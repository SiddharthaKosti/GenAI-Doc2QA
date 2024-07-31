import os
import dotenv
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import TokenTextSplitter
from langchain.docstore.document import Document
from langchain.chat_models import ChatOpenAI
from langchain.prompts import PromptTemplate
from langchain.chains.summarize import load_summarize_chain
from langchain.embeddings.openai import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA

from src.prompt import *
# Load environment variables from .env file

dotenv.load_dotenv()

# Set up OpenAI model
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
os.environ["OPENAI_API_KEY"] = OPENAI_API_KEY

def get_ques_ans_from_pdf(filename):
    loader = PyPDFLoader(filename)
    document = loader.load()

    question_gen = ""
    for doc in document:
        question_gen += doc.page_content

    splitter_ques_gen = TokenTextSplitter(
        model_name="gpt-4o-mini",
        chunk_size=10000,
        chunk_overlap=200
    )

    chunk_ques_gen = splitter_ques_gen.split_text(question_gen)

    document_ques_gen = [Document(item) for item in chunk_ques_gen]

    splitter_ans_gen = TokenTextSplitter(
    model_name = 'gpt-4o-mini',
    chunk_size = 1000,
    chunk_overlap = 100
    )

    document_answer_gen = splitter_ans_gen.split_documents(document_ques_gen)

    return document_ques_gen, document_answer_gen


def llm_pipeline(filename)
    document_ques_gen, document_answer_gen = get_ques_ans_from_pdf(filename)

    llm_ques_gen_pipeline = ChatOpenAI(
    model = 'gpt-4o-mini',
    temperature = 0.3
    )

    PROMPT_QUESTIONS = PromptTemplate(template=prompt_template, input_variables=['text'])

    REFINE_PROMPT_QUESTIONS = PromptTemplate(
    input_variables=["existing_answer", "text"],
    template=refine_template,
    )

    ques_gen_chain = load_summarize_chain(llm = llm_ques_gen_pipeline, 
                                          chain_type = "refine", 
                                          verbose = True, 
                                          question_prompt=PROMPT_QUESTIONS, 
                                          refine_prompt=REFINE_PROMPT_QUESTIONS)
    
    ques = ques_gen_chain.run(document_ques_gen)

    ques_list = ques.split("\n")

    ques_list = [question for question in ques_list if question!=""]
    ques_list = [question for question in ques_list if question.endswith('?') or question.endswith('.')]

    embeddings = OpenAIEmbeddings()

    vector_store = FAISS.from_documents(document_answer_gen, embeddings)

    llm_answer_gen = ChatOpenAI(temperature=0.1, model="gpt-4o-mini")

    answer_generation_chain = RetrievalQA.from_chain_type(llm=llm_answer_gen, 
                                               chain_type="stuff", 
                                               retriever=vector_store.as_retriever())
    
    return answer_generation_chain, ques_list

