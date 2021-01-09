# fast_email
High level email package made to send single or multiple emails in just 2 lines of code (including the import statement).

It uses multiple threads to send emails faster.

<hr>

### example 1 - fast message
```python
from fast_email import fast_email
fast_email('some message to myself')
```
`email@recipient.com OK`

<hr>

### example 2 - message should be html compatible
```python
from fast_email import fast_email
fast_email('<b><u>We are always writing html</u></b> here. <hr>')
```
`email@recipient.com OK`

<hr>

### example 3 - specify recipient and subject
```python
from fast_email import fast_email
fast_email(html_msg='Short notification',
           recipients=['different@recipient.com'],
           subject='some subject')
```
`different@recipient.com OK`

<hr>

### example 4 - send to multiple recipients
```python
from fast_email import fast_email
fast_email('Short notification',
           recipients=[
               'email1@recipient.com',
               'email2@recipient.com',
               'emailN@recipient.com',
           ],
           subject="some subject")
```
`email1@recipient.com OK`<br>
`email2@recipient.com OK`<br>
`emailN@recipient.com OK`<br>

<hr>

### example 5 - send unique message with unique subject to every recipient
**Note:** *if message is unique it doesn't mean that subject must be also (and vice versa)*
```python
from fast_email import fast_email
fast_email(html_msg=[
               'msg 1',
               'msg 2',
               'msg N'],
           recipients=[
               'email1@recipient.com',
               'email2@recipient.com',
               'emailN@recipient.com',
           ],
           subject=[
               "subject 1",
               "subject 2",
               "subject N",
           ])
```
`email1@recipient.com OK`<br>
`email2@recipient.com OK`<br>
`emailN@recipient.com OK`<br>

<hr>

**<span style="color: Red;">Care!</span>** 
Maximum thread number is hardcoded to be 20. I don't know if your email provider can ban you for sending emails that fast (if you send many). I am not responsible if that happens, so use your judgement and do your research if you intend to send a lot of emails. But also please - don't use it for spam :( You can change the maximum thread limit like below:
```python
from fast_email import fast_email
fast_email('some message',
           recipients=a_long_list_of_recipients,
           thread_no=5)
```

<hr>

# setup
In order for this package to work with just 2 lines of code we need to do some setup first. <br>
Basically we need to set 5 environment variables in our terminal of choice. <br>
This varies from terminal to terminal and in between operating systems, so you must research how to set environment variables for your OS and terminal. <br>
5 variables are: 
- `EMAIL_SENDER` : the email address that you will be sending FROM
- `EMAIL_PASSWORD` : the password to the EMAIL_SENDER address
- `EMAIL_SERVER` : the server of the EMAIL_SENDER address
- `EMAIL_PORT` : SMTP port appropriate to your EMAIL_SERVER (if not sure use port 465 for standard encrypted SMTP port and only if it doesn't work search for the one your server decided to use instead)
- `EMAIL_RECIPIENT` : the default recipient email address (this will allow you to email yourself faster with just fast_email('some message to myself'), so without specifying recipients every time)

To give a feeling of how this should look like, I will show my setup on MacOS using `zsh` for my terminal
- open or create `~/.zshenv` file
- create a section like below and place it at the end of `~/.zshenv` file (it's possible it was an empty file - that's fine)
```
export EMAIL_RECIPIENT=my_email@example.com
export EMAIL_SENDER=my_virtual_servant@example.com
export EMAIL_PASSWORD=averystrongandimpeccablepassword
export EMAIL_SERVER=example.com
export EMAIL_PORT=465
```
- save the file and restart the terminal
