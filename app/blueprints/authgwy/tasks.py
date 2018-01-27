from flask import current_app, render_template
from flask_mail import Message
from app.extensions import mail
#from app.extensions import celery
from threading import Thread

# @celery.task(name='tasks.send_email')
# def send_async_email(to, subject, template, **kwargs):
# 	app = current_app._get_current_object()
# 	msg = Message(app.config['MESH_MAIL_SUBJECT_PREFIX'] + ' ' + subject, sender=app.config['MAIL_USERNAME'], recipients=[to])
# 	msg.body = render_template(template + '.txt', **kwargs)
# 	msg.html = render_template(template + '.html', **kwargs)
# 	"""Background task to send an email with Flask-Mail."""
# 	with app.app_context():
# 		mail.send(msg)


def send_async_email(app, msg):
    with app.app_context():
        mail.send(msg)


def send_email(to, subject, template, **kwargs):
    app = current_app._get_current_object()
    print("MAIL_USERNAME in email: " + app.config['MAIL_USERNAME'])
    msg = Message(app.config['BLOG_PREFIX'] + ' ' + subject,
                  sender=app.config['MAIL_USERNAME'], recipients=[to])
    msg.body = render_template(template + '.txt', **kwargs)
    msg.html = render_template(template + '.html', **kwargs)
    thr = Thread(target=send_async_email, args=[app, msg])
    thr.start()
    return thr