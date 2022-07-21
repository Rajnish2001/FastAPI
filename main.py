from fastapi import FastAPI

app = FastAPI() #instance variable


# '/' means localhost Base url 
@app.get('/')
def first():
    return {'name':'Rajnish'}