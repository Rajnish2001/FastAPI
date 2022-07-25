from typing import List
from fastapi import FastAPI,Depends,status,Response,HTTPException
from .schemas import Blog,ShowBlog,User,ShowUser, ViewBlog
from .database import engine,SessionLocal
from .import models
from sqlalchemy.orm import Session
from sqlalchemy import delete,update
from .hashing import Hash



app = FastAPI(title='Database Connection with FastAPI')

#to create table
models.Base.metadata.create_all(bind=engine)

#databade instance
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close_all()

@app.post('/blog')
def blog(request:Blog,db:SessionLocal = Depends(get_db)):
    new_blog = models.Blog(title = request.title,blog = request.blog,creator_id = request.creator_id)
    db.add(new_blog)
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.get('/blog',response_model=List[ShowBlog])
def all_blog(db:SessionLocal=Depends(get_db)):
    blog_data = db.query(models.Blog).all()
    return blog_data

@app.get('/blog/{id}',response_model=ViewBlog)
def all_blog(id,db:SessionLocal=Depends(get_db)):
    blog_data = db.query(models.Blog).filter(models.Blog.id == id).first()
    return blog_data


@app.get('/blog/status/{id}',status_code=status.HTTP_201_CREATED)
def all_blog(id,response:Response,db:SessionLocal=Depends(get_db)):
    blog_data = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog_data:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail':f'id {id} is not available in our database'}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'id {id} is not available in our database')
    return blog_data

@app.delete('/blog/{id}')
def destroy(id,response:Response,db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id==id)
    if blog.first() is not None:
        blog.delete(synchronize_session=False)
        # del db[id]
        db.commit()
        raise HTTPException(status_code=status.HTTP_204_NO_CONTENT,detail=f'Blog id {id} is deleted')
        # response.status_code = status.HTTP_204_NO_CONTENT
        # return {'detail':f'Blog id {id} is deleted'}
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog id {id} is not available data in our database')


@app.put('/blog/{id}')
def update(id,request:Blog,db:SessionLocal=Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Blog id {id} is not found')
    # blog.update({'title':request.title,'blog':request.blog})
    blog.update(request.dict())
    db.commit()
    raise HTTPException(status_code=status.HTTP_202_ACCEPTED,detail=f'Blog id {id} is updated')


# pwd_cxt=CryptContext(schemes=["bcrypt"], deprecated="auto")#for password hashing
@app.post('/user',response_model=ShowUser,tags=['User'])
def create_user(request:User,db:SessionLocal=Depends(get_db)):
    # hashedPassword = pwd_cxt.hash(request.password) #hashed password
    new_user = models.User(name = request.name,email = request.email,password = Hash.bcrypt(request.password))
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get('/user',response_model=List[ShowUser],tags=['User'])
def show_user(db:SessionLocal=Depends(get_db)):
    user = db.query(models.User).all()
    return user

@app.get('/retrive/user/{id}',response_model=ShowUser,tags=['User'])
def show_user(id,db:SessionLocal=Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    return user

