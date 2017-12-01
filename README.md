# W210CapstoneProject
The project folder for capstone

### Patent project - w210 group project 
https://github.com/ganeshsberkeley/W210_project_patentability

### How to run this flask app 
1. Have a machine with python installed, and get a copy of this folder from git.  
2. Install everything in requirements.txt. you can use command: pip install -r requirements.txt
3. Run flask app using the following command: python app.py &
4. If you need to debug your app, modify app.py last section, uncomment the line to run from port 7777 with debug mode and comment out the last line. Please revert this change before checking in since when deploying to heroku, we cannot specify port. 


Tips:
1. To list all process running on port: lsof -i tcp:7777
2. To kill process 1234: kill 1234 
3. To run the flask app after closing the command window:
    a. forever start -c python your_script.py
    b. forever stop your_script.py
    c. nohup python -u code.py &
    d. python app.py &