$(document).ready(function () {
    var addShopping = document.getElementsByClassName("addShopping");
    var subShopping = document.getElementsByClassName("subShopping");
    var pay3 = document.getElementById("pay3");
    var pay11 = document.getElementById("pay11");
    //检查登录状态
    var p_text = $("#huanying").text();
    if (p_text =="欢迎：未登录"){
        document.getElementById("wei").style.display = "block";
        document.getElementById("pay").style.display = "none";
    }else {
        lis = document.getElementsByTagName('li');
        if (lis.length == 0){
            document.getElementById("kong").style.display = "block";
            document.getElementById("pay").style.display = "none";
        }
    }

    //初始全选按钮是否为真
    var asall = 0;
    $.post("/changecart/3/", function (data) {
        if (data.isall){
            pay11.style.display = "block";
            asall = 1
        }else {
            pay11.style.display = "none";
            asall = 0
        }
    });

    for(var i = 0; i< addShopping.length; i++){
        addshopping = addShopping[i];
        addshopping.addEventListener("click", function () {
            pid = this.getAttribute("ga");

            $.post("/changecart/0/", {"productid": pid}, function (data) {
                if (data.data == -1){
                    document.getElementById("wei").style.display ="block"
                }
                if (data.status == "success"){
                    document.getElementById(pid).innerHTML = data.data;
                    document.getElementById(pid + "b").innerHTML = "￥" + data.price;
                    pay3.innerHTML = "共￥"+ data.eff_price;
                    if (data.isall){
                        pay11.style.display = "block"
                        asall = 1
                    }else {
                        pay11.style.display = "none"
                        asall = 0
                    }
                }
            })
        })
    }

    //点击-按钮
    for (var j = 0; j < subShopping.length; j++) {
        subshopping = subShopping[j];
        subshopping.addEventListener("click", function () {
            pid = this.getAttribute("ga");
            $.post("/changecart/1/", {"productid": pid}, function (data) {

                if (data.status == "success") {
                    document.getElementById(pid).innerHTML = data.data;
                    document.getElementById(pid + "b").innerHTML = "￥"+ data.price;
                    pay3.innerHTML = "共￥"+ data.eff_price;
                    if (data.isall){
                        pay11.style.display = "block";
                        asall = 1
                    }else {
                        pay11.style.display = "none";
                        asall = 0
                    }

                    if (data.data == 0){
                        // window.location.href = "http://127.0.0.1:8000/cart/"
                        //dom元素自己不能删除自己,先找到其父元素
                        var li = document.getElementById(pid+"li");
                        li.parentNode.removeChild(li)

                        lis = document.getElementsByTagName('li');
                        if (lis.length == 0){
                            document.getElementById("kong").style.display = "block"
                            document.getElementById("pay").style.display = "none"
                        }
                    }
                }

            })
        })
    }

    //点击选中按钮
    var ischose = document.getElementsByClassName("ischose");
    for (gou = 0; gou<ischose.length; gou++){
        chose = ischose[gou];
        chose.addEventListener("click",function () {
            pid = this.getAttribute("goodsid");
            $.post("/changecart/2/", {"productid":pid}, function (data) {
                if(data.status == "success"){
                    // window.location.href = "http://127.0.0.1:8000/cart/"
                    document.getElementById(pid+"a").innerHTML = data.data;
                    pay3.innerHTML = "共￥"+ data.eff_price;
                    if (data.isall){
                        pay11.style.display = "block";
                        asall = 1
                    }else {
                        pay11.style.display = "none";
                        asall = 0
                    }

                }

            })
        })
    }

    //点击全选按钮
    var pay1 = document.getElementById("pay1");
    pay1.addEventListener("click", function () {
        $.post("/changecart/4/", {"asall":asall},function (data) {
            if (data.status == "success"){
                window.location.href = "http://127.0.0.1:8000/cart/"
            }
        })
    });

    //下单
    var ok = document.getElementById("pay4");
    ok.addEventListener("click", function () {
        var f = confirm("是否确认下单？");
        if (f){
            $.post("/saveorder/", function (data) {
                if (data.status == "success"){
                    window.location.href = "http://127.0.0.1:8000/myorder/"
                }
            })
        }
    })


});