import os
import pandas as pd
import math
from flask import Blueprint, render_template, request, redirect, url_for, flash

from werkzeug.utils import secure_filename

student_list_bp = Blueprint("student_list", __name__)

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
DATA_DIR = os.path.join(BASE_DIR, "data")
UPLOAD_PATH = os.path.join(DATA_DIR, "students.csv")

os.makedirs(DATA_DIR, exist_ok=True)

# Show student list or upload area
@student_list_bp.route("/students", methods=["GET", "POST"])
def students():
    if request.method == "POST":
        file = request.files.get("file")
        if not file:
            flash("請選擇檔案", "error")
            return redirect(url_for("student_list.students"))
        
        if not file.filename.endswith(".csv"):
            flash("請上傳 CSV 檔案", "error")
            return redirect(url_for("student_list.students"))
        
        file.save(UPLOAD_PATH)
        flash("上傳成功", "success")
        return redirect(url_for("student_list.students"))

    if not os.path.exists(UPLOAD_PATH):
        return render_template("students.html", students=None)

    # Only if there is an uploaded file, the student list will be displayed
    per_page = int(request.args.get("per_page", 20))
    page = int(request.args.get("page", 1))

    df = pd.read_csv(UPLOAD_PATH, dtype={"聯絡電話": str})
    df["聯絡電話"] = df["聯絡電話"].apply(lambda x: f"0{x[1:4]}-{x[4:7]}-{x[7:]}" if len(x) == 10 and x.startswith("09") else x)
    total = len(df)
    total_pages = math.ceil(total / per_page)

    start = (page - 1) * per_page
    end = start + per_page
    students_page = df.iloc[start:end]

    return render_template(
        "students.html",
        students=students_page.to_dict(orient="records"),
        total_pages=total_pages,
        current_page=page,
        per_page=per_page
    )
