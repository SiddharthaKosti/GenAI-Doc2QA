# GenAI-Doc2QA

GenAI-Doc2QA is a Streamlit application that allows users to upload PDF documents and generate questions and answers from the content. This application leverages OpenAI's GPT-4o-mini model to generate relevant questions/answers pairs.

## Features

- Upload PDF document
- Enter the number of question/answer pairs required
- Generate questions based on the content of the PDF
- Generate answers to the questions using OpenAI's GPT-4 model

## Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/GenAI-Doc2QA.git
cd GenAI-Doc2QA
```

2. Create and activate a virtual environment:
```
python -m venv venv
source venv/bin/activate   # On Windows use `venv\Scripts\activate`
```

3. Install the required dependencies:
```
pip install -r requirements.txt
```

4.  Set up your environment variables:
create one .env file having the following
```
OPENAI_API_KEY=your_openai_api_key
```

## Usage
1.  Run the Streamlit application:
```
streamlit run app.py
```

2.  Open your web browser and navigate to http://localhost:8501.
3.  Upload a PDF document using the file uploader.
4.  The application will generate questions and answers based on the content of the uploaded PDF.
