## Social media checker

A colection (__cough__ 2 __cough__) of scripts that checks for 
 * Notifications
 * Friend requests
 * Messages

on **Facebook** and **Linkedin**.

**The scripts does not use any API** but scraps the information out the website using Selenium. This project was created for fun and to overcome the need to check for new activity on the social media platforms. 

Basically the opportunities are limitless because of using Selenium. This acts as a browser and the interaction with any web platform is possible. 

#### Requirements for running the checkers:
 1. [Python 3](https://www.python.org/download/releases/3.0/)
 2. [Selenium](https://selenium-python.readthedocs.io/)
 3. [Web Driver](https://www.seleniumhq.org/projects/webdriver/)
 4. [Chrome](https://www.google.com/chrome/)
 

#### Running the scripts
Before getting the benefits of not spending time on checking the activity a few settings must be completed in `config.py`:

* Credentials:
    ```
    'facebook': {'email': 'user@facebook.com',
                 'password': 'thebestpassword'
                 }, 
    ```
    and 
    ```
    'linkedin': {'email': 'user@linkedin.com',
                 'password': 'anotherbestpassword'
                 }`
    ```
* Path to chrome driver
    ```
    chrome_driver_path = /path/to/chromedriver
    ```

* [Optionally] Configure what checks should be done __[by default all are checked]__
 ```
    linkedin_checks = {
        'message_check': True,
        'notification_check': True,
        'connection_invitation_check': True
    }
```
and 
```
facebook_checks = {
    'message_check': True,
    'notification_check': True,
    'friend_request_check': True
}
```

#### Downsides
Is cool not to check facebook and linkedin (and possibly other platforms in the future) but there are a couple of downsides of this project of which I am aware of:
1. Having to add your credentials (password especially) in plain text in a config file is **not cool**
      * I am working on removing that confing and use the already logged in browser
2. The speed in ...not great: ~9-10 seconds for one platform
      * WIP
3. Bugs probably...
4. Heavy tailored for actual state of platforms, if they will change, an update will be needed
        
