import os
import pandas as pd
from sentence_transformers import SentenceTransformer, util
import torch

class InternshipChatbot:
    def __init__(self):
        # Load a lightweight, high-performing embedding model from Hugging Face
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.load_and_prepare_data()

    def load_and_prepare_data(self):
        # Load datasets with robust engine settings
        faq_path = os.path.join("data", "faqs.csv")
        ticket_path = os.path.join("data", "support_tickets.csv")
        
        self.faqs_df = pd.read_csv(faq_path, on_bad_lines='skip', engine='python')
        self.tickets_df = pd.read_csv(ticket_path, on_bad_lines='skip', engine='python')
        
        # Combine questions and support summaries into a unified knowledge base
        self.knowledge_base = []
        
        # Add FAQs
        for _, row in self.faqs_df.iterrows():
            if pd.notna(row.get('question')) and pd.notna(row.get('answer')):
                self.knowledge_base.append({
                    "text": str(row['question']),
                    "response": str(row['answer']),
                    "source": "Official FAQ"
                })
            
        # Add Historical Tickets
        for _, row in self.tickets_df.iterrows():
            if pd.notna(row.get('issue_summary')) and pd.notna(row.get('resolution')):
                self.knowledge_base.append({
                    "text": str(row['issue_summary']),
                    "response": f"Resolved via Ticket: {row['resolution']}",
                    "source": "Historical Support Ticket"
                })
            
        # Pre-compute embeddings for all knowledge base entries
        kb_texts = [item['text'] for item in self.knowledge_base]
        if kb_texts:
            self.kb_embeddings = self.model.encode(kb_texts, convert_to_tensor=True)
        else:
            self.kb_embeddings = None

    def get_response(self, user_query, threshold=0.45):
        """Find the most semantically relevant answer using cosine similarity."""
        if not self.knowledge_base or self.kb_embeddings is None:
            return "The knowledge base is currently empty.", "None", 0.0
            
        query_embedding = self.model.encode(user_query, convert_to_tensor=True)
        
        # Compute cosine similarities between user query and knowledge base
        cos_scores = util.cos_sim(query_embedding, self.kb_embeddings)[0]
        
        # Get the top matching score and index
        best_score_idx = torch.argmax(cos_scores).item()
        best_score = cos_scores[best_score_idx].item()
        
        if best_score < threshold:
            return (
                "I'm sorry, I couldn't find a precise answer to your question in my knowledge base. "
                "Please reach out to your program manager or check the #intern-help Slack channel!", 
                "None", 
                0.0
            )
            
        best_match = self.knowledge_base[best_score_idx]
        return best_match['response'], best_match['source'], round(best_score * 100, 2)