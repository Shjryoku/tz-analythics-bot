CREATE TABLE IF NOT EXISTS videos (
    id BIGINT PRIMARY KEY,                                  -- Уникальный ID видео
    creator_id BIGINT NOT NULL,                             -- ID автора видео
    video_created_at TIMESTAMP NOT NULL,                    -- Дата и время публикации
    views_count BIGINT DEFAULT 0 CHECK (views_count >= 0),  -- Кол-во просмотров
    likes_count BIGINT DEFAULT 0 CHECK (likes_count >= 0),  -- Кол-во лайков                    
    comments_count BIGINT DEFAULT 0,                        -- Кол-во комментариев
    reports_count BIGINT DEFAULT 0,                         -- Кол-во репортов
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,         -- Время создания
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP          -- Время последнего обновления
);

CREATE TABLE IF NOT EXISTS video_snapshots (
    id BIGSERIAL PRIMARY KEY,                                               -- Уникальный ID снапшота
    video_id BIGINT NOT NULL REFERENCES videos(id) ON DELETE CASCADE,       -- Ссылка на видео
    snapshot_time TIMESTAMP NOT NULL,                                       -- Время замера
    views_count BIGINT NOT NULL,                                            -- Просмотры на момент замера
    likes_count BIGINT NOT NULL,                                            -- Лайки на момент замера
    comments_count BIGINT NOT NULL,                                         -- Комментарии на момент замера
    reports_count BIGINT NOT NULL,                                          -- Репорты на момент замера
    delta_views_count BIGINT DEFAULT 0,                                     -- Прирост просмотров
    delta_likes_count BIGINT DEFAULT 0,                                     -- Прирост лайков
    delta_comments_count BIGINT DEFAULT 0,                                  -- Прирост комментариев
    delta_reports_count BIGINT DEFAULT 0,                                   -- Прирост репортов
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,                         -- Время создания записи
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP                          -- Время последнего обновления
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