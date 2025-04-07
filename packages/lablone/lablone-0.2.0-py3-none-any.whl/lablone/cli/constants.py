from pathlib import Path

from platformdirs import user_documents_dir

DEFAULT_ENV_VARIABLE = "GITLAB_ACCESS_TOKEN"

BASE_URL = "https://gitlab.com/api/v4"
REPOS_ENDPOINT = "/projects"

BASE_OUTPUT_FOLDER = Path(user_documents_dir()) / "Backups" / "Repos" / "GitLab"
ARCHIVE_FORMAT = "zip"
