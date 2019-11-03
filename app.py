from flask import Flask, jsonify, request
from flask.logging import create_logger
from pymongo import MongoClient
from flasgger import Swagger
import os
import logging

app = Flask(__name__)
swagger = Swagger(app)

logger = create_logger(app)
logger.setLevel(logging.INFO)


@app.route('/search',  methods=['POST'])
def search():
    """Example endpoint returning a list of colors by palette
    This is using docstrings for specifications.
    ---
    parameters:
      - in: body
        name: name
        required: true
        description: Complete or part of name
        schema:
          $ref: '#/definitions/Request'
    definitions:
      Book:
        type: object
        properties:
          _id:
            type: string
          title:
            type: string
          isbn:
            type: string
          pageCount:
            type: string
          publishedDate:
            type: string
          shortDescription:
            type: string
          status:
            type: string
          thumbnailUrl:
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
      Request:
        type: object
        properties:
          name:
            type: string
    responses:
      200:
        description: A list of colors (may be filtered by palette)
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
            "isbn": "1933988673",
            "pageCount": 416,
            "publishedDate": "Wed, 01 Apr 2009 07:00:00 GMT",
            "shortDescription": "Unlocking Android: A Developer's Guide provides concise, hands-on instruction for the Android operating system and development tools. This book teaches important architectural concepts in a straightforward writing style and builds on this with practical and useful examples throughout.",
            "status": "PUBLISH",
            "thumbnailUrl": "https://s3.amazonaws.com/AKIAJC5RLADLUMVRPFDQ.book-thumb-images/ableson.jpg",
            "title": "Unlocking Android"
          }
    """
    book_name = request.json["name"]
    connection = MongoClient(
        os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
    db = connection.get_database('sample_library')
    books_collection = db.get_collection('books')
    books = books_collection.find_one({ "title": {'$regex': book_name}},{"longDescription":0})

    return jsonify(books)


@app.before_first_request
def initialize():
    connection = MongoClient(
        os.getenv('MONGO_URI', 'mongodb://localhost:27017'))
    db = connection.get_database('sample_library')
    books_collection = db.get_collection('books')


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True)
