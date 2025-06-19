# routes.py
from flask import request, jsonify
from .compare_service import compute_similarity  # hàm đa năng: path | URL | file-like

def register_routes(app):
    @app.route("/compare", methods=["POST"])
    def compare_audio():
        """
        Multipart/form-data:
          • user_audio   = <file .wav>              (bắt buộc)
          • ref_audio    = <file .wav>              (tùy chọn)
          • sample_url   = "https://..."            (tùy chọn)
        Trả JSON: {"similarity": 0.8734}
        """
        # 1️⃣ Lấy đầu vào
        user_audio = request.files.get("user_audio")
        ref_audio  = request.files.get("ref_audio")
        sample_url = request.form.get("sample_url")  # text/plain field

        if not user_audio:
            return jsonify(error="user_audio file is required"), 400
        if not (ref_audio or sample_url):
            return jsonify(error="Provide ref_audio file OR sample_url"), 400

        try:
            # 2️⃣ Chọn nguồn mẫu
            reference_source = ref_audio if ref_audio else sample_url

            # 3️⃣ Tính similarity (hàm tự viết, chấp nhận file-like hoặc URL)
            score = compute_similarity(user_audio, reference_source)

            return jsonify(similarity=round(score, 4))
        except Exception as e:
            # Log chi tiết hơn tuỳ nhu cầu
            return jsonify(error=str(e)), 500
