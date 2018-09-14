from flask import Flask, render_template, session, request, redirect, flash
app = Flask(__name__)
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
from mysqlconnection import connectToMySQL
app = Flask(__name__)
app.secret_key = "ThisIsSecret!"
mysql = connectToMySQL('mydb2')
print("all the emails", mysql.query_db("SELECT * FROM emails;"))



@app.route("/", methods=['GET'])
def index():
    return render_template("index.html")

@app.route("/process", methods=["POST"])
def checker():
    # email
    mysql = connectToMySQL("mydb2")
    check = "SELECT email FROM emails"

    if len(request.form['email']) < 1:
        flash("Email cannot be blank!", "error")
    if not EMAIL_REGEX.match(request.form['email']):
        flash("Invalid Email Address!", "error")
    for i in (mysql.query_db(check)):
        if i['email'] == request.form['email']:
            flash("Email is taken!", "error")
            return redirect("/")

    if '_flashes' in session.keys():
        print("flash!!!!!!!!!!")
        return redirect("/")
    else:
        session['email'] = request.form['email']
        return redirect("/create_email")

@app.route("/create_email")
def create():
    mysql = connectToMySQL("mydb2")
    query = "INSERT INTO emails (email, created_at) VALUES (%(email)s, NOW());"
    data = {
             'email': session['email']
           }
    new_email_id = mysql.query_db(query, data)
    # when we do an insert, we get the newly created id!
    return redirect('/result')

@app.route("/result", methods=["GET"])
def result():
    mysql = connectToMySQL("mydb2")
    all_emails = mysql.query_db("select id, email, created_at from emails")
    print("Fetched all emails", all_emails)
    return render_template("result.html", emails = all_emails)

@app.route("/delete/<id>", methods=['GET'])
def delete(id):
    mysql = connectToMySQL("mydb2")
    query = "DELETE FROM emails WHERE id = %(id)s;"
    data = { "id" : id}
    new_email_id = mysql.query_db(query, data)
    session.clear()
    # when we do an insert, we get the newly created id!
    return redirect('/result')

if __name__=="__main__":
    app.run(debug=True) 