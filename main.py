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


def on_start():
    git.fetch_origin()
    start_msg = f"Starting git-tracker"
    for branch in BRANCHES:
        latest_hash = git.get_hash(branch)
        if not branch in hashes:
            start_msg += f"\n🌟 Started tracking for **{branch}** (current hash: *{latest_hash}*)"
            hashes[branch] = latest_hash
    notifier.send_notification(start_msg)


def cycle():
    git.fetch_origin()
    for branch in BRANCHES:
        latest_hash = git.get_hash(branch)
        if hashes[branch] != latest_hash:
            latest_commit_msg = git.get_latest_commit_message(branch)
            msg = f"🚀 Branch **{branch}** got updated (current hash: *{latest_hash}*\n"
            msg += f"```\n{latest_commit_msg}\n```"

            notifier.send_notification(msg)
            hashes[branch] = latest_hash

    time.sleep(CHECK_INTERVAL)


if __name__ == "__main__":
    on_start()
    while True:
        cycle()
