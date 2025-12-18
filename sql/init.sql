CREATE TABLE IF NOT EXISTS videos (
    id UUID PRIMARY KEY,
    creator_id UUID NOT NULL,
    video_created_at TIMESTAMP NOT NULL,
    views_count BIGINT DEFAULT 0 CHECK (views_count >= 0),
    likes_count BIGINT DEFAULT 0 CHECK (likes_count >= 0),                 
    comments_count BIGINT DEFAULT 0,
    reports_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS video_snapshots (
    id UUID PRIMARY KEY,
    video_id UUID NOT NULL REFERENCES videos(id) ON DELETE CASCADE,
    snapshot_time TIMESTAMP NOT NULL,
    views_count BIGINT NOT NULL,
    likes_count BIGINT NOT NULL,
    comments_count BIGINT NOT NULL,
    reports_count BIGINT NOT NULL,
    delta_views_count BIGINT DEFAULT 0,
    delta_likes_count BIGINT DEFAULT 0,
    delta_comments_count BIGINT DEFAULT 0,
    delta_reports_count BIGINT DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


-- Индексы для оптимизации запросов
CREATE INDEX IF NOT EXISTS idx_videos_creator_id                -- Фильтр по автору
ON videos(creator_id);

CREATE INDEX IF NOT EXISTS idx_videos_video_created_at          -- Фильтр по датам
ON videos(video_created_at);

CREATE INDEX IF NOT EXISTS idx_video_snapshots_snapshot_time    -- Поиск снапшотов по времени
ON video_snapshots(snapshot_time);

CREATE INDEX IF NOT EXISTS idx_video_snapshots_video_id         -- Поиск всех снапшотов для видео
ON video_snapshots(video_id);

CREATE INDEX IF NOT EXISTS idx_videos_creator_id_published      -- Поиск видео автора за диапазон дат
ON videos(creator_id, video_created_at);

CREATE INDEX IF NOT EXISTS idx_video_snapshots_delta_views      -- Отсмотр прироста
ON video_snapshots(delta_views_count);