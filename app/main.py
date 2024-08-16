from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

'''**************************************************************************************'''
#mongo db related begin

import datetime
import pymongo
from pymongo import MongoClient
#client = MongoClient()
#client = MongoClient("mongodb://127.0.0.1:27017/")
#client = MongoClient("0.0.0.0", 27017) # need to change 

MONGODB_URI =  os.getenv("MONGODB_URI")
MONGODB_NAME =  os.getenv("MONGODB_NAME")
MONGODB_COLLECTION_NAME =  os.getenv("MONGODB_COLLETION_NAME")
# function to set up the db connection 
    

# function to insert a payload
def insertrecord(blogentry):
    try:
        # attempt to connect to db 
        client = MongoClient(MONGODB_URI)
        # initialize db
        db = client[MONGODB_NAME]
        # initialize collection
        blogentrycollection = db[MONGODB_COLLECTION_NAME]

        #insert the record and return success message {"message":"success"}        
        
        #blogentry_id = blogentrycollection.insert_one(blogentry).inserted_id
        blogentry.update(insertdate = datetime.datetime.now(tz=datetime.timezone.utc),isActive = True)        
        blogentrycollection.insert_one(blogentry)
        return {"message":"success"}
        
    except Exception as e:
        # if error send an error message {"message":"failed"}
        return {"errormessage":str(e)}
    

# function to return records
def getblogentrybytitle(blogentrytitleasstring):
    try:
        #if record is available then return else return no records found 
        # attempt to connect to db 
        client = MongoClient(MONGODB_URI)
        # initialize db
        db = client[MONGODB_NAME]
        # initialize collection
        blogentrycollection = db[MONGODB_COLLECTION_NAME]

        records = blogentrycollection.find({"blogtitle":blogentrytitleasstring}, {'_id': 0})
        listofrecords = list(records)
        numberofrecords = len(listofrecords)
        if numberofrecords>0:
            return {"query":blogentrytitleasstring,"number of posts found":numberofrecords,"posts":listofrecords}
        else:
            return {"query":blogentrytitleasstring,"number of posts found":0,"posts":[]}       
        
    except Exception as e:
        # if error send an error message {"message":"failed"}
        return {"errormessage":str(e)}


#mongo db related end
'''**************************************************************************************'''

'''**************************************************************************************'''
# api related begin
class blogentry(BaseModel):
    blogtitle: str
    description: str
    tags: str
    author: str 

app = FastAPI()


@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}


@app.post("/saveblogentry/")
async def create_blogentry(blogentry: blogentry):
    try:
        blogentry_dict = blogentry.dict() # convert this explicitly to change it into a dict 
        response = insertrecord(blogentry_dict)
        return response
    except Exception as e:
        return {"message":"request exception"}

@app.get("/getblogentries")
def getentries(q: Union[str, None] = None):
    try:        
        return getblogentrybytitle(q)
    except Exception as e:
        return {"message":"request exception"}
# api related end    
'''**************************************************************************************'''