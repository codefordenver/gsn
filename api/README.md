GSN-API instructions:
download docker and create account
install Homebrew (here I'm assuming that you're using a Macintosh)
using Homebrew, install git
Starting from scratch:
Now, inside your favorite shell (Mac users typically use Terminal), go to a directory of your choosing and clone git repo from 'HTempleman/gsn-api' (Soon to be GSN/gsn-api hopefully!)

type the following command in the root directory (the directory that contains the Dockerfile)

docker-compose run web python /code/gsn-api/manage.py migrate
Next, type the following:

docker-compose up
Your local server should now be running and ready to accept connections. In order to load the dummy data, open up a separate tab in your shell, go to the same directory as before, and type the following command:

docker-compose exec web python /code/gsn-api/manage.py loaddata firstfixture.json
And that should do it! If you visit http://127.0.0.1:8000/gsndb/district in your browser you should encounter the district view for our REST API. It should be populated with the dummy data from our fixture file.

Once you're done playing around, remember to delete your docker containers with the following command:

docker-compose down
This will kill the containers while retaining the docker images, so that if you want to access the instance of the gsn-api that you've been using, all you have to do is run docker-compose-up again. If things didn't work out as planned, please refer to the trouble-shooting section.

What to do if you're using a newer version of the gsn-api:
Under the current paradigm, if any changes are made to the gsn-api, you will need to create a new docker image to let these changes take effect. First, make sure that you aren't running any containers. Inside of your shell, cd to the directory that containst the gsn-api and type the following comand:

docker-compose down
Next, check if there are any docker images that you might wanna get rid of, in our case, that means getting rid of the obselete gsn-api docker images. To do this, you'll need to list the images with the following command:

docker images
You'll be presented with a list of entries in a table. Under the 'Repository' column, you should see our apis image with a name along the lines of 'gsn-api_web'. Git rid of it by copying the number within the 'Image ID' column and running the following command with that number in the <IMAGE ID> placeholder.

docker rmi <IMAGE ID>
I'm being harrased by a container that won't die...
Because you ran docker-compose down earlier, you shouldn't get any errors telling you that a container is running. If, for some reason, a container is still running you can delete it by following similar steps. First list the containers:

docker ps
And then delete the container by using the 'Container ID' number

docker rm <CONTAINER ID>
With that out of the way, you should be good to create another docker image with the most recent version of the gsn-api by following the steps in the first section.

Things still aren't working!
For our project, we are storing any permenant changes made to the database locally. This is to allow any changes you make during development to persist. The up side of this is that you don't have to load the dummy data every time you create a container. The down side is that there is occasional disagreement between your local volumes and a newer version of gsn-api. To fix this, you can delete any and all volumes in local storage that aren't currently being used by containers with the following command:

Danger- Do not do this if you have other Docker projects that are using volumes!

docker volume prune
Instead, do this:

If you're the cautious type, you can identify the volume that is associated with gsn-api by typing the following command:

docker volume ls
And then remove it specifically by typing the following:

docker volume rm <VOLUME NAME>
