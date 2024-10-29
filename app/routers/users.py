from fastapi import APIRouter
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException

from ..models import Family

from ..dependencies import supabase

router = APIRouter(
    prefix="/user"
)

@router.get('/{uid}/families')
async def get_families(uid: str):
    try:
        data = supabase.table('families').select('*').eq('created_by', uid).execute()

        return JSONResponse(
            content=data.data, status_code=200
        )
    except:
        raise HTTPException(
            status_code=404,
            detail="no families associated with this user"
        )

@router.post('/{uid}/families')
async def create_family(uid: str, family: Family):
    try:
        response = supabase.table('families').insert({'created_by': uid, 'name': family.name}).execute()
        
        return JSONResponse(
			content=response.data,
			status_code=200
		)
    
    except:
        raise HTTPException(
            status_code=404,
            detail="something went wrong"
        )