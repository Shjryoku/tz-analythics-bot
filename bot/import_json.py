import sys
import os
import uuid
import json

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from datetime import datetime
from db import SessionLocal
from models import Video, VideoSnapshot
from logs.logger import logger

def parse_dt(value):
    if not value:
        return None
    return datetime.fromisoformat(value)


def import_json(json_file=None):
    if json_file is None:
        json_file = os.path.join(ROOT_DIR, "json_data", "videos.json")

    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    videos = data["videos"]
    
    with SessionLocal() as session:
        for vid in videos:
            try:
                # создаём таблицу видео
                video = Video(
                    id=uuid.UUID(vid["id"]),
                    creator_id=uuid.UUID(vid["creator_id"]),
                    video_created_at=datetime.fromisoformat(vid["video_created_at"]),
                    views_count=vid["views_count"],
                    likes_count=vid["likes_count"],
                    comments_count=vid["comments_count"],
                    reports_count=vid["reports_count"]
                )
                session.add(video)
                session.flush() # для получения video.id
                
                # создаём связанные снапшоты
                for snap in vid.get("snapshots", []):
                    snapshot = VideoSnapshot(
                        id=uuid.UUID(snap["id"]),
                        video_id=video.id,
                        snapshot_time=parse_dt(snap.get("created_at")),
                        views_count=snap["views_count"],
                        likes_count=snap["likes_count"],
                        comments_count=snap["comments_count"],
                        reports_count=snap["reports_count"],
                        delta_views_count=snap.get("delta_views_count", 0),
                        delta_likes_count=snap.get("delta_likes_count", 0),
                        delta_comments_count=snap.get("delta_comments_count", 0),
                        delta_reports_count=snap.get("delta_reports_count", 0)
                    )
                    session.add(snapshot)
                    
            except Exception as e:
                logger.error(f"Ошибка при импорте видео {vid.get('id')}: {e}")
                continue
                
        try:    
            session.commit()
        except Exception as e:
            logger.error(f"Ошибка при commit: {e}")
            raise

if __name__ == "__main__":
    import_json()
    print("Import finished")