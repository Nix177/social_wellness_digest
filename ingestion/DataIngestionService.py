import json
import time
import os
import random
from typing import List, Dict

try:
    import feedparser
except ImportError:
    print("Warning: feedparser not installed. Falling back to mock data.")
    feedparser = None

class DataIngestionService:
    def __init__(self, sources: List[str]):
        self.sources = sources
        self.rss_urls = {
            "Techno-Science": "https://www.techno-science.net/rss.xml",
            "Hacker News": "https://news.ycombinator.com/rss",
            "Futura Tech": "https://www.futura-sciences.com/rss/high-tech/actualites.xml"
        }

    def fetch_rss(self, url: str, source_name: str) -> List[Dict]:
        """Fetches data from a real RSS feed."""
        if not feedparser:
            return []
        
        print(f"  - Requesting {source_name} ({url})...")
        feed = feedparser.parse(url)
        posts = []
        
        for entry in feed.entries[:5]: # Top 5 per feed
            # Clean up struct_time to float timestamp
            if hasattr(entry, 'published_parsed') and entry.published_parsed:
                timestamp = time.mktime(entry.published_parsed)
            else:
                timestamp = time.time()

            posts.append({
                "id": entry.get('id', entry.get('link', str(random.randint(1000,9999)))),
                "source": source_name,
                "content": f"{entry.title} - {entry.get('summary', '')[:200]}...",
                "author": entry.get('author', 'Unknown'),
                "timestamp": timestamp,
                "raw_metadata": {"link": entry.link}
            })
        return posts

    def fetch_mock(self) -> List[Dict]:
        """Fallback mock data."""
        raw_data = []
        topics = ["Biohacking", "Digital Minimalist", "Rust Programming", "Obsidian Workflows", "Neuromorphic Computing"]
        
        for i in range(5):
            topic = random.choice(topics)
            raw_data.append({
                "id": f"mock_{i}",
                "source": "MockStream",
                "content": f"Discovering the benefits of {topic} for mental clarity. #wellness #tech",
                "author": f"WellnessBot_{i}",
                "timestamp": time.time(),
                "raw_metadata": {"likes": random.randint(0, 100)}
            })
        return raw_data

    def load_seeds(self) -> List[Dict]:
        """Loads vetted seed content."""
        seed_path = os.path.join(os.path.dirname(__file__), 'seeds.json')
        if os.path.exists(seed_path):
            try:
                with open(seed_path, 'r', encoding='utf-8') as f:
                    print(f"  - Loading seed content from {seed_path}...")
                    return json.load(f)
            except Exception as e:
                print(f"Error loading seeds: {e}")
        return []

    def fetch_data(self) -> List[Dict]:
        """
        Main fetcher: tries RSS, falls back or adds to mock.
        """
        print("Starting Data Ingestion...")
        all_data = []
        
        # 1. Load Seeds (Always include these for Demo/Pre-fill)
        all_data.extend(self.load_seeds())

        # 2. Try Real RSS
        if feedparser:
            for name, url in self.rss_urls.items():
                try:
                    all_data.extend(self.fetch_rss(url, name))
                except Exception as e:
                    print(f"Error fetching {name}: {e}")
        
        # 3. Add Mock Data (only if total is low)
        if len(all_data) < 3:
            print("Low data volume. Generating mock data.")
            all_data.extend(self.fetch_mock())
            
        print(f"Total items fetched: {len(all_data)}")
        return all_data

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
                    "original_timestamp": item["timestamp"],
                    "extra": item.get("raw_metadata", {})
                }
            })
        return standardized

    def save_to_disk(self, data: List[Dict], filename: str):
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
        print(f"Saved {len(data)} items to {filename}")

if __name__ == "__main__":
    sources = ["RSS"] # Placeholder
    service = DataIngestionService(sources)
    
    raw_posts = service.fetch_data()
    clean_posts = service.standardize_data(raw_posts)
    
    # Save for the next step (Semantic Filter)
    service.save_to_disk(clean_posts, "ingestion/raw_feed.json")
