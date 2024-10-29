import smtplib
from email.mime.text import MIMEText
from flask_mail import Mail

mail=Mail(app)
app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USERNAME'] = 'ihrdmcaproject2019@gmail.com'
app.config['MAIL_PASSWORD'] = 'project@2019'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True



@app.route('/vactime',methods=['get','post'])
def vactime():
    email=request.form['email']
    cmd.execute("SELECT email,vacdate FROM `useremail` WHERE `vid`='" + str(s[1]) + "'")
    s1 = cmd.fetchone()
    print(s1)
    email = s1[0]
    date = s1[1]
    try:
        gmail = smtplib.SMTP('smtp.gmail.com', 587)
        gmail.ehlo()
        gmail.starttls()
        gmail.login('ihrdmcaproject2019@gmail.com', 'project@2019')
    except Exception as e:
        print("Couldn't setup email!!" + str(e))
    msg = MIMEText("Your next vaccination date : " + date)
    print(msg)
    msg['Subject'] = 'Vaccination Info'
    msg['To'] = email
    msg['From'] = 'ihrdmcaproject2019@gmail.com'
    try:
        gmail.send_message(msg)
    except Exception as e:
        print("COULDN'T SEND EMAIL", str(e))
    con.commit()
    return '''<script>alert("successfully"); window.location="/hospital"</script>'''


