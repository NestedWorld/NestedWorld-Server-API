from flask.ext.mail import Mail, Message
from flask.ext.mako import render_template

mail = Mail()

class TemplatedMessage(Message):

    def __init__(self, filename, html=None, **context):
        super().__init__()

        self.body = render_template(filename, **context)

        if html is not None:
            self.html = render_template(html, **context)

    def send(self):
        mail.send(self)
