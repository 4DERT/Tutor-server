SUCCESS = {'status': 'success', 'message': 'Data processed successfully'}, 200

BAD_REQUEST = {'status': 'error', 'message': 'The server cannot or will not process the request due to '
                                             'something that is perceived to be a client error.'}, 400

UNAUTHORIZED = {'status': 'error', 'message': 'The client must authenticate itself to get the requested '
                                              'response.'}, 401

FORBIDDEN = {'status': 'error', 'message': 'The client does not have access rights to the content'}, 403

CONFLICT = {'status': 'error', 'message': 'Request conflicts with the current state of the server.'}, 409
