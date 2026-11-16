"""
PetVision AI - Server Runner
Launches the FastAPI application via Uvicorn.
"""

import sys
import os

# Ensure project root is in python path
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

import uvicorn

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    print(f"======================================================")
    print(f"   PetVision AI - Animal Species Recognition Server   ")
    print(f"   Listening on: http://localhost:{port}              ")
    print(f"======================================================")
    uvicorn.run("app:app", host="127.0.0.1", port=port, reload=False, log_level="info")
