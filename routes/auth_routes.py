from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from services.auth_service import verify_login

auth_bp = Blueprint("auth", __name__)

@auth_bp.route("/")
def index():
    return render_template("index.html")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if verify_login(username, password):
            session["logged_in"] = True
            session["user"] = username
            flash("登入成功", "success")
            return redirect(url_for("student.report_form"))
        else:
            flash("帳號或密碼錯誤", "error")

    return render_template("login.html")

@auth_bp.route("/logout")
def logout():
    session.clear()
    flash("已登出", "success")
    return redirect(url_for("auth.login"))
