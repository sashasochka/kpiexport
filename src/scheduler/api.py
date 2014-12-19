"""API

This module contains functions to interact with different system entities
"""

import os
from base64 import b64decode, b64encode
from hashlib import sha256

from scheduler.model import *


def get_salt(self):
    """Generates a cryptographically random salt and sets its Base64 encoded
    version to the salt column, and returns the encoded salt.
    """
    if not self.id and not self._salt:
        self._salt = b64encode(os.urandom(8))

    if isinstance(self._salt, str):
        self._salt = self._salt.encode('UTF-8')

    return self._salt


def encrypt_password(password, salt):
    """
    Encrypts the password with the given salt using SHA-256. The salt must
    be cryptographically random bytes.

    :param password: the password that was provided by the user to try and
                     authenticate. This is the clear text version that we
                     will need to match against the encrypted one in the
                     database.
    :type password: basestring

    :param salt: the salt is used to strengthen the supplied password
                 against dictionary attacks.
    :type salt: an 8-byte long cryptographically random byte string
    """

    if isinstance(password, str):
        password_bytes = password.encode("UTF-8")
    else:
        password_bytes = password

    hashed_password = sha256()
    hashed_password.update(password_bytes)
    hashed_password.update(salt)
    hashed_password = hashed_password.hexdigest()

    if not isinstance(hashed_password, str):
        hashed_password = hashed_password.decode("UTF-8")

    return hashed_password


def validate_password(self, password):
    """Check the password against existing credentials.

    :type password: str
    :param password: clear text password
    :rtype: bool
    """
    return self._password == encrypt_password(password,
                                                    b64decode(str(self._salt)))


def create_user(writer, **kwargs):
    def user_create_callback(student):
        st = {}
        for field in student._reverse_db_field_map:
            if field not in ['_salt', '_password']:
                st[field] = student.get_field_value(field)
        writer(st)

    student = User(**kwargs)
    get_salt(student)
    student._password = encrypt_password(student.password,
                                        b64decode(str(student._salt)))
    student.save(user_create_callback)


def authenticate_user(writer, **kwargs):
    def user_auth_callback(student):
        try:
            student = student[0]
        except KeyError:
            #writer({})
            raise IOError

        import ipdb; ipdb.set_trace()

        if validate_password(student, kwargs['password']):
            st = {}
            for field in student._reverse_db_field_map:
                if field not in ['_salt', '_password']:
                    st[field] = student.get_field_value(field)

            writer(st)
        else:
            #writer({})
            raise IOError

    student = User.objects \
            .limit(1) \
            .filter(email = kwargs['email']) \
            .find_all(callback=user_auth_callback)


def logout_user(**kwargs):
    pass


def create_university(**kwargs):
    pass


def get_universities(**kwargs):
    pass


def create_group(**kwargs):
    pass


def get_groups(**kwargs):
    pass


def create_class(**kwargs):
    pass


def create_timetable(**kwargs):
    pass


def create_comment(**kwargs):
    pass
