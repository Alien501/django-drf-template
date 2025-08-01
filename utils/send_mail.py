from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils.html import strip_tags
from django.conf import settings

def send_email(subject, to_email, context, template_name, attachments=None):
    """
    Send HTML email with template support
    """
    html_content = render_to_string(template_name, context)
    text_content = strip_tags(html_content)

    email = EmailMultiAlternatives(
        subject=subject,
        body=text_content,
        from_email=settings.EMAIL_HOST_USER,
        to=[to_email]
    )

    email.attach_alternative(html_content, "text/html")
    
    if attachments:
        for attachment in attachments:
            filename, content, mime_type = attachment
            email.attach(filename, content, mime_type)

    email.send()

def send_html_email(subject, to_email, context, template_name, attachments=None):
    """
    Alias for send_email for backward compatibility
    """
    return send_email(subject, to_email, context, template_name, attachments)