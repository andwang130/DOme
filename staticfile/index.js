



var tr="  <tr>\n" +
    "        <td class=\"text-left vertical-middle\">\n" +
    "            <input type=\"checkbox\" class=\"check_item\" name=\"uid[]\" value=\"3294\">\n" +
    "        </td>\n" +
    "        <td class=\"text-left vertical-middle\">{编号}</td>\n" +
    "        <td class=\"text-left vertical-middle\"><span class=\"color-dark\">{TITLE}</span>\n" +
    "            <div class=\"flexs\">\n" +
    "                <label>\n" +
    "                                        <div class=\"switch ng-scope switchOn\"\n" +
    "                         onclick=\"drop_confirm('您确定要暂停活动吗？', './index.php?c=site&a=entry&ty=setstatus&rid=3294&status=0&do=otherset&m=tyzm_diamondvote');\"></div>\n" +
    "                                    </label><span>&nbsp;&nbsp;</span>\n" +
    "                                <span class=\"label label-warning\">未开始</span>\n" +
    "                            </div>\n" +
    "        </td>\n" +
    "        <td class=\"text-left vertical-middle\">\n" +
    "            <a href=\"javascript:;\" class=\"js-clip color-default\"\n" +
    "               data-url=\"{复制活动链接}\">复制活动链接</a><br/>\n" +
    "            <a href=\"javascript:;\"  onclick=\"qr_code(this)\" class=\"color-default\" data-url=\"http://jadl8.zhaojingl.com/app/./index.php?i=25&c=entry&rid=3294&do=index&m=tyzm_diamondvote\" data-toggle=\"modal\" data-target=\"#myModal\" target=\"myFrameName\">活动二维码</a>\n" +
    "        </td>\n" +
    "        <td class=\"text-left vertical-middle\">\n" +
    "            <div class=\"\">\n" +
    "                <a href=\"javascript:;\" class=\"color-dark\">开始：{开始时间}                   <br/>\n" +
    "                    结束：{结束时间}</a>\n" +
    "            </div>\n" +
    "        </td>\n" +
    "        <td class=\"text-left vertical-middle\">\n" +
    "            <p class=\"color-gray\">参与人数：<span class=\"label label-primary\">{参与人数}</span></p>\n" +
    "            <p class=\"color-gray\">投票数量：<span class=\"label label-default\">{投票数量}</span></p>\n" +
    "        </td>\n" +
    "        <td class=\"text-left vertical-middle\">\n" +
    "            <p class=\"color-gray\">礼物数量：<span class=\"label label-danger \">{礼物数量}元</span></p>\n" +
    "            <p class=\"color-gray\">浏 览 量：<span class=\"label label-success\">{浏览量}</span></p>\n" +
    "        </td>\n" +
    "        <td class=\"text-left vertical-middle\">\n" +
    "            <a href=\"./TPUser.html?uuid={uuid}\"\n" +
    "               class=\"color-default we7-margin-right\" rel=\"tooltip\" title=\"投票管理\"><i class=\"fa fa-cog\"></i> 选手管理</a><br/>\n" +
    "            <a href=\"./orderlist.html?uuid={ordel_uuid}\"\n"+
    "               class=\"color-default we7-margin-right\" rel=\"tooltip\" title=\"礼物订单\"><i class=\"fa fa-archive\"></i>\n" +
    "                礼物订单</a><br/>\n" +
    "                    </td>\n" +
    "        <td class=\"text-left vertical-middle\">\n" +
    "            <a class=\"color-default we7-margin-right\" rel=\"tooltip\"\n" +
    "               href=\"./addpoje.html?action=update&uuid={setuuid}\"\n" +
    "               title=\"编辑\"><i class=\"fa fa-edit\"></i> 编辑</a><br/>\n" +
    "            <a class=\"color-default we7-margin-right\" rel=\"tooltip\" href=\"#\"\n" +
    "               onclick=\"drop_confirm('您确定要删除吗?删除不可恢复。', '/poject?action=delete&uuid={delteuuid}');\"\n" +
    "               title=\"删除\"><i class=\"fa fa-times\"></i> 删除</a>\n" +
    "            <br/>\n" +
    "            <a class=\"color-default we7-margin-right\" rel=\"tooltip\"\n" +
    "               href=\"/poject?action=copy&uuid={copyuuid}\"\n" +
    "               title=\"复制活动\"><i class=\"fa fa-copy\"></i> 复制活动</a>\n" +
    "        </td>\n" +
    "    </tr>"
$(document).ready(
    function () {

        get_list(1)
        $(".btn-default").click(set_key)
    }
)
var key;
function set_key() {

    key=$("#keyword").val()
    get_list(1)
}
function drop_confirm(mages,url)
{

    if(confirm(mages))
    {
        window.location=url
    }
}
function get_list(page) {
    now_page=page;
    data={"action":"get_list","page":page}
    if(key)
    {
        data["key"]=key
    }
     $.ajax({
        url:'/poject',
        type: 'POST',
        data:data,
        success: function (arg)
        {
            var data=JSON.parse(arg)
            $("#pojectlist").html("")
           if(data["code"]==0)
           {
                var datalist=data["data"]
               for(var i=0;i<datalist.length;i++)
               {

                   var new_tr=tr.replace(/{编号}/,i).replace(/{TITLE}/,datalist[i]["titile"]).replace(/{开始时间}/,datalist[i]["tiemstatr"])
                       .replace(/{结束时间}/,datalist[i]["timeend"]).replace(/{参与人数}/,datalist[i]["participants"]).replace(/{投票数量}/,datalist[i]["votes"])
                       .replace(/{浏览量}/,datalist[i]["volume"]).replace(/{分享量}/,datalist[i]["Share"]).replace(/{uuid}/,datalist[i]["uuid"]).replace(/{copyuuid}/,datalist[i]["uuid"]).replace(/{setuuid}/,datalist[i]["uuid"])
                       .replace(/{ordel_uuid}/,datalist[i]["uuid"]).replace(/{delteuuid}/,datalist[i]["uuid"]).replace(/{复制活动链接}/,"http://carzy.wang/wx/auoth?uuid="+datalist[i]["uuid"])
                   $("#pojectlist").append(new_tr)

               }
               $(".js-clip").click(setClipboard)
               page_math(data["count"])
           }
        }
    })

}
var now_page=1;
function page_math(count) {
   var page_end=Math.ceil(count/20);

   var THML=""
   var page_html="<li><a href='javacript:get_list({PAGE})'>{PAGE}</a></li>";

   if(page_end>10)
   {
       var new_page_end=page_end
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
               THML +="<li><a page_id='{pageid}' href='#'>{PAGE}</a></li>".replace(/{PAGE}/,i).replace(/{pageid}/,i);;
           }
       }
   }
   else
   {
        for(var i=1;i<page_end+1;i++)
       {
            console.log(page_end)
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

    var page_id=$(this).attr("page_id")
    console.log(page_id);
}

function setClipboard() {

        var t = $(this).attr("data-url")
        window.clipboardData.setData("Text",t.toString());
        alert("成功复制")
    }