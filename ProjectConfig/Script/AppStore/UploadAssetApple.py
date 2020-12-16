"""
A Python script that uploads an app preview to App Store Connect.
See README.md for help configuring and running this script.
"""

import datetime
import hashlib
import http.client
import json
import os
import sys
from urllib.parse import urlparse
import platform 

if 'Darwin' not in platform.system():
    import jwt

########
# KEY CONFIGURATION - Put your API Key info here.
 

class UploadAssetApple:
    KEY_ID = ""
    ISSUER_ID = ""
    PRIVATE_KEY = ""
    tokenKey = ""
    

########
# UPLOAD - This is where the interaction with App Store Connect API happens.
    def UploadPreview(self,appid, platform, version, locale, preview_type, file_path):
        """
        This function does all the real work. It:
        1. Creates an Authorization header value with bearer token (JWT).
        2. Looks up the app by bundle id.
        3. Looks up the version by platform and version number.
        4. Gets all localizations for the version and looks for the requested locale.
        5. Creates the localization if the requested localization doesn't exist.
        6. Gets all available app preview sets from the localization.
        7. Creates the app preview set for the requested type if it doesn't exist.
        8. Reserves an app preview in the selected app preview set.
        9. Uploads each part according to the returned upload operations.
        10. Commits the reservation and provides a checksum.

        If anything goes wrong during this process the error is reported and the
        script exits with a non-zero status.
        """

        selected_localization = self.GetAppLocalization(appid,platform,version,locale)
        auth_header = f"Bearer {self.create_token()}"

        # 6. Get all available app preview sets from the localization.
        #    If a preview set for the desired preview type already exists, use it.
        #    Otherwise, make a new one.
        preview_sets_response = self.make_http_request(
            "GET",
            selected_localization['relationships']['appPreviewSets']['links']['related'],
            headers={
                "Authorization": auth_header
            }
        )
        preview_sets = json.loads(preview_sets_response)['data']
        selected_preview_sets = [set for set in preview_sets
                                if set['attributes']['previewType'] == preview_type]


        # 7. If an app preview set for the requested type doesn't exist, create it.
        if selected_preview_sets:
            selected_preview_set = selected_preview_sets[0]
        else:
            preview_set_response = self.make_http_request(
                "POST",
                "https://api.appstoreconnect.apple.com/v1/appPreviewSets",
                headers={
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                },
                body=json.dumps({
                    "data": {
                        "type": "appPreviewSets",
                        "attributes": {
                            "previewType": preview_type
                        },
                        "relationships": {
                            "appStoreVersionLocalization": {
                                "data": {
                                    "type": "appStoreVersionLocalizations",
                                    "id": selected_localization['id']
                                }
                            }
                        }
                    }
                })
            )
            selected_preview_set = json.loads(preview_set_response)['data']


        # 8. Reserve an app preview in the selected app preview set.
        #    Tell the API to create a preview before uploading the
        #    preview data.
        print("Reserve new app preview.")
        reserve_preview_response = self.make_http_request(
            "POST",
            "https://api.appstoreconnect.apple.com/v1/appPreviews",
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json"
            },
            body=json.dumps({
                "data": {
                    "type": "appPreviews",
                    "attributes": {
                        "fileName": os.path.basename(file_path),
                        "fileSize": os.path.getsize(file_path)
                    },
                    "relationships": {
                        "appPreviewSet": {
                            "data": {
                                "type": "appPreviewSets",
                                "id": selected_preview_set['id']
                            }
                        }
                    }
                }
            })
        )
        preview = json.loads(reserve_preview_response)['data']


        # 9. Upload each part according to the returned upload operations.
        #     The reservation returned uploadOperations, which instructs us how
        #     to split the asset into parts. Upload each part individually.
        #     Note: To speed up the process, upload multiple parts asynchronously
        #     if you have the bandwidth.
        upload_operations = preview['attributes']['uploadOperations']

        for part_number, upload_operation in enumerate(upload_operations):
            print(f"Upload part {part_number+1} of {len(upload_operations)} at offset "
                f"{upload_operation['offset']} with length {upload_operation['length']}.")

            # Read the requested byte range.
            with open(file_path, mode='rb') as file:
                file.seek(upload_operation['offset'])
                data = file.read(upload_operation['length'])

            # Upload the data using the request info specified in the upload operation.
            self.make_http_request(
                upload_operation['method'],
                upload_operation['url'],
                headers={h['name']: h['value'] for h in upload_operation['requestHeaders']},
                body=data
            )


        # 10. Commit the reservation and provide a checksum.
        #     Committing tells App Store Connect the script is finished uploading parts.
        #     App Store Connect uses the checksum to ensure the parts were uploaded
        #     successfully.
        print("Commit the reservation.")
        preview_url = preview['links']['self']
        self.make_http_request(
            "PATCH",
            f"https://api.appstoreconnect.apple.com/v1/appPreviews/{preview['id']}",
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json"
            },
            body=json.dumps({
                "data": {
                    "type": "appPreviews",
                    "id": preview['id'],
                    "attributes": {
                        "uploaded": True,
                        "sourceFileChecksum": hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                    }
                }
            })
        )


        # Report success to the caller.
        print()
        print("App Preview successfully uploaded to:")
        print(self.blue(preview_url))
        print("You can verify success in App Store Connect or using the API.")
        print()


    # 删除所有截图
    # https://developer.apple.com/documentation/appstoreconnectapi/delete_an_app_screenshot_set
    # reserve_preview_response = self.make_http_request(
    #     "DELETE", 
    #     f"https://api.appstoreconnect.apple.com/v1/appScreenshotSets/{selected_preview_set['id']}",
    #     headers={
    #         "Authorization": auth_header, 
    #     }
    # )

    def DeleteAllScreenShot(self,appid, platform, version, locale, display_type):
        # return

        selected_localization = self.GetAppLocalization(appid,platform,version,locale)
        auth_header = f"Bearer {self.create_token()}"
        
        # 6. Get all available app preview sets from the localization.

        #    If a preview set for the desired preview type already exists, use it.
        #    Otherwise, make a new one.
        preview_sets_response = self.make_http_request(
            "GET",
            selected_localization['relationships']['appScreenshotSets']['links']['related'],
            headers={
                "Authorization": auth_header
            }
        )
        preview_sets = json.loads(preview_sets_response)['data']
        # print("preview_sets=",preview_sets)
        selected_preview_sets = [set for set in preview_sets
                                if set['attributes']['screenshotDisplayType'] == display_type]

        
        # 7. If an app preview set for the requested type doesn't exist, create it.
        if selected_preview_sets:
            selected_preview_set = selected_preview_sets[0] 
            print("selected_preview_set=",selected_preview_set)
            preview_set_response = self.make_http_request(
                "DELETE ", 
                f"https://api.appstoreconnect.apple.com/v1/appScreenshotSets/{selected_preview_set['id']}",
                headers={
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                }
            ) 
            print("preview_set_response=",preview_set_response)




    def UploadScreenShot(self,appid, platform, version, locale, display_type, file_path):
        """
        This function does all the real work. It:
        1. Creates an Authorization header value with bearer token (JWT).
        2. Looks up the app by bundle id.
        3. Looks up the version by platform and version number.
        4. Gets all localizations for the version and looks for the requested locale.
        5. Creates the localization if the requested localization doesn't exist.
        6. Gets all available app preview sets from the localization.
        7. Creates the app preview set for the requested type if it doesn't exist.
        8. Reserves an app preview in the selected app preview set.
        9. Uploads each part according to the returned upload operations.
        10. Commits the reservation and provides a checksum.

        If anything goes wrong during this process the error is reported and the
        script exits with a non-zero status.
        """
        # return

        selected_localization = self.GetAppLocalization(appid,platform,version,locale)
        auth_header = f"Bearer {self.create_token()}"
        
        # 6. Get all available app preview sets from the localization.

        #    If a preview set for the desired preview type already exists, use it.
        #    Otherwise, make a new one.
        preview_sets_response = self.make_http_request(
            "GET",
            selected_localization['relationships']['appScreenshotSets']['links']['related'],
            headers={
                "Authorization": auth_header
            }
        )
        preview_sets = json.loads(preview_sets_response)['data']
        # print("preview_sets=",preview_sets)
        selected_preview_sets = [set for set in preview_sets
                                if set['attributes']['screenshotDisplayType'] == display_type]


        # 7. If an app preview set for the requested type doesn't exist, create it.
        if selected_preview_sets:
            selected_preview_set = selected_preview_sets[0]
        else:
            preview_set_response = self.make_http_request(
                "POST",
                "https://api.appstoreconnect.apple.com/v1/appScreenshotSets",
                headers={
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                },
                body=json.dumps({
                    "data": {
                        "type": "appScreenshotSets",
                        "attributes": {
                            "screenshotDisplayType": display_type
                        },
                        "relationships": {
                            "appStoreVersionLocalization": {
                                "data": {
                                    "type": "appStoreVersionLocalizations",
                                    "id": selected_localization['id']
                                }
                            }
                        }
                    }
                })
            )
            selected_preview_set = json.loads(preview_set_response)['data']
 

        # 8. Reserve an app preview in the selected app preview set.
        #    Tell the API to create a preview before uploading the
        #    preview data.
        print("Reserve new app preview.")
        reserve_preview_response = self.make_http_request(
            "POST",
            "https://api.appstoreconnect.apple.com/v1/appScreenshots",
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json"
            },
            body=json.dumps({
                "data": {
                    "type": "appScreenshots",
                    "attributes": {
                        "fileName": os.path.basename(file_path),
                        "fileSize": os.path.getsize(file_path)
                    },
                    "relationships": {
                        "appScreenshotSet": {
                            "data": {
                                "type": "appScreenshotSets",
                                "id": selected_preview_set['id']
                            }
                        }
                    }
                }
            })
        )
        preview = json.loads(reserve_preview_response)['data']


        # 9. Upload each part according to the returned upload operations.
        #     The reservation returned uploadOperations, which instructs us how
        #     to split the asset into parts. Upload each part individually.
        #     Note: To speed up the process, upload multiple parts asynchronously
        #     if you have the bandwidth.
        upload_operations = preview['attributes']['uploadOperations']

        for part_number, upload_operation in enumerate(upload_operations):
            print(f"Upload part {part_number+1} of {len(upload_operations)} at offset "
                f"{upload_operation['offset']} with length {upload_operation['length']}.")

            # Read the requested byte range.
            with open(file_path, mode='rb') as file:
                file.seek(upload_operation['offset'])
                data = file.read(upload_operation['length'])

            # Upload the data using the request info specified in the upload operation.
            ret = self.make_http_request(
                upload_operation['method'],
                upload_operation['url'],
                headers={h['name']: h['value'] for h in upload_operation['requestHeaders']},
                body=data
            )
            print("upload ret =",ret)

        # 10. Commit the reservation and provide a checksum.
        #     Committing tells App Store Connect the script is finished uploading parts.
        #     App Store Connect uses the checksum to ensure the parts were uploaded
        #     successfully.
        print("Commit the reservation.")
        preview_url = preview['links']['self']
        self.make_http_request(
            "PATCH",
            f"https://api.appstoreconnect.apple.com/v1/appScreenshots/{preview['id']}",
            headers={
                "Authorization": auth_header,
                "Content-Type": "application/json"
            },
            body=json.dumps({
                "data": {
                    "type": "appScreenshots",
                    "id": preview['id'],
                    "attributes": {
                        "uploaded": True,
                        "sourceFileChecksum": hashlib.md5(open(file_path, 'rb').read()).hexdigest()
                    }
                }
            })
        )


        # Report success to the caller.
        print()
        print("App Preview successfully uploaded to:")
        print(self.blue(preview_url))
        print("You can verify success in App Store Connect or using the API.")
        print()

 
    def GetAppLocalizationId(self,appid, platform, version, locale): 
        return self.GetAppLocalization(appid,platform,version,locale)['id']

    def GetAppLocalization(self,appid, platform, version, locale):
       
        # 1. Create an Authorization header value with bearer token (JWT).
        #    The token is set to expire in 20 minutes, and is used for all App Store
        #    Connect API calls.
        auth_header = f"Bearer {self.create_token()}"


        print("Find (or create) app preview set.")
     
        
        # 3. Look up the version version by platform and version number.
        #    If the version is not found, report an error and exit.
        version_response = self.make_http_request(
            "GET",
            # f"https://api.appstoreconnect.apple.com/v1/apps/{app['id']}/appStoreVersions?"
            f"https://api.appstoreconnect.apple.com/v1/apps/{appid}/appStoreVersions?"
            f"filter[versionString]={version}&filter[platform]={platform}",
            headers={
                "Authorization": auth_header
            }
        )
        versions = json.loads(version_response)['data']
        if versions:
            version = versions[0]
        else:
            self.die(2, f"No app store version found with version {version}.")

        # 4. Get all localizations for the version and look for the requested locale.
        localizations_response = self.make_http_request(
            "GET",
            f"https://api.appstoreconnect.apple.com/v1/appStoreVersions/{version['id']}/"
            "appStoreVersionLocalizations",
            headers={
                "Authorization": auth_header
            }
        )
        localizations = json.loads(localizations_response)['data']
        selected_localizations = [loc for loc in localizations if loc['attributes']['locale'] == locale]


        # 5. If the requested localization does not exist, create it.
        #    Localized attributes are copied from the primary locale so there's
        #    no need to worry about them here.
        if selected_localizations:
            selected_localization = selected_localizations[0]
        else:
            selected_localization_response = self.make_http_request(
                "POST",
                "https://api.appstoreconnect.apple.com/v1/appStoreVersionLocalizations",
                headers={
                    "Authorization": auth_header,
                    "Content-Type": "application/json"
                },
                body=json.dumps({
                    "data": {
                        "type": "appStoreVersionLocalizations",
                        "attributes": {
                            "locale": locale
                        },
                        "relationships": {
                            "appStoreVersion": {
                                "data": {
                                    "type": "appStoreVersions",
                                    "id": version['id']
                                }
                            }
                        }
                    }
                })
            )
            selected_localization = json.loads(selected_localization_response)['data']
        
        return selected_localization

    
 

    ########
    # API SUPPORT - Code to support HTTP API calls and logging.

    def make_http_request(self,method, url, **kwargs):
        print(self.green(method), self.blue(url))

        parsed_url = urlparse(url)
        path_plus_query = parsed_url.path + (f"?{parsed_url.query}" if parsed_url.query else '')

        try:
            connection = http.client.HTTPSConnection(parsed_url.netloc)
            connection.request(method, path_plus_query, **kwargs)
            response = connection.getresponse()
            body = response.read().decode('UTF-8')
        finally:
            if connection:
                connection.close()

        if response.status >= 200 and response.status < 300:
            return body

        message = "An error occurred calling the App Store Connect API."
        message += "\nStatus:" + str(response.status)
        if "x-request-id" in response.headers.keys():
            message += "\nRequest ID:" + response.headers['x-request-id']
        message += "\nResponse:\n" + body
        self.die(3, message)
        return None


    def create_token(self):

        if len(self.tokenKey)!=0:
            return self.tokenKey
            
        """
        Creates a token that lives for 20 minutes, which should be long enough
        to upload the app preview. In a long-running script, adjust the code to
        issue a new token periodically.
        """
        # print("create_token self.KEY_ID="+self.KEY_ID)
        # print("create_token self.ISSUER_ID="+self.ISSUER_ID)
        # print("create_token self.PRIVATE_KEY="+self.PRIVATE_KEY)
        if self.KEY_ID == "XXXXXXXXXX":
            die(-2, "Missing the API key. Configure your key information at the top of the "
                    "upload-preview.py file first.")

        expiry = datetime.datetime.utcnow() + datetime.timedelta(minutes=20)
        token_data = jwt.encode(
            {
                'iss': self.ISSUER_ID,
                'aud': 'appstoreconnect-v1',
                'exp': expiry
            },
            self.PRIVATE_KEY,
            headers={
                'kid': self.KEY_ID
            },
            algorithm='ES256'
        )
        return token_data.decode('UTF-8')


    def die(self,status, message):
        print(self.red(message), file=sys.stderr)
        sys.exit(status)

    ########
    # TEXT COLORS - Functions to color text for pretty output.
    def red(self,text):
        return f"\033[91m{text}\033[0m"

    def green(self,text):
        return f"\033[92m{text}\033[0m"

    def blue(self,text):
        return f"\033[94m{text}\033[0m"

mainUploadAssetApple =  UploadAssetApple()

########
# ENTRY POINT - When run directly, check arguments and call upload().
# if __name__ == "__main__":
    # if len(sys.argv) != 7:
    #     die(-1, "usage: python3 upload-preview.py {bundle id} {platform} {version} {locale} "
    #             "{preview type} {file path}")
    # upload(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5], sys.argv[6])
    # HW5BW4DSC7  886x1920
    # UploadPreview("1532591216", "IOS", "1.0.0", "zh-Hans", "IPHONE_65", "E:\\moon\\Videos\\1.mp4")
    # UploadScreenShot("1532591216", "IOS", "1.0.0", "zh-Hans", "APP_IPHONE_65", "my_screenshot.png")
     