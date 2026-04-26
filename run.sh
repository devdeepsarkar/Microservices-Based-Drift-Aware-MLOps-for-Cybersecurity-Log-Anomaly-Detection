#!/bin/bash

echo "Activating virtual environment..."
source venv/bin/activate

echo "Starting FastAPI Backend..."
cd prediction_service
python app.py &
BACKEND_PID=$!
cd ..

echo "Waiting for backend to start..."
sleep 3

echo "Starting Streamlit Frontend..."
streamlit run frontend/app.py &
FRONTEND_PID=$!

echo "Both services are running!"
echo "Backend PID: $BACKEND_PID"
echo "Frontend PID: $FRONTEND_PID"
echo "Press Ctrl+C to stop both services."

# Trap Ctrl+C (SIGINT) to kill background processes
trap "echo 'Stopping services...'; kill $BACKEND_PID; kill $FRONTEND_PID; exit" SIGINT

wait
