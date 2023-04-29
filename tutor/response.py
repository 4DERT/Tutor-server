SUCCESS = {'status': 'success', 'message': 'Data processed successfully'}, 200

BAD_REQUEST = {'status': 'error', 'message': 'The server cannot or will not process the request due to '
                                             'something that is perceived to be a client error.'}, 400

UNAUTHORIZED = {'status': 'error', 'message': 'The client must authenticate themself to get the requested '
                                              'response.'}, 401

FORBIDDEN = {'status': 'error', 'message': 'The client does not have access rights to the content'}, 403

CONFLICT = {'status': 'error', 'message': 'Request conflicts with the current state of the server.'}, 409

EXISTING_EMAIL = {'status': 'error', 'message': 'User with given email already exists.'}, 409

NOT_VALID_EMAIL = {'status': 'error', 'message': 'Email is not valid.'}, 409

EXISTING_PHONE = {'status': 'error', 'message': 'User with given phone number already exists.'}, 409

NOT_VALID_PHONE = {'status': 'error', 'message': 'Phone number is not valid.'}, 409

EXISTING_USERNAME = {'status': 'error', 'message': 'User with given username already exists.'}, 409

NOT_STUDENT = {'status': 'error', 'message': 'To perform this action you must be a student.'}, 409

NOT_VALID_DEGREE_COURSE = {'status': 'error', 'message': 'Degree course is not valid.'}, 409

EXISTING_DEGREE_COURSE = {'status': 'error', 'message': 'Degree course already exists.'}, 409

EXISTING_SUBJECT = {'status': 'error', 'message': 'Subject already exists.'}, 409

NOT_VALID_SUBJECT = {'status': 'error', 'message': 'Subject is not valid.'}, 409

NOT_VALID_RATE = {'status': 'error', 'message': 'Rate must be an int between 1 and 5.'}, 409

NOT_VALID_SEMESTER = {'status': 'error', 'message': 'Semester must be an int between 1 and 7.'}, 409

NOT_VALID_PASSWORD = {'status': 'error', 'message': 'Old password is not correct.'}, 409

MISSING_FILE = {'status': 'error', 'message': 'Missing avatar file.'}, 409

FILE_TOO_BIG = {'status': 'error', 'message': 'Avatar must be max 512x512px.'}, 409

FILE_FORMAT = {'status': 'error', 'message': 'File must be either PNG or JPEG.'}, 409
