from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore
from langchain_community.document_loaders import TextLoader

from langchain_core.documents import Document
from langchain_core.messages import AIMessage
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.tools import tool

from langchain.agents import create_agent



from dotenv import load_dotenv
import os
load_dotenv()

GEMINI_API = os.getenv("GEMINI_API")

class TranscriptRAGAgent:

    def create_agent(self, transcript, query):
        # print("hi there")

    
        #1. load the txt file
        # file_path = "./example.txt"
        # loader = TextLoader(file_path)
        # docs = loader.load()
        # print(len(docs))
        # print(docs)

        #with tranctipt
        transcript_text = " ".join([item['text'] for item in transcript])
        docs = [Document(page_content=transcript_text)]
        # print(len(docs))



        #2. text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        all_splits = text_splitter.split_documents(docs)
        # print(len(all_splits))
        print(f"Splited into {len(all_splits)} sub-documents.")
    

        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=GEMINI_API)
        vector_store = InMemoryVectorStore(embeddings)

        # vector_1 = embeddings.embed_query(all_splits[1].page_content)

        # print(f"Generated vectors of length {len(vector_1)}\n")


        document_ids = vector_store.add_documents(documents=all_splits)
        # print("some doc ids: ", document_ids[:3])


        llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=GEMINI_API)

        @tool
        def retrieve_context(query: str) -> str:
            """Retrieve information from the video transcript to help answer a query."""
            retrieved_docs = vector_store.similarity_search(query, k=2)
            serialized = "\n\n".join(
                (f"Source: {doc.metadata}\nContent: {doc.page_content}")
                for doc in retrieved_docs
            )
            return serialized

        tools = [retrieve_context]
        system_prompt = (
            "You are a helpful AI assistant with access to a tool that retrieves context "
            "from a video transcript. Use it to help answer user queries as accurately as possible."
        )

        agent = create_agent(model=llm, tools=tools, system_prompt=system_prompt)
        result = agent.invoke({"messages": [{"role": "user", "content": query}]})

        # Extract final answer from the last AI message
        messages = result.get("messages", [])
        final_answer = ""
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.content:
                final_answer = msg.content if isinstance(msg.content, str) else str(msg.content)
                break

        print("\n")
        print("------------ans to your query: ", query, " ------------")
        print("this is result: ", final_answer)


