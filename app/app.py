from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def welcome():
    x = {"message": "HELLO WORLD!!! Welcome to fastAPI!!"}
    return x
