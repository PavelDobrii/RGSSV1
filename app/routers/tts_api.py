from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from ..deps import get_tts_service, api_key_auth
from ..schemas import TTSSynthesizeRequest
from ..services.tts_service import TTSService

router = APIRouter(prefix="/api/v1/tts", tags=["tts"])


@router.get("/by-id")
async def tts_by_id(rid: str = Query(...), poi: str = Query(...), service: TTSService = Depends(get_tts_service)):
    audio = service.get_cached(rid, poi)
    if not audio:
        raise HTTPException(status_code=404, detail="audio not found")
    return StreamingResponse(iter([audio]), media_type="audio/mpeg")


@router.post("/synthesize")
async def synthesize(req: TTSSynthesizeRequest, service: TTSService = Depends(get_tts_service), _: str = Depends(api_key_auth)):
    audio = service.synthesize(text=req.text, language_code=req.language_code, voice_name=req.voice_name)
    return StreamingResponse(iter([audio]), media_type="audio/mpeg")
