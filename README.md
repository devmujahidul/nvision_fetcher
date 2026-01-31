# nvision M3U Auto-Downloader ✅

This repo contains a small Python script and a GitHub Actions workflow that download the provided M3U file daily and save it as `nvision.m3u` in the repository root.

## Files

- `scripts/download_m3u.py` — Python downloader. It will use the URL in this order:
  1. `--url` argument
  2. `M3U_URL` environment variable
  3. built-in default URL (the one you provided)

- `.github/workflows/download-m3u.yml` — runs daily and commits the downloaded `nvision.m3u` back to the repo when it changes.

## Setup

1. (Required) Add repository secrets `M3U_USERNAME` and `M3U_PASSWORD`. Go to Settings -> Secrets and variables -> Actions -> New repository secret to add them. The workflow will fail if these secrets are not set.

2. The workflow runs once per day by schedule. You can also run it manually from the Actions tab (workflow_dispatch).

3. To run locally:

```bash
python scripts/download_m3u.py --output nvision.m3u
# or
M3U_URL="<your url>" python scripts/download_m3u.py --output nvision.m3u
```

## Notes

- The script uses only the standard library (no external dependencies).
- The script builds the URL from `M3U_USERNAME` and `M3U_PASSWORD` environment variables and will exit with an error if either is missing (set them as repository secrets in Actions for security).
- The workflow uses `GITHUB_TOKEN` to push changes back to the repo.

If you'd like, I can also add tests, logging improvements, or rotate the cron schedule to match your timezone. 🔧
