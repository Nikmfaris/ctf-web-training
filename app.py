from flask import Flask, render_template, request, jsonify, session
import json

app = Flask(__name__)
app.secret_key = 'dev-secret-key'

# Simple student database (stored in memory)
students = []

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/plugins')
def plugins():
    return render_template('plugins.html')

@app.route('/api/me', methods=['GET'])
def me():
    return jsonify({
        "name": session.get('username', 'guest'),
        "isadmin": bool(session.get('is_admin', False))
    })

@app.route('/api/login', methods=['POST'])
def login():
    data = request.get_json() or {}
    session['username'] = data.get('username', 'guest')
    session['is_admin'] = bool(data.get('isadmin', False))
    return jsonify({
        "name": session['username'],
        "isadmin": session['is_admin']
    })

@app.route('/api/logout', methods=['POST'])
def logout():
    session.clear()
    return jsonify({"success": True})

# SIMPLE VULNERABLE API
# Any person can add/delete students without permission!
@app.route('/api/students', methods=['GET', 'POST'])
def get_students():
    global students
    
    if request.method == 'GET':
        return jsonify(students)
    
    # POST - Add student (NO VALIDATION!)
    data = request.get_json()
    student = {
        "id": len(students) + 1,
        "name": data.get('name', 'Unknown'),  # Takes ANY data!
        "added_by": session.get('username', 'guest'),
        "isadmin": bool(session.get('is_admin', False))
    }
    students.append(student)
    return jsonify(student)

# DELETE - Anyone can delete (NO PERMISSION CHECK!)
@app.route('/api/students/<int:sid>', methods=['DELETE'])
def delete_student(sid):
    global students
    if not session.get('is_admin', False):
        return jsonify({"error": "Admin only"}), 403
    if 0 < sid <= len(students):
        students.pop(sid - 1)
        # Return the flag when a delete succeeds
        return jsonify({"success": True, "flag": "CTF{deleted_student_success}"})
    return jsonify({"error": "Not found"}), 404

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=6767)
