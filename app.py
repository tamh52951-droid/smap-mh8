from flask import Flask, jsonify, request

app = Flask(__name__)

# قاعدة بيانات مؤقتة لتخزين الأكواد (يمكنك تعديلها أو ربطها بقاعدة بيانات حقيقية لاحقاً)
activation_codes = {
    "SNAP-1234-5678": {"status": "active", "type": "month"},
    "SNAP-9999-8888": {"status": "active", "type": "year"},
}


@app.route("/")
def home():
    return "مرحباً بك في لوحة تحكم سيرفر سناب! السيرفر يعمل بنجاح 🚀"


# مسار للتحقق من الكود (يستخدمه التطبيق)
@app.route("/check_code", methods=["POST"])
def check_code():
    data = request.get_json()
    code = data.get("code")

    if code in activation_codes and activation_codes[code]["status"] == "active":
        return (
            jsonify(
                {
                    "status": "success",
                    "message": "الكود صحيح ومفعل بنجاح",
                    "type": activation_codes[code]["type"],
                }
            ),
            200,
        )
    else:
        return (
            jsonify({"status": "error", "message": "الكود غير صالح أو منتهي"}),
            400,
        )


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
