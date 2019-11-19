# gsn
An application to assist social workers in monitoring k-12 student performance. 

## ALERT: Domain Name expiration / HTTP Server EOL:
The gsndev.com domain expired on 11/04/2019. The gsn-api.com domain will expire on 11/24/2019. The server that hosts the api will also be deactivated on 11/24/2019. As the code for the API is readily available on Github, it should be relatively trivial to spin up another server. I recommend DigitalOcean, or maybe just a Raspberry with a DDNS Cloudflare rig to keep costs down. Of course there's Heroku too!

Hopefully someone will come along and find this project worthy of dusting off! :smiley:

## Setting up your project from GitHub:

To get things going quickly, it will be easiest if your local repo is a clone of the remote repo at codefordenver/gsn. Git has an elegant command to achieve just that:

```git
git clone https://github.com/codefordenver/gsn.git
```

You should now have a copy of the remote repo, along with all of it's branches, on your local machine. Now, type the following to determine the total branches that exist within the codefordenver/gsn repo at a given moment:

```git
git branch
```

You should see a list of branches, with an asterisk next to the word 'master', indicating that you are currently on the master branch. You can check out other branches with an aptly named command. Type the following to explore the 'new_models' branch:

```
git checkout new_models
```

If you're curious about the differences between two branches, you can use the diff command. Let's try that with the master branch and the new_models branch.

```git
git diff master new_models
```

The output will have plus signs next to lines which are absent from the master branch, indicating that they have been added within the new_models branch. Likewise, leading minus signs indicate that something present in the master branch has been deleted in the new_models branch. If you reverse the branch order of the previous command (`git diff new_models master`) you will see a correspondent inversion of plus and minus signs. This is because the latter example has us seeing changes from the master branch's perspective instead of the new_models perspective. If this seems confusing, just remember that the order in which you list branches after calling `git diff` determines the perspective of changes.

If you've gotten this far, you are likely serious about contributing to codefordenver/gsn! This seems like an excellent time to create your own branch. To do this, type the following:

```
git checkout -b <your_branch_name>
```

In one command, you have both created a branch and switched over to your newly created branch. You can now make some changes to the project from within your branch without fear of affecting the master branch. We'll keep things superficial for the sake of demonstration by creating an empty file.

```
touch myfile
```

To confirm that git has noticed this change, type the following command:

```
git status
```

The output here should tell you many things. For one, it should confirm that you are on the branch you created in case you had any doubts. Furthermore, you should observe that your newly created file (myfile) is untracked and waiting to be staged for a commit. To stage the file, type the following:

```
git add myfile
```

This stages myfile to be committed to gits record of changes. Now, you'll want to commit those changes and include a message that describes how things have been modified.

```
git commit -m "I added a file named myfile!"
```

And now you should be ready to push the changes you've made to the remote repository! So far, all of the changes you've made have been in your local repository. To push modifications to codefordenver/gsn, set it up as your remote repository by typing the following:

```
git remote add origin https://github.com/codefordenver/gsn.git
```

By convention, the remote repo for a github project is typically entitled "origin". You can name it whatever you like, but keeping things conventional will help to avoid confusion down the line. 

Finally, you should push your newly created branch to the remote repository on GitHub. To do this, type the following command:

```git
git push -u origin <your_branch_name> 
```

The '-u' flag instructs git to set an _upstream_ branch in the remote repo that will track changes to your current local branch. Again, for the sake of simplicity, we're abiding by convention here when we set our upstream branch to share the same name as our local branch. You could specify that the upstream branch for <your_branch_name> have a different name of your choosing by using colon notation (`git push -u origin <your_branch_name>:<upstram_branch_name>`). Avoid doing this unless you have a good reason, otherwise you are adding unecessary complexity to the project. 

Now your changes should be recorded on the remote repo. You've officially contributed to the project! Although your changes haven't affected the manner in which the API or Frontend operate, you have contributed nonetheless by learning something new and showing that your interest in GSN is more than a passing fancy!

