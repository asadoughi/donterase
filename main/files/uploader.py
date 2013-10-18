from poster.encode import multipart_encode
from poster.streaminghttp import register_openers
import urllib2
import urllib
import json


class Uploader(object):
    def upload(file):
        pass


class FilePicker(Uploader):
    APIKEY = 'FILL_IN_YOUR_OWN_KEY'
    APIURL = 'https://www.filepicker.io/api/upload/'

    def __init__(self):
        register_openers()

    def upload(self, file):
        '''Return FilePicker.IO url where file is hosted or failure.'''

        js_session = urllib.urlencode({
            'js_session': json.dumps({
                'apikey': FilePicker.APIKEY,
                'mimetypes': ['*/*'],
                'persist': 'false',
                'auth_tokens': {}
            })
        })

        url = FilePicker.APIURL + '?' + js_session
        datagen, headers = multipart_encode({'fileUpload': file})
        request = urllib2.Request(url, datagen, headers)
        response = urllib2.urlopen(request).read()

        try:
            return json.loads(response)['data'][0]['url']
        except:
            return None

# class AmazonS3(Uploader):
#     pass

# class RackspaceFiles(Uploader):
#     pass
