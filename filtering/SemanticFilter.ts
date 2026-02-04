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
     * analyzing content based on a keyword heuristic to simulate "Semantic Filtering".
     * In a production env, this would call an LLM API.
     */
    private async analyzeWithLLM(post: Post): Promise<ScoredPost> {
        // Keywords aligned with "Social Wellness" & "Tech Balance"
        const highValueKeywords = [
            "burnout", "mental health", "déconnexion", "addiction",
            "dopamine", "nature", "meditation", "focus", "deep work",
            "privacy", "surveillance", "éthique", "ethics", "slow web"
        ];

        const techKeywords = [
            "ai", "ia", "rust", "python", "algorithm", "data",
            "tech", "future", "innovation", "science"
        ];

        const content = (post.text + " " + (post.metadata?.extra?.link || "")).toLowerCase();

        let score = 0;
        let reasoning = "General tech content.";

        // Scoring Logic
        let matchedWellness = highValueKeywords.filter(k => content.includes(k));
        let matchedTech = techKeywords.filter(k => content.includes(k));

        if (matchedWellness.length > 0) {
            score += 60 + (matchedWellness.length * 10);
            reasoning = `Relevant to wellness topics: ${matchedWellness.join(", ")}`;
        } else if (matchedTech.length > 0) {
            score += 30 + (matchedTech.length * 5);
            reasoning = `General tech update: ${matchedTech.join(", ")}`;
        } else {
            score = 10;
            reasoning = "Low relevance match.";
        }

        // Boost for specific sources if needed (optional)
        if (post.source.includes("Techno-Science")) score += 5;

        return {
            ...post,
            relevanceScore: Math.min(score, 100),
            category: score >= 70 ? "High Value" : (score >= 40 ? "Interesting" : "Noise"),
            reasoning: reasoning
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
