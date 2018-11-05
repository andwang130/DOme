

$(document).ready(function () {
    $("#submit").click(login)
})
function  login() {
    var name=$("#username").val();
    var pswd=$("#password").val();
    if(!name)
    {
        alert("用户名不可为空");
    }
    if(!pswd)
    {
        alert("密码不可为空");
    }
    if(name,pswd)
    {
        login_ajax(name,pswd)
    }


}
function login_ajax(name,pswd)
{
    var data={"usname":name,"pswd":pswd}
     $.ajax({
        url:'/login',
        type: 'POST',
        data:data,
        success: function (arg) {
            json_data=JSON.parse(arg)
            if (json_data["code"] == 0) {
              window.location.href='/admin/index.html'
            }
        }
    })


}