import os
import smtplib, email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import re
from threading import Thread
from copy import deepcopy

MAX_THREADS = 20

d = {}
d['EMAIL_SENDER'] = os.environ.get('EMAIL_SENDER')
d['EMAIL_PASSWORD'] = os.environ.get('EMAIL_PASSWORD')
d['EMAIL_SERVER'] = os.environ.get('EMAIL_SERVER')
d['EMAIL_PORT'] = os.environ.get('EMAIL_PORT')


def html_to_text(html):
    text = html.replace("<br>", "\n") \
               .replace("<br />", "\n")

    r = re.compile(r'<.*?>', re.DOTALL)
    text = r.sub("", text)

    return text


def fast_email(recipients=None, subject='MSG', html_msg='', thread_no=None):
    """
    This function can send many emails very fast by using multiple threads.
    It can send the same message with the same subject to many recipients 
    at once, or it can send a different message to every recipient.

    Input
    -----
    recipients : a list of e-mail addresses as strings
    subject : a single string or a list of strings
    html_msg : a single string with html text or a list of strings
    thread_no : an integer that can override the default number of threads to use

    Output
    ------
    If there are no input errors the function doesn't return anything, but it
    sends all e-mails and prints each e-mail address and either 'OK' or 
    'ERROR' next to it.

    Caution
    -------
    If subject or html_msg are lists, they must be the same length as
    recipients.
    """
    if recipients is None:
        recipients = [os.environ.get('EMAIL_RECIPIENT')]

    if thread_no is None:
        thread_no = min(len(recipients), MAX_THREADS)

    if type(recipients) != list or recipients == []:
        # here should be raise element instead of return string
        return  "recipients should be a list with at least one e-mail address"
    if type(subject) == list and len(subject) != len(recipients):
        # here should be raise element instead of return string
        return "Number of subjects doesn't equal the number of recipients."
    if type(html_msg) == list and len(html_msg) != len(recipients):
        # here should be raise element instead of return string
        return "Number of html messages doesn't equal the number of recipients."

    msg_data = {}
    """
    {
        'recipients': ['email1', 'email2', ...],
        'subject': ['subject1', 'subject2', ...],
        'html_msg': ['html_msg1', 'html_msg2', ...],
        'text_msg': ['text_msg1', 'text_msg2', ...],
    }
    """
    msg_data['recipients'] = recipients

    if type(html_msg) == str:
        msg_data['html_msg'] = [html_msg for i in range(len(recipients))]
        
        text_msg = html_to_text(html_msg)
        msg_data['text_msg'] = [text_msg for i in range(len(recipients))]
    
    elif type(html_msg) == list:
        msg_data['html_msg'] = html_msg
        msg_data['text_msg'] = []

        for i, html in enumerate(html_msg):
            text_msg = html_to_text(html)
            msg_data['text_msg'].append(text_msg)

    if type(subject) == str:
        msg_data['subject'] = [subject for i in range(len(recipients))]

    elif type(subject) == list:
        msg_data['subject'] = subject


    def send(msg_data, d):
        server = smtplib.SMTP_SSL(d['EMAIL_SERVER'], d['EMAIL_PORT'])
        server.ehlo()
        server.login(d['EMAIL_SENDER'], d['EMAIL_PASSWORD'])

        message = MIMEMultipart("alternative")
        message["From"] = d['EMAIL_SENDER']

        for i in range(len(msg_data['recipients'])):
            del(message['Subject'])
            message['Subject'] = msg_data['subject'][i]

            part1 = MIMEText(msg_data['text_msg'][i], "plain")
            part2 = MIMEText(msg_data['html_msg'][i], "html")

            message.attach(part1)
            message.attach(part2)

            del(message['To'])
            message["To"] = msg_data['recipients'][i]

            try:
                server.sendmail(
                    d['EMAIL_SENDER'],
                    msg_data['recipients'][i],
                    message.as_string().encode('utf-8')
                )
            except:
                print(f'{msg_data["recipients"][i]} ERROR')
            else:
                print(f'{msg_data["recipients"][i]} OK')

        server.quit()


    # split recipients into groups, each group being 
    # one sublist of targets variable
    y = {
        'recipients': [],
        'subject': [],
        'html_msg': [],
        'text_msg': [],
    }
    targets = [deepcopy(y) for i in range(thread_no)]

    for i in range(len(recipients)):
        targets[i % thread_no]['recipients'].append(msg_data['recipients'][i])
        targets[i % thread_no]['subject'].append(msg_data['subject'][i])
        targets[i % thread_no]['html_msg'].append(msg_data['html_msg'][i])
        targets[i % thread_no]['text_msg'].append(msg_data['recipients'][i])

    # run multithreads
    threads = []

    for i in range(thread_no):
        t = Thread(target=send, args=(targets[i], d))
        threads.append(t)
        t.start()

    # wait until all threads are finished
    for t in threads:
        t.join()
