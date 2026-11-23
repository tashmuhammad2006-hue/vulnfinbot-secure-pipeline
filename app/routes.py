import re
from flask import Blueprint, jsonify, request

bp = Blueprint("api", __name__)

MAX_MESSAGE_LENGTH = 500

INJECTION_PATTERNS = [
    r"ignore\s+(all\s+)?previous\s+instructions",
    r"system\s+prompt",
    r"reveal\s+(your\s+)?(instructions|secrets|api\s*key|password)",
    r"execute\s+command",
    r"drop\s+table",
    r"<script>",
]


def is_malicious_input(text: str) -> bool:
    return any(re.search(pattern, text, re.IGNORECASE) for pattern in INJECTION_PATTERNS)


def sanitize_output(text: str) -> str:
    return re.sub(r"<[^>]*?>", "", text)


def generate_ai_response(user_message: str) -> str:
    msg_lower = user_message.lower()
    if "budget" in msg_lower:
        raw_response = "You can start by tracking your income and expenses."
    elif "invest" in msg_lower:
        raw_response = "Consider diversification and long-term index funds."
    else:
        raw_response = f"Financial assistant response for: '{user_message[:50]}'."

    return sanitize_output(raw_response)


@bp.route("/health", methods=["GET"])
def health_check():
    return jsonify({"status": "healthy"}), 200


@bp.route("/api/chat", methods=["POST"])
def chat():
    if not request.is_json:
        return jsonify({"error": "Content-Type must be application/json"}), 415

    data = request.get_json(silent=True)
    if data is None or not isinstance(data, dict):
        return jsonify({"error": "Invalid JSON payload"}), 400

    if "message" not in data:
        return jsonify({"error": "Missing 'message' field"}), 400

    message = data["message"]
    if not isinstance(message, str):
        return jsonify({"error": "'message' must be a string"}), 400

    cleaned_message = message.strip()
    if not cleaned_message:
        return jsonify({"error": "Message cannot be empty"}), 400

    if len(cleaned_message) > MAX_MESSAGE_LENGTH:
        return jsonify({"error": f"Message exceeds maximum length of {MAX_MESSAGE_LENGTH} characters"}), 400

    response_text = generate_ai_response(cleaned_message)
    return jsonify({"response": response_text}), 200


@bp.app_errorhandler(404)
def not_found(error):
    return jsonify({"error": "Resource not found"}), 404


@bp.app_errorhandler(500)
def internal_error(error):
    return jsonify({"error": "Internal server error"}), 500