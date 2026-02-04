#!/bin/bash

echo "==================================="
echo "Starting Stable MySQL AI Chatbot"
echo "==================================="

# Check if MySQL is running
if ! command -v mysql &> /dev/null; then
    echo "Warning: MySQL command not found. Please ensure MySQL is installed and running."
fi

# Check if database exists
echo "Checking database..."
mysql -u root -prootroot -e "CREATE DATABASE IF NOT EXISTS chatbot_ai;" 2>/dev/null || {
    echo "Note: Could not auto-create database. Please create 'chatbot_ai' database manually."
}

# Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating virtual environment..."
source venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo ""
echo "Starting server on http://localhost:8000"
echo "Press Ctrl+C to stop"
echo ""

cd backend
python main.py
