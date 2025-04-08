from .webserv.apirequest import default_request_handler
from .webserv.apirequest import stream_request_handler
from .webserv.apirequest import SimpleRequest
from .webserv.apirequest import ErrorResult

from fastapi.responses import StreamingResponse
from fastapi import APIRouter, Query
from fastapi.responses import StreamingResponse
from typing import AsyncIterator
from .authprovider import AuthPermission
appmain=None
router = APIRouter()
import os

@router.post("/request/login")
async def login_route(data:SimpleRequest):return await default_request_handler(data,login)

@router.post("/request/check_login")
async def check_login(data:SimpleRequest):return await default_request_handler(data,check_login)


@router.post("/request/get_project_list")
async def get_project_list(data:SimpleRequest):return await default_request_handler(data,get_project_list)

@router.post("/request/get_study_list")
async def get_study_list(data:SimpleRequest):return await default_request_handler(data,get_study_list)

@router.post("/request/get_study_list_ids")
async def get_study_list_ids(data:SimpleRequest):return await default_request_handler(data,get_study_list_ids)

@router.post("/request/get_study")
async def get_study(data:SimpleRequest):return await default_request_handler(data,get_study)



async def check_login(data,parent):
    global appmain
    session_data=appmain.session_manager.get_session(data["token"])
    if not session_data:return {}
    return {"username":session_data["username"]}

async def login(data,parent):
    global appmain
    if not await appmain.auth.needs_credentials():
        result= await appmain.auth.authenticate(appmain)
        if result is None:
            return ErrorResult("Invalid username or password")
        
        session_token =  appmain.session_manager.create_session(data=result)
        return {"token":session_token,"username":result["username"]}
    return ErrorResult("Invalid username or password")


async def get_project_list(data,parent):
    global appmain
    session_data=appmain.session_manager.get_session(data["token"])
    if not session_data:return ErrorResult("Not logged in")

    ret = []
    for project in appmain.projects.values():
        ret.append(project.to_dict())
    return ret

async def get_study_list(data,parent):
    global appmain
    session_data=appmain.session_manager.get_session(data["token"])
    if not session_data:return ErrorResult("Not logged in")
    project = appmain.projects[data["project"]]   
    return await project.get_study_list_async(data,session_data)

async def get_study_list_ids(data,parent):
    global appmain
    session_data=appmain.session_manager.get_session(data["token"])
    if not session_data:return ErrorResult("Not logged in")
    project = appmain.projects[data["project"]]   
    return await project.get_study_list_async(data,session_data,id_only=True,limit=100000)



async def get_study(data,parent):
    global appmain
    session_data=appmain.session_manager.get_session(data["token"])
    if not session_data:return ErrorResult("Not logged in")
    project = appmain.projects[data["project"]]   
    return await project.get_study_async(data)