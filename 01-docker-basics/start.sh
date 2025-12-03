#!/bin/bash
source .venv/bin/activate
streamlit run src/main.py --server.address 0.0.0.0 --server.port 8501
