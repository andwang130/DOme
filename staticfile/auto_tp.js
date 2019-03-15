var tr="<tr>\n" +
    "                \t<input type=\"hidden\" value=\"262592\">\n" +
    "                    <td class=\"text-left vertical-middle\">{间隔}</td>\n" +
    "\t\t\t\t\t<td class=\"text-left vertical-middle\"><span class=\"label label-info\">{活动名称}</span></td>\n" +
    "\t\t\t\t\t<td class=\"text-left vertical-middle _ticket\"><span class=\"label label-primary _ticket_lable\">{start}-{end}</span></td><!-- 移入移出事件  -->\n" +
    "\t\t\t\t\t<td class=\"text-left vertical-middle\"><p>\n" +
    "\t\t\t\t\t<a class=\"color-default we7-margin-right\" title=\"编辑\" href=\"/addauto_click.html?action=update&autoid={autoid}\"><i class=\"fa fa-edit\"></i> 编辑</a>\n" +
    "\t\t\t\t\t<a class=\"color-default we7-margin-right\" rel=\"tooltip\" href=\"#\" onclick=\"drop_confirm('您确定要删除吗?删除不可恢复，同时删除所有相关数据！','{delete}');\" title=\"删除\"><i class=\"fa fa-times\"></i> 删除</a></p>\n" +
    "                    </td>\n{span}" +
    "                </tr>";
$(document).ready(
    function () {

        get_list(1);
        $(".btn-default").click(set_key)
    }
);
var key;
function set_key() {

    key=$("#keyword").val();
    get_list(1)
}
function drop_confirm(mages,url)
{

    if(confirm(mages))
    {
        data={"action":"delete","autoid":url};
         $.ajax({
        url:'/auto_click',
        type: 'POST',
        data:data,
        success: function (arg)
        {
            location.href="/auto_click.html"
        }
         })
    }
}
function get_list(page) {
    now_page=page;
    data={"action":"list","page":page};

     $.ajax({
        url:'/auto_click',
        type: 'POST',
        data:data,
        success: function (arg)
        {
            var data=JSON.parse(arg);
            $("#pojectlist").html("");
           if(data["code"]==0)
           {
                var datalist=data["data"];
               for(var i=0;i<datalist.length;i++)
               {
                   var new_tr=tr.replace(/{间隔}/,datalist[i]["times"]).replace(/{活动名称}/,datalist[i]["name"])
                       .replace(/{start}/,datalist[i]["start"]).replace(/{end}/,datalist[i]["end"]).replace(/{autoid}/,datalist[i]["autoid"])
                       .replace(/{delete}/,datalist[i]["autoid"]);

                   if(datalist[i]["status"]==0)
                   {
                      new_tr= new_tr.replace(/{span}/,'<td class="text-left vertical-middle"><span class="label label-default">未开启</span></td>')
                   }
                   else {
                       new_tr=new_tr.replace(/{span}/,'<td class="text-left vertical-middle"><span class="label label-success">开启</span></td>')
                   }


                   $("#pojectlist").append(new_tr)
               }

               page_math(data["count"])
           }
        }
    })

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
    $("#page_active li a").click(on_a_cliek)
}
function  on_a_cliek()
{

    var page_id=$(this).attr("page_id");
     now_page=Number(page_id);
    get_list(now_page)
}
