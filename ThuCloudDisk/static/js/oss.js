/* =============================================================
    oss_js_sdk.js v1.0.0
    by xiaoh16@gmail.com
 * ============================================================ */
var get_authorization_header = function(method,bucket,object,content_md5,callback){
        $.ajax({
            type:'GET',
            url:'/get_authorization_header',
            dataType: "json",
            data:{method:method,bucket:bucket,object:object,content_md5:content_md5},
        }).done(function(msg){
            callback(msg);
        })
    }
var get_object_list = function(bucket,object){
        callback = function(msg){
        source = 'http://'+bucket+'.oss.aliyuncs.com/'+object+'?Expires='+msg.Expires+'&Signature='+escape(msg.Signature)+'&OSSAccessKeyId='+msg.OSSAccessKeyId;
        $.get(source,function(data){
              alert( "Data Loaded: " + data );
        });
        $.ajax({
            type:"GET",
            url:source,
            headers: {'X-Alt-Referer': 'http://'+bucket+'.oss.aliyuncs.com'},
            success:function(data){
              alert( "Data Loaded: " + data );
            }
        })
        };
        get_authorization_header('GET',bucket,object,'',callback)
    }
var get_host_list = function(){
    $.ajax({
        type:'GET',
        url:'/get_bucket_name'
    }).done(function(msg){
        this_user_bucket = msg;
        get_object_list(this_user_bucket,'')
    });
}