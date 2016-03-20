from django.conf import settings
from django.core.urlresolvers import set_script_prefix
from django.core.mail import EmailMultiAlternatives
from django.template import Context, RequestContext
from django.template.loader import get_template

def send_email(recipients, subject, template_name, email_context=Context()):
    text_content = get_template('notification/%s.txt'%template_name).render(email_context)
    html_content = get_template('notification/%s.html'%template_name).render(email_context)
    msg = EmailMultiAlternatives(subject, text_content, settings.DEFAULT_FROM_EMAIL, recipients)
    if html_content:
        msg.attach_alternative(html_content, "text/html")
    msg.send()

def notify(request, booking, subject, template_name, recipient=None):
    recipient = recipient or request.user.email
    email_context = RequestContext(request, {'booking': booking})
    send_email([recipient], subject, template_name, email_context)
