This is split into 4 sections:

A. Step by step instructions for how to download the file with git, how to run docker, and how to upload back into git

B. Your very first contribution to the project!

C. Next contributions...

D. Overview of Docker & download

# A. Step by step instructions for GitHub & Docker
First you will create a local repository. Then you will add code. Then you will get Docker up and running. Then you may need to go into the container. Then you exit Docker. Then you uplaod the changes to GitHub.

#### How to create local repository
1. First you need to get a local repository from GitHub. In your command line, clone gsn.

****IF YOU ARE ON WINDOWS****
```git
git clone https://github.com/codefordenver/gsn.git --config core.autocrlf=false
```
****otherwise you can simply type****
```git
git clone https://github.com/codefordenver/gsn.git
```
2. Next, we need to decide what branch we are working on. Change directories into the gsn repository and then get a list of all branches available.
````git
cd gsn
git branch -a
````
3. Of this list, you need to decide which one best fits your task.  For example, if you are working on creating a Django model, you should use new_models. (Ask for help if you aren't sure).

To switch to the branch you want the following:
````git
git checkout <BRANCH YOU WANT TO USE>
````
4. Then, off of this branch create a new one by typing the following command
````git
  git checkout -b <YOUR BRANCH NAME>
````

#### Go and add to the code
1. Open the code in your file directory and add to the code.

#### Get Docker up and running
1. In your command line, change the current working directory to the folder that has the docker-compose.yml file (gsn > api).

2. In your command line, now run 
````git
docker-compose up
````
Give it time to run. This file is running a script that will automatically make new migrations & migrate any new models.

3. You can check to see if your code is up and running by going to a web browser and typing localhost:80/<PATH>. For example, localhost:80/gsndb/student.
****If you are on Windows****
type 192:168:99:100/80/<PATH>. For example, 192:168:99:100/80/gsndb/student.
  
#### If you need to get into a container
1. If you need to get into the database container, type into a new command line
````git
docker-compose exec db bash
````
If you need to get into the web container, type into a new command line
````git
docker-compose exec gsn_web sh
````

From either of these you can run commands. For example, in the database container you could type in 
````git
psql -U postgres
````
to be able to access postgresql commands.

2. If you need to get out of a container, simply type 
````git
exit
````

#### If you need to get out of Docker
1. Unfortunately, you will have to close out of Docker and reopen every time you make a change. In order to close it down, stop the docker-compose up command by typing CTR-C. Then type
````git
docker-compose down
````
in the command line.

#### If you are ready to upload changes to GitHub
1. First you need to see what changes have been made. In your command line type
````git
git status
````
This will tell you what has been added/deleted/modified.

2. Now you need to stage changes & commit. There should be on commit per file that was added/deleted/modified. Type
````git
git add <FILE PATH>
````
This staged the change from that file.

3. To create a commit for this file, type in the command line
````git
git commit -m "Put your comments about this change here"
````

4. If you are editing a different branch, you are going to need to fetch and merge. This is to ensure you have the most up to code and aren't overwriting what someone has recently added. To do this

````git
git fetch
````

````git
git merge
````

Then do a push request. Type in the command line
````git
git remote add origin https://github.com/codefordenver/gsn.git
````
and then
```git
git push -u origin <BRANCH NAME> 
```
Type in your username and password for GitHub.

5. Go to your branch on github.com/codefordenver/gsn/tree/<BRANCH NAME>.
 
6. Click the green button "Compare and Pull Request".

7. Compare base (the file you found that was similar to what you were doing, eg new_models) to compare (the branch you created). Fill in a description of what you did and push "Create Pull Request".

# B. Your very first contribution to the project!
For your first contribution, you are going to add your name to the bottom of this ABOUTME.md

1. Using A (above), pull the master branch. Switch to a branch named add_my_name (if it isn't created, create it). 

2. Open the ABOUTME.md in gsn/api. Type your name at the bottom.

3. Follow the instructions from A (above) to fetch, merge, and push. (Don't forget to fetch and merge or you may write over someone else's name!)

4. Congrats! You've contributed!

# C. Next contributions...
1. Next we will add more contributions. We currently have needs/tasks split under the Issues tab https://github.com/codefordenver/gsn/issues. You can filter it by "backend" or "frontend". Within "backend" you can filter it by "beginner" tasks, "medium" tasks, and "difficult" tasks. If this is your first time adding or you are still trying to get comfortable with the project, choose a "beginner" task.

2. Make sure the task isn't yet assigned to anybody. If it isn't and you are interested in the task, assign yourself to it.

3. Make sure to follow A (above) for basic structure of how to pull the project into a local repository, how to run docker, and how to push it back to github.

4. When you are done with a task, mark it as complete. Feel free to ask any questions you have and don't feel intimidated! We have people ranging from beginner to not beginner on this project!

# D. Overview of Docker & Download- GSN-API instructions:

* download docker and create account
* install Homebrew (here I'm assuming that you're using a Macintosh)
* using Homebrew, install git

## Starting from scratch:
Now, inside your favorite shell (Mac users typically use Terminal), go to a directory of your choosing and clone git repo from 'codefordenver/gsn'

type the following command in the root directory (the directory that contains the Dockerfile)

```bash
docker-compose run gsn_web python /code/gsn_api/manage.py migrate
```

Next, type the following:

```bash
docker-compose up
```

Your local server should now be running and ready to accept connections. In order to load the dummy data, open up a separate tab in your shell, go to the same directory as before, and type the following command:

```bash
docker-compose exec gsn_web python /code/gsn_api/manage.py loaddata new_models_fixture.json	
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


## Instructions for admin users updating the server:

Once you have been given access and read/write/docker permissions to the development server, you will be capable of integrating changes tht have been made into the codebase so that frontend developers can interact with the most up-to-date version of the api! 

#### Updating The Server From the Master Branch:
*First, make sure you are in the /home/gsn/ directory*
```bash
git pull origin master
cd api
docker-compose down
docker rmi api_gsn_web
docker-compose -f docker-compose.yml -f docker-compose-prod.yml up -d
```

And that should be it! If the api doesn't go live after a minute or so, you may need to destroy and rebuild the api_gsn_web image once more. For reasons that should be apparent to me, but aren't nonetheless, it occasionally takes multiple image builds to get the container up and running. This odd behavior should likely be posted as an issue in need of resolution...

Another point: We should probably get around to hosting our images on docker-hub. Our current implementation is a little ad-hoc. 

