from heapq import merge
import os
from tracemalloc import start
from unicodedata import category
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random
import json

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  
  #Set up CORS. Allow '*' for origins.
  CORS(app, resources={r"/api/*": {"origins": "*"}})

  #After_request decorator to set Access-Control-Allow
  
  @app.after_request
  def after_request(response):
    response.headers.add(
      "Access-Control-Allow-Headers", "Content-Type,Authorization,true"
    )
    response.headers.add(
            "Access-Control-Allow-Methods", "GET,POST,DELETE,OPTIONS"
        )
    return response

  #Function formats the categories in the desired format
  def getFormattedCategories():

    # Get all the available categories
    categories = Category.query.all()

    # Initialize
    format_categories = {}

    #Iterate through the categories and format them into desired output format
    for category in categories:
      format_categories = format_categories | category.format()
    
    return format_categories
  
  # Function return category type for the category ID
  def getCategory(categoryId):

    # Get the category based on the ID Passed
    category = Category.query.get(categoryId)

    return category.type
    
  @app.route("/categories", methods=["GET"])
  def getCategories():
    
    
    format_categories = getFormattedCategories()
    
    #Send the response
    return jsonify({
      "success": True,
      "categories": format_categories
    })

  #Endpoint to handle GET requests for questions, including pagination (every 10 questions)

  @app.route("/questions", methods=["GET"])
  def getQuestion():

    # Get the page query parameter, if not found default to 1
    page= request.args.get("page",1,type=int)

    #calculate start and end position
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    #Get all the questions and format
    questions = Question.query.order_by(Question.id).all()
    formatted_question = [question.format() for question in questions]

    # Check if anything to return
    if len(formatted_question[start:end]) == 0:
      abort(404)

    #Get the first question category as the current category
    currentCategory = getCategory(formatted_question[start]['category'])

    return jsonify(
      {
        "success": True,
        "questions": formatted_question[start:end],
        "total_questions": len(formatted_question),
        "categories": getFormattedCategories(), #Get all the categories
        "current_category": currentCategory
      }
    )


  # DELETE question using a question ID.
  @app.route("/questions/<int:questionId>", methods=["DELETE"])
  def deleteQuestion(questionId):
    # Get the question by id
    question = Question.query.get(questionId)

    # If the question is not found, send 404 error
    if question is None:
      abort(422)
    else:
      question.delete()
      return jsonify(
        {
          "success": True,
          "deleted": questionId
        }
      )

  #Endpoint to POST a new question
  @app.route("/questions", methods=["POST"])
  def createQuestion():
    
    body = request.get_json()
    
    #Parse all the request fields
    new_question = body.get("question", None)
    new_difficulty = body.get("difficulty", None)
    new_category = body.get("category", None)
    new_answer = body.get("answer", None)

    try:
      # Create the object for inserting
      question = Question(question= new_question, 
                        answer= new_answer,
                        category= new_category,
                        difficulty= new_difficulty)

      question.insert()

      # Return the response
      return jsonify({
      "success": True,
      "created": question.id
      })
    
    except:
      # If some issue while inserting
      abort(422)
    
    
  #Endpoint to POST a new question
  @app.route("/questions/search", methods=["POST"])
  def searchQuestion():
    
    data = json.loads(request.data)
    print(data)
    
    # Validate the input data
    if "searchTerm" not in data:
      abort(400)

    # Create the ilike parameter
    searchTerm = data["searchTerm"]
    queryTerm = '%' + searchTerm + '%'
    


    #Fetch the questions based on the search term
    questions = Question.query.filter(Question.question.ilike(queryTerm)).order_by(Question.id).all()

    # Check if not even a single question has search term
    if  len(questions) == 0:
      abort(404)

    
    #Format the questions
    formatted_question = [question.format() for question in questions]

    #Get the first question category, and set that as current category
    currentCategory = getCategory(formatted_question[0]['category'])
    
    #Send the response
    return jsonify({
        "success": True,
        "questions": formatted_question,
        "total_questions": len(formatted_question),
        "current_category": currentCategory
      })

  # GET endpoint to get questions based on category. 
  @app.route('/categories/<int:id>/questions', methods=['GET'])
  def getQuestionByCategory(id):
    # Get all the questions for given categories
    
    questions = Question.query.filter(Question.category == id).order_by(Question.id).all()
    
    # Check if question for given category doesn't exist
    if len(questions) == 0:
      abort(404)

    #Format the object in JSON 
    formatted_question = [question.format() for question in questions]
    
    
    #Set the current category by fetching the category type
    currentCategory = getCategory(id)
    
    #return the response
    return jsonify({
      "success": True,
      "questions": formatted_question,
      "total_questions": len(formatted_question),
      "current_category": currentCategory
    })

  # Get questions to play the quiz. 
  # Pass category and previous question parameters and return a random questions within the given category, if provided, and that is not one of the previous questions. 

  @app.route('/quizzes', methods=['POST'])
  def playQuiz():
    data = json.loads(request.data)
    previousQuestions = []

    # Check if previous questions exists
    if "previous_questions" in data:
      previousQuestions = data["previous_questions"]
    
    categoryId = data["quiz_category"]["id"]
    
    if (categoryId == 0):
      # Get all the question for the quiz
      question = Question.query.filter(Question.id.notin_(previousQuestions)).first()
    else:
      # Get the question for the quiz, based on the category
      question = Question.query.filter(Question.id.notin_(previousQuestions)).filter(Question.category == categoryId).first()
    
    if question:
      #return the response
      return jsonify({
        "success": True,
        "question": question.format()
      })
    else: 
      # Questions are finished
      return jsonify({
        "success": True,
        "question": None
      })


 # Error Handlers 
  @app.errorhandler(404)
  def not_found(error):
      return (
          jsonify({"success": False, "error": 404, "message": "resource not found"}),
          404,
      )

  @app.errorhandler(422)
  def unprocessable(error):
      return (
          jsonify({"success": False, "error": 422, "message": "unprocessable"}),
          422,
      )

  @app.errorhandler(400)
  def bad_request(error):
      return jsonify({"success": False, "error": 400, "message": "bad request"}), 400

  @app.errorhandler(405)
  def not_found(error):
      return (
          jsonify({"success": False, "error": 405, "message": "method not allowed"}),
          405,
        )

  return app

    