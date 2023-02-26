"""Python file to serve as the frontend"""
import streamlit as st
from streamlit_chat import message
from langchain.embeddings import OpenAIEmbeddings
from langchain.vectorstores import FAISS
from streamlit_extras import add_vertical_space as avs
from mainchain import chat_chain
from ingest import ingest_txt
from io import StringIO

def App(file):
    # create list of Document objects 
    docs_from_text = ingest_txt(file, as_text=True)
    
    # Embedd list of Document objects and generate vectorstore
    embeddings = OpenAIEmbeddings(openai_api_key=st.secrets['OPENAI_KEY'])
    vectorstore = FAISS.from_documents(docs_from_text, embeddings)
        
    # load ChatVectorDBChain
    chain = chat_chain(vectorstore)

    # if "generated" not in st.session_state:
    #     st.session_state["generated"] = []

    # if "past" not in st.session_state:
    #     st.session_state["past"] = []
        
    # if "chat_history" not in st.session_state:
    #     st.session_state["chat_history"] = []


    def get_text():
        input_text = st.text_input("What's on your mind? ", key="input")
        return input_text
        
    user_input = get_text()

    if user_input:
        # run chain with user input and chat history
        output = chain({"question": user_input, "chat_history": st.session_state["chat_history"]}, return_only_outputs=False)
   
        # Putting 5 vertical spaces
        avs.add_vertical_space(5)
        st.session_state.past.append(user_input)
        st.session_state.generated.append(output['answer'])

    if st.session_state["generated"]:
        st.session_state["chat_history"].append((user_input, output['answer']))
        for i in range(len(st.session_state["generated"]) - 1, -1, -1):
            message(st.session_state["generated"][i], key=str(i))
            message(st.session_state["past"][i], is_user=True, key=str(i) + "_user")
            
            
def UI():
    col1, col2  = st.columns([1, 1], gap='large')
    
    with st.sidebar:

        avs.add_vertical_space(5)
        
        file = st.file_uploader("Upload a file", type=["txt"])
    
        
    with col1:
        if file:
            # To convert to a string based IO:
            stringio = StringIO(file.getvalue().decode("utf-8"))
            # To read file as string:
            string_data = stringio.read()
            App(string_data)

        else:
            st.write("Please upload a text file to begin")
        
    with col2:
        # widgets(col2)
        pass