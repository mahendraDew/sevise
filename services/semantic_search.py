import asyncio


from langchain_community.document_loaders import TextLoader
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
# from langchain_ollama import OllamaEmbeddings
# from langchain_huggingface import HuggingFaceEmbeddings
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_core.vectorstores import InMemoryVectorStore

from dotenv import load_dotenv
import os
load_dotenv()

GEMINI_API = os.getenv("GEMINI_API")

class SemanticSearching:

    async def semanticSearch(self, transcript, search_query):

        #1. load the txt file
        transcript_text = " ".join([item['text'] for item in transcript])

        # loader = TextLoader(transcript_text)
        # loader = TextLoader(file_path)
        docs = [Document(page_content=transcript_text)]

        # docs = loader.load()

        # print(len(docs))
        print(docs)


        #2. text splitter
        text_splitter = RecursiveCharacterTextSplitter(
            chunk_size=1000, chunk_overlap=200, add_start_index=True
        )
        all_splits = text_splitter.split_documents(docs)

        print(len(all_splits))
        print(all_splits)
        # print(type( all_splits))
        # this is the pagecontent: print(all_splits[0].page_content)



        #3. embedding the text data

        # from google import genai

        # # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        # client = genai.Client(api_key=GEMINI_API)

        # response = client.models.generate_content(
        #     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
        # )
        # print(response.text)
        embeddings = GoogleGenerativeAIEmbeddings(model="models/gemini-embedding-001", google_api_key=GEMINI_API)

        vector_1 = embeddings.embed_query(all_splits[1].page_content)

        # print(f"Generated vectors of length {len(vector_1)}\n")
        # print(vector_1)

        # print(vector_1[:10])
        # from google import genai

        # # The client gets the API key from the environment variable `GEMINI_API_KEY`.
        # client = genai.Client(api_key=GEMINI_API)

        # response = client.models.generate_content(
        #     model="gemini-2.5-flash", contents="Explain how AI works in a few words"
        # )
        # print(response.text)


        #4. storing the generated vectors - in memory by creating a vector_store


        vector_store = InMemoryVectorStore(embeddings)  # this is just creating a vector storage named 'vector_store" and it will create a vector store according to the "embeddings" so that later when you store 'embedding' and corresponding document in this, it'll be commpatible to that

        #4.1 add documents to the vector store- basically means storing the embeddings + their associated text in an efficient search structure.
        ids = vector_store.add_documents(documents=all_splits) #now here we are actually storing the embedding and the documents in the 'vector_store'
        
        # que ="what are the primary need that langchain aims to address?" 
        results = await vector_store.asimilarity_search(search_query)
        print('\n')
        print('------------ans to your query: "', search_query , '" ------------')
        print(results[0].page_content)




    

# Run the async function
# asyncio.run(main())