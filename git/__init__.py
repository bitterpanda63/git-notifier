import subprocess


class GitController:
    def __init__(self, directory):
        self.directory = directory

    def fetch_origin(self):
        try:
            subprocess.run(
                ['git', '-C', self.directory, 'fetch', 'origin'],
                check=True
            )
        except subprocess.CalledProcessError as e:
            print(f"Error fetching from origin: {e}")

    def get_hash(self, branch_name):
        try:
            result = subprocess.run(
                ['git', '-C', self.directory, 'rev-parse', branch_name],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting latest commit hash: {e}")
            return None
    def get_latest_commit_message(self, branch_name):
        try:
            result = subprocess.run(
                ['git', '-C', self.directory, 'log', '-1', '--pretty=%B', branch_name],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except subprocess.CalledProcessError as e:
            print(f"Error getting latest commit message: {e}")
            return "Unknown commit message"