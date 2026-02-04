/**
 * DraftManager.js
 * Manages local draft storage and enforces the Sunday posting rule.
 */
class DraftManager {
    constructor() {
        this.STORAGE_KEY = 'slow_social_drafts';
        this.db = localStorage; // Simulating local DB with localStorage for prototype
    }

    /**
     * Save a draft locally.
     * @param {string} content 
     */
    saveDraft(content) {
        const drafts = this.getAllDrafts();
        const newDraft = {
            id: Date.now(),
            content: content,
            timestamp: new Date().toISOString(),
            status: 'draft'
        };
        drafts.push(newDraft);
        this.db.setItem(this.STORAGE_KEY, JSON.stringify(drafts));
        console.log('Draft saved successfully.');
        return newDraft;
    }

    /**
     * Retrieve all drafts.
     */
    getAllDrafts() {
        const stored = this.db.getItem(this.STORAGE_KEY);
        return stored ? JSON.parse(stored) : [];
    }

    /**
     * Check if it is currently Sunday (UTC).
     * @returns {boolean}
     */
    isSunday() {
        const now = new Date();
        // 0 is Sunday in getUTCDay()
        return now.getUTCDay() === 0;
    }

    /**
     * Attempt to publish a draft.
     * Only allowed on Sundays.
     * @param {number} draftId 
     */
    publishDraft(draftId) {
        if (!this.isSunday()) {
            console.warn("It's not Sunday yet. Keep refining your ritual.");
            return { success: false, message: "Posting allowed only on Sundays." };
        }

        const drafts = this.getAllDrafts();
        const draftIndex = drafts.findIndex(d => d.id === draftId);

        if (draftIndex === -1) {
            return { success: false, message: "Draft not found." };
        }

        // In a real app, this would push to the backend.
        // For now, we update local status.
        drafts[draftIndex].status = 'published';
        drafts[draftIndex].publishedAt = new Date().toISOString();

        this.db.setItem(this.STORAGE_KEY, JSON.stringify(drafts));
        console.log(`Draft ${draftId} published!`);
        return { success: true, message: "Published successfully." };
    }
}

// Export for usage (if using modules) or attach to window
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DraftManager;
} else {
    window.DraftManager = DraftManager;
}
