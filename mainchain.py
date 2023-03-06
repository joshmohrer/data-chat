import streamlit as st
from langchain.llms import OpenAI
from langchain.chains import ChatVectorDBChain
from langchain.chains.llm import LLMChain
from streamingCallback import StreamingCallbackHandler
from langchain.chains.chat_vector_db.prompts import (
    CONDENSE_QUESTION_PROMPT, QA_PROMPT)
from langchain.callbacks.base import CallbackManager
from langchain.chains.question_answering import load_qa_chain
from langchain.chains.qa_with_sources import load_qa_with_sources_chain


@st.cache_resource
def chat_chain(_vectorstore):
    print("Loading conversation chain...")

    llm = OpenAI(temperature=0, openai_api_key=st.secrets["OPENAI_KEY"])
    streaming_llm = OpenAI(temperature=0, openai_api_key=st.secrets["OPENAI_KEY"], verbose=True,
                           streaming=True, callback_manager=CallbackManager([StreamingCallbackHandler()]))
    question_generator = LLMChain(llm=llm, prompt=CONDENSE_QUESTION_PROMPT)
    doc_chain = load_qa_with_sources_chain(
        streaming_llm, chain_type="stuff", prompt=QA_PROMPT)
    chat = ChatVectorDBChain(
        vectorstore=_vectorstore, combine_docs_chain=doc_chain, question_generator=question_generator)

    return chat
