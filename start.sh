#!/bin/bash

echo "🔧 Installing dependencies..."

source venv/bin/activate
pip install -r requirements.txt

echo "🚀 Starting your agent..."
python borrower_agent.py &
python matcher_agent.py &
python lender_agent.py