from flask import Flask, jsonify, render_template, request

from . import app, recommender


@app.route('/api/v1/recommender/categories', methods=['GET'])
def api_categories():
    if 'category' in request.args:
        category = request.args['category']
        print(category)
    else:
        return "Error: No id field provided. Please specify an id."

    return jsonify(recommender.getBestByCategory(category))
