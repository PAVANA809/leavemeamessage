from flask import Flask, redirect, render_template, url_for, flash, session, jsonify
from flask.globals import request
from datetime import timedelta
import crud
import dotenv
from dotenv import load_dotenv
import os

load_dotenv()

SECRETE_KEY = os.getenv('SECRETE_KEY')


app = Flask(__name__)
app.config['SECRET_KEY'] = SECRETE_KEY
app.permanent_session_lifetime = timedelta(days=5)

host_id = "192.168.1.100"

@app.route("/")
def main():
    return render_template("main.html")


@app.route("/generate_link",methods=['GET','POST'])
def generate_link():
    uname = session["user"]
    link = "https://leavemeamessage.herokuapp.com/message/"+uname
    return jsonify({ "status":"ok","link" : link})

@app.route("/message/<username>")
def home(username):
    return render_template("leavemeamessage.html",user=username)


@app.route("/end")
def end():
    return render_template("end.html")


@app.route("/send/<username>", methods=['GET', 'POST'])
def send(username):
    data = request.get_json(force=True)
    msg = data["msg"]
    crud.lmam['messages'].update_one({'To':username},{'$push':{'Msg':msg}})
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
            "Password": data["Password"]
        }
        crud.user_insert("Users",dat)
        crud.lmam['messages'].insert_one({'To': data['Uname'], 'Msg': []})
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
        msgs = crud.lmam['messages'].find({'To': user}, {'_id': 0, 'Msg': 1})
        x = list()
        for i in msgs:
            x = i
        profile_data = {
            "user":user,
            "msg_list": x['Msg']
        }
        return render_template("profile.html",user=profile_data)
    return redirect(url_for("login"))


@app.route("/delete",methods=["GET","POST"])
def delete():
    if request.method == "POST":
        if "user" in session:
            data = request.get_json(force=True)
            crud.lmam['messages'].update_one({'To': session['user']}, {'$pull': {'Msg': data["msg"]}})
            return jsonify({"msg": "deleted"})

if __name__ == "__main__":
    app.run(debug=True)
