#! /usr/bin/python
# -*- coding: utf-8 -*-

from flask import Flask, jsonify
from flask_restful import reqparse, abort, Api, Resource
import time

app = Flask(__name__)
api = Api(app)


@app.route('/helloworld/')
def hello_world():
    return jsonify({'hello': {'world': {'1': '3'}}})


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
