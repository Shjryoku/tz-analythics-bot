<h1>Telegram Analytics Bot</h1>

<p>Бот для Telegram, который принимает текстовые запросы на естественном языке и возвращает статистику по видео и видео-снапшотам из базы данных PostgreSQL через LLM (Ollama).</p>

<h2>1. Установка</h2>
<ol>
    <li>Клонируйте репозиторий:
        <pre><code>git clone &lt;https://github.com/Shjryoku/tz-analythics-bot&gt;
cd &lt;https://github.com/Shjryoku/tz-analythics-bot&gt;</code></pre>
    </li>
    <li>Создайте виртуальное окружение и активируйте его:
        <pre><code>python -m venv venv
# Windows
venv\Scripts\activate
# Linux / MacOS
source venv/bin/activate</code></pre>
    </li>
    <li>Установите зависимости:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
</ol>

<h2>2. Настройка переменных окружения</h2>
<p>Создайте файл <code>.env</code> в корне проекта на основе .env.example:</p>
<pre><code>POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password

TELEGRAM_BOT_TOKEN=your_telegram_bot_token

OLLAMA_URL=http://localhost:11434/api/generate
OLLAMA_MODEL=your_model_name

APP_ENV=local</code></pre>

<h2>3. Инициализация базы данных</h2>
<p>Создайте таблицы Video и VideoSnapshot:</p>
<pre><code>python init_db.py</code></pre>

<p>Импорт тестовых данных (опционально):</p>
<pre><code>python import_json.py</code></pre>
<p>По умолчанию используется файл <code>json_data/videos.json</code></p>

<h2>4. Запуск бота</h2>
<pre><code>python bot/main.py</code></pre>
<ul>
    <li>Бот будет слушать новые сообщения через polling</li>
    <li>Старые апдейты Telegram удаляются автоматически</li>
</ul>

<h2>5. Примеры запросов</h2>
<h3>1. Сколько всего видео?</h3>
<pre><code>Сколько всего видео есть в системе?</code></pre>
<pre><code>{
  "entity": "videos",
  "metric": null,
  "aggregation": "count",
  "filters": {
    "creator_id": null,
    "views_gt": null,
    "date_from": null,
    "date_to": null
  }
}</code></pre>

<h3>2. Сколько видео набрало больше 1000 просмотров?</h3>
<pre><code>Сколько видео набрало больше 1000 просмотров?</code></pre>
<pre><code>{
  "entity": "videos",
  "metric": "views",
  "aggregation": "count",
  "filters": {
    "creator_id": null,
    "views_gt": 1000,
    "date_from": null,
    "date_to": null
  }
}</code></pre>

<h3>3. Суммарный прирост просмотров за 28 ноября 2025</h3>
<pre><code>На сколько просмотров в сумме выросли все видео 28 ноября 2025?</code></pre>
<pre><code>{
  "entity": "video_snapshots",
  "metric": "views",
  "aggregation": "sum",
  "filters": {
    "creator_id": null,
    "views_gt": null,
    "date_from": "2025-11-28",
    "date_to": "2025-11-28"
  }
}</code></pre>

<h2>6. Логирование ошибок</h2>
<p>Ошибки сохраняются в папку <code>logs</code> в файл:</p>
<pre><code>logs/errors.log</code></pre>
<p>Логи ротационные: максимальный размер файла 1 КБ, сохраняется 1 резервная копия</p>

<h2>7. Зависимости</h2>
<pre><code>aiogram>=2.25,&lt;3.0
SQLAlchemy>=2.0
psycopg2-binary>=2.9
python-dotenv>=1.0
requests>=2.31</code></pre>

<h2>8. Примечания</h2>
<ul>
    <li>Бот работает через Ollama LLM, поэтому локальный сервер Ollama должен быть доступен по <code>OLLAMA_URL</code>.</li>
    <li>Все даты возвращаются в формате <code>YYYY-MM-DD</code>.</li>
    <li>Фильтры <code>creator_id</code> и <code>views_gt</code> применяются при необходимости.</li>
</ul>

</body>
</html>
