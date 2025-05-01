from flask import Flask, render_template, request, url_for, redirect, make_response,flash
from email.message import EmailMessage
import smtplib, os
import logging

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24)

# Setup logging
app.logger.setLevel(logging.INFO)

@app.route('/')
def index():
    alertMessage= request.args.get('alertMessage')
    return render_template('index.html', alertMessage=alertMessage)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/thank/<name>')
def thank(name):
    message = request.args.get('message')
    return render_template("thank.html", name=name, message=message)

@app.route('/login/logged', methods=['POST'])
def logged():
    name = request.form.get("username")
    email = request.form.get("useremail")
    password = request.form.get("userpassword")
    remember = request.form.get("remember")
    
    if remember == "on":
        resp = make_response(redirect(url_for('thank', name=name, message='Registering')))
        resp.set_cookie("username", name, max_age=60*60)
        resp.set_cookie("useremail", email, max_age=60*60)
        resp.set_cookie("userpassword", password, max_age=60*60)
        return resp
    
    return redirect(url_for('thank', name=name, message="Registering"))

@app.route('/sendemail/', methods=['GET', 'POST'])
def sendEmail():
    if request.method == "POST":
        name = request.form.get('username').strip()
        email = request.form.get('useremail').strip()
        profession = request.form.get('profession')
        message = request.form.get('usermessage').strip()
        
        my_email = os.environ.get("PORTFOLIO_EMAIL")
        my_password = os.environ.get("PORTFOLIO_EMAIL_PASSWORD")
        
        # Compose the email
        msg = EmailMessage()
        msg.set_content(f"Name: {name}\nEmail: {email}\nProfession: {profession}\nMessage: {message}")
        msg["To"] = my_email
        msg["From"] = email
        msg["Subject"] = f"Hi, I am {name}"

        try:
            # Set up the SMTP server
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.ehlo()
                server.starttls()
                server.login(my_email, my_password)
                if (message and len(message.replace(" ", "")) >=50):
                    server.send_message(msg)
                elif (message and len(message.replace(" ", "")) <50) :
                    flash('Your message must have minimum 50 letters')
                    return redirect(url_for('index'))
                else:
                    flash("Your message cannot be Empty")
                    return redirect(url_for('index'))
            
            return redirect(url_for('thank', name=name, message="Sending message"))
            
        except Exception as e:
            app.logger.error(f"Failed to send email: {e}")
    
    return redirect('/')

@app.route('/projects/<path:directory>')
def projects(directory):
    if request.cookies.get("username") and request.cookies.get("userpassword"):
        if directory != "null":
            return redirect(f"https://github.com/sasmal-samiran/{directory}")
        else:
            return "<h1>Project Not Available</h1>"
    
    return redirect(url_for('login'))

