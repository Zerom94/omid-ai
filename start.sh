#!/bin/bash
python3 smart_router.py &
uvicorn web_ui:app --host 0.0.0.0 --port 8000
