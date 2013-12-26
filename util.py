import re
import random
import hmac
from string import letters

USER_RE = re.compile(r"^[a-zA-Z0-9_-]{3,20}$")

def valid_name(name):
	return name and USER_RE.match(name)

PASS_RE = re.compile(r"^.{3,20}$")

def valid_pass(password):
	return password and PASS_RE.match(password)

EMAIL_RE  = re.compile(r'^[\S]+@[\S]+\.[\S]+$')

def valid_email(email):
	return email or PASS_RE.match(email)

def make_salt(length = 5):
    return ''.join(random.choice(letters) for x in xrange(length))

def salt_password(password, salt = None):
	if not salt:
		salt = make_salt()
