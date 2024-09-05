To complete this task:
1:   Setup database in command promtp
2:   In VS Code: imported flask, MySql, flask-marshmallo,json
3:   Created folders Module6Lesson2.py and Task3.py
4:  In Terminal:
        python -m venv Module6Lesson2
        Module6Lesson2/Scripts/activate
        pip install flask
        pip install MySql
        pip install flask-marshmallow
        pip install json
          repeated for Task3.py
In MySql there are two folders for members and scheduel
5. For task 2 open Module6Lesson2.py
      in terminal: Module6Lesson2/scripts/activate
Goto Postman

6:   create new folder
7:   in the new folder: To get all members
          new request
          Get and http://127.0.0.1:5000/members
          in headers key=Content-Type, values = application json
          click send
        To add new member:
            new request
            Post and http://127.0.0.1:5000/members
            in body Raw, json
            update new member
            click send
        To update
            new request
            PUT and http://127.0.0.1:5000/members/1   #("1" member you want to update)
        To delete
            new request 
            DELETE and http://127.0.0.1:5000/members/1   #("1" member you want to delete)
For TASK 3:
5. For task 2 open Task3.py
      in terminal: Task3/scripts/activate
Goto Postman

6:   create new folder
7:   in the new folder: To get all schedules
          new request
          Get and http://127.0.0.1:5000/scheduel
          in headers key=Content-Type, values = application json
          click send
        To add new schedule:
            new request
            Post and http://127.0.0.1:5000/scheduel
            in body Raw, json
            add new schedule
            click send
        To update
            new request
            PUT and http://127.0.0.1:5000/scheduel/1   #("1" member you want to update)
            in body Raw, json
            update new schedule
            click send
       To View schedule of a specific member
           GET and http://127.0.0.1:5000/scheduel/1   #("1" member you want to see all data)
            click send
      
    
