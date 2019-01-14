

GSN-API instructions:

* download docker and create account
* install Homebrew (here I'm assuming that you're using a Macintosh)
* using Homebrew, install git

Now, go to a directory of your choosing and clone git repo from 'gsn/api'

type the following command in the root directory (with the Dockerfile)

```bash
docker-compose run web python /code/gsn-api/manage.py migrate
```

Next, type the following:

```bash
docker-compose up
```

And that should do it! If you visit `127.0.0.1:8000/gsndb/district` in your browser you should encounter the district view for our REST API. 
