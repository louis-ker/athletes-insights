# Athletes Insights: A RAG-Powered Video Content Generator (in development)

**Athletes Insights** is an intelligent content generation platform, aiming to create personalized short-track speed skating videos enriched with **data-driven** insights, charts, and voice-over narration.
It leverages **Retrieval-Augmented Generation** (RAG) and machine learning to explore how engaging and factual stories can be tailored to each user's interests.

---

## Project Overview

This project is developed as part of the **[DataHack – "Data on Ice" challenge by Thinksport](https://thinksport.org/)**, aiming to transform ISU’s extensive data archives (videos, bios, results) into **rich, personalized narratives** for fans, journalists, and governing bodies.

> **Challenge mission:**  
> Mine structured and unstructured data from short-track speed skating to deliver predictive stories, insightful analyses, and unforgettable fan experiences.

---

## Objectives

- Generate **video content** featuring:
  - **Text overlays** summarizing insights  
  - **Dynamic charts** generated from real data  
  - **AI-generated voice-over narration**
- Use **Retrieval-Augmented Generation (RAG)** to ensure factual accuracy and minimize hallucinations.
- Personalize content recommendations based on user interest profiles through **machine learning**.
- Integrate **real-time data visualization** powered by OpenAI and Recharts.

---

## 💬 Chatbot & RAG System

The chatbot is designed to **answer user questions** about short-track speed skating using a **retrieval-augmented generation pipeline**:

1. **Document Retrieval:**  
   Uses **LangChain** to search through thousands of scraped articles (Wikipedia, ISU website, etc.) split into text chunks.

2. **Answer Generation:**  
   When no relevant chunk is found, the system triggers **Tavily** for a live web search.

3. **Data Visualization Tool:**  
   Through OpenAI’s API, users can request the generation of **custom charts** powered by **Recharts**, directly inside the conversation.

4. **Factuality Safeguards:**  
   The system filters hallucinations and ensures responses are based solely on verified and contextually relevant data.

---

## 🧩 Installation for LOCAL USE or Development

### 1. Clone the repository
```bash
git clone https://github.com/louis-ker/athletes-insights.git
cd athletes-insights
```

### 2. Backend Setup
```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```
### 3. Frontend Setup
```bash
cd ../frontend
npm install
```
### 4. Small URL changes for local use
#### 4.1 Look for frontend/src/components/MessageBox.jsx &#8594; handleSend():

Replace:
```python
...
const response = await fetch("https://athletes-insights-backend.onrender.com/api/ask",
...
```
By:
```python
...
const response = await fetch("http://localhost:4000/api/run",
...
```
#### 4.2 Look for backend/app.py:

Replace:
```python
...
@app.route("/api/ask", methods=["POST"])
...
```
By:
```python
...
@app.route("/api/run", methods=["POST"])
...
```
### 5. Run the app
Run the backend:
```bash
cd backend
python app.py
```
Run the frontend:
```bash
cd fontend
npm run dev
```