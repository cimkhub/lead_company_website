1) Activate virutel environment: python -m venv venv
2) Activate virtual environment: source venv/bin/activate
3) Install requirmenets: pip install -r requirements.txt
4) Add .env with Open_AI_Key -> OPENAI_API_KEY = ".."
5) Start FastAPI with uvicorn main:app --host 127.0.0.1 --port 8000
6) Start ngrok connection: ngrok http 8000
7) Backend-Endpoint can be access via https://.....ngrok-free.app/scrape_and_analyze [enter your link]
