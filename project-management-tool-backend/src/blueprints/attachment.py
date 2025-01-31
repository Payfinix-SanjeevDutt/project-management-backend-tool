from flask import Blueprint, request

from src.handlers import UploadFileHandler
from src.handlers import GetAllAttachments
from src.handlers import AttachmentDeleteHandler
from src.handlers import AttachmentDownloadHandler

attachment_blueprint = Blueprint("attachment", __name__)

@attachment_blueprint.route("/upload_small_file", methods=['POST'])
def upload_small_file():
    return UploadFileHandler(request=request).sendAttachment()

@attachment_blueprint.route("/get_attached_files", methods=['POST'])
def get_attached_files():
    return GetAllAttachments(request=request).get_attached_files()

@attachment_blueprint.route("/delete_attached_files", methods=['DELETE'])
def delete_attached_files():
    return AttachmentDeleteHandler(request=request).deleteattachment()

@attachment_blueprint.route("/download_attached_files", methods=['POST'])
def download_attached_files():
    return AttachmentDownloadHandler(request=request).downloadattachment()
