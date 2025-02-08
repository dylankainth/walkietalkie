from fastapi import FastAPI

app = FastAPI()

@app.get("/pyapi")
def hello_world():
    return {"message": "Hello World", "api": "Python"}

@app.get("/pyapi/test")
def test():
    return {"message": "Test"}