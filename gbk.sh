#!/bin/bash
sync_dir=$(date +'%Y_%m_%d')
echo ${sync_dir}
watch -n 30  "rclone sync --update --verbose --transfers 30 --checkers 8 --contimeout 60s --local-no-check-updated  --timeout 300s --retries 3 --low-level-retries 10 --stats 1s "/home/jiechi/workspace/github/huya_scraper/${sync_dir}" "google-drive:MFen/${sync_dir}""
