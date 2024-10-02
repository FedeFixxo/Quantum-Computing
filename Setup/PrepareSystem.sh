#!/bin/bash

pip install -r requirements.txt

echo "Libraries installed!"

if command -v python 2>&1 >/dev/null
then
    pyton SaveAccount.py
    exit 0
fi

if command -v python3 2>&1 >/dev/null
then
    python3 SaveAccount.py
    exit 0
fi

echo "Something went wrong, try to execute SaveAccount.py manually :("
exit 1