from typing import Optional,Union
from fastapi import FastAPI,Query
from pydantic import BaseModel

app = FastAPI(
    title = "Learning FastAPI",
    description = "This is the first attempt",
    version = "0.1.0",
) #instance variable


# '/' means localhost Base url 
@app.get('/')
def first():
    return {'name':'Rajnish'}

@app.get('/about/')
def about():
    return {'data':{'name':'This is about page'}}


@app.get('/about/{id}')
def aboutid(id):
    return {'data':id}

@app.get('/aboutid/{id:int}')
def aboutid(id):
    return {'data':id}

@app.get('/published/')
def published(limit,publish:bool,sort:Optional[str]):
    if publish:
        return {'data':'50 comments limited'}
    return {'data':f'{limit} comments limited'}

#Request Body
#create model using base model
class Blog(BaseModel):
    title : str
    dis : str
    publish : Optional[bool]

@app.post('/requestblog/')
async def blog(request: Blog):
    return request


class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

@app.post("/items/")
async def create_item(item: Item):
    item_dict = item.dict()
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    return item_dict

# @app.put('/item/udate/{item_id}')
# def update_item(item_id:int,item:Item):
#     print(item.dict())
#     return {'item_id':item_id,**item.dict()}

#item updation  
@app.put('/item/udate/{item_id}')
def update_item(item_id:int,item:Item,q:Union[str,None]=None):
    result = {'item_id':item_id,**item.dict()}
    print(result)
    if q:
        result.update({'q':q})
    print('=======',result)
    return result



#Query Parameters and String Validations
@app.get("/items/query1/")
async def read_items(q: Union[str, None] = None):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

#Additional validation
@app.get("/items/query2/")
async def read_items(q: Union[str, None] = Query(default=None, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Use Query as the default value and Add more validations
@app.get("/items/query3/")
async def read_items(q: Union[str, None] = Query(default=None, min_length=3, max_length=50)):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results

# Add regular expressions
@app.get("/items/query4/")
async def read_items(q: Union[str, None] = Query(default=None, min_length=3, max_length=50, regex="^Rajnish$")):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if q:
        results.update({"q": q})
    return results
#How to Debug