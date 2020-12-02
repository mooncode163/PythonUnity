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

"""Changes the description, promo text and title of an app in en-US and en-GB.
"""

import argparse
import sys

sys.path.append('../../') 
sys.path.append('./') 

from apiclient import sample_tools
from oauth2client import client 
from ProjectConfig.Script.AppInfo.AppInfo import mainAppInfo
# from ProjectConfig.Script.Project.Resource import mainResource
from Common import Source 

TRACK = 'alpha'  # Can be 'alpha', beta', 'production' or 'rollout'

# Declare command-line flags.
argparser = argparse.ArgumentParser(add_help=False)
argparser.add_argument('package_name',
                       help='The package name. Example: com.android.sample')
argparser.add_argument('country',  help='title')
argparser.add_argument('isHD',  help='title')
argparser.add_argument('lan',  help='title')
argparser.add_argument('cmdPath',  help='title')

# argparser.add_argument('title',  help='title')
# argparser.add_argument('detail',  help='title')
# argparser.add_argument('shortdetail',  help='title') 

# package lan title detail shortdetail
def main(argv):
  print( " argv=",argv)
  count = len(argv)
  package = ""  
  country = ""
  strHD = ""
  lan = "" 
  cmdPath = ""

  for i in range(1,count):
      print("参数", i, argv[i])
      if i==1:
          package = argv[i] 
      if i==2:
          country = argv[i]
      if i==3:
          strHD = argv[i]
      if i==4:
          lan = argv[i]
      if i==5:
          cmdPath = argv[i]



  isHD = False
  if strHD=="True":
      isHD = True

  print("update_listings cmdPath =",cmdPath)
#   mainResource.SetCmdPath(cmdPath)
  mainAppInfo.SetCmdPath(cmdPath)
#   print("update_listings getGameName =",mainResource.getGameName())
  title = mainAppInfo.GetAppName(Source.ANDROID, isHD,lan) 
  detail =mainAppInfo.GetAppDetail(isHD,lan)  
  shortdetail =mainAppInfo.GetAppPromotion(isHD,lan)

  
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

  try:
    edit_request = service.edits().insert(body={}, packageName=package_name)
    result = edit_request.execute()
    edit_id = result['id']

    listing_response_us = service.edits().listings().update(
        editId=edit_id, packageName=package_name, language=country,
        body={'fullDescription': detail,
              'shortDescription': shortdetail,
              'title': title}).execute()

    print ('Listing for language %s was updated.' % listing_response_us['language'])

    # listing_response_gb = service.edits().listings().update(
    #     editId=edit_id, packageName=package_name, language='en-GB',
    #     body={'fullDescription': 'Pudding boot lorry',
    #           'shortDescription': 'Pancetta ipsum',
    #           'title': 'App Title UK'}).execute()

    # print ('Listing for language %s was updated.'  % listing_response_gb['language'])

    commit_request = service.edits().commit(
        editId=edit_id, packageName=package_name).execute()

    print ('Edit "%s" has been committed' % (commit_request['id']))

  except client.AccessTokenRefreshError:
    print ('The credentials have been revoked or expired, please re-run the '
           'application to re-authorize')

if __name__ == '__main__':
  main(sys.argv)
