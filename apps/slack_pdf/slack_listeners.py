import logging
import requests
from django.conf import settings
from slack_bolt import App
from io import BytesIO
from PyPDF2 import PdfReader
from langchain.chains import create_retrieval_chain
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from langchain.chains.combine_documents import create_stuff_documents_chain

load_dotenv()

logger = logging.getLogger(__name__)

app = App(
    token=settings.SLACK_BOT_TOKEN,
    signing_secret=settings.SLACK_SIGNING_SECRET,
    token_verification_enabled=False,
)

def get_pdf_text(pdf_docs):
    text = ""
    for pdf in pdf_docs:
        pdf_reader = PdfReader(pdf)
        for page in pdf_reader.pages:
            text += page.extract_text() or ""
    return text

def get_text_chunks(text):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    return text_splitter.split_text(text)

def get_vector_store(text_chunks):
   
    embeddings=OpenAIEmbeddings() 
    vector_store = FAISS.from_texts(text_chunks, embedding=embeddings)
    vector_store.save_local("faiss_index")


@app.event("app_mention")
def handle_app_mention(event,say,client):
    user_id = event["user"]
    files = event.get("files", [])
    if files:
        pdf_docs = []
        for file in files:
            file_url = file["url_private_download"]
            
            headers = {"Authorization": f"Bearer {client.token}"}
            response = requests.get(file_url, headers=headers)
            if response.status_code == 200:
                pdf_stream = BytesIO(response.content)
                pdf_docs.append(pdf_stream)
            
            else:
                say(f"Failed to read file: {file['name']}")
                return

        extracted_text = get_pdf_text(pdf_docs)
        text_chunks = get_text_chunks(extracted_text)
        get_vector_store(text_chunks)
        say("Extracted knowledge from the files Successfully")
    else:
        say(f"Hi <@{user_id}>, I noticed you mentioned me, but I couldn't find any files to read.")

    
def get_conversational_chain():

    system_prompt = (
    "You are an assistant for question-answering tasks. "
    "Use the following pieces of retrieved context to answer "
    "the question. If you don't know the answer, say that you "
    "don't know. Use three sentences maximum and keep the "
    "answer concise."
    "\n\n"
    "{context}"
    )

    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            ("human", "{input}"),
        ]
    )

    model = ChatOpenAI(model="gpt-4o-mini")

    return create_stuff_documents_chain(model, prompt)



def user_input(user_question,channel_id,thread_ts):
    
    embeddings=OpenAIEmbeddings()
    try:
        new_db = FAISS.load_local("faiss_index", embeddings, allow_dangerous_deserialization=True)
    except ValueError as e:
        print(f"Error loading FAISS index: {e}")
        return
    
    retriever=new_db.as_retriever()
    question_answer_chain = get_conversational_chain()
    rag_chain = create_retrieval_chain(retriever, question_answer_chain)
    response = rag_chain.invoke({"input": user_question})
    res=response["answer"]
    app.client.chat_postMessage(channel=channel_id, text=f"reply:{res}",thread_ts=thread_ts)
    
    

@app.command("/ask")
def handle_ask_command(ack, respond, command):
    ack()
    user_question=command["text"]
    channel_id = command["channel_id"]
    response=app.client.chat_postMessage(channel=channel_id, text=f"Question : {user_question}")
    thread_ts = response['ts']
    if user_question:
        user_input(user_question,channel_id,thread_ts)
