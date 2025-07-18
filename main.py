
from flask import Flask, render_template, request, redirect, flash
import datetime

app = Flask(__name__)
app.secret_key = 'your_secret_key'

# تحميل الأكواد الصالحة من ملف
with open("valid_codes.txt", "r") as f:
    valid_codes = set(code.strip() for code in f.readlines())

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        phone = request.form["phone"]
        plate_letters = request.form["plate_letters"]
        plate_numbers = request.form["plate_numbers"]
        full_plate = f"{plate_letters}-{plate_numbers}"
        activation_code = request.form["activation_code"]

        if len(phone) != 10 or not phone.isdigit():
            flash("رقم الجوال يجب أن يتكون من 10 أرقام", "error")
            return render_template("index.html")

        # تحقق من الكود
        if activation_code not in valid_codes:
            flash("❌ الكود المدخل خطأ أو مستخدم من قبل", "error")
        else:
            valid_codes.remove(activation_code)
            with open("valid_codes.txt", "w") as f:
                f.write("\n".join(valid_codes))

            with open("records.txt", "a") as f:
                f.write(f"{datetime.datetime.now()} | {name} | {phone} | {full_plate} | {activation_code}\n")

            flash("✅ تم تفعيل الضمان\nشكرًا لثقتك في ترو شـيلد", "success")
        return render_template("index.html")
    return render_template("index.html")
