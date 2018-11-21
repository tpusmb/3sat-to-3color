# probleme-3-coloration


## Installation.

For this project you will need a python3 version.

You will need the following package:
    
    sudo apt install python3
    sudo apt install virtualenv
    sudo apt install python3-pip
    sudo apt install python3-tk
 
Prepare your virtualenv:

    virtualenv venv
    . venv/bin/activate
    pip install -r requirements.txt   

If you want to exit your virtualenv:

    deactivate

## Usage

### Run Specific algorithm

To run a specific algorithm


    python problem_3_coloration.py mygraph.txt --generate-and-test
    python problem_3_coloration.py mygraph.txt --solve-back-tracking

This command will run the 2 algorithm    

    python problem_3_coloration.py mygraph.txt --generate-and-test --solve-back-tracking

If you want to visualise the solution you just have to add --show flag

    python problem_3_coloration.py mygraph.txt --generate-and-test --solve-back-tracking --show

This line will run generate and test and show the graph color. Then run solve back tracking and show the graph color

    