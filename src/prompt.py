def prompt_template(n):
    return f"""
    You are an expert in creating questions given a document.
    Your goal is to prepare a set of question:

    ------------
    {{text}}
    ------------

    Create questions that will prepare the coders or programmers for their tests.
    Make sure not to lose any important information.
    Only create {n} questions.

    QUESTIONS:
    """

refine_template = ("""
You are an expert at creating practice questions based on coding material and documentation.
Your goal is to help a coder or programmer prepare for a coding test.
We have received some practice questions to a certain extent: {existing_answer}.
We have the option to refine the existing questions or add new ones.
(only if necessary) with some more context below.
------------
{text}
------------

Given the new context, refine the original questions in English.
If the context is not helpful, please provide the original questions.
QUESTIONS:
"""
)