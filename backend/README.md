# Backend - Full Stack Trivia API 

### Installing Dependencies for the Backend

1. **Python 3.7** - Follow instructions to install the latest version of python for your platform in the [python docs](https://docs.python.org/3/using/unix.html#getting-and-installing-the-latest-version-of-python)


2. **Virtual Enviornment** - We recommend working within a virtual environment whenever using Python for projects. This keeps your dependencies for each project separate and organaized. Instructions for setting up a virual enviornment for your platform can be found in the [python docs](https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/)


3. **PIP Dependencies** - Once you have your virtual environment setup and running, install dependencies by naviging to the `/backend` directory and running:
```bash
pip install -r requirements.txt
```
This will install all of the required packages we selected within the `requirements.txt` file.


4. **Key Dependencies**
 - [Flask](http://flask.pocoo.org/)  is a lightweight backend microservices framework. Flask is required to handle requests and responses.

 - [SQLAlchemy](https://www.sqlalchemy.org/) is the Python SQL toolkit and ORM we'll use handle the lightweight sqlite database. You'll primarily work in app.py and can reference models.py. 

 - [Flask-CORS](https://flask-cors.readthedocs.io/en/latest/#) is the extension we'll use to handle cross origin requests from our frontend server. 

### Database Setup
With Postgres running, restore a database using the trivia.psql file provided. From the backend folder in terminal run:
```bash
psql trivia < trivia.psql
```

### Running the server

From within the `./src` directory first ensure you are working using your created virtual environment.

To run the server, execute:

```bash
flask run --reload
```

The `--reload` flag will detect file changes and restart the server automatically.

## Endpoints
### GET '/categories'
- Fetches a dictionary of categories in which the keys are the ids and the value is the corresponding string of the category
- Request Arguments: None
- Returns: An object with a single key, categories, that contains a object of id: category_string key:value pairs. 
```
{'1' : "Science",
'2' : "Art",
'3' : "Geography",
'4' : "History",
'5' : "Entertainment",
'6' : "Sports"}
```
### GET '/questions?page=1'
- Paginate and fetches the questions in below format.
- The Page number is passed as a query parameter, and each page contains 10 questions
- Request Arguments: None
- Returns: Array of questions, current_category, all categories and total questions. 
```
{
    "categories": {
        "1": "Science",
        "2": "Art",
        "3": "Geography",
        "4": "History",
        "5": "Entertainment",
        "6": "Sports"
    },
    "current_category": "History",
    "questions": [
        {
            "answer": "Maya Angelou",
            "category": 4,
            "difficulty": 2,
            "id": 5,
            "question": "Whose autobiography is entitled 'I Know Why the Caged Bird Sings'?"
        }
    ],
    "total_questions": 21
}
```
- Error: HTTP ERROR CODE: 404, When no records are found. The response would be as follows:
```
{
    "error": 404,
    "message": "resource not found",
    "success": false
}
```
### DELETE '/questions/2'
- Deletes the question with id '2'.
- Request Arguments: None
- Returns: The id of the deleted message back. 
```
{
    "deleted": 5
}
```
- Error: If the question requested to be deleted is not found. Then HTTP ERROR CODE: 422 is returned.
```
{
    "error": 422,
    "message": "unprocessable",
    "success": false
}
```
### POST '/questions'
- Creates a new question.
- Request Arguments: 
```
{
    "question":  "Hello this a test question",
    "difficulty": 2,
    "category": 2,
    "answer": "Answer"
}
```
- Returns: The id of the created message back. 
```
{
    "created": 50
}
```
- Error: If the question creation fails, Then HTTP ERROR CODE: 422 is returned.
```
{
    "error": 422,
    "message": "unprocessable",
    "success": false
}
```
### POST '/questions/search'
- Searches a the question based on the search term passed in the input.
- Request Arguments: 
```
{
    "searchTerm":  "Hello"
}
```
- Returns: All the question containing the search term, current category and total questions. 
```
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Answer",
            "category": 2,
            "difficulty": 2,
            "id": 32,
            "question": "Hello this a test question"
        },
        {
            "answer": "Answer",
            "category": 2,
            "difficulty": 2,
            "id": 33,
            "question": "Hello this a test question"
        }
    ]
    "total_questions": 2
}
```
- Error: If the none of the question has search term, Then HTTP ERROR CODE: 404 is returned.
```
{
    "error": 404,
    "message": "resource not found"
}
```
### GET '/categories/2/questions'
- Return all the question for a given category. In the above URI '2' denotes the category id.
- Request Arguments: None
- Returns: All all the question as a array, current_category and total_questions. 
```
{
    "current_category": "Art",
    "questions": [
        {
            "answer": "Escher",
            "category": 2,
            "difficulty": 1,
            "id": 16,
            "question": "Which Dutch graphic artist–initials M C was a creator of optical illusions?"
        },....
    ]
    "total_questions": 6
}
```
- Error: If the none of the question is found for the category, Then HTTP ERROR CODE: 404 is returned.
```
{
    "error": 404,
    "message": "resource not found"
}
```
### POST '/quizzes'
- Provide an endpoint to get questions to play the quiz. 
- Pass category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions.
- If category is selected as all, then the questions are not filtered on categories.
- Request Arguments: 
{
"quiz_category": {"id":2},
"previous_questions": [16]
}
- Returns: A random question for category, whcih is not in previous question. 
```
{
    "question": {
        "answer": "Mona Lisa",
        "category": 2,
        "difficulty": 3,
        "id": 17,
        "question": "La Giaconda is better known as what?"
    }
}
- Returns: When no more question are left, following is returned:
```
{
    "question": null
}

```

## Testing
To run the tests, run
```
dropdb trivia_test
createdb trivia_test
psql trivia_test < trivia.psql
python test_flaskr.py
```
