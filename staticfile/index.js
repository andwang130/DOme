



var tr="  <tr>\n" +
    "        <td class=\"text-left vertical-middle\">\n" +
    "            <input type=\"checkbox\" class=\"check_item\" name=\"uid[]\" value=\"3294\">\n" +
    "        </td>\n" +
    "        <td class=\"text-left vertical-middle\">{编号}</td>\n" +
    "        <td class=\"text-left vertical-middle\"><span class=\"color-dark\">{TITLE}</span>\n" +
    "            <div class=\"flexs\">\n" +
    "                <label>\n" +
    "                                        <div class=\"switch ng-scope switchOn\"\n" +
    "                         \"></div>\n" +
    "                                    </label><span>&nbsp;&nbsp;</span>\n" +
    "                                {是否开始}\n" +
    "                            </div>\n" +
    "        </td>\n" +
    "        <td class=\"text-left vertical-middle\">\n" +
    "            <a href=\"javascript:;\" data-clipboard-action='copy' class=\"js-clip color-default\"\n" +
    "               data-clipboard-text=\"{复制活动链接}\">复制链接</a><br/><a href=\"javascript:;\" class='js-clip' data-clipboard-text=\"{copyuuid}\">复制ID</a>" +
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
    "               href=\"./addpoje.html?action=update&uuid={setuuid}&page={page}&key={key}&start={start}&end={end}&times={times}&findend={findend}\"\n" +
    "               title=\"编辑\"><i class=\"fa fa-edit\"></i> 编辑</a><br/>\n" +
    "            <a class=\"color-default we7-margin-right\" rel=\"tooltip\" href=\"#\"\n" +
    "               onclick=\"drop_confirm('您确定要删除吗?删除不可恢复。', '/poject?action=delete&uuid={delteuuid}');\"\n" +
    "               title=\"删除\"><i class=\"fa fa-times\"></i> 删除</a>\n" +
    "            <br/>\n" +
    "            <a class=\"color-default we7-margin-right\" href='#' rel=\"tooltip\" onclick=\"copy('{copypoject}')\"\n"  +
    "               title=\"复制活动\"><i class=\"fa fa-copy\"></i> 复制活动</a>\n" +
    "        </td>\n" +
    "    </tr>";

var key='';
var start='';
var end='';
var times="";
var findend="";
$(document).ready(
    function () {
        var page=GetRequest("page")
         if(page.page)
         {
             now_page=page.page
         }
       var  new_key=GetRequest("key")
         if(new_key.key){
             key=new_key.key
         }
        var new_end=GetRequest("end")
        if(new_end.end)
        {
            end=new_end.end
        }
        var new_times=GetRequest("times")
        if(new_times.times)
        {
            times=new_times.times
        }
        var new_findend=GetRequest("findend")
        if(new_findend.findend){
            findend=new_findend.findend
        }
        for(i=0;i<7;i++)
        {
            var newtimes=fun_date(i)
            var html="<div class=\"input-group pull-left col-sm-1\">\n" +
                "\t\t\t\t\t<a class=\"btn btn-gray timeget\">"+newtimes+"</a>\n" +
                "\t\t\t\t</div>"
            $("#timelist").append(html)
        }

        $(".timeget").click(times_get)
        get_list(now_page);
        $(".btn-default").click(set_key)
    }
);

