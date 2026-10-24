# 🤖 AI Chatbot for Internship Support

An intelligent conversational assistant built to answer intern queries, explain company policies, and reference historical support tickets using **Sentence-Transformers** semantic search and **Streamlit**.

---

## 🚀 Features

*   **Semantic Matching:** Uses Hugging Face transformer models (`all-MiniLM-L6-v2`) to accurately match user questions against FAQs and historical support logs based on meaning rather than exact keywords.
*   **Unified Knowledge Base:** Combines official company FAQs and past support resolutions into a searchable vector database.
*   **Confidence & Source Tracking:** Displays transparency metrics including the source category (FAQ vs. Support Ticket) and match confidence percentage.
*   **Clean Interactive UI:** Built with Streamlit for a fast, responsive, and clean chat experience with easy conversation resets.

---
🛠️ Installation & Setup Instructions
1. Navigate to Project Directory
Open your terminal inside the project root folder:

Bash
cd internship_chatbot/
2. Install Dependencies
Make sure Python is installed, then install the required packages:

Bash
pip install -r requirements.txt
3. Run the Chat Application
Launch the interactive web app by running:

Bash
streamlit run app.py
📊 Dataset Format
data/faqs.csv

Code snippet
question,answer
"How do I submit my weekly progress report?","You can submit your weekly progress report through the intern portal under the Reports tab before every Friday at 5 PM."
data/support_tickets.csv

Code snippet
ticket_id,issue_summary,resolution
T001,"I am unable to access the company GitHub repository.","Reach out to DevOps lead to get added to the organization with your GitHub username."
💡 Tech Stack
Frontend & UI: Streamlit (st.chat_message, st.chat_input)

NLP & Embeddings: sentence-transformers, PyTorch, Scikit-Learn

Data Handling: Pandas
