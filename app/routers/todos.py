from fastapi import APIRouter
from ..models import TodoItemPatchSchema
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from ..dependencies import supabase

router = APIRouter(
	prefix="/todo"
)

@router.get('/')
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

@router.get('/{todo_id}/')
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

@router.patch('/item/{item_id}/')
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
@router.delete('/item/{item_id}/')
async def delete_todo_item(item_id: str):
	try:
		response = supabase.table("todoItems").update({"deleted": True}).eq("id", item_id).execute()
		return JSONResponse(
			content=response.data,
			status_code=200
		)
	except:
		raise HTTPException(
			status_code=500,
			detail="something went wrong"
		)