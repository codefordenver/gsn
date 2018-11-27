# Generation Schools Network
##
The aim of this project is to provide a maintainable and navigable database that should aid social workers in providing assistance to at-risk youth. 

## Goals & Features:
GSN should enable social workers to monitor student metrics as they change. Ideally, we will achieve this by piping data directly from [Infinite Campus](https://www.infinitecampus.com/). In the unlikely event that we are unable to pull student data from Infinite Campus, we will need to conceive a **_very_** user friendly system in which CSV files are uploaded to be parsed by our API.

In terms of usability, social workers should have access to their own profiles that will be set up upon registration, which can then be used to personalize their own simple dashboard of specific students, schools, districts, etc. 

Finally, the fun part for the frontend will lie in the data visualization. When we get there, we'll likely use D3 in the absence of a better suggestion. 

For the time being, here is a simple flowchart that should indicate the technologies at play. The REST API will interact with the database using the Django ORM (Python stuff), whereas React will interact with Django REST through JSON objects passed through HTTP requests. 

---

![alt text](https://i.imgur.com/KICVtCf.png)

---

## A Brief (non-technical) Technical Overview:
Any moderately complex website can be broken down into two main components:
1. A side that interacts with users, often called the frontend.
2. A side that interacts with data, often called the backend. 

GSN will be moderately complex, so both the frontend and backend should use robust technologies that can accommodate the needs of the project as it scales. 

* For the frontend, we are using [React](https://reactjs.org/ "Official React Website"), a popular Javascript library developed by Facebook. 

* To structure our backend, we are using the [Django REST framework](https://www.django-rest-framework.org/ "Official Django REST Website"), a tool that enables developers to quickly create Restful API's that can pass requests between user and database with ease. 

* For our database, we will be using [PostgreSQL](https://www.postgresql.org/ "Official PostgreSQL Website"), a Relational Database that is well liked for its extensibility.

* For both the REST API and our database, we will use [Docker](https://www.docker.com/why-docker "Official Docker Website") containers, as they should make it easier for new developers to jump on the project. 

Every step of the way, we are making use of open source technologies, meaning they are freely available to the general public. 

## Developer Guide:
###### This guide should hopefully be far simpler once things are properly containerized.
If you are interested in contributing to GSN, that's fantastic! As the project grows, there will be many opportunities for developers to jump on board and contribute their thoughts and skills, regardless of expertise or background. But before you can do anything, you'll need to set things up on your computer! 
##### A note: This quickstart is written for Unix environments (Linux/Mac OS). It can be modified to accomodate Windows users as the need arises. 

### For Mac:
These instructions are mostly lifted from a wondeful breakdown posted by Lisa Tagliaferri on [DigitalOcean](https://www.digitalocean.com/community/tutorials/how-to-install-python-3-and-set-up-a-local-programming-environment-on-macos), though they diverge once the concern shifts to establishing a virtual environment. If, at any point, you encounter an error, I'd suggest you search the error on Google and seek out an answer to your problem on StackOverflow or a germane message board. 

#### Install Xcode:
Open your preferred command shell (Terminal is default on Mac), and check that you have Xcode before you do anything else.

```shell
xcode-select -p 
```

After pressing enter, the following line should be displayed in your shell if Xcode is installed. 

```shell
/Library/Developer/CommandLineTools
```

If you don't see that, then go ahead and install Xcode by [downloading](https://itunes.apple.com/us/app/xcode/id497799835?mt=12&ign-mpt=uo%3D2) it from the Mac app store.

#### Install HomeBrew:
Now you'll want to install [Homebrew](https://brew.sh/ "Official Homebrew Website"), a wonderful package manager for Mac.
```shell
/usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

After Homebrew is installed, create/open your `~/.bash_profile` with the following command:
```shell
vim ~/.bash_profile
```
###### If you're checking this against the guide I referenced earlier, you'll notice that I'm using Vim instad of nano. Treat this as a small indulgence on my part- a fleeting moment of unmitigated opinion. If you opt for nano, things will still work swimmingly...

Now that you're inside the `~/.bash_profile` configuration file, press the `i` key to insert text, and type the following:

```shell 
export PATH=/usr/local/bin:$PATH
```

By including this line in `~/.bash_profile`, you are allowing bash to prioritize the directory that houses Homebrew when it searches for packages installed by Homebrew, such as `'pipenv`, instead of wasting time poring over a bunch of directories located elsewhere in your computer and potentially calling the wrong program!

Save your changes in vim by typeing `:wq` (write, quit) and type the following once you are back in your shell:

```
source ~/.bash_profile
```

Now BASH has updated it's configuration without the need to restart. Check that Homebrew was set up correctly by running the following:

``` shell
brew doctor
```

If Homebrew is set up correctly, you should get a response saying as much. If things aren't working right, copy and paste your error message into Google. 

#### Install Python:

Run the following command in your shell:

``` brew install python```
This should install the newest version of python on your computer and save it to the homebrew directory, it may take a few minutes. 

##### A note on Python versions:
###### For the time being, we will try to use the newest version of Python with the GSN website so as to keep things simple for those who are unfamiliar with modifying PATH environment variables in BASH. 

#### Install Pipenv:
[Pipenv](https://pipenv.readthedocs.io/en/latest/ "Pipenv Documentation") is a python virtual environment manager, essentially a combination of Ruby's Gemfile and Python's Virtualenv. It's wonderful. We've gotten most of the initial setup out of the way, so installing Pipenv should be easy!
```bash
brew install pipenv
```

#### Install Postgres:
You may be detecting a pattern:
``` bash
brew install postgres
```

#### Clone the repository from Github:
Install Git using Homebrew if you don't have it already. 
```bash
brew install git
```
With Git, a version control system for managing projects with multiple contributers, you can easily retrieve GSN from a remote repository and make modifications to it locally on your computer. In our case, the remote repository is located on Github. 

Go to a directory of your choosing, maybe one entitled 'projects'. Once there, clone the remote repository from `codefordenver/gsn` with the following command:
```bash 
git clone git@github.com:codefordenver/gsn.git
```

Now you should have the GSN website's project directory in a folder entitled 'gsn'. Now type `cd gsn` to enter the gsn project folder and type the following command to install all of the python dependencies with pipenv.
``` shell
pipenv install
```

If everything installs without a hitch, you should be able to start your virtual environment with the following commande:
``` shell
pipenv shell
```

#### Ensure that the settings.py folder agrees with your postgres instance:
We're near the end of the tunnel. The final step we need to take before we get our local server up and running involves wiring up a Postgres instance that can work properly alongside our django project. If you open up the ```settings.py``` file inside of the gsn app (confusingly nested within two other ```gsn``` project folders) you can scroll down and see the database configuration for our Django project:

``` shell
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'gsndb',
        'USER': 'gsn',
        'PASSWORD': 'gsn.gsnsecrets.db_password',
        'HOST': 'localhost',
        'PORT': '',
    }
}
```

A quick read of this configuration suggests that our django project expects to connect to a Postgres database instance named ```gsndb``` that is owned by a user ```gsn```. But, you also might notice that there is a password stored in a python file entitled ```gsnsecrets```. This is a precaution to ensure that whatever password is used to access the database cannot be swiped by some malefactor intent on misusing student data to meet his/her/their own nefarious ends! With all this in mind, let's set up our database to agree with the configuration presented above.

1. Enter the Postgres shell by typeing ```psql``` in your BASH shell and create a user named gsn and give that user a password of your own choosing.
``` shell
CREATE USER gsn WITH PASSWORD 'yourpassword';
```
2. Now go ahead and create a database named ```gsndb``` that is owned by our newly created user:
``` shell
CREATE DATABASE gsndb WITH OWNER gsn;
```
3. Finally, exit the Postgres shell and create a file named ```gsnsecrets.py``` in the same directory as the settings.py file. Inside the file, instantiate a variable called ```db_password``` and assign it a string value corresponding to the password you chose for the gsn user.
``` shell
db_password = 'yourpassword';
```
And that should do it. As per the password field in the database configuration of our settings.py, Django will search for the ```gsnsecrets.py``` file that you just created and use the value stored in ```db_password``` to access the ```gsndb``` Postgres database instance. 

###### If you were carefully reading through the settings.py file, you may have noticed that there is another field entitled ```SECRET_KEY``` that accepts a value from our gsnsecrets.py file. You will need this for authentication purposes soon enough. For the moment things will work up to a point without it.  

#### Run the server, see if things are working as they should.
At this point, you should be able to view the website on your local server by going into the gsn Django project folder and running the following commands:
``` shell
npm run dev
python manage.py runserver
```
You should see the following:
``` shell
Django version 2.1.3, using settings 'gsn.settings'
Starting development server at http://127.0.0.1:8000/
Quit the server with CONTROL-C.
```
If you see that, everything is working! You can visit the url address for the development server and you'll see a very bare bones incarnation of the gsn website. Much of the interactivity will be limited until you're given the SECRET_KEY that Django employs for authenticating users, but you should at least see a landing page. If, on the other hand, you get an error, then there was likely some hitch along the way that resulted from improper configuration or improper instruction (the latter being my fault). Don't worry, setting things up can be onerous. Attempt to solve the problem on your own by following the errors wherever they might lead you. If you find yourself running up against a brick wall, don't be afraid to reach out to a fellow team member! As the saying goes, Rome wasn't built in a day.




[![Stories Ready to Work On](https://badge.waffle.io/codefordenver/gsn.svg?label=ready&title=Cards%20Ready%20To%20Work%20On)](https://waffle.io/codefordenver/gsn)

This repo was created from https://cfd-new.herokuapp.com. Use [the Waffle board](https://waffle.io/codefordenver/gsn) for this repo to always know what to do next for your project!
