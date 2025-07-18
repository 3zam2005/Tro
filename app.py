
from flask import Flask, render_template, request, redirect, flash
import os

app = Flask(__name__, template_folder="templates", static_folder="static")
app.secret_key = "secret_key"

VALID_CODES_FILE = "valid_codes.txt"
RECORDS_FILE = "records.txt"

def is_valid_code(code):
    with open(VALID_CODES_FILE, "r") as file:
        codes = [line.strip() for line in file]
    return code in codes

def is_code_used(code):
    if not os.path.exists(RECORDS_FILE):
        return False
    with open(RECORDS_FILE, "r") as file:
        return code in file.read()

def save_record(data):
    with open(RECORDS_FILE, "a") as file:
        file.write(f"{data}\n")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name")
        phone = request.form.get("phone")
        plate1 = request.form.get("plate1")
        plate2 = request.form.get("plate2")
        plate3 = request.form.get("plate3")
        plate_numbers = request.form.get("plate_numbers")
        code = request.form.get("code")

        full_plate = f"{plate1}-{plate2}-{plate3} {plate_numbers}"

        if not phone or len(phone) != 10 or not phone.isdigit():
            flash("❌ رقم الجوال غير صحيح", "error")
        elif not is_valid_code(code):
            flash("❌ الكود المدخل خطأ أو غير موجود", "error")
        elif is_code_used(code):
            flash("❌ الكود مستخدم من قبل", "error")
        else:
            save_record(f"{name},{phone},{full_plate},{code}")
            flash("✅ تم تفعيل الضمان. شكرًا لثقتك في ترو شيلد", "success")
    return render_template("index.html")
    