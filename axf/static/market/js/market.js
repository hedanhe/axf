
//修改购物车表
$(document).ready(function () {
    //获取当前页面的页码显示小黄条
    var test = window.location.pathname;
    var aaa = document.getElementById(test.match(/\d+/));
    aaa.style.display = "block";

    var addShopping = document.getElementsByClassName("addShopping");
    var subShopping = document.getElementsByClassName("subShopping");


    for (var i = 0; i < addShopping.length; i++){

        addshopping = addShopping[i];
        addshopping.addEventListener("click", function () {
            pid = this.getAttribute("ga");
            $.post("/changecart/0/", {"productid": pid}, function (data) {
                if (data.data == -1) {
                    window.location.href = "http://127.0.0.1:8000/login/"
                }else {
                    if (data.status == "success"){
                        document.getElementById(pid).innerHTML = data.data

                    }
                }

            })
        })
    }

    for (var j = 0; j < subShopping.length; j++) {
        subshopping = subShopping[j];
        subshopping.addEventListener("click", function () {
            pid = this.getAttribute("ga");
            $.post("/changecart/1/", {"productid": pid}, function (data) {
                if (data.data == -1) {
                    window.location.href = "http://127.0.0.1:8000/login/"
                } else {
                    if (data.status == "success") {
                        document.getElementById(pid).innerHTML = data.data
                    }
                }
            })
        })
    }



});


