
var uuid="";
var sort_type="createtime";
var key="";
var status="";
var now_page=1;
$(document).ready(
    function () {
        uuid=GetRequest("uuid");
        var urlpage=GetRequest("page");
        if(urlpage.page)
        {
            now_page=urlpage.page
        }
        $("#addbth").attr("href",$("#addbth").attr("href")+uuid.uuid);
        $("#addthlist").attr("href",$("#addthlist").attr("href")+uuid.uuid);
        $("#fa-search").click(set_Key);
        url_init();
        get_user(1)
    }
);
function set_Key() {
    key=$("#keyword").val();
    get_user(1)
}
function url_init() {

      $("#order").attr("href","/orderlist.html?uuid="+uuid.uuid);
        $("#add").attr("href","/addTpuser.html?action=create&uuid="+uuid.uuid);
        $("#tpindex").attr("href","/TPUser.html?uuid="+uuid.uuid);
        $("#getcsv").attr("href",'/tpuserscv?uuid='+uuid.uuid)
}
function  get_user(page) {
    if(uuid.uuid) {
        data = {"action": "get_list", "uuid": uuid.uuid,"page":page,"sorttype":sort_type,"status":status};
       if(key)
       {
           data["key"]=key
       }
        $.ajax({
                url: '/Tpuser',
                type: 'POST',
                data: data,
                success: function (arg) {
                    arg = JSON.parse(arg);
                    if (arg["code"] == "0") {
                        var data=arg["data"];
                        $("#userlist").html("");
                        for(var i=0;i<data.length;i++)
                        {
                            //var datatime=new Date(parseInt(data[i]["createtime"]+) * 1000).toLocaleString().replace(/:\d{1,2}$/,' ');
                            var tr=" <tr name='"+data[i]["userid"]+"'>\n" +
                                "                \t<input type=\"hidden\"  value=\"262592\" >\n" +
                                "                    <td  class=\"text-left vertical-middle\">"+data[i]["index"]+"</td>\n" +
                                "\t\t\t\t\t<td  class=\"text-left vertical-middle\">"+data[i]["name"]+"<span class=\"label label-{success}\">{是否审核}</span></td>\n" +
                                "\t\t\t\t\t<td class=\"text-left vertical-middle\"><span class=\"label label-info\">"+data[i]["vheat"]+"</span></td>\n" +
                                "\t\t\t\t\t<td  class=\"text-left vertical-middle _ticket\"><span class=\"label label-primary _ticket_lable\">"+data[i]["votenum"]+"</span> <button onclick='add_votedate(this,\""+data[i]["userid"]+"\")'>+</button><span style='display: none'><input style='width: 60px' type='number' name='votenum'><span></td><!-- 移入移出事件  -->\n" +
                                "\t\t\t\t\t<td  class=\"text-left vertical-middle\"><span class=\"label label-danger\">"+data[i]["liwu"]+"</span></td>\n" +
                                "\t\t\t\t\t<td class=\"text-left vertical-middle\">"+getLocalTime(data[i]["createtime"])+"</td>\n" +
                                "                    <td class=\"text-left vertical-middle\">\n" +
                                "                    "+ data[i]["phone"]+"</td>\n" +
                                "                    <td  class=\"text-left vertical-middle\">\n" +
                                "\t\t\t\t\t<p>\n" +
                                "\t\t\t\t\t<a class=\"color-default we7-margin-right\" title=\"投票数据\" href=\"/votedata.html?userid="+data[i]["userid"]+"&uuid="+uuid.uuid+"\" ><i class=\"fa fa-star-o\"></i> 投票数据</a>\n" +
                                "\t\t\t\t\t<a class=\"color-default we7-margin-right\" title=\"钻石数据\" href=\"./usorder.html?userid="+data[i]["userid"]+"&uuid="+uuid.uuid+"\" ><i class=\"fa fa-codepen\"></i> 礼物订单</a>\n" +
                                "\t\t\t\t\t<a class=\"color-default we7-margin-right\" title=\"编辑\" href=\"/addTpuser.html?action=update&uuid="+uuid.uuid+"&Userid="+data[i]["userid"]+"&page="+now_page+"\" ><i class=\"fa fa-edit\"></i> 编辑</a>\n" +
                                "\t\t\t\t\t<a class=\"color-default we7-margin-right\" rel=\"tooltip\" href=\"#\" onclick=\"drop_confirm('您确定要删除吗?删除不可恢复，同时删除所有相关数据！','"+data[i]["userid"]+"');\" title=\"删除\"><i class=\"fa fa-times\"></i> 删除</a></p>\n" +
                                "                    </td>\n" +
                                "                </tr>";
                            if(data[i]["status"]==0)
                            {
                            tr=tr.replace(/{success}/,"success").replace(/{是否审核}/,"已审核")
                            }
                            else if(data[i]["status"]==1)
                            {
                                tr=tr.replace(/{success}/,"default").replace(/{是否审核}/,"未审核")
                            }
                            $("#userlist").append(tr)

                        }
                         page_math(arg["count"]);
                    }
                }
            }
        )
    }
}
function drop_confirm(mages,userid) {

    data = {"userid": userid, "action": "delete"};

    if (confirm(mages)) {
        $.ajax({
            url: '/Tpuser',
            type: 'POST',
            data: data,
            success: function (arg) {
                data = JSON.parse(arg);
                if (data["code"] == 0) {

                    location.reload()
                }
                 else if(data["code"]==-110){
               location.href="/login.html"
           }
            }
        })
    }
}
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
    get_user(Number(page_id));
    console.log(page_id);
}

function sort_func(type)
{
    sort_type=type;
    get_user(1)
}
function add_votedate(e,userid) {

    $(e).next().css("display","block")
     $(e).next().find('input[name="votenum"]').focus()
    $(e).next().find('input[name="votenum"]').keyup(function () {

        if(event.keyCode == 13){
              $(e).next().find('input[name="votenum"]').blur()
        }
    })
     $(e).next().find('input[name="votenum"]').on("blur",function () {
         var num= $(e).next().find('input[name="votenum"]').val()
         $(e).next().find('input[name="votenum"]').val("")
           $(e).next().css("display","none")
             data = {"userid": userid, "action": "add_votedate","votenum":num};
         $.ajax({
            url: '/Tpuser',
            type: 'POST',
            data: data,
            success: function (arg) {
                data = JSON.parse(arg);
                if (data["code"] == 0) {
                  get_user(now_page)
                }
            }
        })

     })
}
function get_Unaudited(e) {
    var text= $(e).text()
    if(text=="未审核"){
        status="1"
         $(e).text("全部")
    }
    else if(text=="全部"){
        status=""
        $(e).text("未审核")
    }
    get_user(1)
}