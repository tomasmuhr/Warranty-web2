from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.config import settings
from app.database import get_db
from app.schemas import DatabaseInfo, MessageResponse, PurgeRequest
from app.utils import (
    allowed_backup_filename,
    export_database,
    purge_shops,
    purge_warranties,
    restore_database,
)

router = APIRouter(prefix="/database", tags=["database"])


@router.get("/info", response_model=DatabaseInfo)
def database_info():
    return DatabaseInfo(path=str(settings.database_path.resolve()))


@router.get("/export")
def database_export():
    if not settings.database_path.exists():
        raise HTTPException(status_code=404, detail="Database file not found")
    backup_path = export_database()
    return FileResponse(
        path=backup_path,
        filename=settings.db_name_backup,
        media_type="application/octet-stream",
    )


@router.post("/restore", response_model=MessageResponse)
async def database_restore(file: UploadFile = File(...)):
    if not file.filename or not allowed_backup_filename(file.filename):
        raise HTTPException(
            status_code=400,
            detail=f"Invalid backup filename. Expected {settings.db_name_backup}",
        )

    temp_path = settings.db_dir / f"upload_{settings.db_name_backup}"
    content = await file.read()
    temp_path.parent.mkdir(parents=True, exist_ok=True)
    temp_path.write_bytes(content)

    try:
        restore_database(temp_path)
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc)) from exc
    finally:
        temp_path.unlink(missing_ok=True)

    return MessageResponse(message="The database has been successfully restored.")


@router.post("/purge", response_model=MessageResponse)
def database_purge(payload: PurgeRequest, db: Session = Depends(get_db)):
    if payload.option in ("warranties", "both"):
        purge_warranties(db)
    if payload.option in ("shops", "both"):
        purge_shops(db)
    return MessageResponse(message="The database has been successfully purged.")
