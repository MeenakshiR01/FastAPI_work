from fastapi import FastAPI, Form, HTTPException
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from typing import Dict

app = FastAPI()

class Item(BaseModel):
    name: str

items: Dict[int, Item] = {}

@app.get("/", response_class=HTMLResponse)
def read_root():
    return """<html>
              <head>
                <title>FastAPI Website</title>
                <style>
                  body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                  h1 { color: #3498db; }
                  p { font-size: 18px; }
                  a { text-decoration: none; color: #2ecc71; font-weight: bold; }
                  form { margin-top: 20px; }
                  input, button { padding: 10px; margin-top: 10px; }
                </style>
              </head>
              <body>
                <h1>Welcome to Webpage</h1>
                <p>This is a simple webpage containing HTML and CSS code. Also, it is built with FastAPI.</p>
                <a href="/api">Go to API Endpoint</a>
                <br><br>
                <form action="/submit" method="post">
                  <input type="text" name="name" placeholder="Enter your name" required>
                  <button type="submit">Submit</button>
                </form>
              </body>
              </html>"""

@app.get("/api")
def api_endpoint():
    return {"message": "Hello from my FastAPI!"}

@app.post("/submit")
def submit_form(name: str = Form(...)):
    return {"message": f"Hello, {name}! Welcome to my FastAPI webpage."}

