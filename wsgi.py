#!/usr/bin/python
import os
import cgi
from cgi import parse_qs, escape
from wsgiref.simple_server import make_server
import urllib
import json
import vk

is_auth = False
vkapi = vk.API

# $c - commit
# $n - build num
# $o - owner
# $m - message
# $s - status message
# $r - repo name
# $rid - repo id
# $bid - build id
# $rurl - repo url
# $burl - build url
# $started - started time
# $finished - finished build time
# $duration - duration
# $branch - branch
# $compareurl - compare commit url
# $commitername - commiter name
# $commitermail - commiter mail
# $tag - tag
# $pullrequest - pull request
# $pullrequestnum - pull request number
# $pullrequesttitle - pull request title
# Standart format: $o/$r build number #$n: $s\ncommit: $m\n$burl

def format_message(buffer, message_format):
    decoded = json.loads(buffer)
    repo = decoded['repository']
    formats = { "$pullrequestnum": decoded['pull_request_number'],
                "$pullrequesttitle": decoded['pull_request_title'],
                "$pullrequest": decoded['pull_request'],
                "$rid": str(repo['id']),
                "$bid": str(decoded['id']),
                "$rurl": 'https://github.com/'+repo['owner_name']+'/'+repo['name'],
                "$burl": decoded['build_url'],
                "$started": decoded['started_at'],
                "$finished": decoded['finished_at'],
                "$duration": str(decoded['duration']),
                "$branch": decoded['branch'],
                "$compareurl": decoded['compare_url'],
                "$commitername": decoded['committer_name'],
                "$commitermail": decoded['committer_email'],
                "$tag": decoded['tag'],
                "$c": decoded['commit'],
                "$n": decoded['number'],
                "$o": repo['owner_name'],
                "$m": decoded['message'],
                "$s": decoded['status_message'],
                "$r": repo['name'],
                "\\n": "\n"
    }
    message = message_format
    for key, value in formats.iteritems():
        if isinstance(value, basestring):
            message = message.replace(key, value)
    return message

def application(environ, start_response):
    global is_auth
    global vkapi

    d = parse_qs(environ['QUERY_STRING'])
    user_ids = d.get('ids', [])
    user_ids = [escape(user_id) for user_id in user_ids]
    
    message_format = d.get('format', [])
    if message_format:
        message_format = urllib.unquote(escape(message_format[0])).decode('utf8')
    else:
        message_format = "$o/$r build number #$n: $s\ncommit: $m\n$burl"

    if environ['REQUEST_METHOD'] == 'POST':
        length = int(environ.get('CONTENT_LENGTH', '0'))

        if not is_auth:
            vkapi = vk.API(app_id=app_id, user_login=user_login, user_password=user_password, scope="messages,friends")
            is_auth = True
        
        message = format_message(environ['wsgi.input'].read(length), message_format) 
        vkapi.messages.send(user_ids=user_ids, message=message)
    
    status = '200 OK'
    response_headers = [('Content-Type', "text/plain"), ('Content-Length', str(len("")))]
    start_response(status, response_headers)
    return [""]

if __name__ == '__main__':
    print "Started server..."
    httpd = make_server('localhost', 8051, application)
    httpd.serve_forever()
