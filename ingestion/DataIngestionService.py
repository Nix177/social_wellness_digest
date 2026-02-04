import json
import time
import random
from typing import List, Dict

# Simulating external dependencies
# import requests 

class DataIngestionService:
    def __init__(self, sources: List[str]):
        self.sources = sources

    def fetch_data(self) -> List[Dict]:
        """
        Simulates fetching data from configured sources (X, LinkedIn, RSS).
        In a real scenario, this would handle pagination and rate limits.
        """
        print(f"Fetching data from: {', '.join(self.sources)}...")
        # Simulate network delay
        time.sleep(1)
        
        # Mock data generation
        raw_data = []
        topics = ["AI", "Burnout", "Productivity", "Marketing", "Rust", "Python", "Mental Health"]
        
        for i in range(20):
            topic = random.choice(topics)
            raw_data.append({
                "id": f"post_{i}",
                "source": random.choice(self.sources),
                "content": f"Here is some interesting content about {topic}. #tech #growth",
                "author": f"User_{i}",
                "timestamp": time.time(),
                "raw_metadata": {"likes": random.randint(0, 100), "retweets": random.randint(0, 20)}
            })
            
        return raw_data

    def standardize_data(self, raw_data: List[Dict]) -> List[Dict]:
        """
        Converts raw JSON from different sources into a standard format for the LLM.
        """
        standardized = []
        for item in raw_data:
            standardized.append({
                "id": item["id"],
                "text": item["content"],
                "source": item["source"],
                "metadata": {
                    "author": item["author"],
                    "original_timestamp": item["timestamp"]
                }
            })
        return standardized

    def save_to_disk(self, data: List[Dict], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} items to {filename}")

if __name__ == "__main__":
    sources = ["Twitter", "LinkedIn", "RSS_Tech"]
    service = DataIngestionService(sources)
    
    raw_posts = service.fetch_data()
    clean_posts = service.standardize_data(raw_posts)
    
    # Save for the next step (Semantic Filter)
    service.save_to_disk(clean_posts, "ingestion/raw_feed.json")
