function sendmessage() {
    url = window.location.href.split("/")
    var msg = "";
    //msg = document.getElementById("text").value
    msg = $("#text").val()
    if(msg === ""){
         alert("Enter somthing")
    }else{
        data = {
            "msg": msg    
            }
        fetch("/send/"+url[4],{
            method: "POST",
            Headers: {'Content-Type': 'appilication/json' },
            body: JSON.stringify(data)
        }).then(res =>{
            if (res.redirected) {
              window.location.href = res.url;
            }
        }).catch(function(e){
            console.log(e);
        })  
     }
}

var nameflag = 0

function checkname(){
  x = $("#uname").val();
  if(x.split(" ").length >= 2){
      $("#unameerror").html("Do not include spaces in your username");
      nameflag = 0
      return
  }else{
    $("#unameerror").html("")
    nameflag = 1
    return
  }
}


var flag1 = 0
var flag2 = 0
function pwreq(){
    pw = $("#password").val()
    if( pw.length < 7){
        $("#plength").html("Password must contain atleast 7 characters");
        flag = 0
        return
    }else{
        $("#plength").html("");
        flag1 = 1
        checkpassword()
    }
}

function checkpassword(){
    pw1 = $("#password").val()
    pw2 = $("#pw").val()
    if(pw1 !== pw2){
        $("#err").html("Password Mismatch")
        flag2 = 0
        return
    }else{
        $("#err").html("")
        flag2 = 1
    }
}

function register(){
    if(flag1 === 0 || flag2 === 0){
        alert("Enter password properly")
        return
    }
    if(nameflag === 0) {
      alert("Enter username properly");
      return;
    }
    var uname = ""
    uname = $("#uname").val()  
    if(uname === ""){
      alert("Enter username")
      return
    }
    data = {
      "Uname": $("#uname").val(),
      "Password": $("#password").val()
    }
    fetch("/register", {
      method: "POST",
      headers: { "Contenr-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((res) => {
        if (res.redirected) {
          window.location.href = res.url;
        } 
        else {
          return res.json();
        }
      }).then(function (json) {
        $("#unameerror").html(json.msg);
      }).catch(function (e) {
        console.log(e);
      });
}

function login(){
    uname = $("#uname").val()
    password = $("#password").val()
    if(uname === "" || password === ""){
      alert("Enter username and password properly")
      return
    }
    data = {
      "Uname":uname,
      "Password":password
    }
    fetch("/login",{
      method: "POST",
      headers:{"Content-Type":"application/json"},
      body: JSON.stringify(data)
    }).then(res =>{
      if(res.redirected){
        window.location.href = res.url
      }else{
        return res.json()
      }
    }).then(function(json){
      $("#login_error").html(json.msg);
    }).catch(function(e){
      console.log(e)
    })
}


function generate_link(){
  fetch("/generate_link",{
    method:"GET",
    headers:{"Content-Type":"application/json"},
  }).then(res =>{
    return res.json()
  }).then(function(json){
    if(json.status === "ok"){
    $("#link").html(json.link)
    }else{
      $("#msg").html(json.msg)
    }
  }).catch(function(e){
    console.log(e);
  });
  $("#copy").html("Copy Link");
}

function copyToClipboard(element) {
  var $temp = $("<input>");
  $("body").append($temp);
  $temp.val($(element).text()).select();
  document.execCommand("copy");
  $temp.remove();
  $("#copy").html("Copied ")
}


function deletemsg(x){
  comfirm = confirm("do you want to delete?")
  if(comfirm){
    var v = "msg_" + x;
    msgs = document.getElementById(v).innerHTML;
    data = {
      msg: msgs,
    };
    fetch("/delete", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(data),
    })
      .then((res) => {
        return res.json();
      })
      .then(function (json) {
        x = "div" + x;
        document.getElementById(x).classList.add("nonecls");
      })
      .catch(function (e) {
        console.log(e);
      });
  }else{
   return;  
  }
}