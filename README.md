# 🤖 AI RFP Assistant – Automate Government RFP Analysis with GenAI

**AI RFP Assistant** is an end-to-end Generative AI-powered tool designed to simplify and accelerate government RFP (Request for Proposal) analysis. It summarizes RFPs, checks eligibility, validates structure, suggests improvements, and even drafts high-quality proposals — all enhanced by a chatbot assistant for real-time document interaction.

---

## 🔍 Features

- 📄 **RFP Summary Generator**
- ✅ **Eligibility Check & Compliance Match**
- 🧩 **Proposal Structure Validator**
- ✨ **Improvement Recommendations**
- 📝 **Draft & Final Proposal Generator**
- 💬 **Chatbot Assistant for Q&A (RAG-powered)**
- 🧠 Powered by **LangChain**, **Ollama LLMs**, and **Streamlit**
- 💾 Uses **FAISS** for semantic vector search

---

## 📦 Tech Stack

- `Python`
- `LangChain` + `Ollama` (`Gemma 2B`, `LLaMA3`, etc.)
- `FAISS` for local vector storage
- `Streamlit` for UI
- `Prompt Engineering` with `.txt` templates
- `Chatbot` for interactive RFP Q&A using local embeddings (RAG)

---

## 🛠️ Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Aarya1931/RFP_Pilot.git
cd RFP_Pilot
2. Set Up Environment
pip install -r requirements.txt
Ensure you have Ollama installed and running locally with required models.

3. Start the App

streamlit run app.py
🧠 LLM & RAG Workflow
RFP & Company Profile Input

Multiple Prompt Templates invoked on the LLM for each step:

Summary

Eligibility

Structure

Improvements

Proposal Drafting

Final Polishing

Chatbot uses FAISS + LangChain retriever to answer questions using supporting documents
