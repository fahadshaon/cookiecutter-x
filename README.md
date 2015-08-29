# CookiecutterX

There are a lot of good open source code-generator projects that very efficiently generates source 
code from different types of templates. However, I particularly liked cookiecutter because of its 
wide adoption, great documentation, unit testing, etc.
For more information please visit project's [Github](https://github.com/audreyr/cookiecutter), 
[Documentation](http://cookiecutter.rtfd.org), [PyPI](https://pypi.python.org/pypi/cookiecutter). 

However, traditional code generators generates source code once and left any additional changes for the programmer. 
In my case, I often want to add different boilerplate code to my project that is already generated before. 
For example, I am developing a [flask](http://flask.pocoo.org/) web application 
and later I  decided to add [bootstrap](http://getbootstrap.com/) web framework to it 
or generate static content using [frozen-flask](http://pythonhosted.org/Frozen-Flask/). 
In such scenarios, I need to add several boilerplate files manually. 

I wrote this tool help me with such cases, where project is already generated and might have 
code that does not follow a patterns any more but requires additional boilerplate code. 

## Installation 

This project is in very early stage. Now please create a separate virtual environment for this project 
and install dependencies.

    $ git clone https://github.com/fahadshaon/cookiecutter-x.git
    $ cd cookiecutter-x
    $ virutalenv venv 
    (venv)$ source venv/bin/activate
    (venv)$ pip install -r requirements.txt
    
Finally, create variable and alias in bash startup file, such as `.bashrc` 
 
    export CCX_HOME="path/to/cookiecutter-x"
    alias cookiecutter-x="$CCX_HOME/venv/bin/python $CCX_HOME/cookiecutter_x.py "

Now you can use the `cookiecutter-x` as a command in related shells.  

*I know this is a very naive way of doing installation. I will keep working on this on next versions. 
Thank you for trying the project.*

## Tutorial 
 
Let us create a flask application named `awesomeness`, then add bootstrap for better ui, 
and finally add frozen flask to generate static files of the project.
I will be using the templates with the project.

Create a directory named `awesomeness` 

    $ mkdir awesomeness

Create a file name `cookiecutter.json` with the following variables 
 
    {
      "app_name": "awesomeness",
      "app_name_title": "Awesomeness",
      "app_description": "Awesomeness exploded"
    }

Now create the starter app
   
    (venv)$ cookiecutter-x process $CCX_HOME/example-templates/flask_starter
    [2015-08-29 14:42:38,500] INFO: Processing cookie cutter template at: /home/fahad/cookiecutter-x/example-templates/flask_starter
    [2015-08-29 14:42:38,501] INFO: Read context data: 
    {
        "app_name_title": "Awesomeness", 
        "app_name": "awesomeness", 
        "ccx_output_directory": "/home/fahad/projects/exp", 
        "app_description": "Awesomeness exploded"
    }
    [2015-08-29 14:42:38,502] INFO: Path does not exit, creating: .ccx_archive/flask_starter
    [2015-08-29 14:42:38,522] INFO: Copying different files
    [2015-08-29 14:42:38,522] INFO: Path does not exit, creating: ././awesomeness/awesomeness
    [2015-08-29 14:42:38,522] INFO: .ccx_archive/flask_starter/./awesomeness/awesomeness/awesomeness.py -> ././awesomeness/awesomeness
    [2015-08-29 14:42:38,523] INFO: Path does not exit, creating: ././awesomeness/awesomeness/templates
    [2015-08-29 14:42:38,523] INFO: .ccx_archive/flask_starter/./awesomeness/awesomeness/templates/layout.html -> ././awesomeness/awesomeness/templates
    [2015-08-29 14:42:38,523] INFO: Path does not exit, creating: ././awesomeness/awesomeness/static
    [2015-08-29 14:42:38,524] INFO: .ccx_archive/flask_starter/./awesomeness/awesomeness/static/robots.txt -> ././awesomeness/awesomeness/static
    [2015-08-29 14:42:38,524] INFO: .ccx_archive/flask_starter/./awesomeness/requirements.txt -> ././awesomeness
    [2015-08-29 14:42:38,524] INFO: .ccx_archive/flask_starter/./awesomeness/local_deploy.py -> ././awesomeness
    [2015-08-29 14:42:38,524] INFO: .ccx_archive/flask_starter/./awesomeness/awesomeness/__init__.py -> ././awesomeness/awesomeness
    [2015-08-29 14:42:38,524] INFO: .ccx_archive/flask_starter/./awesomeness/awesomeness/templates/home.html -> ././awesomeness/awesomeness/templates
    [2015-08-29 14:42:38,525] INFO: .ccx_archive/flask_starter/./awesomeness/awesomeness/core.py -> ././awesomeness/awesomeness

    
Additionally create a virtual environment and install dependencies
 
    $ virtualenv venv
    New python executable in venv/bin/python
    Installing setuptools, pip...done.
    
    $ source venv/bin/activate
    (venv)$ pip install -r requirements.txt 

Next update with bootstrap addition 

    (venv)$ cookiecutter-x process $CCX_HOME/example-templates/flask_bootstrap
    [2015-08-29 14:42:43,647] INFO: Processing cookie cutter template at: /home/fahad/cookiecutter-x/example-templates/flask_bootstrap
    [2015-08-29 14:42:43,648] INFO: Read context data: 
    {
        "app_name_title": "Awesomeness", 
        "app_name": "awesomeness", 
        "ccx_output_directory": "/home/fahad/projects/exp", 
        "app_description": "Awesomeness exploded"
    }
    [2015-08-29 14:42:43,648] INFO: Path does not exit, creating: .ccx_archive/flask_bootstrap
    
    Install the bootstrap javascript and css run
    
        $ cd awesomeness/awesomeness/static
        $ bower install
    
        
    [2015-08-29 14:42:43,675] INFO: Copying different files
    [2015-08-29 14:42:43,675] INFO: .ccx_archive/flask_bootstrap/./awesomeness/awesomeness/static/bower.json -> ././awesomeness/awesomeness/static
    [2015-08-29 14:42:43,675] INFO: Copying already existing files
    [2015-08-29 14:42:43,676] INFO: Moving old files: ./awesomeness/awesomeness/templates/layout.html -> ./awesomeness/awesomeness/templates/layout.html.1
    [2015-08-29 14:42:43,676] INFO: .ccx_archive/flask_bootstrap/./awesomeness/awesomeness/templates/layout.html -> ././awesomeness/awesomeness/templates
    [2015-08-29 14:42:43,676] INFO: Moving old files: ./awesomeness/awesomeness/templates/home.html -> ./awesomeness/awesomeness/templates/home.html.1
    [2015-08-29 14:42:43,677] INFO: .ccx_archive/flask_bootstrap/./awesomeness/awesomeness/templates/home.html -> ././awesomeness/awesomeness/templates
 

Finally add frozen flak

    (venv)$ cookiecutter-x process $CCX_HOME/example-templates/flask_frozen
    [2015-08-29 14:43:00,379] INFO: Processing cookie cutter template at: /home/fahad/cookiecutter-x/example-templates/flask_frozen
    [2015-08-29 14:43:00,379] INFO: Read context data: 
    {
        "app_name_title": "Awesomeness", 
        "app_name": "awesomeness", 
        "ccx_output_directory": "/home/fahad/projects/exp", 
        "app_description": "Awesomeness exploded"
    }
    [2015-08-29 14:43:00,379] INFO: Path does not exit, creating: .ccx_archive/flask_frozen
    
    Install frozen flask
    
        $ pip install Frozen-Flask
    
    Also save dependencies into `requirements.txt`
    
        $ pip freeze > requirements.txt
    
        
    [2015-08-29 14:43:00,396] INFO: Copying different files
    [2015-08-29 14:43:00,397] INFO: .ccx_archive/flask_frozen/./awesomeness/frozen.py -> ././awesomeness


## TODOs

- Make an installable python library, so that the install process is cleaner.
- Generated project structure reconsideration
- Different policy for overwriting files
- Improve examples and README
 