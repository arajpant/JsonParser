# Json Parser
This project is based on Parsing the json and dumping it to CSV via Flask api post method. 
- Huge json file can be parsed by just executing the main.py file and open the url http://127.0.0.1:5000/parsing.
- please provide the POST method and provide body value as json body object ( take example_account-model.json file as example)

- dumping the result in CSV file.
- Mostly used Parsed result for data analysis purpose.

#Steps or Guides to run the project.

- Create a Virtual environment
    $ python3 -m venv env

- Activate Virtual Environment

    $ source env/bin/activate

 
- Install the following command for lxml. 
    pip install lxml-4.6.3-cp310-cp310-win_amd64.whl

- Install required Packages
   $ pip install -r requirements.txt

- Testing :
   
   For testing run the following command
   
    $ python3 main.py 



   