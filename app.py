from flask import Flask, redirect, render_template, url_for, flash, session, jsonify
from flask.globals import request
from datetime import timedelta
import lmam_bot as bot
import crud
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()

SECRETE_KEY = os.getenv('SECRETE_KEY')


app = Flask(__name__)
app.config['SECRET_KEY'] = 'fkfdydjg7r57gyi7879t8o787rgil7.,;jgyuf'
app.permanent_session_lifetime = timedelta(days=5)

host_id = "192.168.1.104"

@app.route("/")
def main():
    return render_template("main.html")


@app.route("/generate_link",methods=['GET','POST'])
def generate_link():
    uname = session["user"]
    x = crud.lmam["Users"].find({"Uname":uname},{"chat_id":1,"_id":0})
    for i in x:
        chat_id = i["chat_id"]
    if chat_id:
        link = "https://leavemeamessage.herokuapp.com/message/"+uname
        return jsonify({ "status":"ok","link" : link})
    return jsonify({"status":"error","msg": "Telegram bot is not authenticated"})

@app.route("/message/<username>")
def home(username):
    return render_template("leavemeamessage.html")


@app.route("/end")
def end():
    return render_template("end.html")


@app.route("/send/<username>", methods=['GET', 'POST'])
def send(username):
    data = request.get_json(force=True)
    msg = "Msg: " + data["msg"]
    
    x = crud.lmam["Users"].find({"Uname":username},{"chat_id":1,"_id":0})
    for i in x:
        chat_id = i["chat_id"]
    bot.sendmessage(chat_id,str(msg))

    dat = {
        "To": username,
        "Msg": data["msg"]
    }
    crud.message_insert("messages",dat)
    return redirect(url_for('end'))



@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json(force=True)
        check = crud.find_uname("Users", {"Uname": data["Uname"]})
        if check == 1:
            return jsonify({"Status":"Error","msg":"Username Already Exist!"})
        dat = {
            "Uname": data["Uname"],
            "Password": data["Password"],
            "Skey": data["Skey"],
            "chat_id":""
        }
        crud.user_insert("Users",dat)
        return redirect(url_for('login'))
    elif "user" in session:
        return redirect(url_for("login"))
    return render_template("register.html")

@app.route("/login",methods=['GET','POST'])
def login():
    if request.method == "POST":
        data = request.get_json(force=True)
        x = crud.find_uname("Users",{"Uname":data["Uname"]})
        if x==1:
            opw = crud.lmam["Users"].find({"Uname":data["Uname"]},{"Password":1,"_id":0})
            for i in opw:
                opassw = i
            if data["Password"] != opassw["Password"]:
                return jsonify({"msg":"Incorrect Password"})
            else:
                session.permanent = True
                session["user"] = data["Uname"]
                return redirect(url_for("profile"))
        else:
            return jsonify({"msg":"Invalid Username"})
    elif "user" in session:
        return redirect(url_for("profile"))
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

@app.route("/profile")
def profile():
    if "user" in session:
        user = session["user"]
        return render_template("profile.html",user=user)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(debug=True,host=host_id)
