import uvicorn
from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
from supabase import create_client, Client
from gotrue.errors import AuthApiError
from models import LoginSchema, SignUpSchema, TodoItemPatchSchema


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

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")

supabase: Client = create_client(url, key)




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
	
		return JSONResponse(
			content={
				"id": data.user.id,
				"email": data.user.email,
				"aud": data.user.aud,
				"meta_data": data.user.user_metadata
			}, status_code=200
		)
	except:
		raise HTTPException(
			status_code=400,
			detail="invalid credentials"
		)
	
@app.get('/todo')
async def get_todos():
	try:
		data = supabase.table('todos').select('*, category:category(title), item_count: todoItems(count)').execute()
	
		return JSONResponse(
			content=data.data, status_code=200
		)
	except:
		raise HTTPException(
			status_code=404,
			detail="todo lists not found"
		)

@app.get('/todo/{todo_id}/')
async def get_todo(todo_id: str):
	try:
		data = supabase.table('todos').select('*, category:category(title), items: todoItems!inner(id, title, completed)').eq('id', todo_id).eq('todoItems.deleted', False).single().execute()
		
		
		return JSONResponse(
			content=data.data,
			status_code=200
		)
	except:
		raise HTTPException(
			status_code=404,
			detail="todo not found"
		)

@app.patch('/todo/item/{item_id}/')
async def update_todo_item(item_id: str, value: TodoItemPatchSchema):
	try:
		response = (supabase.table('todoItems').update({"completed": value.completed}).eq("id", item_id).execute())
		return JSONResponse(
			content=response.data,
			status_code=200
		)
	except:
		raise HTTPException(
			status_code=500,
			detail="something went wrong"
		)

if __name__ == "__main__":
	uvicorn.run("main:app",reload=True)