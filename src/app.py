"""
This module takes care of starting the API Server, Loading the DB and Adding the endpoints
"""
import os
from flask import Flask, request, jsonify, url_for
from flask_cors import CORS
from utils import APIException, generate_sitemap
from datastructures import FamilyStructure
#from models import Person

app = Flask(__name__)
app.url_map.strict_slashes = False
CORS(app)

jackson_family = FamilyStructure("Jackson")
@app.errorhandler(APIException)
def handle_invalid_usage(error):
    return jsonify(error.to_dict()), error.status_code
@app.route('/members', methods=['GET'])
def show_all_members():
    members= jackson_family.get_all_members()
    return jsonify (members )
@app.route('/member/<int:member_id>', methods=['GET'])
def show_one_member(member_id):
    member= jackson_family.get_member(member_id)
    return jsonify (member )
@app.route('/members', methods=['POST'])
def add_member():
    new_member= jackson_family.add_member(request.json)
    return jsonify(new_member)
@app.route('/member/<int:member_id>', methods=['DELETE'])
def kill_member(member_id):
    diying_member= jackson_family.delete_member(member_id)
    return jsonify(diying_member)

@app.route('/')
def sitemap():
    return generate_sitemap(app)
# this only runs if `$ python src/app.py` is executed
if __name__ == '__main__':
    PORT = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=PORT, debug=True)
