from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from typing_extensions import Annotated
from langchain_community.embeddings import HuggingFaceInferenceAPIEmbeddings
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import MongoDBAtlasVectorSearch
from langchain_community.document_loaders import PyPDFLoader
from dotenv import load_dotenv, dotenv_values
from pymongo import MongoClient
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA, StuffDocumentsChain, LLMChain
from langchain_community.llms import HuggingFaceHub
from pydantic import BaseModel
from langchain_community.document_transformers import (
    LongContextReorder,
)
from langchain.callbacks.base import BaseCallbackHandler
import os
# import langchain
# langchain.debug = True

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
load_dotenv()
config = {**os.environ}
client = MongoClient(config['DB_URL'])


class MyCustomHandler(BaseCallbackHandler):
    def on_llm_end(self, event, context):
        print(event, context, "##$#$#$$%#$#$#$")


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.post("/add-document-to-knowledge-base")
def addOneDocumentToKnowledgeBase(documentUrl: str) -> bool:
    collection = client[config['DB_NAME']
                        ][config['VECTOR_EMBEDDINGS_COLLECTION_NAME']]
    doesDocumentEmbeddingsExists = collection.find_one({'source': documentUrl})
    if (doesDocumentEmbeddingsExists is None):
        loader = PyPDFLoader(documentUrl)
        docs = loader.load()
        # TODO : Load Only the English Part of the Document
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1024, chunk_overlap=100)
        texts = text_splitter.split_documents(docs)

        embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=config['HUGGINGFACEHUB_API_TOKEN'],
            model_name="sentence-transformers/all-MiniLM-l6-v2"
        )
        vector_search = MongoDBAtlasVectorSearch.from_documents(
            documents=texts,
            embedding=embeddings,
            collection=client[config['DB_NAME']
                              ][config['VECTOR_EMBEDDINGS_COLLECTION_NAME']],
            index_name=config['VECTOR_SEARCH_INDEX'],
        )
        return vector_search is not None
    else:
        raise HTTPException(
            status_code=418, detail="Embeddings for this document already exists in DB")


@app.post("/semantic-search")
def performSemanticSearch(query: str, k: int = 5) -> object:
    if len(query) == 0:
        raise HTTPException(
            status_code=418, detail="Please enter valid query string")
    else:
        embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=config['HUGGINGFACEHUB_API_TOKEN'],
            model_name="sentence-transformers/all-MiniLM-l6-v2"
        )

        vector_search = MongoDBAtlasVectorSearch.from_connection_string(
            config['DB_URL'],
            config['DB_NAME'] + "." +
            config['VECTOR_EMBEDDINGS_COLLECTION_NAME'],
            embeddings,
            index_name=config['VECTOR_SEARCH_INDEX'],
        )

        results = vector_search.similarity_search_with_score(
            query=query,
            k=k,
        )

        json_data = [
            {
                "document": {
                    "page_content": doc.page_content,
                    "source": doc.metadata['source'],
                    "source_page_number": doc.metadata['page'],
                    "similarity_score": score,
                }
            }
            for doc, score in results
        ]
        return json_data


class Query(BaseModel):
    queryText: str
    k: int = 25


@app.post("/generate-AI-response")
def generateAIResponseFromTheQuery(query: Query) -> str:
    if len(query.queryText) == 0:
        raise HTTPException(
            status_code=418, detail="Please enter valid query string")
    else:
        embeddings = HuggingFaceInferenceAPIEmbeddings(
            api_key=config['HUGGINGFACEHUB_API_TOKEN'],
            model_name="sentence-transformers/all-MiniLM-l6-v2"
        )

        vector_search = MongoDBAtlasVectorSearch.from_connection_string(
            config['DB_URL'],
            config['DB_NAME'] + "." +
            config['VECTOR_EMBEDDINGS_COLLECTION_NAME'],
            embeddings,
            index_name=config['VECTOR_SEARCH_INDEX'],
        )

        qa_retriever = vector_search.as_retriever(
            search_type="similarity",
            search_kwargs={"k": query.k}
        )
        docs = qa_retriever.get_relevant_documents(query.queryText)
        reordering = LongContextReorder()
        reordered_docs = reordering.transform_documents(docs)
        document_prompt = PromptTemplate(
            input_variables=["page_content"], template="{page_content}"
        )

        document_variable_name = "context"

        llm = HuggingFaceHub(
            repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", model_kwargs={"temperature": 0.9, "max_length": 500, "max_new_tokens": 500})

        stuff_prompt_override = """You are a helpful legal compliance assistant who will refer the following context to answer the questions and also mention the section number or subsection number in your answer . at the end. If you don't know the answer, just say that you don't know, don't try to make up an answer
        -----
        {context}
        -----
        Please answer the following question:
        {query}"""
        prompt = PromptTemplate(
            template=stuff_prompt_override, input_variables=[
                "context", "query"]
        )

        # Instantiate the chain
        llm_chain = LLMChain(llm=llm, prompt=prompt)
        chain = StuffDocumentsChain(
            llm_chain=llm_chain,
            document_prompt=document_prompt,
            document_variable_name=document_variable_name,


        )
        res = chain.run(input_documents=reordered_docs, query=query.queryText)
        print(res)
        return res


if __name__ == '__main__':
    url = "https://www.fssai.gov.in/upload/notifications/2022/06/62ac3f9dba33cGazette_Notification_Vegan_Food_17_06_2022.pdf"
    q = Query(queryText="I want to sell cheese online", k=25)
    generateAIResponseFromTheQuery(q)
