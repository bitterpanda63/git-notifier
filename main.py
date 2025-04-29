import configparser
import os
import time

from git import GitController
from messaging.discord import DiscordNotifier

# Read configuration from config.ini
config = configparser.ConfigParser()
config_path = os.path.join(os.path.dirname(__file__), 'config.ini')
config.read(config_path)

# Configuration
git = GitController(config.get('settings', 'REPO_PATH'))
notifier = DiscordNotifier(config.get('settings', 'DISCORD_WEBHOOK_URL'))
CHECK_INTERVAL = config.getint('settings', 'CHECK_INTERVAL')
BRANCHES = [config.get('branches', key) for key in config['branches']]

# Storage
hashes = dict()


def cycle():
    git.fetch_origin()
    for branch in BRANCHES:
        latest_hash = git.get_hash(branch)

        if not branch in hashes:
            notifier.send_notification(f"🌟 Started tracking for **{branch}** (current hash: *{latest_hash}*)")
            hashes[branch] = latest_hash

        if hashes[branch] != latest_hash:
            latest_commit_msg = git.get_latest_commit_message(branch)
            msg = f"🚀 Branch **{branch}** got updated\n"
            msg += f"* Latest Hash: *{latest_hash}*\n"
            msg += f"* Latest Commit Message: *{latest_commit_msg}*"

            notifier.send_notification(msg)
            hashes[branch] = latest_hash

    time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    while True:
        cycle()
