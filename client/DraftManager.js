/**
 * DraftManager.js
 * Manages local draft storage and enforces the Sunday posting rule.
 * Part of Slow Social: Le Rituel du Dimanche
 */
class DraftManager {
    constructor() {
        this.STORAGE_KEY = 'slow_social_drafts';
        this.db = localStorage;
        this.demoMode = false;
    }

    /**
     * Enable/disable demo mode (bypasses time restrictions)
     */
    setDemoMode(enabled) {
        this.demoMode = enabled;
        console.log(`Demo mode: ${enabled ? 'ON' : 'OFF'}`);
    }

    /**
     * Save a draft locally.
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
     * Get only published capsules.
     */
    getPublished() {
        return this.getAllDrafts().filter(d => d.status === 'published');
    }

    /**
     * Get only pending drafts.
     */
    getPendingDrafts() {
        return this.getAllDrafts().filter(d => d.status === 'draft');
    }

    /**
     * Check if it is currently Sunday AND after 18:00 UTC.
     */
    isSunday() {
        if (this.demoMode) return true;

        const now = new Date();
        const isSundayDay = now.getUTCDay() === 0;
        const isAfter18 = now.getUTCHours() >= 18;
        return isSundayDay && isAfter18;
    }

    /**
     * Get time remaining until next Sunday 18:00 UTC.
     */
    getTimeUntilSunday() {
        const now = new Date();
        let target = new Date(now);

        const dayOfWeek = now.getUTCDay();
        const daysUntilSunday = dayOfWeek === 0 ? 0 : (7 - dayOfWeek);
        target.setUTCDate(target.getUTCDate() + daysUntilSunday);
        target.setUTCHours(18, 0, 0, 0);

        if (dayOfWeek === 0 && now.getUTCHours() >= 18) {
            target.setUTCDate(target.getUTCDate() + 7);
        }

        const diff = target - now;
        return {
            total: diff,
            days: Math.floor(diff / (1000 * 60 * 60 * 24)),
            hours: Math.floor((diff % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60)),
            minutes: Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60)),
            seconds: Math.floor((diff % (1000 * 60)) / 1000)
        };
    }

    /**
     * Attempt to publish a draft.
     * Only allowed on Sundays after 18:00 UTC (or demo mode).
     */
    publishDraft(draftId) {
        if (!this.isSunday()) {
            console.warn("It's not Sunday yet. Keep refining your ritual.");
            return { success: false, message: "Publication uniquement le dimanche à 18h00 UTC." };
        }

        const drafts = this.getAllDrafts();
        const draftIndex = drafts.findIndex(d => d.id === draftId);

        if (draftIndex === -1) {
            return { success: false, message: "Brouillon introuvable." };
        }

        drafts[draftIndex].status = 'published';
        drafts[draftIndex].publishedAt = new Date().toISOString();

        this.db.setItem(this.STORAGE_KEY, JSON.stringify(drafts));
        console.log(`Draft ${draftId} published!`);
        return { success: true, message: "Capsule publiée avec succès !" };
    }

    /**
     * Clear all drafts (for testing).
     */
    clearAll() {
        this.db.removeItem(this.STORAGE_KEY);
        console.log('All drafts cleared.');
    }
}

// Export for usage
if (typeof module !== 'undefined' && module.exports) {
    module.exports = DraftManager;
} else {
    window.DraftManager = DraftManager;
}
