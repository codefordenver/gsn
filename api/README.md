
# GSN-API instructions:

* download docker and create account
* install Homebrew (here I'm assuming that you're using a Macintosh)
* using Homebrew, install git

## Starting from scratch:
Now, inside your favorite shell (Mac users typically use Terminal), go to a directory of your choosing and clone git repo from 'gsn/api'

type the following command in the root directory (the directory that contains the Dockerfile)

```bash
docker-compose run web python /code/gsn-api/manage.py migrate
```

Next, type the following:

```bash
docker-compose up
```

Your local server should now be running and ready to accept connections. In order to load the dummy data, open up a separate tab in your shell, go to the same directory as before, and type the following command:

```bash
docker-compose exec gsn_web python /code/gsn_api/manage.py loaddata database_fixture.json
```


And that should do it! If you visit [http://127.0.0.1:8000/gsndb/district](http://127.0.0.1:8000/gsndb/district) in your browser you should encounter the district view for our REST API. It should be populated with the dummy data from our fixture file. 

Once you're done playing around, remember to delete your docker containers with the following command:
```bash
docker-compose down
```

This will kill the containers while retaining the docker images, so that if you want to access the instance of the gsn-api that you've been using, all you have to do is run `docker-compose-up` again.
If things didn't work out as planned, please refer to the trouble-shooting section.

## What to do if you're using a newer version of the gsn-api:
Under the current paradigm, if any changes are made to the gsn-api, you will need to create a new docker image to let these changes take effect. First, make sure that you aren't running any containers. Inside of your shell, cd to the directory that containst the gsn-api and type the following comand:

```bash
docker-compose down
```

Next, check if there are any docker images that you might wanna get rid of, in our case, that means getting rid of the obselete gsn-api docker images. To do this, you'll need to list the images with the following command:
```bash
docker images
```
You'll be presented with a list of entries in a table. Under the 'Repository' column, you should see our apis image with a name along the lines of 'gsn-api_web'. Git rid of it by copying the number within the 'Image ID' column and running the following command with that number in the ```<IMAGE ID>``` placeholder.
```bash
docker rmi <IMAGE ID>
```
___
#### I'm being harrased by a container that won't die...
Because you ran `docker-compose down` earlier, you shouldn't get any errors telling you that a container is running. If, for some reason, a container is still running you can delete it by following similar steps. First list the containers:
```bash
docker ps
```
And then delete the container by using the 'Container ID' number
```bash
docker rm <CONTAINER ID>
```

With that out of the way, you should be good to create another docker image with the most recent version of the gsn-api by following the steps in the first section.

### Things still aren't working!
For our project, we are storing any permenant changes made to the database locally. This is to allow any changes you make during development to persist. The up side of this is that you don't have to load the dummy data every time you create a container. The down side is that there is occasional disagreement between your local volumes and a newer version of gsn-api. To fix this, you can delete any and all volumes in local storage that aren't currently being used by containers with the following command:

**_Danger- Do not do this if you have other Docker projects that are using volumes!_**


```bash
docker volume prune
```
**_Instead, do this:_**

If you're the cautious type, you can identify the volume that is associated with gsn-api by typing the following command:
```bash
docker volume ls
```
And then remove it specifically by typing the following:
```bash
docker volume rm <VOLUME NAME>
```
## Interacting with the API:
Besides the many paths that can be used for retrieving lists and details of the gsn database. The most dynamic api view currently available allows the client to retrieve information on student **behavior**, **attendance**, and **grades**. To retrieve any of the three, simply include a JSON object in the request payload who's value is the student's first and last name. The following example uses HTTPie:

```bash
http POST http://127.0.0.1:8000/gsndb/student/attendance studentName="Alexander Glover"
```
Unfortunately, the API hasn't quite figured out middle names, so any information related to "Cloe White Thomas" will be inaccessible. This should hopefully be remedied within a week. I encourage anyone working on the front end to find other ways to break this style of path, as it is currently learning to walk and needs a good beating. 

An astute reader may be wondering why we're retrieving information with a POST request. This is because it is historically frowned upon to include data in the payload of a GET request that would then be parsed by the server. In our case, the sensitivity of the information being exchanged precludes transmission of certain parameters through the request url, consigning us to the constraints of the payload. Moreover, though HTTPS ensures URL encryption, the API wouldn't pass muster if it relied soley on SSL/TLS for basic security.

If this seems like a positively archaic perspective, I invite any and all dissenters to respectfully volunteer their opinions on the flowdock. Or perhaps create a ticket to address the issue in a seminary pow-wow. 


