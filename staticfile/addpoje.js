
var t_in_click=undefined;
var action="";
var uuid="";
var ue1
var ue2
var page=1
var start=""
var end=""
var times=""
var findend=""
$(document).ready(function (){
     ue1 = UM.getEditor('myEditor1');
     ue2 = UM.getEditor('myEditor2');
    $("#topimg").change(upload_img);
     $("#topimg2").change(upload_img);
      $("#topimg3").change(upload_img);
    $("#shareimg").change(upload_img);
    $("#himg").change(upload_img);
    $(".tttt").click(tttt_click);
    $("#filse").change(filse_change);
    $("#submitForm").click(submi_send);
    $("#customized").html("<p>活动规则介绍</p>");
    $("#buttonpane").html("<p>活动规则介绍</p>");
    $("#btn_add_liwu").click(btn_add_liwu);
    $("#videofile").change(video_change)
    action=GetRequest("action");
    uuid=GetRequest("uuid");
    page=GetRequest("page").page;
    start=GetRequest("start").start;
    end=GetRequest("end").end;
    times=GetRequest("times").times;
    findend=GetRequest("findend").findend;

    if(uuid.uuid)
    {
     get_info(uuid.uuid)
    }
    }
);
function get_info(uuid) {

    data={"uuid":uuid};
    data["action"]="get_info";
      $.ajax({
        url:'/poject',
        type: 'POST',
        data:data,
        success: function (arg)
        {
            arg=JSON.parse(arg);
    if(arg["code"]=="0")
    {
    var data=arg["data"];
        var titile=$("#titile").val(data["titile"]);
    var himgV=$("#himgV").attr("src",data["himgV"]);
    var description=$("#description").val(data["description"]);
    var tiemstatr=$("#tiemstatr").val(data["tiemstatr"]);
    var timeend=$("#timeend").val(data["timeend"]);
        $("#daterangetime").text(data["tiemstatr"]+" 至 "+data["timeend"]);

    var aptimestart=$("#aptimestart").val(data["aptimestart"]);
    var aptimeend=$("#aptimeend").val(data["aptimeend"]);
     $("#aptdatetime").text(data["aptimestart"]+" 至 "+data["aptimeend"]);

        var aptimestart=$("#votestart").val(data["votestart"]);
    var aptimeend=$("#voteend").val(data["voteend"]);
     $("#voteendtime").text(data["votestart"]+" 至 "+data["voteend"]);
     $("#volume").val(data["volume"])

    var topimgV=$("#topimgV").attr("src",data["topimgV"]);
    var topimg2V=$("#topimg2V").attr("src",data["topimg2V"]);
 var topimg3V=$("#topimg3V").attr("src",data["topimg3V"]);
    $("#videourl").attr("href",data["videourl"])
    $("#videourl").text(data["videoname"])
   ue1.ready(function () {
        ue1.setContent(data["customized"]); //

   })
        ue2.ready(function () {
             ue2.setContent(data["buttonpane"]); //
        })


    var sharetitle=$("#sharetitle").val(data["sharetitle"]); //
    var shareimgV=$("#shareimgV").attr("src",data["shareimgV"]); //
    var sharedesc=$("#sharedesc").val(data["sharedesc"]);//
                    $("#ratio").val(data["ratio"])
    $("#rangetime").val(data["rangetime"])
    $("#rangenum").val(data["rangenum"])
    // $(":radio[name='rstatus'][value="+data['rstatus']+"]").attr("checked","checked");




    var liwus=data["liwulist"];
        console.log(liwus);
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
    var rangetime=$("#rangetime").val()
    var rangenum=$("#rangenum").val()
    var volume=$("#volume").val()
    var description=$("#description").val();
    var tiemstatr=$("#tiemstatr").val();
    var timeend=$("#timeend").val();
    var aptimestart=$("#aptimestart").val();
    var aptimeend=$("#aptimeend").val();
    var votestart=$("#votestart").val();
    var voteend=$("#voteend").val();
    var topimgV=$("#topimgV").attr("src");
      var videourl=$("#videourl").attr("href")
        var videoname=$("#videourl").text()
    if(topimgV=="./resource/images/nopic.jpg")
    {
        topimgV=""
    }
    var topimg2V=$("#topimg2V").attr("src");
      if(topimg2V=="./resource/images/nopic.jpg")
    {
        topimg2V=""
    }
    var topimg3V=$("#topimg3V").attr("src");
      if(topimg3V=="./resource/images/nopic.jpg")
    {
        topimg3V=""
    }
    var ratio=$("#ratio").val()
    var customized=ue1.getContent()
    var buttonpane=ue2.getContent()
    var sharetitle=$("#sharetitle").val();
    var shareimgV=$("#shareimgV").attr("src");
    var sharedesc=$("#sharedesc").val();
    var rstatus=$('input:radio[name="rstatus"]:checked').val();
   var liwulist=[];

    var liwus=$("tr[name='liwus']");
    for(var i=0;i<liwus.length;i++)
    {
        var gifttitle=$(liwus[i]).find("td:nth-child(1) input[name='gifttitle']").val();
        var gifimg=$(liwus[i]).find("td:nth-child(2) div a img").attr("src");
        var giftprice=$(liwus[i]).find("td:nth-child(3) div input[name='giftprice']").val();
        var giftvote=$(liwus[i]).find("td:nth-child(4) input[name='giftvote']").val();
        var data={"gifttitle":gifttitle,"gifimg":gifimg,"giftprice":giftprice,"giftvote":giftvote};
        liwulist[i]=data;

    }

    var list_str=JSON.stringify(liwulist);
    var data={"titile":titile,"himgV":himgV,"description":description,"votestart":votestart,"voteend":voteend,
       "tiemstatr":tiemstatr,"timeend":timeend,"topimgV":topimgV,"customized":customized,"buttonpane":buttonpane,
       "sharetitle":sharetitle,"shareimgV":shareimgV,"sharedesc":sharedesc,"aptimestart":aptimestart,"aptimeend":aptimeend,
        "liwulist":list_str,"topimg2V":topimg2V,"topimg3V":topimg3V,"ratio":ratio,"rangetime":rangetime,"rangenum":rangenum,
        "videourl":videourl,"videoname":videoname,"volume":volume
   };
   console.log(data);
   if(action.action) {
    data["uuid"]=uuid.uuid;
    data["action"]=action.action
   }
    else
   {
    data["action"]="create"
        }

      $.ajax({
        url:'/poject',
        type: 'POST',
        data:data,
        success: function (arg)
        {

            arg=JSON.parse(arg);
            if (action.action=="update") {
                location.href = "/index.html?page=" + page + "&start=" + start + "&end=" + end + "&times=" + times + "&findend=" + findend
            }
            else{
                location.href = "/index.html"
            }

        }
    })
}
function upload_img() {
     var fiel= $(this).prop('files');
     var this_=this;
     var this_id=$(this).attr("id");
     console.log(fiel[0]);
        if((fiel[0].size/1024/1024)>10)
            {
                alert("文件过大");
                return
            }
            filepath=fiel[0].name;
            var extStart=filepath.lastIndexOf(".");
            var ext=filepath.substring(extStart,filepath.length).toUpperCase();
            if(ext!=".BMP"&&ext!=".PNG"&&ext!=".GIF"&&ext!=".JPG"&&ext!=".JPEG")
            {

                alert("图片限于png,gif,jpeg,jpg格式");
                return
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
            arg=JSON.parse(arg);

            if(arg["code"]=="0")
            {
                var data=arg["data"];
                var new_id="#"+ this_id+"V";
                $(new_id).attr("src",data[0]["path"]);
                $(this_).attr("value",data[0]["path"])


            }
        }
    })
}
function filse_change() {
     var fiel= $(this).prop('files');
     var this_=this;
     console.log(fiel[0]);
        if((fiel[0].size/1024/1024)>10)
            {
                alert("文件过大");
                return
            }
            filepath=fiel[0].name;
            var extStart=filepath.lastIndexOf(".");
            var ext=filepath.substring(extStart,filepath.length).toUpperCase();
            if(ext!=".BMP"&&ext!=".PNG"&&ext!=".GIF"&&ext!=".JPG"&&ext!=".JPEG")
            {

                alert("图片限于png,gif,jpeg,jpg格式");
                return
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
            arg=JSON.parse(arg);

            if(arg["code"]=="0")
            {
                var data=arg["data"];
                $($(t_in_click).children("img")).attr("src",data[0]["path"])

            }
        }
    })
}


