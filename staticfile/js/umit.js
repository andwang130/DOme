
function get_cookie(name) {
    var arr,reg=new RegExp("(^| )"+name+"=([^;]*)(;|$)");
    if(arr=document.cookie.match(reg))
        return unescape(arr[2]);
    else
        return null;
}
function GetRequest() {
    var url = location.search; //获取url中"?"符后的字串
    var theRequest = {};
    if (url.indexOf("?") != -1) {
        var str = url.substr(1);
        strs = str.split("&");
        for(var i = 0; i < strs.length; i ++) {
            theRequest[strs[i].split("=")[0]]=unescape(strs[i].split("=")[1]);
        }
    }
    return theRequest;
}
function getLocalTime(nS) {
    return new Date(parseInt(nS) * 1000).toLocaleString().substr(0,17)}
function getTimes (strtime) {


    var date = new Date(strtime.replace(/-/g, '/'));


    return time1 = date.getTime();
}
function getNowTimes() {
    var timestamp =Date.parse(new Date());
    return timestamp
}