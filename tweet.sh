#!/bin/bash

source keys.env
source venv/bin/activate

# Retry up to 10 times
for _ in {1..10}; do
python my_twitter_bot.py && break
sleep 3;
done