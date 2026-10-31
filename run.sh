#!/usr/bin/env bash
echo "==================================================================="
echo "  Smart Inventory & Dead Stock Management System"
echo "==================================================================="
echo ""
echo "Installing requirements..."
pip install -r requirements.txt
echo ""
echo "Launching application on http://127.0.0.1:5000 ..."
python3 main.py
