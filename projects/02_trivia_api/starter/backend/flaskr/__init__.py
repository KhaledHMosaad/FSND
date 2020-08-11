import os
from flask import Flask, request, abort, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS, cross_origin
import random

from models import setup_db, Question, Category,db

QUESTIONS_PER_PAGE = 10

def paginate_questions(request, selection):
  page = request.args.get('page', 1, type=int)
  start =  (page - 1) * QUESTIONS_PER_PAGE
  end = start + QUESTIONS_PER_PAGE

  questions = [question.format() for question in selection]
  current_questions = questions[start:end]

  return current_questions

def create_app(test_config=None):
  # create and configure the app
  app = Flask(__name__)
  setup_db(app)


  cors = CORS(app, resources={r"*": {"origins": "*"}})

  @app.after_request
  def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type,true')
    response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
    return response


  @cross_origin
  @app.route('/categories')
  def get_categories():
    categories = [category.format() for category in Category.query.all()]
    if len(categories) == 0:
      abort(404)
    else:
      return jsonify({
        "success" : True,
        "categories" : categories,
        "total_categories" : len(categories)
      })

  @cross_origin
  @app.route('/questions', methods=['POST', 'GET'])
  def get_paginated_questions():
    if request.method == 'GET':
        questions = Question.query.all()
        current_questions = paginate_questions(request, questions)
        categories = [category.format() for category in Category.query.all()]

        if len(current_questions) == 0:
            abort(404)
        else:
            return jsonify({
                "success" : True,
                "questions" : current_questions,
                "total_questions" : len(current_questions),
                "categories" : categories,
                "current_category" : None
            })
    elif request.method == 'POST':
        try:
            payload = request.get_json()
            question = Question(question=payload.get('question', None),
                               answer=payload.get('answer', None),
                               difficulty=payload.get('difficulty', None),
                               category=payload.get('category', None))

            if question.question is None:
                abort(422)
            question.insert()
        except:
            db.session.rollback()
            abort(422)
        finally:
            db.session.close()
        current_questions = paginate_questions(request, Question.query.all())
        return jsonify({
            "success" : True,
            "message"  : "New Question Added Successfully",
            "questions" : current_questions,
            "total_questions" : len(current_questions)
        })


  @cross_origin()
  @app.route('/questions/<int:question_id>', methods=['DELETE'])
  def delete_question(question_id):
    question = Question.query.get(question_id)
    if question is None:
      abort(404)
    try:
      question.delete()
      db.session.commit()
    except:
      db.session.rollback()
      db.session.close()
      abort(422)
    finally:
      db.session.close()
    questions = Question.query.all()
    paginated_questions = paginate_questions(request, questions)
    return jsonify({
      "success" : True,
      "message" : "Question has been deleted successfully",
      "questions" : paginated_questions,
      "total_questions" : len(paginated_questions)
    })

# /questions/search?q=MohamedAli
  @cross_origin()
  @app.route('/questions/search', methods=['POST'])
  def search_question():
      res_questions = []
      payload = request.get_json()
      search_term = payload.get('searchTerm')
      questions = Question.query.all()
      if search_term is not None:
          for question in questions:
              if question.question.lower().find(search_term.lower()) != -1 :
                  res_questions.append(question)
          current_questions = paginate_questions(request, res_questions)
      else:
          current_questions = paginate_questions(request, questions)
      if len(current_questions) == 0:
          abort(404)
      else:
          return jsonify({
              "success" : True,
              "questions" : current_questions,
              "total_questions" : len(current_questions)
          })

# /categories/<int:category_id>/questions
  @cross_origin()
  @app.route('/categories/<int:category_id>/questions')
  def get_questions_by_category(category_id):
      category = Category.query.get(category_id)
      current_questions = paginate_questions(request, Question.query.filter_by(category = category_id).all())
      categories = [category.format() for category in Category.query.all()]
      if len(current_questions) == 0:
          abort(404)
      else:
          return jsonify({
              "success" : True,
              "questions" : current_questions,
              "total_questions" : len(current_questions),
              "categories" : categories,
              "current_category" : category.format()
          })

# /quizzes
  @cross_origin()
  @app.route('/quizzes', methods=['POST'])
  def get_questions_for_quiz():
    payload = request.get_json(force=True)
    previous_questions = payload.get('previous_questions', None)
    category = payload.get('quiz_category', None)
    print(category)
    if category['id'] == 0 or Category.query.get(category['id']) is not None:
        if category['id'] == 0 :
            questions = Question.query.all()
        else:
            questions = Question.query.filter(Question.category == category['id']).all()
        if previous_questions is not None:
            for question in questions:
                for q in previous_questions:
                    if question.equals(Question.query.get(q)):
                        questions.remove(question)
            formatted_questions = [question.format() for question in questions]
        else:
            formatted_questions = [question.format() for question in questions]
        if len(formatted_questions) != 0:
            return jsonify({
                "success" : True,
                "question" : formatted_questions[random.randint(0, len(formatted_questions) - 1)]
            })
        else:
            return jsonify({
                "success" : True,
                "question" : None
            })
    else:
        abort(404)
  @app.errorhandler(404)
  def not_found(error):
    return jsonify({
        "success" : False,
        "error" : 404,
        "message" : "Not Found"
    }), 404

  @app.errorhandler(422)
  def unprocessable(error):
    return jsonify({
        "success" : False,
        "error" : 422,
        "message" : "Unprocessable"
    }), 422

  return app

