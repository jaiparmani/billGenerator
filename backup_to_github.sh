#!/bin/bash

cd /home/jaiparmani411/billGenerator || exit 1

git add .

# Exit if nothing changed
git diff --cached --quiet && exit 0

git commit -m "Automatic backup $(date '+%Y-%m-%d %H:%M:%S')"

git push origin master
