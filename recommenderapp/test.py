from flask import Flask, render_template, request, jsonify
from . import app


@app.route('/test')
def some_view():
    name = request.args.get('name', 'Anonymous')
    request.is_xhr
    if request.is_xhr:
        template_name = 'test_ajax.html'
    else:
        template_name = 'test.html'
    return render_template(template_name, name=name)