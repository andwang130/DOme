var userid;
var uuid;
$(document).ready(
    function () {
        userid=GetRequest("userid")
        uuid=GetRequest("uuid")
        if(userid.userid)
        {
           $("#all").attr("href","/TPUser.html?uuid="+uuid.uuid)

         $("#vote").attr("href","/votedata.html?userid="+userid.userid+"&"+"uuid="+uuid.uuid)
         $("#order").attr("href","/usorder.html?userid="+userid.userid+"&"+"uuid="+uuid.uuid)
           inti(1)
        }

    }
)
function inti(page) {

    data={"userid":userid.userid,"action":"get_votedate","page":page}
      $.ajax({
             url: '/Tpuser',
             type: 'POST',
             data: data,
             success: function (arg) {
                 arg = JSON.parse(arg)
                 info=arg["info"]
                 data=arg["data"]
                 if (arg["code"] == "0") {
                    $("#avatar").attr("src",info["avatar"])
                     $("#name").text(info["name"])
                     $("#votenum").text(info["votenum"])
                     $("#liwu").text(info["liwu"])
                     $("#body").html("")
                     body_inti(data)
                     page_math(arg["count"])
                 }
             }
         }
     )
}

function body_inti(data) {
    for(var i=0;i<data.length;i++) {
       var id_td="<td>"+data[i]["orderid"]+"</td>";
       var img_td='<td style="text-align:center"><img src="'+data[i]["headimg"]+'" onerror="" width="48"></td>'
       var  openid_td='<td><br>'+data[i]["openid"]+'<span class="label label-danger" onclick="addblack('+'\''+data[i]["openid"]+'\''+',0);"\">加入黑名单</span></td>'
       var ip_td='<td>'+data[i]["ip"]+'<span class="label label-danger" onclick="addblack('+'\''+data[i]["ip"]+'\''+',1);">加入黑名单</span></td>'
       var  times_id='<td>'+data[i]["times"]+'</td>'
       var HTML='<tr>'+id_td+img_td+openid_td+ip_td+times_id+'</tr>'
        $("#body").append(HTML)
    }

}
var now_page=1;
function page_math(count) {
   var page_end=Math.ceil(count/25);

   var THML=""
   var page_html="<li><a href='javacript:get_list({PAGE})'>{PAGE}</a></li>";

   if(page_end>10)
   {
       var new_page_end=page_end
       if(page_end-now_page>10)
       {
           new_page_end=now_page+10;
       }

       THML+="<li><a page_id='{pnow_page-5ageid}' href='javascript:void(0)'>上一页</a></li>".replace(/{pageid}/,now_page-1);
       for(var i=new_page_end-10;i<new_page_end+1;i++)
       {
           if(i==now_page) {
               THML +="<li class='active'><a href='#'>{PAGE}</a></li>".replace(/{PAGE}/,i);
           }
           else
           {
               THML +="<li><a page_id='{pageid}' href='#'>{PAGE}</a></li>".replace(/{PAGE}/,i).replace(/{pageid}/,i);;
           }
       }
   }
   else
   {
        for(var i=1;i<page_end+1;i++)
       {

           if(i==now_page) {
               THML +="<li class='active'><a href='#' >{PAGE}</a></li>".replace(/{PAGE}/,i)
           }
           else
           {
               THML +="<li><a page_id='{pageid}' href='#' >{PAGE}</a></li>".replace(/{PAGE}/,i).replace(/{pageid}/,i);
           }
       }
   }
    THML+="<li><a page_id='{pageid}' href='#'>下一页</a></li>".replace(/{pageid}/,now_page+1);

    $("#page_active").html(THML);
    $("#page_active li a").click(on_a_cliek)
}

function  on_a_cliek()
{

    var page_id=$(this).attr("page_id")
    now_page=Number(page_id)
    inti(Number(page_id));
    console.log(page_id);
}
function addblack(value ,statr)
{
    var data={"value":value,"start":statr,"action":"addblack"}
     $.ajax({
         url: '/black',
         type: 'POST',
         data: data,
         success: function (arg) {
            var json_data=JSON.parse(arg)
             if(json_data["code"]==0)
             {
                 alert("添加成功")
             }

         }
     })
}