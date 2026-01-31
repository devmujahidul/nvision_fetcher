#!/usr/bin/env python3
"""Download an M3U file and save it to disk.

Usage:
  python scripts/download_m3u.py --output nvision.m3u
  python scripts/download_m3u.py --url <URL> --output nvision.m3u

The downloader will read the URL from (in order):
 - the --url argument
 - the M3U_URL environment variable
 - the built-in default URL (the one you provided)

Exit status: 0 on success, non-zero on failure.
"""

import argparse
import os
import sys
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

# Template for the URL. Username/password are required unless --url is provided.
DEFAULT_URL_TEMPLATE = "http://starter.nvisionbd.net/get.php?username={username}&password={password}&type=m3u_plus&output=mpegts"


def download(url: str, out_path: str) -> bool:
    req = Request(url, headers={"User-Agent": "nvision-m3u-downloader/1.0"})
    try:
        with urlopen(req, timeout=30) as r:
            data = r.read()
            # Ensure parent dir exists
            os.makedirs(os.path.dirname(out_path) or '.', exist_ok=True)
            with open(out_path, "wb") as f:
                f.write(data)
        print(f"Saved {len(data)} bytes to {out_path}")
        return True
    except HTTPError as e:
        print(f"HTTP error: {e.code} {e.reason}", file=sys.stderr)
    except URLError as e:
        print(f"URL error: {e.reason}", file=sys.stderr)
    except Exception as e:
        print(f"Unexpected error: {e}", file=sys.stderr)
    return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Download an M3U file and save as nvision.m3u")
    parser.add_argument("--url", help="M3U URL (overrides environment/default)")
    parser.add_argument("--output", default="nvision.m3u", help="Output filename (default: nvision.m3u)")
    args = parser.parse_args()

    if args.url:
        url = args.url
    else:
        username = os.environ.get("M3U_USERNAME")
        password = os.environ.get("M3U_PASSWORD")
        if not username or not password:
            parser.print_usage()
            print("Error: M3U_USERNAME and M3U_PASSWORD environment variables must be set, or provide --url", file=sys.stderr)
            sys.exit(2)
        url = DEFAULT_URL_TEMPLATE.format(username=username, password=password)


    ok = download(url, args.output)
    sys.exit(0 if ok else 1)
