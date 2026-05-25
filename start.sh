#!/bin/sh

uvicorn api.main:app --host 0.0.0.0 --port 8000 &

python -m streamlit run clients/streamlit_app.py --server.port 8501 --server.address 0.0.0.0