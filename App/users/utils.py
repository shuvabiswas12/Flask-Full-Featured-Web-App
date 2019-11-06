import os
from PIL import Image
import secrets
from App import app
from flask import url_for
from flask_mail import Message
from App import mail


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, file_extension = os.path.splitext(form_picture.filename)

    # rename the image with the hex number
    picture_filename = random_hex + file_extension

    # picture path where will save that
    picture_path = os.path.join(app.root_path, 'static/css/profile_pic', picture_filename)

    # resizing the image
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)

    # saving the image to the path
    i.save(picture_path)

    return picture_filename


def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message('Password Reset Request',
                  sender='noreply@demo.com',
                  recipients=[user.email])

    msg.body = f''' To reset your password, visit the following link:
    {url_for('reset_token', token=token, _external=True)}

    If you did not make this request then simply ignore this request and no change the password
    '''
    mail.send(msg)

