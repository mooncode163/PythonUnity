#!/usr/bin/python
#
# Copyright 2014 Google Inc. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the 'License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Uploads apk to alpha track and updates its listing properties."""

import argparse
import sys
from apiclient import sample_tools
from oauth2client import client

TRACK = 'alpha'  # Can be 'alpha', beta', 'production' or 'rollout'

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('package_name',
                       help='The package name. Example: com.android.sample')
argparser.add_argument('image_file',
                       nargs='?',
                       default='test.apk',
                       help='The path to the APK file to upload.')
argparser.add_argument('lan', help='lan en-US')
argparser.add_argument('imageType', help='imageType phoneScreenshots')
# package imageFile lan imageType
def main(argv):
  count = len(argv)
  package = ""
  imageFile = "1.jpg" 
  lan = "en-US"
  imageType = "phoneScreenshots"
  

  for i in range(1,count):
      print("参数", i, argv[i])
      if i==1:
          package = argv[i] 
      if i==2:
          imageFile = argv[i]
      if i==3:
          lan = argv[i]
      if i==4:
          imageType = argv[i] 

  # Authenticate and construct service.
  service, flags = sample_tools.init(
      argv,
      'androidpublisher',
      'v3',
      __doc__,
      __file__, parents=[argparser],
      scope='https://www.googleapis.com/auth/androidpublisher')

  # Process flags and read their values.
  package_name = flags.package_name
  image_file = flags.image_file

  try:
    edit_request = service.edits().insert(body={}, packageName=package_name)
    result = edit_request.execute()
    edit_id = result['id']

# https://developers.google.cn/android-publisher/api-ref/rest/v3/AppImageType?hl=zh-cn
# upload(packageName, editId, language, imagpheType, media_body=None, media_mime_type=None)
    image_response = service.edits().images().upload(
        editId=edit_id,
        packageName=package_name,
        language=lan,
        imageType=imageType,
        media_body=image_file).execute()

    # print ('Version code %d has been uploaded' % image_response['versionCode'])

    # track_response = service.edits().tracks().update(
    #     editId=edit_id,
    #     track=TRACK,
    #     packageName=package_name,
    #     body={u'releases': [{
    #         u'name': u'My first API release with release notes',
    #         u'versionCodes': [str([apk_response['versionCode']])],
    #         u'releaseNotes': [
    #             {u'recentChanges': u'Apk recent changes in en-US'},
    #         ],
    #         u'status': u'completed',
    #     }]}).execute()

    # print 'Track %s is set with releases: %s' % (
    #     track_response['track'], str(track_response['releases']))

    commit_request = service.edits().commit(
        editId=edit_id, packageName=package_name).execute()

    # print 'Edit "%s" has been committed' % (commit_request['id'])

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)
