/* this is the API for Swift
* author:XiaoHe
* email:xiaoh16@gmail.com*/

var Swift={
    createNew:function(username,userpass,host,port){
        var swift = {}
        swift.username = username;
        swift.userpass = userpass;
        swift.host = host;
        swift.port = port;
        swift.host_url = host+':'+port;
        swift.getToken = function(){
            $.ajax({
                method:'GET',
                url:swift.host_url
                /*headers:{
                    'X-Storage-User': swift.username,
                    'X-Storage-Pass': swift.userpass
                }*/
            }).done(function(data){
                alert(data)
            }).fail(function( jqXHR, textStatus ) {
                alert( "Request failed: " + textStatus );
            });
        }
        return swift;
    }

}