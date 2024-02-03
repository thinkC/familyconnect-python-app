from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from datetime import date, datetime, time, timedelta
from fastapi.middleware.cors import CORSMiddleware
from random import randrange


app = FastAPI()

# Add CORS middleware to allow requests from all origins
app.add_middleware(
    CORSMiddleware,
    # This allows all origins, you can customize it based on your needs
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

my_posts = [
    {
        "id": 1,
        "post_date": "2024-01-12",
        "post_desc": "This is a nice posts",
        "post_img": "img1.png",
        "user_id": 2
    },
    {
        "id": 2,
        "post_date": "2024-02-02",
        "post_desc": "This is psot 2",
        "post_img": "img1.png",
        "user_id": 1
    },
    {
        "id": 3,
        "post_date": "2024-01-17",
        "post_desc": "This is psot 3",
        "post_img": "img1.png",
        "user_id": 3
    },
]


class Post(BaseModel):
    post_date: datetime
    post_desc: str
    post_img: str
    user_id: int


# find a post
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p

# find post by index


def find_post_index(id):
    for i, p in enumerate(my_posts):
        if p["id"] == id:
            return i


@app.get("/posts")
def get_posts():
    return {"data": my_posts}


@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: Post):
    # print(post)
    post_dict = post.model_dump()
    post_dict['id'] = randrange(0, 1000000)
    my_posts.append(post_dict)
    # print(post.dict())
    # print(post.model_dump())
    print(post_dict)
    return {"data": post_dict}

# get a post


@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    # print(id)
    post = find_post(int(id))
    if not post:
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {"message": f"post with {id} not found!"}
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found!")
    return {"post": post}


# delete post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found!")
    my_posts.pop(index)
    # return {"message": "post was deleted succefully"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)


# update

@app.put("/posts/{id}")
def update_posts(id: int, post: Post):
    # print(post)
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found!")
    post_dict = post.model_dump()
    post_dict["id"] = id
    my_posts[index] = post_dict
    return {"data": post_dict}
