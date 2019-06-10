import logging
 
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model
from test_nord.celery import app
 
 
@app.task
def send_email(user_id):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(pk=user_id)
        send_mail(
            'You have just registered in our bookshop' ,
            'This is your login {} and password {}'.format(user.email, user.password),
            'from@my_blog.dev', 
            [user.email],
            fail_silently=False,
        )
    except UserModel.DoesNotExist:
        logging.warning("Tried to send verification email to non-existing user '%s'" % user_id)