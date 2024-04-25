from flask import url_for
from flask_mail import Message
from app import mail

def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request', sender='no-reply@bisu.edu.ph', recipients=[user.email])
    msg.body = f'''To reset your password, vist the following link:
{url_for('users.reset_token', token=token, _external=True)}

If you did not request a password reset, then you can ignore this email
'''
    mail.send(msg)