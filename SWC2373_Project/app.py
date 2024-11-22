import json
from flask import Flask, render_template, request, redirect, url_for, session
import os
import uuid
from flask import flash


app = Flask(__name__)
app.secret_key = "ZWNiNmU5OGMtNmJlZS00OWMxLTlmM2EtZTZkM2I3MzZhOGVkMjNlZDEwYzEtNmYx_P0A1_652b5f1d-9846-4334-8b83-52d9cf3b9b81"  

USER_DATA_FILE = "users.json"  # File to store user data
MEETING_DATA_FILE = "meetings.json"  # File to store meeting data

# Utility function to load user data
def load_users():
    try:
        with open('users.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_users(users):
    with open('users.json', 'w') as file:
        json.dump(users, file, indent=4)

# Utility function to load meeting data
def load_meetings():
    try:
        with open(MEETING_DATA_FILE, "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return []

# Utility function to save meeting data
def save_meetings(meetings):
    with open(MEETING_DATA_FILE, "w") as file:
        json.dump(meetings, file, indent=4)

# Generate a unique room ID
def generate_room_id():
    return str(uuid.uuid4().hex)[:8]  # Generate an 8-character unique room ID

@app.route('/')
def home():
    return redirect('/login')  # Redirect to the login page or any default page

# Route for user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        # Fetch form data
        title = request.form.get('title')
        first_name = request.form.get('first_name')
        last_name = request.form.get('last_name')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Load existing user data
        users = load_users()
        
        # Check if user already exists
        if email in users:
            flash('User already exists! Please try logging in.', 'error')
            return render_template('register.html', error="User already exists!")
        
        # Save new user
        users[email] = {
            'title': title,
            'first_name': first_name,
            'last_name': last_name,
            'password': password
        }
        save_users(users)
        
        # Flash success message
        flash('Registration successful! You can now log in.', 'success')
        return redirect(url_for('login'))

    # Render registration page for GET requests
    return render_template('register.html')


# Route for user login
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        users = load_users()

        if email in users and users[email]['password'] == password:
            session['username'] = users[email]['first_name']  # Use first name or full name
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid credentials', 'danger')

    return render_template('login.html')

# Route for dashboard
@app.route('/dashboard', methods=['GET'])
def dashboard():
    if 'username' in session:
        meetings = load_meetings()  # Make sure `load_meetings()` loads data from `meetings.json`
        return render_template('dashboard.html', username=session['username'], meetings=meetings)
    return redirect(url_for('login'))

# Route for scheduling a meeting
@app.route('/schedule', methods=['GET', 'POST'])
def schedule():
    if request.method == 'POST':
        room_name = request.form['room_name']
        date = request.form['date']
        time = request.form['time']
        room_id = generate_room_id()  # Create a unique room ID

        # Save meeting data
        meetings = load_meetings()
        meetings.append({
            "room_id": room_id,
            "room_name": room_name,
            "date": date,
            "time": time,
            "participants": []
        })
        save_meetings(meetings)

        # Redirect to the meeting room
        return redirect(url_for('meeting', room_id=room_id))

    return render_template('schedule.html')

@app.route('/meeting/<room_id>')
def meeting(room_id):
    if 'username' not in session:
        return redirect(url_for('login'))  # Redirect to login if not logged in

    meetings = load_meetings()
    meeting_data = next((m for m in meetings if m['room_id'] == room_id), None)
    if not meeting_data:
        return "Meeting not found!", 404

    # Add the current user to the participants list if not already added
    username = session.get('username')
    if username not in meeting_data.get('participants', []):
        meeting_data['participants'].append(username)
        save_meetings(meetings)  # Save the updated meeting data

    return render_template(
        'meeting.html',
        username=username,
        meeting=meeting_data,
        participants=meeting_data.get('participants', [])
    )

#route for join meeting
@app.route('/join_meeting/<room_id>')
def join_meeting(room_id):
    meetings = load_meetings()  # Make sure `load_meetings()` is defined
    meeting = next((m for m in meetings if m['room_id'] == room_id), None)
    if not meeting:
        return "Meeting not found!", 404

    return redirect(url_for('meeting', room_id=room_id))

# Route for user logout
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    print("Available routes:")
    print(app.url_map)  # This will list all registered routes
    app.run(debug=True, port=5000)
