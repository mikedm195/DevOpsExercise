from flask import Flask, jsonify, request, Response
from flask.logging import create_logger
from pymongo import MongoClient
from flasgger import Swagger
import os
import logging
import json

app = Flask(__name__)
swagger = Swagger(app)

logger = create_logger(app)
logger.setLevel(logging.INFO)


@app.route('/search')
def search():
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    parameters:
      - in: query
        name: name
        required: true
        description: Name of the book
        default: Android
    definitions:
      Book:
        type: object
        properties:
          title:
            type: string
          shortDescription:
            type: string
          authors:
            type: array
            items:
              $ref: '#/definitions/Author'
          categories:
            type: array
            items:
              $ref: '#/definitions/Category'
      Author:
        type: string
      Category:
        type: string
    responses:
      200:
        description: A book
        schema:
          $ref: '#/definitions/Book'
        examples:
          book: {
            "_id": 1,
            "authors": [
                "W. Frank Ableson",
                "Charlie Collins",
                "Robi Sen"
            ],
            "categories": [
                "Open Source",
                "Mobile"
            ],
            "shortDescription": "Unlocking Android: A Developer's Guide provides concise, hands-on instruction for the Android operating system and development tools. This book teaches important architectural concepts in a straightforward writing style and builds on this with practical and useful examples throughout.",            
            "title": "Unlocking Android"
          }
    """
    try:
        book_name = request.args.get("name")
        connection = MongoClient(
            os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
        db = connection.get_database('sample_library')
        books_collection = db.get_collection('books')
        books = books_collection.find_one({ "title": {'$regex': book_name}},{"title":1, "shortDescription": 1, "authors": 1, "categories": 1})
        if books is not None:
            return Response(json.dumps(books), status=200, mimetype='application/json')
        else:
            return Response(json.dumps({"Error": "The book could not be found"}), status=404, mimetype='application/json')
    except Exception as e:
        return Response(json.dumps({"Error": str(e)}), status=500, mimetype='application/json')
    


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
