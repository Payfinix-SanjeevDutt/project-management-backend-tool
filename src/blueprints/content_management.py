from flask import Blueprint, request, jsonify

from src.services.sharepoint.file_manager.actions import SharepointFileManager

content_blueprint = Blueprint("content", __name__)

@content_blueprint.route('/get_folder_data', methods=['POST'])
def get_folder_data():
    data = request.get_json()
    if not data or 'folder_path' not in data:
        return jsonify({"error": "Missing folder_path in request body"}), 400

    folder_path = data['folder_path']
    
    folder_data_response = SharepointFileManager(request)
    folder_files_response = folder_data_response.get_folder_data(folder_path)
    
    return jsonify(folder_files_response)
