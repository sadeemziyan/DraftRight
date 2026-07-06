#!/bin/bash
streamlit run frontend/app.py --server.port $PORT --server.address 0.0.0.0
chmod +x start_frontend.sh