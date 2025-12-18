from sqlalchemy import func
from bot.models import Video, VideoSnapshot

def execute_query(
    parsed: dict,
    session
) -> int:
    if "error" in parsed:
        raise ValueError(parsed["error"])
    
    entity = parsed["entity"]
    metric = parsed["metric"]
    aggregation = parsed["aggregation"]
    filters = parsed.get("filters", {})
    
    # определяем таблицу по запросу
    if entity == "videos":
        query = session.query(Video)
        date_field = Video.video_created_at
    elif entity == "video_snapshots":
        query = session.query(VideoSnapshot)
        date_field = VideoSnapshot.snapshot_time
    else:
        raise ValueError("unknown_entity")
    
    # фильрация по создателю
    creator_id = filters["creator_id"]
    if creator_id:
        if entity == "videos":
            query = query.filter(Video.creator_id == creator_id)
        else:
            query = query.join(Video).filter(Video.creator_id == creator_id)
    
    # фильтрация по просмотрам
    if filters.get("views_gt") and entity == "videos":
        query = query.filter(Video.views_count > filters["views_gt"])
    
    # фильтрация по дате
    if filters.get("date_from"):
        query = query.filter(date_field >= filters["date_from"])
    
    if filters.get("date_to"):
        query = query.filter(date_field <= filters["date_to"])
    
    # агрегации
    if aggregation == "count":
        return query.count()
    
    if aggregation == "distinct_count":
        if entity == "video_snapshots":
            return query.with_entities(func.count(func.distinct(VideoSnapshot.video_id))).scalar()
        elif entity == "videos":
            return query.with_entities(func.count(func.distinct(Video.id))).scalar()
        else:
            raise ValueError("unsupported_entity_distinct")
    
    if aggregation == "sum":
        # определяем колонку для суммы
        column_map = {
            ("videos", "views"): Video.views_count,
            ("videos", "likes"): Video.likes_count,
            ("videos", "comments"): Video.comments_count,
            ("videos", "reports"): Video.reports_count,
            ("video_snapshots", "views"): VideoSnapshot.delta_views_count,
            ("video_snapshots", "likes"): VideoSnapshot.delta_likes_count,
            ("video_snapshots", "comments"): VideoSnapshot.delta_comments_count,
            ("video_snapshots", "reports"): VideoSnapshot.delta_reports_count,
        }
        
        column = column_map.get((entity, metric))
        if not column:
            raise ValueError("unsupported_metric")
        
        return query.with_entities(func.coalesce(func.sum(column), 0)).scalar()
    
    raise ValueError("unsupported_aggregation")