from flask import Flask, render_template, request, url_for, redirect, make_response, flash
from email.message import EmailMessage
from dotenv import load_dotenv
import os, smtplib, logging

load_dotenv()

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Setup logging
app.logger.setLevel(logging.INFO)

def is_registered():
    return request.cookies.get("registered-username") and request.cookies.get("registered-userpassword")

def is_logged_in():
    return request.cookies.get("login-username") and request.cookies.get("login-userpassword")

@app.route('/')
def index():
    alertMessage = request.args.get('alertMessage')
    return render_template('index.html', alertMessage=alertMessage)

@app.route('/login')
def login():
    alertMessage = request.args.get('alertMessage')
    next_page = request.args.get('next')
    return render_template('login.html', alertMessage=alertMessage, next=next_page)

@app.route('/thank/<name>')
def thank(name):
    message = request.args.get('message')
    return render_template("thank.html", name=name, message=message)

@app.route('/register')
def register():
    alertMessage = request.args.get('alertMessage')
    return render_template("register.html", alertMessage=alertMessage)

@app.route('/register/registered', methods=['POST'])
def registered():
    if not is_registered():
        userFirstName = request.form.get("userfirstname").strip()
        userLastName = request.form.get("userlastname").strip()
        userName = f"{userFirstName} {userLastName}"
        email = request.form.get("useremail").strip()
        password = request.form.get("userpassword").strip()

        resp = make_response(redirect(url_for('thank', name=userName, message='Registering')))
        max_age = 60 * 60 * 24 * 365 * 20
        resp.set_cookie("registered-username", userName.lower(), max_age=max_age)
        resp.set_cookie("registered-useremail", email, max_age=max_age)
        resp.set_cookie("registered-userpassword", password, max_age=max_age)
        return resp
    flash("You already have an Active Account")
    return redirect(url_for('login'))

@app.route('/login/logged', methods=['POST'])
def logged():
    if is_registered():
        name = request.form.get("username").strip().lower()
        email = request.form.get("useremail").strip()
        password = request.form.get("userpassword").strip()
        remember = request.form.get("remember")
        next_page = request.form.get('next') or url_for('index')

        registered_name = request.cookies.get("registered-username")
        registered_email = request.cookies.get("registered-useremail")
        registered_password = request.cookies.get("registered-userpassword")

        if name == registered_name and email == registered_email and password == registered_password:
            resp = make_response(redirect(next_page))
            if remember == "on":
                max_age = 60 * 60
                resp.set_cookie("login-username", name, max_age=max_age)
                resp.set_cookie("login-useremail", email, max_age=max_age)
                resp.set_cookie("login-userpassword", password, max_age=max_age)
            return resp

        flash('Wrong Credentials!')
        return redirect(url_for('login'))

    flash("You do not have an Active Account")
    return redirect(url_for('register'))

@app.route('/forgetpass')
def forgetpass():
    if is_registered():
        registered_name = request.cookies.get("registered-username")
        registered_email = request.cookies.get("registered-useremail")
        registered_password = request.cookies.get("registered-userpassword")

        return f'''<h1> YOUR LOGIN DETAILS! </h1>
                <h5>&emsp;Username: {registered_name}</h5>
                <h5>&emsp;Email: {registered_email}</h5>
                <h5>&emsp;Password: {registered_password}</h5>'''
    
    flash('Please register yourself')
    return redirect(url_for('register'))

@app.route('/projects/')
def projects():
    next_page = request.args.get('next')
    if not next_page:
        return '''<h1>This Project is Not Available!</h1>
                <h1>Check other Projects</h1>'''
    
    if not is_registered():
        return redirect(url_for('register'))

    if not is_logged_in():
        return redirect(url_for('login', next=next_page))
    
    return redirect(next_page)

@app.route('/sendemail/', methods=['GET', 'POST'])
def sendEmail():
    if request.method == "POST":
        name = request.form.get('username').strip()
        email = request.form.get('useremail').strip()
        profession = request.form.get('profession')
        message = request.form.get('usermessage').strip()

        my_email = os.getenv("PORTFOLIO_EMAIL")
        my_password = os.getenv("PORTFOLIO_EMAIL_PASSWORD")

        msg = EmailMessage()
        msg.set_content(f"Name: {name}\nEmail: {email}\nProfession: {profession}\nMessage: {message}")
        msg["To"] = my_email
        msg["From"] = email
        msg["Subject"] = f"Hi, I am {name}"

        try:
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(my_email, my_password)

                if message and len(message.replace(" ", "")) >= 50:
                    server.send_message(msg)
                elif message:
                    flash('Your message must have minimum 50 letters')
                    return redirect(url_for('index'))
                else:
                    flash("Your message cannot be Empty")
                    return redirect(url_for('index'))

            return redirect(url_for('thank', name=name, message="Sending message"))

        except Exception as e:
            app.logger.error(f"Failed to send email: {e}")
            flash("Something went wrong while sending the message.")

    return redirect('/')
