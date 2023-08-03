
Set Up by typing the following commands on your terminal:

    python3 -m venv .venv
    source .venv/bin/activate
    python3 -m pip install --upgrade pip
    python3 -m pip install flask
    export FLASK_APP=sudoku.py
    flask run


Testing: 

    In the terminal, run this command:
        python3 sudoku.py

    For Part1-5:
        The output should give the printed values for Part1-5

    For Part6: 
        The output should also give a url such as http://127.0.0.1:5000
        Copy and paste the given url on a search engine to see the website

        On the website, type numbers into some cells
        Click the "Solve Puzzle" button
        You should then be able to see the final solved sudoku puzzle

    If you just want the output to test Part6:
    In the terminal, run this command:
        flask run


To reset the web application:

    In the terminal:
        ^C
    




