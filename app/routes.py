from flask import request, jsonify
from .compare_service import compute_similarity_from_files

def register_routes(app):
    @app.route("/compare", methods=["POST"])
    def compare_audio():
        try:
            user_audio = request.files["user_audio"]
            ref_audio = request.files["ref_audio"]

            score = compute_similarity_from_files(user_audio, ref_audio)
            return jsonify({"similarity": round(score, 4)})
        except Exception as e:
            return jsonify({"error": str(e)}), 500
