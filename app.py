from flask import Flask,render_template, request, url_for, redirect, make_response
from email.message import EmailMessage
import smtplib, os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/thank/<name>')
def thank(name):
    return render_template("thank.html", name=name)

@app.route('/login/logged', methods=['POST'])
def logged():
    name = request.form.get("username")
    email = request.form.get("useremail")
    password = request.form.get("userpassword")
    remember = request.form.get("remember")
    
    if remember=="on":
        resp = make_response(redirect(url_for('thank')))
        resp.set_cookie("username", name, max_age=60*60)
        resp.set_cookie("useremail", email, max_age=60*60)
        resp.set_cookie("userpassword", password, max_age=60*60)
        return resp
    
    return redirect(url_for('thank', name=name))


@app.route('/sendemail/', methods=['GET','POST'])
def sendEmail():
    if request.method == "POST":
        name = request.form.get('username')
        email = request.form.get('useremail')
        profession = request.form.get('profession')
        message = request.form.get('usermessage')

        my_email = os.environ.get("PORTFOLIO_EMAIL")
        my_password =  os.environ.get("PORTFOLIO_EMAIL_PASSWORD")
        
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
                # Send the email
                server.send_message(msg)
            
        except Exception as e:
            print(f"Failed to send email: {e}")
        return "Done"
    
    return redirect('/')

@app.route('/projects/')
def projects():
    if request.cookies.get("username") and request.cookies.get("userpassword"):
        return redirect("https://github.com/sasmal-samiran/javaAwt.git")
    
    return redirect(url_for('login'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
