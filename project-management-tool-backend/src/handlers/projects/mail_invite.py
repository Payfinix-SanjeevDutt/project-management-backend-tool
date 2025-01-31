from flask import jsonify
import jwt
from datetime import datetime, timedelta

JWT_SECRET = 'your_jwt_secret_key'
JWT_ALGORITHM = 'HS256'

class SendInvite:
    def __init__(self, request):
        self.request = request

    def generate_token(self, email, project_id):
        """Generate a JWT token for a given email and project."""
        payload = {
            "email": email,
            "project_id": project_id,
            "exp": datetime.utcnow() + timedelta(hours=24), 
        }
        return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

    def send_invite(self):
        data = self.request.json
        print(data)
        try:
            project_name = data.get("project_name", "")
            cover_image = data.get("cover_image", "")
            project_id = data.get("project_id")
            emails = data.get("emails", [])

            if not emails:
                return jsonify({"status": False, "message": "No emails provided"}), 400

            links = {}
            for email in emails:
                token = self.generate_token(email, project_id)
                link = f"http://localhost:3032/dashboard/project-access/{token}"
                links[email] = link

            print("Generated Invitation Links:")
            for email, link in links.items():
                print(f"{email}: {link}")

            return jsonify({
                "status": True,
                "message": "Links generated successfully (not sent via email)",
                "links": links, 
            }), 200

        except Exception as e:
            return jsonify({"status": False, "message": str(e)}), 500
