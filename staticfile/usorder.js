var userid="";
var start=3;
var uuid;
$(document).ready(
    function () {
        uuid=GetRequest("uuid");
        userid=GetRequest("userid");
        if(userid.userid) {

            get_ordel(userid.userid,1);
            url_inti();
            $(" .btn-primary").click(primary_click)
        }

    }
);

function url_inti() {
     $("#all").attr("href","/TPUser.html?uuid="+uuid.uuid);
     $("#vote").attr("href","/votedata.html?userid="+userid.userid+"&"+"uuid="+uuid.uuid);
     $("#order").attr("href","/usorder.html?userid="+userid.userid+"&"+"uuid="+uuid.uuid)
}
function primary_click() {

   var text_=$(this).text();
  if(text_=="已付款订单")
  {
      start=1;
      $(this).text("全部订单")
  }
  else
  {     start=3;
       $(this).text("已付款订单")
  }
 get_ordel(uuid.uuid,1)


}
function get_ordel(userid,page)
{
    now_page=page;
    data = {"action": "user_order", "userid": userid,"page":page,"start":start};
    $.ajax({
        url: '/order',
        type: 'POST',
        data: data,
        success: function (arg) {
            arg = JSON.parse(arg);
            data=arg["data"];
            var info=arg["info"];
            if (arg["code"] == "0") {
                body_init(data);
                page_math(arg["count"]);
                 $("#avatar").attr("src",info["avatar"]);
                 $("#name").text(info["name"]);
                 $("#votenum").text(info["votenum"]);
                 $("#liwu").text(info["liwu"])
            }
            else if(arg["code"]==-110){
               location.href="/login.html"
           }
        }
    })
}

function body_init(data) {

    $("#body").html('');
    order=["orderid","userid","uuid","money","liwu","num","votenum","times","ip","start"];
    for(var i=0;i<data.length;i++)
    {
        var id_td='<td class="text-left vertical-middle">'+data[i]["orderid"]+'</td>';
        var name_td='<td class="text-left vertical-middle">'+data[i]["username"]+'</td>';
        var num_td='<td class="text-left vertical-middle"><p><span class="label label-primary">'+data[i]["money"]+'</span>/<span class="label label-info">'+data[i]["num"]+'</span>/<span class="label label-warning">'+data[i]["votenum"]+'</span></p></td>';
        var ip_time_td='<td class="text-left vertical-middle">'+getLocalTime(data[i]["times"])+'<p>'+data[i]["ip"]+'</p></td>';
        var start_td;
        var money_td;
        if(data[i]["start"]==1)
        {
          start_td='<td class="text-left vertical-middle"><p><span class="label label-success">已付款</span></p></td>';
        money_td='<td class="text-left vertical-middle"><p><span class="label label-danger">'+data[i]["money"]+'元</span></p></td>'

        }
        else
        {
            start_td='<td class="text-left vertical-middle"><p><span class="label label-default">未付款</span></p></td>';
                    money_td='<td class="text-left vertical-middle"><p><span class="label label-default">'+data[i]["money"]+'元</span></p></td>'


        }

        var html="<tr>"+id_td+name_td+money_td+num_td+ip_time_td+start_td+"</tr>>";
        $("#body").append(html)
    }

}
var now_page=1;
function page_math(count) {
   var page_end=Math.ceil(count/25);

   var THML="";
   var page_html="<li><a href='javacript:get_list({PAGE})'>{PAGE}</a></li>";

   if(page_end>10)
   {
       var new_page_end=page_end;
       if(page_end-now_page>10)
       {
           new_page_end=now_page+10;
       }

       THML+="<li><a page_id='{pageid}' href='javascript:void(0)'>上一页</a></li>".replace(/{pageid}/,now_page-1);
       for(var i=new_page_end-10;i<new_page_end+1;i++)
       {
           if(i==now_page) {
               THML +="<li class='active'><a href='#'>{PAGE}</a></li>".replace(/{PAGE}/,i);
           }
           else
           {
               THML += "<li><a page_id='{pageid}' href='#'>{PAGE}</a></li>".replace(/{PAGE}/, i).replace(/{pageid}/, i);
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

    var page_id=$(this).attr("page_id");
    now_page=Number(page_id);
    get_ordel(userid.userid,Number(page_id));
}