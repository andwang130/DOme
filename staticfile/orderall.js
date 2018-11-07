
var start=3
$(document).ready(
    function () {



        get_ordel(1)
        $(" .btn-primary").click(primary_click)


    }
)
function primary_click() {

   var text_=$(this).text()
  if(text_=="已付款订单")
  {
      start=1;
      $(this).text("全部订单")
  }
  else
  {     start=3
       $(this).text("已付款订单")
  }
 get_ordel(1)


}
function get_ordel(page)
{
    now_page=page
    data = {"action": "all_ordel","page":page,"start":start}
    $.ajax({
        url: '/order',
        type: 'POST',
        data: data,
        success: function (arg) {
            arg = JSON.parse(arg)
            data=arg["data"]
            if (arg["code"] == "0") {
                body_init(data)
                page_math(arg["count"])
            }
        }
    })
}

function body_init(data) {

    $("#body").html('')
    order=["orderid","userid","uuid","money","liwu","num","votenum","times","ip","start"]
    for(var i=0;i<data.length;i++)
    {
        var id_td='<td class="text-left vertical-middle">'+data[i]["orderid"]+'</td>'
        var name_td='<td class="text-left vertical-middle">'+data[i]["username"]+'</td>'
        var num_td='<td class="text-left vertical-middle"><p><span class="label label-primary">'+data[i]["money"]+'</span>/<span class="label label-info">'+data[i]["num"]+'</span>/<span class="label label-warning">'+data[i]["votenum"]+'</span></p></td>'
        var ip_time_td='<td class="text-left vertical-middle">'+getLocalTime(data[i]["times"])+'<p>'+data[i]["ip"]+'</p></td>'
        var start_td;
        var money_td;
        if(data[i]["start"]==1)
        {
          start_td='<td class="text-left vertical-middle"><p><span class="label label-success">已付款</span></p></td>'
        money_td='<td class="text-left vertical-middle"><p><span class="label label-danger">'+data[i]["money"]+'元</span></p></td>'

        }
        else
        {
            start_td='<td class="text-left vertical-middle"><p><span class="label label-default">未付款</span></p></td>'
                    money_td='<td class="text-left vertical-middle"><p><span class="label label-default">'+data[i]["money"]+'元</span></p></td>'


        }

        var html="<tr>"+id_td+name_td+money_td+num_td+ip_time_td+start_td+"</tr>>"
        $("#body").append(html)
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
    get_ordel(Number(page_id));
}