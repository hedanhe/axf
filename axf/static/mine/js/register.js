$(document).ready(function () {
    var accunt = document.getElementById("accunt");
    var accunterr = document.getElementById("accunterr");
    var checkerr = document.getElementById("checkerr");
    var userok = document.getElementById("userok");

    var pass = document.getElementById("pass");
    var passerr = document.getElementById("passerr");
    var passwd = document.getElementById("passwd");
    var passwderr = document.getElementById("passwderr");
    var passwdok = document.getElementById("passwdok");

    accunt.addEventListener("focus", function () {
        accunterr.style.display = "none";
        checkerr.style.display = "none";
        userok.style.display = "none"

    },false);

    accunt.addEventListener("blur", function () {
        instr = this.value;
        //检测帐号长度6~12
        if (instr.length < 6 || instr.length > 12){
            accunterr.style.display = "block";
            return;
        }

        //检测帐号是否备注测
        $.post("/checkuserid/", {"userid": instr}, function (data) {
            if (data.status == "error"){
                checkerr.style.display = "block"
            }
            if (data.status == "success") {
                userok.style.display = "block"
            }
        })

    },false);

    //检测密码长度6～16
    pass.addEventListener("focus", function () {
        passerr.style.display = "none";
    },false);

    pass.addEventListener("blur", function () {
        instr1 = this.value;
        if (instr1.length < 6 || instr1.length > 16){
            passerr.style.display = "block";
            return;
        }
    });

    //检测两次密码是否相同
    passwd.addEventListener("focus", function () {
        passwderr.style.display = "none";
        passwdok.style.display = "none";
    },false);

    passwd.addEventListener("blur", function () {
        instr2 = this.value;
        if (instr1 != instr2){
            passwderr.style.display = "block";
            return;
        }
        else if (instr1 == instr2){
            passwdok.style.display = "block";
            return;
        }
    })



});