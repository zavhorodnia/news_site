# News Site
This is an introduction to my news website. It's pretty basic and easy to use. So, let's see what you can do!

## Set up
First, you need to set up the project. After you've cloned this repository, perform the following steps:
* Install required packages (which are described at **requirements.txt** file)
* Go to **news_site/settings.py**. You'll have to configure email settings in order to let News Site send mails (for email confirmation on registration etc). News Site is using gmail's smtp to handle this, so you'll need to add your gmail accout credentials. This is what you should add to your **settings.py** file:
```
# your gmail address
EMAIL_HOST_USER = 'username@gmail.com'

# password from your gmail account
EMAIL_HOST_PASSWORD = 'your_password'

# optinal field - tells how to display the sender name
DEFAULT_FROM_EMAIL = 'News Site <username@gmail.com>'
```
* From within the directory where you cloned the project, run django server:
```
python manage.py runserver
```
That's all. Now, you can start using the site.

## User accounts and groups
Before you can see the site's content, you'll have to create an account. There are three groups of users:
* _users_ - default group with minimal access. When a new account is created, it's being added to the "users" group automatically. Permissions: writing posts (but not publishing), adding comments to posts.
* _moderators_ - a group for site moderation. Permissions: publishing posts without pre-modration, editing posts, publishing posts created by "users", hiding posts from published, deleting comments.
* _administrators_ - superusers. Permissions: except of all of the moderator's permissions, administrators have an access to the admin panel, which enables the following actions: deleting posts, modifying comments, changing user's group, adding/modifying/deleting users & groups.

As soon as you start django server, you'll be redirected to the login page. You can choose __*Sign up*__ button to create a new accout (it's really simple, the only extra thing you'll have to do is an email confirmation) or login to the existing admin account.

##### Superuser account
There is an existing admin account, which is available for you to log in. Credentials: username - NewsSiteAdmin, password - NewsSite123. Admin interface is available by **/admin/** url.

## Using the site
Now, when you are logged in, you can use the website functionality.
As a user, you can:
* Read the news posts
* Add comments
* Add posts (which will be published after pre-moderation).
Also, when someone will comment your post, you'll receive an email notification.

As a moderator, you also can:
* Add posts without pre-moderation
* See posts that are waiting for moderation, and
	* edit them
	* publish
	* hide back to unpublished
* Delete comments

Go ahead and try it yourself!