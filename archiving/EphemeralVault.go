package main

import (
	"flag"
	"fmt"
	"time"
)

// MockPost represents a social post
type MockPost struct {
	ID        int
	Content   string
	Published time.Time
	Status    string
}

// EphemeralVault manages the archiving of posts
type EphemeralVault struct {
	DryRun bool
	// In a real app, this would be a DB connection
	DB []MockPost
}

func NewEphemeralVault(dryRun bool) *EphemeralVault {
	// Initialize with some dummy data
	// Some posts from last Sunday, some from today
	now := time.Now().UTC()
	yesterday := now.Add(-24 * time.Hour)
	twoDaysAgo := now.Add(-48 * time.Hour)

	return &EphemeralVault{
		DryRun: dryRun,
		DB: []MockPost{
			{ID: 1, Content: "Old Sunday POst", Published: twoDaysAgo, Status: "public"},
			{ID: 2, Content: "Recent Post", Published: yesterday, Status: "public"},
			{ID: 3, Content: "Just Now", Published: now, Status: "public"},
		},
	}
}

// ArchiveOldPosts scans for posts older than 24h and archives them
func (v *EphemeralVault) ArchiveOldPosts() {
	fmt.Println("Starting Archive Scan...")
	cutoff := 24 * time.Hour
	now := time.Now().UTC()

	for i, post := range v.DB {
		if post.Status == "public" {
			age := now.Sub(post.Published)
			if age > cutoff {
				v.archive(i)
			}
		}
	}
}

func (v *EphemeralVault) archive(index int) {
	post := v.DB[index]
	if v.DryRun {
		fmt.Printf("[DRY-RUN] Would archive post ID %d (Age: %s): %s\n", post.ID, time.Since(post.Published), post.Content)
	} else {
		// Update status in "DB"
		v.DB[index].Status = "archived"
		fmt.Printf("[ARCHIVED] Post ID %d moved to private vault.\n", post.ID)
	}
}

func main() {
	dryRun := flag.Bool("dry-run", false, "Simulate archiving without changing state")
	flag.Parse()

	vault := NewEphemeralVault(*dryRun)
	vault.ArchiveOldPosts()
}
