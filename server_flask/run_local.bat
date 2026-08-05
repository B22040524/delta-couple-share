@echo off
py -m venv .venv
call .venv\Scripts\activate
pip install -r requirements.txt
set PUBLIC_BASE_URL=http://127.0.0.1:8080
python app.py
