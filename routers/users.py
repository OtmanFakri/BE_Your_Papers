import os
from dotenv import load_dotenv
from fastapi import APIRouter
from fastapi import HTTPException
from schemes.auth.requests import Sign_in as form_Sign_in
from schemes.auth.requests import Sign_up as form_Sign_up
from supabase import Client
from supabase import create_client

load_dotenv()

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supa: Client = create_client(url, key)
router = APIRouter(
    prefix="/user",
    tags=["user"],
)


@router.post("/sign_in")
def sign_in(pyload: form_Sign_in):
    try:
        res = supa.auth.sign_in_with_password(
            {
                "email": pyload.email,
                "password": pyload.password,
            }
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"{e}")


@router.post("/sign_up")
def sign_up(pyload: form_Sign_up):
    try:
        res = supa.auth.sign_up(
            {
                "email": pyload.email,
                "password": pyload.password,
                "options": {"data": {"display_name": pyload.display_name}},
            }
        )
        return res
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"{e}")


@router.post("/sign_out")
def sign_out():
    return supa.auth.sign_out()