function set_key() {

    key=$("#keyword").val();
    start=$("#start").val()
    end=$("#end").val()
    times=""
    get_list(1)
}
function drop_confirm(mages,url)
{

    if(confirm(mages))
    {
         $.ajax({
        url:url,
        type: 'POST',
        success: function (arg) {
            var data = JSON.parse(arg);
            $("#pojectlist").html("");
            if (data["code"] == 0)
            {
                get_list(now_page)
                 $.sendSuccessToTop('删除成功', 3000, function() {
                 console.log('sendSuccessToTop closed');
             });
            }

        }
    })
    }
}
function copyuuid() {


}
function copy(uuid) {
    var data={"action":"copy","uuid":uuid}
      $.ajax({
        url:'/poject',
        type: 'POST',
        data:data,
        success: function (arg) {
            var data = JSON.parse(arg);
            $("#pojectlist").html("");
            if (data["code"] == 0)
            {
                  get_list(now_page)
                 $.sendSuccessToTop('复制成功', 3000, function() {
                 console.log('sendSuccessToTop closed');
             });
            }

        }
    })
}
function get_list(page) {
    now_page=page;
    data={"action":"get_list","page":page,"start":start,"end":end,"times":times,"findend":findend};
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
            var data=JSON.parse(arg);
            $("#pojectlist").html("");
           if(data["code"]==0)
           {
                var datalist=data["data"];
               for(var i=0;i<datalist.length;i++)
               {
                   //"http://www.nkwwcj.com/wx/auoth?uuid="+datalist[i]["uuid"]

                   var new_tr=tr.replace(/{编号}/,i).replace(/{TITLE}/,datalist[i]["titile"]).replace(/{开始时间}/,datalist[i]["tiemstatr"])
                       .replace(/{结束时间}/,datalist[i]["timeend"]).replace(/{参与人数}/,datalist[i]["participants"]).replace(/{投票数量}/,datalist[i]["votes"])
                       .replace(/{浏览量}/,datalist[i]["volume"]).replace(/{分享量}/,datalist[i]["Share"]).replace(/{uuid}/,datalist[i]["uuid"]).replace(/{copyuuid}/,datalist[i]["uuid"]).replace(/{setuuid}/,datalist[i]["uuid"]).replace(/{copypoject}/,datalist[i]["uuid"])
                       .replace(/{ordel_uuid}/,datalist[i]["uuid"]).replace(/{delteuuid}/,datalist[i]["uuid"])
                       .replace(/{复制活动链接}/,"http://www.nkwwcj.com/wx/wxindex?uuid="+datalist[i]["uuid"]).replace(/{礼物数量}/,datalist[i]["liwunum"]).
                   replace(/{key}/,key).replace(/{start}/,start).replace(/{end}/,end).replace(/{times}/,times).replace(/{findend}/,findend).replace(/{page}/,page);
                   var nowtime=Date.parse(new Date());
                   if(getTimes(datalist[i]["tiemstatr"])<nowtime&&getTimes(datalist[i]["timeend"])>nowtime)
                   {
                       new_tr = new_tr.replace(/{是否开始}/,'<span class="label label-success">开始</span>')
                   }
                   else if(nowtime>getTimes(datalist[i]["timeend"]))
                   {
                        new_tr = new_tr.replace(/{是否开始}/,'<span class="label label-default">已结束</span>')
                   }
                   else {
                          new_tr = new_tr.replace(/{是否开始}/,'<span class="label label-warning">未开始</span>')
                   }
                   $("#pojectlist").append(new_tr)

               }
             var clipboard=new Clipboard('.js-clip');
               clipboard.on("success",function (e) {
                    $.sendSuccessToTop('复制成功', 3000, function() {
                 console.log('sendSuccessToTop closed');
             });
               });
               page_math(data["count"])
           }
           else if(data["code"]==-110){
               location.href="/login.html"
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

// function setClipboard() {
//         var t=""
//          t = $(this).attr("data-url")
//         window.clipboardData.setData("Text",t);
//         alert("成功复制")
//     }
function fun_date(AddDayCount){
    var dd = new Date();
    dd.setDate(dd.getDate()+AddDayCount);//获取AddDayCount天后的日期
    var y = dd.getFullYear();
    var m = (dd.getMonth()+1)<10?"0"+(dd.getMonth()+1):(dd.getMonth()+1);//获取当前月份的日期，不足10补0
    var d = dd.getDate()<10?"0"+dd.getDate():dd.getDate();//获取当前几号，不足10补0
    return y+"-"+m+"-"+d;
}
function times_get() {
     key="";
     start=""
     end=""
    findend=""
    times=$(this).text()
    get_list(1)
}
function get_end(e) {

    var text= $(e).text()
    if(text=="已经结束的"){
        findend="end"
    }
    else if(text=="全部"){
        findend=""
    }
    else if(text=="已经开始的"){
        findend="start"
    }
  get_list(1)


}