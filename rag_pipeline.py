# --- Updated rag_pipeline.py ---

from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.vectorstores import FAISS
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.chains import RetrievalQA
from langchain_core.documents import Document
import os
import pickle

llm = OllamaLLM(model="llama3")
embeddings = OllamaEmbeddings(model="llama3")
DB_PATH = "rfp_faiss_index"


# Load Prompt Template from file
def load_prompt(path):
    with open(path, encoding="utf-8") as f:
        return PromptTemplate.from_template(f.read())


# RAG Pipeline Logic
def run_all(rfp_text, company_text, agency, rfp_number, title, rfp_instructions=""):
    results = {}

    # Save to FAISS
    chunks = split_and_store_embeddings(rfp_text)

    summary_prompt = load_prompt("prompts/summary_prompt.txt")
    results["summary"] = (summary_prompt | llm).invoke(
        {"rfp": rfp_text, "company": company_text}
    )

    eligibility_prompt = load_prompt("prompts/eligibility_prompt.txt")
    results["eligibility"] = (eligibility_prompt | llm).invoke(
        {"rfp": rfp_text, "company": company_text}
    )

    structure_prompt = load_prompt("prompts/structure_prompt.txt")
    results["structure"] = (structure_prompt | llm).invoke(
        {"rfp": rfp_text, "company": company_text}
    )

    improvement_prompt = load_prompt("prompts/improvement_prompt.txt")
    results["improvement"] = (improvement_prompt | llm).invoke(
        {"rfp": rfp_text, "company": company_text}
    )

    recommendations_prompt = load_prompt("prompts/recommendations_prompt.txt")
    results["recommendations"] = (recommendations_prompt | llm).invoke(
        {"rfp": rfp_text, "company": company_text}
    )

    proposal_prompt = load_prompt("prompts/proposal_prompt.txt")
    results["proposal_draft"] = (proposal_prompt | llm).invoke(
        {
            "summary": results["summary"],
            "rfp": rfp_text,
            "improvements": results["improvement"],
            "company": company_text,
        }
    )

    polish_prompt = load_prompt("prompts/polish_prompt.txt")
    results["final_proposal"] = (polish_prompt | llm).invoke(
        {
            "improvements": results["improvement"],
            "rfp_number": rfp_number,
            "agency": agency,
            "rfp_instructions": rfp_instructions,
            "company": company_text,
            "title": title,
        }
    )

    return results


# Split RFP and store in FAISS
def split_and_store_embeddings(rfp_text):
    splitter = RecursiveCharacterTextSplitter(chunk_size=100, chunk_overlap=10)
    chunks = splitter.split_text(rfp_text)
    docs = [Document(page_content=chunk) for chunk in chunks]

    db = FAISS.from_documents(docs, embeddings)
    db.save_local(DB_PATH)
    return chunks


# Query Bot


def query_rfp(user_query):
    if not os.path.exists(DB_PATH):
        return "❌ Please run analysis first to index the RFP."

    db = FAISS.load_local(DB_PATH, embeddings, allow_dangerous_deserialization=True)
    qa = RetrievalQA.from_chain_type(
        llm=llm, retriever=db.as_retriever(), return_source_documents=False
    )
    response = qa.invoke(user_query)
    return response["result"]
