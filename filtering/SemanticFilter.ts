import * as fs from 'fs';
import * as path from 'path';

// Interface for the Standardized Post
interface Post {
    id: string;
    text: string;
    source: string;
    metadata: any;
}

// Interface for the Scored Post
interface ScoredPost extends Post {
    relevanceScore: number;
    category: string;
    reasoning: string;
}

class SemanticFilter {
    private threshold: number;

    constructor(threshold: number = 80) {
        this.threshold = threshold;
    }

    /**
     * Simulates sending content to an LLM (e.g., Azure OpenAI)
     * Returns a score, category, and reasoning.
     */
    private async analyzeWithLLM(post: Post): Promise<ScoredPost> {
        // MOCK LLM LOGIC
        // In reality, this would be a fetch call to OpenAI API using LangChain

        const keywords = ["Burnout", "Mental Health", "AI", "Rust"];
        let score = Math.floor(Math.random() * 60); // Base noise

        const content = post.text.toLowerCase();

        // Boost score if meaningful keywords are found
        if (keywords.some(k => content.includes(k.toLowerCase()))) {
            score += 40;
        }

        return {
            ...post,
            relevanceScore: Math.min(score, 100),
            category: score > 70 ? "High Value" : "Noise",
            reasoning: score > 70 ? "Relevant to user interests" : "Generic content"
        };
    }

    public async processFeed(inputFile: string, outputFile: string) {
        console.log(`Reading from ${inputFile}...`);
        const rawData = fs.readFileSync(inputFile, 'utf-8');
        const posts: Post[] = JSON.parse(rawData);

        console.log(`Analyzing ${posts.length} posts...`);
        const scoredPosts: ScoredPost[] = [];

        for (const post of posts) {
            const result = await this.analyzeWithLLM(post);
            if (result.relevanceScore >= this.threshold) {
                scoredPosts.push(result);
            }
        }

        console.log(`Filtered down to ${scoredPosts.length} relevant posts.`);
        fs.writeFileSync(outputFile, JSON.stringify(scoredPosts, null, 2));
        console.log(`Saved to ${outputFile}`);
    }
}

// Execution
async function main() {
    const filter = new SemanticFilter(75); // User preference threshold

    // Check if input exists (created by Python step)
    const inputPath = path.join(__dirname, '../ingestion/raw_feed.json');
    const outputPath = path.join(__dirname, 'filtered_feed.json');

    if (fs.existsSync(inputPath)) {
        await filter.processFeed(inputPath, outputPath);
    } else {
        console.error(`Input file not found: ${inputPath}`);
        console.log("Please run the Python ingestion service first.");
    }
}

main();
