<h1>Telegram Analytics Bot</h1>

<p>A Telegram bot that accepts natural language text queries and returns statistics on videos and video snapshots from a PostgreSQL database via an LLM (Ollama).</p>

<h2>1. Installation</h2>
<ol>
    <li>Clone the repository:
        <pre><code>git clone &lt;https://github.com/Shjryoku/tz-analythics-bot&gt;
cd &lt;https://github.com/Shjryoku/tz-analythics-bot&gt;</code></pre>
    </li>
    <li>Create and activate a virtual environment:
        <pre><code>python -m venv venv
# Windows
venv\Scripts\activate
# Linux / MacOS
source venv/bin/activate</code></pre>
    </li>
    <li>Install dependencies:
        <pre><code>pip install -r requirements.txt</code></pre>
    </li>
</ol>

<h2>2. Environment Variables Setup</h2>
<p>Create a <code>.env</code> file in the project root based on .env.example:</p>
<pre><code>POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=your_db
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password

TELEGRAM_BOT_TOKEN=your_telegram_bot_token

OLLAMA_URL=[http://localhost:11434/api/generate](http://localhost:11434/api/generate)
OLLAMA_MODEL=your_model_name

APP_ENV=local</code></pre>

<h2>3. Database Initialization</h2>
<p>Create the Video and VideoSnapshot tables:</p>
<pre><code>python init_db.py</code></pre>

<p>Import test data (optional):</p>
<pre><code>python import_json.py</code></pre>
<p>By default, the file <code>json_data/videos.json</code> is used</p>

<h2>4. Running the Bot</h2>
<pre><code>python bot/main.py</code></pre>
<ul>
    <li>The bot listens for new messages via polling</li>
    <li>Old Telegram updates are automatically cleared</li>
</ul>

<h2>5. Example Queries</h2>
<h3>1. How many videos are there in total?</h3>
<pre><code>How many videos are there in the system?</code></pre>
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

<h3>2. How many videos have more than 1000 views?</h3>
<pre><code>How many videos have more than 1000 views?</code></pre>
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

<h3>3. Total view growth on November 28, 2025</h3>
<pre><code>What is the total increase in views across all videos on November 28, 2025?</code></pre>
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

<h2>6. Error Logging</h2>
<p>Errors are saved in the <code>logs</code> folder in the file:</p>
<pre><code>logs/errors.log</code></pre>
<p>Logs are rotated: maximum file size is 1 KB, with 1 backup copy retained</p>

<h2>7. Dependencies</h2>
<pre><code>aiogram>=2.25,&lt;3.0
SQLAlchemy>=2.0
psycopg2-binary>=2.9
python-dotenv>=1.0
requests>=2.31</code></pre>

<h2>8. Notes</h2>
<ul>
    <li>The bot works via the Ollama LLM, so a local Ollama server must be available at <code>OLLAMA_URL</code>.</li>
    <li>All dates are returned in <code>YYYY-MM-DD</code> format.</li>
    <li>Filters <code>creator_id</code> and <code>views_gt</code> are applied when needed.</li>
</ul>
