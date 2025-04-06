from openai import OpenAI
import numpy as np

class Client:
    def __init__(self, choices: list[str]):
        self.openai_emb_model = "text-embedding-3-small"
        self.choices = [choice.lower().strip() for choice in choices]
        self.client = None

        try:
            self.client = OpenAI()
        except Exception as e:
            raise Exception("OpenAI API key not found. Please set the OPENAI_API_KEY environment variable.")
        
        # Embed each choice
        self.choice_embeddings = {}
        for choice in self.choices:
            response = self.client.embeddings.create(
                model=self.openai_emb_model,
                input=choice
            )
            self.choice_embeddings[choice] = response.data[0].embedding
        
    def classify(self, answer: str) -> str:
        # Lowercase and strip the answer
        answer = answer.lower().strip()
        
        # First try direct matching
        for choice in self.choices:
            if answer == choice:
                return choice
                
        # If no direct match, use embeddings for semantic similarity
        answer_embedding = self.client.embeddings.create(
            model=self.openai_emb_model,
            input=answer
        ).data[0].embedding
        
        # Calculate cosine similarity with each choice
        max_similarity = -1
        best_match = None
        
        for choice in self.choices:
            similarity = self._cosine_similarity(answer_embedding, self.choice_embeddings[choice])
            if similarity > max_similarity:
                max_similarity = similarity
                best_match = choice
                
        return best_match
    
    def _cosine_similarity(self, vec1, vec2):
        """Calculate cosine similarity between two vectors."""
        dot_product = sum(a * b for a, b in zip(vec1, vec2))
        norm_a = np.sqrt(sum(a * a for a in vec1))
        norm_b = np.sqrt(sum(b * b for b in vec2))
        return dot_product / (norm_a * norm_b)
