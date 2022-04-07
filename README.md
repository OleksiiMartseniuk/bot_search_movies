# Search Movies
`Telegram bot`

<hr>

 * aiogram
 * celery
 * redis
 * sqlalchemy

## Current features

<hr>

 * Request to api IMDB once a day to collect data
 * Bot
    * Сategory selection
    * Choice of action
        * All(Movie/TV)
        * Top 10(Movie/TV)
        * Random(Movie/TV)
 
## Instructions
1. ### Installations

Make sure to have python version 3 install on you pc or laptop.
<br>
**Clone repository**
<br>
`https://github.com/OleksiiMartseniuk/bot_search_movies.git`

2. ### Create Database
Run the file `src/database/create_db.py`

3. ### Run docker 

Create file `.env`

```
export API_KEY='You api_key IMDB'

export API_TOKEN='You api_token Telegram'
```

Run command: `docker-compose up --build`
