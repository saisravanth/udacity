import os
import random
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import random

from models import setup_db, Question, Category

QUESTIONS_PER_PAGE = 10

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)
  cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

  def paginate_questions(request, selection):
    page = request.args.get('page', 1, type=int)
    start = (page - 1) * QUESTIONS_PER_PAGE
    end = start + QUESTIONS_PER_PAGE

    questions = [question.format() for question in selection]
    current_questions = questions[start:end]

    return current_questions

  '''
  @TODO: Set up CORS. Allow '*' for origins. Delete the sample route after completing the TODOs
  '''
  '''
  @TODO: Use the after_request decorator to set Access-Control-Allow
  '''
  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PUT,POST,DELETE,OPTIONS')
    return response


  '''
  @TODO: 
  Create an endpoint to handle GET requests 
  for all available categories.
  '''
  @app.route("/categories", methods=['GET'])
  def get_categories():
    categories = Category.query.all()
    details = {category.id:category.type for category in categories}

    return jsonify({
      'success': 200,
      'categories': details
    })


  '''
  @TODO: 
  Create an endpoint to handle GET requests for questions, 
  including pagination (every 10 questions). 
  This endpoint should return a list of questions, 
  number of total questions, current category, categories. 

  TEST: At this point, when you start the application
  you should see questions and categories generated,
  ten questions per page and pagination at the bottom of the screen for three pages.
  Clicking on the page numbers should update the questions. 
  '''
  @app.route("/questions", methods=['GET'])
  def get_questions():
    questions = Question.query.all()
    totalQuestions = len(questions)
    questions = paginate_questions(request, questions)
    categories = Category.query.all()
    details = {category.id:category.type for category in categories}

    if len(questions) == 0:
      abort(404)
    
    return jsonify({
      'success': 200,
      'questions': questions,
      'total_questions': totalQuestions,
      'categories': details,
      'current_category': None
    })


  '''
  @TODO: 
  Create an endpoint to DELETE question using a question ID. 

  TEST: When you click the trash icon next to a question, the question will be removed.
  This removal will persist in the database and when you refresh the page. 
  '''
  @app.route("/questions/<int:id>", methods=['DELETE'])
  def remove_question_by_id(id):
    try:
      #status = Question.query.filter_by(id=id).delete()
      question = Question.query.get(id)
      question.delete()
      return jsonify({
        'success': 200
      })      
    except:
      abort(404)

  '''
  @TODO: 
  Create an endpoint to POST a new question, 
  which will require the question and answer text, 
  category, and difficulty score.

  TEST: When you submit a question on the "Add" tab, 
  the form will clear and the question will appear at the end of the last page
  of the questions list in the "List" tab.  
  '''
  @app.route("/questions", methods=['POST'])
  def create_question():
    try:
      request_json = request.get_json()
      question = request_json.get('question','')
      answer = request_json.get('answer','')
      difficulty = request_json.get('difficulty',0)
      category = request_json.get('category','')
      
      question = Question(question=question, answer=answer, difficulty=int(difficulty), category=category)
      question.insert()
      
      return jsonify({
        'success': 200
      })      
    except:
      abort(422)


  '''
  @TODO: 
  Create a POST endpoint to get questions based on a search term. 
  It should return any questions for whom the search term 
  is a substring of the question. 

  TEST: Search by any phrase. The questions list will update to include 
  only question that include that string within their question. 
  Try using the word "title" to start. 
  '''
  @app.route("/questions/<searchTerm>", methods=['POST'])
  def get_questions_by_search(searchTerm):
    print("searchTerm: ", searchTerm)
    questions = Question.query.filter(Question.question.ilike('%' + searchTerm + '%')).all()
    totalQuestions = len(questions)
    questions = paginate_questions(request, questions)
    
    if len(questions) == 0:
      abort(404)
    
    return jsonify({
      'success': 200,
      'questions': questions,
      'total_questions': totalQuestions,
      'current_category': None
    })

  '''
  @TODO: 
  Create a GET endpoint to get questions based on category. 

  TEST: In the "List" tab / main screen, clicking on one of the 
  categories in the left column will cause only questions of that 
  category to be shown. 
  '''
  @app.route("/categories/<int:id>/questions", methods=['GET'])
  def get_questions_by_category(id):
    questions = Question.query.filter_by(category=id).all()
    totalQuestions = len(questions)
    questions = paginate_questions(request, questions)
    
    if len(questions) == 0:
      abort(404)
    
    return jsonify({
      'success': 200,
      'questions': questions,
      'totalQuestions': totalQuestions,
      'currentCategory': id
    })


  '''
  @TODO: 
  Create a POST endpoint to get questions to play the quiz. 
  This endpoint should take category and previous question parameters 
  and return a random questions within the given category, 
  if provided, and that is not one of the previous questions. 

  TEST: In the "Play" tab, after a user selects "All" or a category,
  one question at a time is displayed, the user is allowed to answer
  and shown whether they were correct or not. 
  '''

  @app.route("/quizzes", methods=['POST'])
  def get_random_questions():
    
    request_json = request.get_json()
    quiz_category = request_json.get('quiz_category','')
    id = quiz_category.get('id', 0)
    previous_question_ids = request_json.get('previous_questions','')
      
    if id != 0:
      questions = Question.query.filter_by(category=id).all()
    else:
      questions = Question.query.all()
  
    questions = [question.format() for question in questions]

    if len(questions) == 0:
      abort(404)

    if len(questions) == len(previous_question_ids):
      abort(503)
    else:
      while True:
        question = random.choice(questions)
        if question['id'] not in previous_question_ids:
          random_question = Question.query.filter_by(id=question['id']).first()
          random_question = random_question.format()
          break
        
      return jsonify({
        'success': 200,
        'question': random_question
      })
    

  '''
  @TODO: 
  Create error handlers for all expected errors 
  including 404 and 422. 
  '''

  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
      "success": False, 
      "error": 404,
      "message": "Not found"
      }), 404
  
  @app.errorhandler(405)
  def not_allowed(error):
    return jsonify({
      "success": False, 
      "error": 405,
      "message": "Method not allowed"
      }), 405
  
  @app.errorhandler(400)
  def bad_request(error):
    return jsonify({
      "success": False, 
      "error": 400,
      "message": "Bad Request"
      }), 400
  
  @app.errorhandler(422)
  def unprocessible_request(error):
    return jsonify({
      "success": False, 
      "error": 422,
      "message": "Unprocessible Request"
      }), 422  

# Service Unavailabel 
  @app.errorhandler(503)
  def out_of_questions(error):
    return jsonify({
      "success": False, 
      "error": 503,
      "message": "We are out of questions !!"
      }), 503 
  
  return app

    