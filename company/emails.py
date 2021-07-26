from django.core.mail import send_mail, EmailMessage
from django.template.loader import render_to_string
from django.conf import settings


def sendEmail():
    context = {
        'news': 'We have good news!'
    }
    send_mail(
        subject='Test Send Mail #1',
        message='Kindly Ignore',
        from_email='druashley@gmail.com',
        recipient_list=['druashley@gmail.com', ],
        fail_silently=False,
        html_message=render_to_string('email.html', context=context)
    )


# def send_html_email(to_list, subject, template_name, context, sender=settings.DEFAULT_FROM_EMAIL):
#     msg_html = render_to_string(template_name, context)
#     msg = EmailMessage(subject=subject, body=msg_html,
#                        from_email=sender, bcc=to_list)
#     msg.content_subtype = "html"  # Main content is now text/html
#     return msg.send()
