var uuid=""
$(document).ready(function () {
    uuid=GetRequest("uuid")
    $("#files").on("input propertychange",files_oninpit)
})

function files_oninpit() {
        var fiels= $("#files").prop('files');
        console.log(fiels)
        var formFile = new FormData();
        for(var i=0;i<fiels.length;i++)
        {

            console.log(fiels[i].size)
            if((fiels[i].size/1024/1024)>10)
            {
                alert("文件过大");
                return
            }
            filepath=fiels[i].name;
            var extStart=filepath.lastIndexOf(".");
            var ext=filepath.substring(extStart,filepath.length).toUpperCase();
            if(ext!=".BMP"&&ext!=".PNG"&&ext!=".GIF"&&ext!=".JPG"&&ext!=".JPEG")
            {

                alert("图片限于png,gif,jpeg,jpg格式");
                return
            }
             formFile.append(fiels[i].name, fiels[i]); //加入文件对象
        }

        $.ajax({
        url:'/uploadfile',
        type: 'POST',
        data:formFile,
        processData: false,//用于对data参数进行序列化处理 这里必须false
        contentType: false, //必须
        success: function (arg)
        {
            arg=JSON.parse(arg)

            if(arg["code"]=="0")
            {
                var data=arg["data"]
                var namelist=[]
                for(var i=0;i<data.length;i++)
                {
                    namelist.push({"name":data[i]["odlname"].split(".")[0],"avatar":data[i]["path"]});
                }
                if(namelist&&uuid.uuid) {
                    var new_data = {"namelist":JSON.stringify(namelist), "action": "create_list","uuid":uuid.uuid}
                    create_list(new_data)
                }

            }
        }

        })
}
function create_list(data) {
      $.ajax({
             url: '/Tpuser',
             type: 'POST',
             data: data,
             success: function (arg) {
                 arg = JSON.parse(arg)

                     window.href="/TPUser.html?uuid="+uuid.uuid
             }
         }
     )
}
