
var t_in_click=undefined
var action=""
var uuid=""
$(document).ready(
    function () {
          KindEditor.ready(function(K) {
                window.editor = K.create('#customized');
        });
    $("#topimg").change(upload_img)
    $("#shareimg").change(upload_img)
    $("#himg").change(upload_img)
    $(".tttt").click(tttt_click)
    $("#filse").change(filse_change)
    $("#submitForm").click(submi_send)
    $("#customized").html("<p>活动规则介绍</p>");
    $("#buttonpane").html("<p>活动规则介绍</p>");
    $("#btn_add_liwu").click(btn_add_liwu);
    action=GetRequest("action")
    uuid=GetRequest("uuid")
    if(uuid.uuid)
    {
     get_info(uuid.uuid)
    }
    }
)
function get_info(uuid) {

    data={"uuid":uuid}
    data["action"]="get_info"
      $.ajax({
        url:'/poject',
        type: 'POST',
        data:data,
        success: function (arg)
        {
            arg=JSON.parse(arg)
    if(arg["code"]=="0")
    {
    var data=arg["data"]
        var titile=$("#titile").val(data["titile"]);
    var himgV=$("#himgV").attr("src",data["himgV"]);
    var description=$("#description").val(data["description"]);
    var tiemstatr=$("#tiemstatr").val(data["tiemstatr"]);
    var timeend=$("#timeend").val(data["timeend"]);
        $("#daterangetime").text(data["tiemstatr"]+" 至 "+data["timeend"])

    var aptimestart=$("#aptimestart").val(data["aptimestart"]);
    var aptimeend=$("#aptimeend").val(data["aptimeend"]);
     $("#aptdatetime").text(data["aptimestart"]+" 至 "+data["aptimeend"])

        var aptimestart=$("#votestart").val(data["votestart"]);
    var aptimeend=$("#voteend").val(data["voteend"]);
     $("#voteendtime").text(data["votestart"]+" 至 "+data["voteend"])


    var topimgV=$("#topimgV").attr("src",data["topimgV"]);//
    var customized=$("#customized").html(data["customized"]); //
    var buttonpane=$("#buttonpane").html(data["buttonpane"]); //

    var sharetitle=$("#sharetitle").val(data["sharetitle"]) //
    var shareimgV=$("#shareimgV").attr("src",data["shareimgV"]) //
    var sharedesc=$("#sharedesc").val(data["sharedesc"]);//
    // $(":radio[name='rstatus'][value="+data['rstatus']+"]").attr("checked","checked");




    var liwus=data["liwulist"]
        console.log(liwus)
    for(var i=0;i<liwus.length;i++)
    {
     liwu_init(liwus[i]["gifttitle"],liwus[i]["gifimg"],liwus[i]["giftprice"],liwus[i]["giftvote"])
    }


            }
        }
    })
}
function submi_send() {
    var titile=$("#titile").val();
    var himgV=$("#himgV").attr("src");
    var description=$("#description").val();
    var tiemstatr=$("#tiemstatr").val();
    var timeend=$("#timeend").val();
    var aptimestart=$("#aptimestart").val();
    var aptimeend=$("#aptimeend").val();
    var votestart=$("#votestart").val();
    var voteend=$("#voteend").val();
    var topimgV=$("#topimgV").attr("src");
    var customized=$("#customized").html();
    var buttonpane=$("#buttonpane").html();
    var sharetitle=$("#sharetitle").val()
    var shareimgV=$("#shareimgV").attr("src")
    var sharedesc=$("#sharedesc").val();
    var rstatus=$('input:radio[name="rstatus"]:checked').val();
   var liwulist=new Array()

    var liwus=$("tr[name='liwus']");
    for(var i=0;i<liwus.length;i++)
    {
        var gifttitle=$(liwus[i]).find("td:nth-child(1) input[name='gifttitle']").val();
        var gifimg=$(liwus[i]).find("td:nth-child(2) div a img").attr("src");
        var giftprice=$(liwus[i]).find("td:nth-child(3) div input[name='giftprice']").val();
        var giftvote=$(liwus[i]).find("td:nth-child(4) input[name='giftvote']").val();
        var data={"gifttitle":gifttitle,"gifimg":gifimg,"giftprice":giftprice,"giftvote":giftvote}
        liwulist[i]=data;

    }

    var list_str=JSON.stringify(liwulist)
    var data={"titile":titile,"himgV":himgV,"description":description,"votestart":votestart,"voteend":voteend,
       "tiemstatr":tiemstatr,"timeend":timeend,"topimgV":topimgV,"customized":customized,"buttonpane":buttonpane,
       "sharetitle":sharetitle,"shareimgV":shareimgV,"sharedesc":sharedesc,"aptimestart":aptimestart,"aptimeend":aptimeend,
        "liwulist":list_str
   }
   console.log(data)
   if(action.action) {
    data["uuid"]=uuid.uuid
    data["action"]=action.action
   }
    else
   {
       action="create"

    data["action"]=action
        }

      $.ajax({
        url:'/poject',
        type: 'POST',
        data:data,
        success: function (arg)
        {
            arg=JSON.parse(arg)
            window.href="/index.html"

        }
    })
}
function upload_img() {
     var fiel= $(this).prop('files');
     var this_=this
     var this_id=$(this).attr("id")
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
                var new_id="#"+ this_id+"V"
                $(new_id).attr("src",data[0]["path"])
                $(this_).attr("value",data[0]["path"])


            }
        }
    })
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
}


function tttt_click() {
     t_in_click=this
    $("#filse").click()

}
function btn_add_liwu() {
        liwu_init("钻石","images/diamond.png",1,3)
}
function liwu_init (gifttitle,gifimg,giftprice,giftvote) {
     html="<tr name='liwus'>\n" +
        "\t\t<td class=\"text-left\" ><input type=\"text\" placeholder=\"输入名称\" value=\""+gifttitle+"\" class=\"form-control\" name=\"gifttitle\"></td>\n" +
        "\t\t<td><div class=\"adimgbo\"><a  href=\"#\" class=\"tttt\"><img src=\"/"+gifimg+"\"  height=\"30\"><input type=\"hidden\" value=\"/images/diamond.png\" name=\"gifticon\"></a></div></td>\n" +
        "\t\t<td class=\"text-left\" ><div class=\"input-group\">\n" +
        "          <input type=\"text\" placeholder=\"输入支付价格\" value=\""+giftprice+"\" class=\"form-control\" name=\"giftprice\">\n" +
        "\t\t  <span class=\"input-group-addon\">元</span>\n" +
        "        </div></td>\n" +
        "\t\t<td class=\"text-left\" >\n" +
        "\t\t<div class=\"input-group\">\n" +
        "          <input type=\"text\" placeholder=\"输入礼物奖励的票数\" value=\""+giftvote+"\" class=\"form-control\" name=\"giftvote\">\n" +
        "        </div>\n" +
        "\t\t</td>\n" +
        "\t\t<td><button type=\"button\" class=\"btn btn-danger btn_del_ad btn-xs\">删除</button></td>\n" +
        "\t</tr>"
        $("#js-table-2").append(html);
}