#!/usr/bin/env python
# coding: utf-8

# Scores Headlines API
# Summer 2025 MLE
# Paul Pham

# In[2]:


import requests


# In[3]:


host = "localhost"
port = "8015"


# In[12]:


from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/status")
def status():
    return {"status": "OK"}


# In[16]:


import logging
import subprocess
import json
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List


# Configure log in library
logging.basicConfig(
    filename="api_service.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)


# FastAPI App
app = FastAPI()

class HeadlinesRequest(BaseModel):
    headlines: List[str]

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logging.info(f"Incoming request: {request.method} {request.url}")
    try:
        response = await call_next(request)
        logging.info(f"Request completed with status code {response.status_code}")
        return response
    except Exception as e:
        logging.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Internal server error"})

@app.get("/status")
def status():
    logging.info("Status check request received")
    return {"status": "OK"}

@app.post("/score_headlines")
def score_headlines(req: HeadlinesRequest):
    logging.info(f"Scoring headlines: {req.headlines}")

    try:
        # Run your score headlines model
        result = subprocess.run(
            ["./score_headlines"] + req.headlines,
            capture_output=True,
            text=True
        )

        # Check for errors in subprocess 
        if result.returncode != 0:
            logging.error(f"score_headlines failed: {result.stderr}")
            return JSONResponse(status_code=500, content={"error": "Model execution failed"})

        # Parse output
        try:
            output = json.loads(result.stdout)
            logging.info(f"Model output: {output}")
            return output
        except json.JSONDecodeError:
            logging.error(f"Invalid JSON from score_headlines: {result.stdout}")
            return JSONResponse(status_code=500, content={"error": "Invalid output format"})

    except FileNotFoundError:
        logging.critical("score_headlines executable not found")
        return JSONResponse(status_code=500, content={"error": "score_headlines not found"})
    except Exception as e:
        logging.error(f"Unexpected error: {str(e)}", exc_info=True)
        return JSONResponse(status_code=500, content={"error": "Unexpected error"})

