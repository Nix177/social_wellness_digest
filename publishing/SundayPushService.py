import datetime
import time
import argparse
import os
import shutil

class SundayPushService:
    def __init__(self, dry_run=False):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.digest_path = os.path.join(self.base_dir, "weekly_digest.html")
        self.archive_dir = os.path.join(self.base_dir, "archiving")
        
        self.dry_run = dry_run
        self.TARGET_HOUR = 18  # 18:00 UTC (Sunday)

        # Ensure archive dir exists
        if not os.path.exists(self.archive_dir):
            os.makedirs(self.archive_dir)

    def is_push_time(self):
        now = datetime.datetime.utcnow()
        # Sunday is 6
        is_sunday = now.weekday() == 6
        is_time = now.hour == self.TARGET_HOUR
        return is_sunday and is_time

    def publish(self):
        if not os.path.exists(self.digest_path):
            print(f"[WARN] No digest found at {self.digest_path}")
            return

        timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H%M%S")
        archive_name = f"digest_{timestamp}.html"
        archive_path = os.path.join(self.archive_dir, archive_name)

        print(f"[{datetime.datetime.utcnow()}] Publishing Digest...")

        if self.dry_run:
            print(f"[DRY-RUN] Would archive to: {archive_path}")
        else:
            try:
                shutil.copy2(self.digest_path, archive_path)
                print(f"[SUCCESS] Digest published/archived to: {archive_path}")
                # Optional: Here you would trigger an email API or upload to S3
            except Exception as e:
                print(f"[ERROR] Failed to archive digest: {e}")

    def run(self, force=False):
        print("Starting Sunday Push Service...")
        print(f"Monitoring: {self.digest_path}")
        
        if force:
            print("[FORCE] Ignoring schedule, publishing immediately.")
            self.publish()
            return

        while True:
            if self.is_push_time():
                print("It is Sunday 18:00 UTC! Releasing the capsule...")
                self.publish()
                # Sleep enough to not double-publish in the same hour
                time.sleep(3600) 
            else:
                # print(f"Waiting... (Current UTC: {datetime.datetime.utcnow()})")
                time.sleep(60) # check every minute

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--force", action="store_true", help="Force publish immediately")
    parser.add_argument("--dry-run", action="store_true", help="Don't perform actual writes")
    args = parser.parse_args()

    service = SundayPushService(dry_run=args.dry_run)
    service.run(force=args.force)
