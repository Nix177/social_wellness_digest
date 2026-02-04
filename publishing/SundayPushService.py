import datetime
import time
import argparse

# Mock Redis client for demonstration
class MockRedis:
    def __init__(self):
        self.queue = [
            {"id": 101, "content": "Sunday Ritual #1", "user": "alice"},
            {"id": 102, "content": "Quiet moments...", "user": "bob"}
        ]

    def lpop(self, queue_name):
        if self.queue:
            return self.queue.pop(0)
        return None

    def llen(self, queue_name):
        return len(self.queue)

class SundayPushService:
    def __init__(self, dry_run=False):
        self.redis = MockRedis()
        self.queue_name = "ready_to_publish"
        self.dry_run = dry_run
        self.TARGET_HOUR = 18  # 18:00 UTC

    def is_push_time(self):
        now = datetime.datetime.utcnow()
        # Check if it's Sunday (0=Monday, 6=Sunday)
        # Python datetime.weekday(): Monday is 0, Sunday is 6.
        # Requirements said Sunday.
        is_sunday = now.weekday() == 6
        is_time = now.hour == self.TARGET_HOUR
        
        # For demo purposes, we might want to relax this or just log it
        return is_sunday and is_time

    def process_queue(self):
        print(f"[{datetime.datetime.utcnow()}] Checking queue...")
        
        while self.redis.llen(self.queue_name) > 0:
            item = self.redis.lpop(self.queue_name)
            if item:
                self.publish(item)
            else:
                break
    
    def publish(self, item):
        if self.dry_run:
            print(f"[DRY-RUN] Would publish: {item['content']} by {item['user']}")
        else:
            print(f"[PUBLISH] Live: {item['content']} by {item['user']}")
            # Here we would do the actual DB write / API call

    def run(self):
        print("Starting Sunday Push Service...")
        if self.dry_run:
            print("Mode: DRY-RUN (Will not actually publish)")
            # Force run for testing
            self.process_queue()
            return

        while True:
            if self.is_push_time():
                print("It is Sunday 18:00 UTC! Releasing the capsule...")
                self.process_queue()
                # Sleep to avoid re-triggering immediately within the same hour/minute logic
                # For robust cron, we'd sleep longer or use a scheduler lib
                time.sleep(3600) 
            else:
                print(f"Not time yet. Current UTC: {datetime.datetime.utcnow()}")
                time.sleep(60) # check every minute

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--test", action="store_true", help="Run in test mode (ignore time check)")
    parser.add_argument("--dry-run", action="store_true", help="Don't perform actual writes")
    args = parser.parse_args()

    service = SundayPushService(dry_run=args.dry_run)
    
    if args.test:
        print("Test mode enabled: Ignoring time check, processing queue immediately.")
        service.process_queue()
    else:
        service.run()
