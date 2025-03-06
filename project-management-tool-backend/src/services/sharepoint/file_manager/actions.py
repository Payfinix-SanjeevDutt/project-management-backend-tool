import requests
from src.config import SharePointApi
from src.utils import SharePointAccess
from flask import request, Response, jsonify

import json


class SharepointFileManager:

    def __init__(self, requestData):

        if requestData is None:
            raise Exception("File data is None")

        self.access_token = SharePointAccess()
        self.requestData = requestData

    def __generateHeaders(self):
        headers = {
            "Authorization": f"Bearer {self.access_token.generate_token()}",
            "Content-Type": "application/json",
        }
        return headers

    def createFolder(self):
        folder_name = self.requestData.get('folder_name', None)
        path = self.requestData.get('path', '')

        url = f"{SharePointApi.BASE_URL}{path}:/children"

        # url = f"{SharePointApi.BASE_URL}/{path}/{folder_name}:/children"

        payload = {
            "name": folder_name,
            "folder": {},
            "@microsoft.graph.conflictBehavior": "fail"  # "rename" or "replace" or "fail"
        }

        response = requests.post(
            url, headers=self.__generateHeaders(), json=payload)

        if not response.ok:
            raise Exception(f"unable to create folder {response.status_code}")
        if response.ok:
            return response.json()  # Assuming this contains folder details
        else:
            raise Exception(f"Unable to create folder: {response.status_code}, {response.text}")

    def uploadSmallFile(self, folder_path, file):
        if not file or not folder_path:
            return {"status": False, "message": "Missing file or folder path"}

        file_name = file.filename

        url = f"{SharePointApi.BASE_URL}{folder_path}/{file_name}:/content" # lessthan 4 MB

        print(url)

        response = requests.put(
            url, headers=self.__generateHeaders(), data=file.read())

        if not response.ok:
            raise Exception(f"unable to upload file {response.status_code}")

    def uploadLargeFile(self, folder_path, file):
        
        if not file or not folder_path:
            return {"status": False, "message": "Missing file or folder path"}

        file_name = file.filename

        url = f"{SharePointApi.BASE_URL}{folder_path}/{file_name}:/createUploadSession" # greater than 4 MB

        print(url)

        response = requests.put(url, headers=self.__generateHeaders(), data=file.read())

        if not response.ok :
            raise Exception(f"unable to upload file {response.status_code}")
        
    def get_folder_data(self, folder_path):
        
        # folder_path = self.requestData.get('folder_path', SharePointApi.BASE_URL)

        url = f"{SharePointApi.BASE_URL}{folder_path}:/children"

        response = requests.get(url, headers=self.__generateHeaders())

        if response.status_code == 200:
            files = response.json().get('value', [])
            print(files)
            transformed_data = []

            folder_level = len(folder_path.split('/')) if folder_path else 0

            for idx, file in enumerate(files, start=1):
                file_extension = file['name'].split(
                    '.')[-1] if '.' in file['name'] else 'unknown'
                is_folder = 'folder' in file

                total_folders = 0
                total_files = 0

                if is_folder:
                    # folder_id = file.get('id', '')
                    folder_url = f"{SharePointApi.BASE_URL}{file.get('name', 'Unnamed Folder')}:/children" if not folder_path else f"{SharePointApi.BASE_URL}{folder_path}/{file.get('name', 'Unnamed Folder')}:/children"
                    print("folder_url", folder_url)
                    folder_response = requests.get(folder_url, headers=self.__generateHeaders())
                    print("folder_response", folder_response)
                    if folder_response.status_code == 200:
                        children = folder_response.json().get('value', [])

                        for child in children:
                            if 'folder' in child:
                                total_folders += 1
                            else:
                                total_files += 1

                transformed_data.append({
                    "id": idx,
                    "name": file.get('name', 'Unnamed Folder'),
                    "isFavorited": False,
                    "modifiedAt": file.get('lastModifiedDateTime', ''),
                    "createdAt": file.get('createdDateTime', ''),
                    "length": 0,
                    'shared': [],
                    'tags': [],
                    "folder_path": folder_path,
                    "size": file.get('size', 0),
                    "totalFiles": total_files if is_folder else 0,
                    "totalFolders": total_folders if is_folder else 0,
                    "type": "folder" if is_folder else file_extension,
                    "url": file.get('webUrl', 'https://api-dev-minimal-v6.vercel.app/assets/images/cover/cover-2.webp')
                })

            return {"status": True, "files": transformed_data, "level": folder_level, "folder_path": folder_path}
        


    def delete_folder(self, folder_path):
        # access_token = requests.get(url, headers=self.__generateHeaders())

        if not folder_path:
            return {"status": False, "message": "Missing access token or folder path"}


        url = f"{SharePointApi.BASE_URL}{folder_path}"

        response = requests.delete(url, headers=self.__generateHeaders())
        print(response)
        if not response.ok :
            raise Exception(f"unable to upload file {response.status_code}")
    

    def delete_file(self, file_path):
        # access_token = requests.get(url, headers=self.__generateHeaders())

        if not file_path:
            return {"status": False, "message": "Missing file path"}

        url = f"{SharePointApi.BASE_URL}{file_path}"

        response = requests.delete(url, headers=self.__generateHeaders())

        print(response)
        if not response.ok :
            raise Exception(f"unable to delete file {response.status_code}")
    

    def download_file(self, file_path):
        if not file_path:
            return jsonify({'status': False, "message": "Missing file path"}), 400

        url = f"{SharePointApi.BASE_URL}{file_path}"
        try:
            response = requests.get(url, headers=self.__generateHeaders())
            response.raise_for_status()  # Raise exception for HTTP errors

            data = response.json()
            download_url = data.get('@microsoft.graph.downloadUrl')
            if not download_url:
                return jsonify({'status': False, 'message': 'Download URL not found in response'}), 500
            return download_url
        except requests.exceptions.RequestException as e:
            return jsonify({'status': False, 'error': 'Unable to download the file', 'message': str(e)}), 500