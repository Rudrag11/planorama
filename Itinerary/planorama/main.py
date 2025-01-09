from flask import Flask, render_template, request, redirect, session, url_for
import mysql.connector as ms
from itinerary_generator import generate_itinerary  

GOOGLE_MAPS_API_KEY = 'AIzaSyCVvS3wpd8Lm1tm7NyTsIBMF-DWqTZIWN8'

conn = ms.connect(host="localhost", port=3306, user="root", passwd="Rudrag11!", database="itinerary")
mc = conn.cursor()

app = Flask(__name__)

@app.route('/')
def main_page():
    return render_template("landing.html")

@app.route('/signup/whereto', methods=['POST'])
def enter_details():
    if request.method == 'POST':
        global username
        username = request.form['username']
        password = request.form['password']
        mc.execute("insert into users values(%s,%s)", (username, password))
        conn.commit()
        return render_template("wheretopage.html")

@app.route('/signup')
def signup_page():
    return render_template("signup.html")

@app.route('/login')
def login_page():
    return render_template("login.html")

@app.route('/whereto', methods=['GET','POST'])
def dashboard_page():
    if request.method == 'POST':
        global username
        username = request.form['username']
        password = request.form['password']
        mc.execute("SELECT * FROM users WHERE username=%s AND password=%s", (username, password))
        result = mc.fetchall()
        conn.commit()
        
        if result:
            return render_template("wheretopage.html")
        else:
            err = "Invalid username or password!"
            return render_template("login.html")
    else:
        return render_template("wheretopage.html")

@app.route('/details', methods=['POST'])
def get_details():
    if request.method == 'POST':
        global destination
        destination = request.form['dest']
        mc.execute(
            "INSERT INTO itineraries (username, dest) VALUES (%s,%s)",
            (username, destination)
        )
        conn.commit()
        return render_template("details.html", destination=destination)

@app.route('/generate-itinerary', methods=['POST'])
def create_itinerary():
    if request.method == 'POST':
        budget = int(request.form['budget'])
        start_date = request.form['startDate']
        end_date = request.form['endDate']
        num_people = int(request.form['numPeople'])
        min_rating = float(request.form['minRating'])
        print(num_people, budget, start_date, end_date, min_rating, username, destination)

        itinerary = generate_itinerary(destination, budget, min_rating, start_date, end_date)

        # Update itinerary details in the database
        mc.execute(
            "UPDATE itineraries SET nop = %s, budget = %s, start = %s, end = %s, rate = %s WHERE username = %s and dest=%s",
            (num_people, budget, start_date, end_date, min_rating, username, destination)
        )
        conn.commit()

        # Pass itinerary data including place IDs and photo references to the template
        return render_template("itinerary.html", itinerary=itinerary, username=username)

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('main_page'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)
