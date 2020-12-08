from flask import Flask, jsonify, render_template, request

from . import app, recommender


@app.route('/api/v1/recommender/categories', methods=['GET'])
def api_categories():
    if 'category' in request.args:
        category = request.args['category']
        print(category)
    else:
        return "Error: No Category field provided. Please specify an Category."

    return jsonify(recommender.getBestByCategory(category))
