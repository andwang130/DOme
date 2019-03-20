var t_in_click=undefined;
var action;
var  autoid;
$(document).ready(
    function () {
        $("#submit").click(sudbit_click);
         action=GetRequest("action");
         autoid=GetRequest("autoid");
        if(action.action=="update"&&autoid.autoid)
        {
            get_info(autoid.autoid);
        }
    }
);

function  get_info(autoid) {

    data={"autoid":autoid,"action":"info"};
         $.ajax({
             url: '/auto_click',
             type: 'POST',
             data: data,
             success: function (arg) {
                 arg = JSON.parse(arg);

                 var data=arg["data"];
                 if (arg["code"] == 0) {
                     console.log(arg);
                     $("#uuid").val(data["uuid"]);
                     $("#tiems").val(data["times"]);
                     $("#start").val(data["start"]);
                     $("#end").val(data["end"]);
                     $("input[name='status']:radio[value={value}]".replace(/{value}/,data['status'])).attr('checked','true');
                 }

             }
         }
     )

}
function sudbit_click() {

    var data={};
    data["action"]=action.action;
    if(data["action"]=="update")
    {
        data["autoid"]=autoid.autoid
    }
     data["uuid"]= $("#uuid").val();
     data["times"]=$("#tiems").val();
     data["start"]=$("#start").val();
     data["end"]=$("#end").val();
     data["status"]=$('input[name="status"]:checked').val();
     $.ajax({
             url: '/auto_click',
             type: 'POST',
             data: data,
             success: function (arg) {

                     location.href="/auto_click.html"


             }
         }
     )

}


