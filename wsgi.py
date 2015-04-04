#!/usr/bin/python
import os
import cgi
import vk
import json

virtenv = os.environ['OPENSHIFT_PYTHON_DIR'] + '/virtenv/'
virtualenv = os.path.join(virtenv, 'bin/activate_this.py')
try:
    execfile(virtualenv, dict(__file__=virtualenv))
except IOError:
    pass

EVGENY_ACCESS_TOKEN='#####################################################################################'
USER_ID=283030161

#
# IMPORTANT: Put any additional includes below this line.  If placed above this
# line, it's possible required libraries won't be in your searchable path
#

def application(environ, start_response):

    html = ""
    if environ['REQUEST_METHOD'] == 'POST':
        post_environ = environ.copy()
        post_environ['QUERY_STRING'] = ''
        post = cgi.FieldStorage(
            fp=environ['wsgi.input'],
            environ=post_environ,
            keep_blank_values=True
        )

        decoded = json.loads(post['payload'].value)
        repository = decoded['repository']
        repo = repository['name']
        owner = repository['owner_name']
        build_num = decoded['number']
        build_url = decoded['build_url']
        message = decoded['message']
        result = decoded['status_message']

        new_message = owner + "/" + repo + " build number #" + build_num + ": " + result + "\ncommit: " + message + "\n" + build_url
        vkapi = vk.API(access_token=EVGENY_ACCESS_TOKEN)
        vkapi.messages.send(user_ids=USER_ID, message=new_message)

    status = '200 OK'
    response_headers = [('Content-Type', "text/plain"), ('Content-Length', str(len(html)))]
    #
    start_response(status, response_headers)
    return [""]

#
# Below for testing only
#
if __name__ == '__main__':
    from wsgiref.simple_server import make_server
    httpd = make_server('localhost', 8051, application)
    # Wait for a single request, serve it and quit.
    httpd.serve_forever()