function tttt_click() {
     t_in_click=this;
    $("#filse").click()

}
function btn_add_liwu() {
        liwu_init("钻石","/images/diamond.png",1,3)
}
function liwu_init (gifttitle,gifimg,giftprice,giftvote) {
     html="<tr name='liwus'>\n" +
        "\t\t<td class=\"text-left\" ><input type=\"text\" placeholder=\"输入名称\" value=\""+gifttitle+"\" class=\"form-control\" name=\"gifttitle\"></td>\n" +
        "\t\t<td><div class=\"adimgbo\"><a  href=\"#\" class=\"tttt\"><img src=\""+gifimg+"\"  height=\"30\"><input type=\"hidden\" value=\"/images/diamond.png\" name=\"gifticon\"></a></div></td>\n" +
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
        "\t</tr>";
        $("#js-table-2").append(html);
}
 function video_change() {
     var fiel= $(this).prop('files');
     var this_=this;
     console.log(fiel[0]);
        if((fiel[0].size/1024/1024)>500)
            {
                alert("文件过大");
            }
            filepath=fiel[0].name;
            var extStart=filepath.lastIndexOf(".");
            var ext=filepath.substring(extStart,filepath.length).toUpperCase();
            if(ext!=".MP4")
            {

                alert("限于MP4格式");
                return
            }
             var formFile = new FormData();
               formFile.append("video", fiel[0]); //加入文件对象

       $.mask_element('#test_mask');
       $.ajax({
        url:'/user?action=new_upload_video',
        type: 'POST',
        data:formFile,
        processData: false,//用于对data参数进行序列化处理 这里必须false
        contentType: false, //必须
        success: function (arg)
        {
            arg=JSON.parse(arg);

            if(arg["code"]=="0")
            {

                var data=arg["data"];
                $("#videourl").attr("href",data["url"])
                  $("#videourl").text(data["filename"])
               $.mask_close("#test_mask");
                 $.sendSuccessToTop('上传成功', 3000, function() {
                 console.log('sendSuccessToTop closed');
             });
            }
        }
    });

}
var cache = {};
	$.mask_element = function(ele_id, timeout){
		//判断当前元素是否已经添加遮罩，如果已添加，则直接返回
		if($(".mask[ele="+ele_id+"]").length > 0){
			return;
		}
		//添加遮罩元素
		var mask = '<div class="mask" ele='+ele_id+' style="width: '+$(ele_id).width()+'px !important; height: '+$(ele_id).height()+'px !important; left: '+$(ele_id).offset().left+'px !important; top: '+$(ele_id).offset().top+'px !important;"><div>数据加载中...</div></div>';
		$("body").append(mask);
		clearTimeout(cache[ele_id]);
		if(timeout && timeout > 0){
			var s = setTimeout(function(){
				$(".mask[ele="+ele_id+"]").remove();
			}, timeout);
			cache[ele_id] = s;
		}
	}
	$.mask_close = function(ele_id){
		$(".mask[ele="+ele_id+"]").remove();
	}
    $.sendSuccessToTop= function(msg, duration, callback) {
      var content = '<div class="dialog-success-top">' + '    <i class="i-icon"></i>' + msg + '</div>';

      $('body').append(content);

      var $tipBox = $('.dialog-success-top'),
          width = $tipBox.width();

      $tipBox.css({
        'margin-left': -(width / 2),
        'margin-top': 20,
        'opacity': 0
      });

      $tipBox.animate({
        'opacity': 1,
        'margin-top': 0
      }, 400, function() {
        // 自动隐藏
        clearTimeout(window.cc_timerSendSuccessToTop);
        window.cc_timerSendSuccessToTop = setTimeout(function() {
          $tipBox.fadeOut(function() {
            $tipBox.remove();
            typeof callback === 'function' && callback();
          })
        }, duration || 3000);
      });
    }


