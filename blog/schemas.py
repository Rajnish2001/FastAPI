from typing import List
from unicodedata import name
from pydantic import BaseModel


class Blog(BaseModel):
    title : str
    blog : str
    creator_id : int
    
class ViewBlog(BaseModel):
    title : str
    blog : str
    class Config():
        orm_mode = True


class ShowBlog(BaseModel):
    title: str
    blog : str
    creator_id : int

    class Config():
        orm_mode = True


class User(BaseModel):
    name : str
    email : str
    password : str




class ShowUser(BaseModel):
    id : int
    name : str
    email : str
    blogs : List[ViewBlog] = []

    class Config():
        orm_mode = True