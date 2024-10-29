
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from gotrue.errors import AuthApiError
from app.models import LoginSchema, SignUpSchema

from .routers import todos, users
from .dependencies import supabase


app = FastAPI(
	descrption="this is the REST API for HomeSync",
	title="Firebase API",
	docs_url="/"

)
origins = [
	"http://localhost",
	"http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(todos.router)
app.include_router(users.router)






@app.post('/signup')
async def create_account(user_data:SignUpSchema):

	credentials = {
    "email": user_data.email,
    "password": user_data.password,
	"options": {
		"data": {
			"first_name": user_data.first_name,
			"last_name": user_data.last_name,
		}
	}
  }

	try:
		user = supabase.auth.sign_up(credentials)

		return JSONResponse(content={"message": f"User account created successfully", "status_code": 200})
	except AuthApiError:
		raise HTTPException(
			status_code=400,
			detail= f"Account already exists for email {user_data.email}"
		)


@app.post('/login')
async def create_access_token(user_data:LoginSchema):
	credentials = {
    "email": user_data.email,
    "password": user_data.password
  }

	try:
		data = supabase.auth.sign_in_with_password(credentials)
		family = supabase.table('families').select('*').eq('created_by', data.user.id).execute()

		return JSONResponse(
			content={
				"id": data.user.id,
				"email": data.user.email,
				"aud": data.user.aud,
				"meta_data": data.user.user_metadata,
				"families": family.data,
				"access": data.session.access_token
			}, status_code=200
		)
	except:
		raise HTTPException(
			status_code=400,
			detail="invalid credentials"
		)
	