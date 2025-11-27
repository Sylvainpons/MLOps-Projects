#!/bin/bash
source .venv/bin/activate
streamlit run src/main.py --server.address 192.168.1.149 --server.port 8501
