#!/usr/bin/env bash

export PULP_FILE_PR_NUMBER=$(echo $COMMIT_MSG | grep -oP 'Required\ PR:\ https\:\/\/github\.com\/pulp\/pulp_file\/pull\/(\d+)' | awk -F'/' '{print $7}')

cd ..
git clone --depth=1 https://github.com/pulp/pulp_file.git
if [ -n "$PULP_FILE_PR_NUMBER" ]; then
  cd pulp_file
  git fetch --depth=1 origin +refs/pull/$PULP_FILE_PR_NUMBER/merge
  git checkout FETCH_HEAD
  cd ..
fi

pip install --upgrade --force-reinstall ./pulp_file
cd pulp-certguard
