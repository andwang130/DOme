
var start=0;
$(document).ready(
    function () {
        $(".we7-page-tab li").click(li_click);

        get_backlist(1)
    }
);
function li_click() {

    console.log("sss");
    var startid=$(this).attr("start");
    if(Number(startid)==0)
    {
        start=0;
    }
    else if(Number(startid)==1)
    {
        start=1;
    }
    $(this).attr("class","active");
    $(this).siblings(".active").attr("class","");
    get_backlist(1)

}
function get_backlist(page) {

     var data={"start":start,"action":"getblack","page":page};
     $.ajax({
         url: '/black',
         type: 'POST',
         data: data,
         success: function (arg) {
            var json_data=JSON.parse(arg);
             if(json_data["code"]==0)
             {
                 backlit_init(json_data["data"])
             }
                else if(json_data["code"]==-110){
               location.href="/login.html"
           }

         }
     })
}
function backlit_init(data) {
     $("#body").html("");
    for(var  i=0;i<data.length;i++)
    {
        var delete_td = "<td><a class='btn btn-default' onclick='delete_back('"+data[i]["blackid"]+"')'>移除</a></td>";
        var value_td="<td>" + data[i]["value"] + "</td>";
        var start_td="<td>" + data[i]["start"] + "</td>";
        var times_td="<td>" +getLocalTime(data[i]["times"]) + "</td>";
        var HTML='<tr>'+start_td+value_td+times_td+delete_td+'</tr>';
        $("#body").append(HTML)
    }
}
var now_page=1;
function page_math(count) {
   var page_end=Math.ceil(count/20);

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
            console.log(page_end);
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
    $("#page_active li a").click()
}
function  on_a_cliek()
{

    var page_id=$(this).attr("page_id");
    now_page=page_id;

   get_backlist(now_page)
}
function delete_back(blackid) {

    var data = {"action": "delete","blackid":blackid};
    $.ajax({
        url: '/black',
        type: 'POST',
        data: data,
        success: function (arg) {
            var json_data = JSON.parse(arg);
            if (json_data["code"] == 0) {
                get_backlist(now_page)
            }
            else if (json_data["code"] == -110) {
                location.href = "/login.html"
            }

        }
    })
}