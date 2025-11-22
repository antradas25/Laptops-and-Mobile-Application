#!/bin/bash
# Helper script to push to GitHub
# Usage: ./push.sh YOUR_PERSONAL_ACCESS_TOKEN

if [ -z "$1" ]; then
    echo "Usage: ./push.sh YOUR_PERSONAL_ACCESS_TOKEN"
    echo ""
    echo "To create a token:"
    echo "1. Go to https://github.com/settings/tokens"
    echo "2. Generate new token (classic)"
    echo "3. Select 'repo' scope"
    echo "4. Copy the token and use it here"
    exit 1
fi

TOKEN=$1
git remote set-url origin https://preet7777777:${TOKEN}@github.com/preet7777777/laptops.git
git push origin main
git remote set-url origin https://github.com/preet7777777/laptops.git

echo "✅ Push completed!"

