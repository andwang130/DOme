var t_in_click=undefined
var action;
var  uuid;
var  Userid;
$(document).ready(
    function () {
         $("#filse").change(filse_change)
        $("#submit").click(sudbit_click);
         $(".thumbnail").click(img_on_cliek)
         action=GetRequest("action")
          uuid=GetRequest("uuid")
         Userid=GetRequest("Userid")
        url_init()
        if(action.action=="update"&&Userid.Userid)
        {
            get_info(uuid.uuid,Userid.Userid);
        }

    }
)
function url_init() {

     $("#order").attr("href","/orderlist.html?uuid="+uuid.uuid)
        $("#add").attr("href","/addTpuser.html?action=create&uuid="+uuid.uuid)
        $("#tpindex").attr("href","/TPUser.html?uuid="+uuid.uuid)
}
function  get_info(uuid,userid) {

    data={"userid":userid,"action":"get_info"}

         $.ajax({
             url: '/Tpuser',
             type: 'POST',
             data: data,
             success: function (arg) {
                 arg = JSON.parse(arg)

                 var data=arg["data"]
                 if (arg["code"] == 0) {
                     console.log(arg)
                     $("#name").val(data["name"])
                     $("#votenum").val(data["votenum"])
                     $("#phone").val(data["phone"])
                      $("#description").val(data["description"])
                     $("#vheat").val(data["vheat"])
                      $("#avatar").attr("src",data["avatar"])
                      $("#images1").attr("src",data["images1"])
                     $("#images2").attr("src",data["images2"])
                     $("#images3").attr("src",data["images3"])
                     $("#images4").attr("src",data["images4"])
                    $("#images5").attr("src",data["images5"])
                     $("#introduction").val(data["introduction"])
                     $("#conten").val(data["conten"]);
                     console.log(data['status'])
                     $("input[name='status']:radio[value={value}]".replace(/{value}/,data['status'])).attr('checked','true');
                 }
             }
         }
     )

}
function sudbit_click() {
    var name=$("#name").val()
    if(!name)
    {
        alert("姓名必填")
    }
    var votenum=$("#votenum").val()
    var phone=$("#phone").val()
    if(!phone)
    {
         alert("手机必填")
    }
    var description=$("#description").val()
    var vheat=$("#vheat").val()
    if(!vheat)
    {
        alert("至少一张图片")
    }

    var avatar=$("#avatar").attr("src")
    var images1=$("#images1").attr("src")
    var images2=$("#images2").attr("src")
    var images3=$("#images3").attr("src")
    var images4=$("#images4").attr("src")
    var images5=$("#images5").attr("src")
    var introduction=$("#introduction").val()
    var conten=$("#conten").val();
    var status=$('input[name="status"]:checked').val();
    data={"name":name,"votenum":votenum,"phone":phone,"description":description,"vheat":vheat,
        "avatar":avatar,"images1":images1,"images2":images2,"images3":images3,"images4":images4,"images5":images5,
        "introduction":introduction,"conten":conten,"status":status
    }

    data["action"]=action.action

    data["uuid"]=uuid.uuid
    if(data["action"]=="update")
    {
        data["userid"]=Userid.Userid
    }
     $.ajax({
             url: '/Tpuser',
             type: 'POST',
             data: data,
             success: function (arg) {

                     location.href="/TPUser.html?uuid="+uuid.uuid


             }
         }
     )

}
function img_on_cliek(imgid)
{
     t_in_click=this

    $("#filse").click()

}

function filse_change() {
     var fiel= $(this).prop('files');
     var this_=this
     console.log(fiel[0])
        if((fiel[0].size/1024/1024)>10)
            {
                alert("文件过大");
            }
            filepath=fiel[0].name;
            var extStart=filepath.lastIndexOf(".");
            var ext=filepath.substring(extStart,filepath.length).toUpperCase();
            if(ext!=".BMP"&&ext!=".PNG"&&ext!=".GIF"&&ext!=".JPG"&&ext!=".JPEG")
            {

                alert("图片限于png,gif,jpeg,jpg格式");
            }
             var formFile = new FormData();
               formFile.append(fiel[0].name, fiel[0]); //加入文件对象
       $.ajax({
        url:'/uploadfile',
        type: 'POST',
        data:formFile,
        processData: false,//用于对data参数进行序列化处理 这里必须false
        contentType: false, //必须
        success: function (arg)
        {
            arg=JSON.parse(arg)

            if(arg["code"]=="0")
            {
                var data=arg["data"]
                $($(t_in_click).children("img")).attr("src",data[0]["path"])

            }
        }
    })
return
}


