/* =============================================================
    oss.js v1.0.0
    by xiaoh16@gmail.com
 * ============================================================ */
 var current_path = ''
 var current_bucket = ''
if (!String.prototype.format) {
      String.prototype.format = function(args) {
        var s = this;
        for( x in args){
            pattern = new RegExp('{'+x+'}','g')
            s = s.replace(pattern,args[x]);
        }
        return s;
    };
}
function get_file_name(path){
    array = path.split('/');
    if(array[array.length - 1] == "")
        return array[array.length - 2]
    return array[array.length - 1]
}
var parseLIST= function(data){
    $("#filebody").remove();
    $("#filetable").append("<tbody id='filebody'></tbody>")
    root_pattern = new RegExp("^\/[^/\]+\/$",'g');
    if(!root_pattern.test(current_path) && current_path != ''){
        $("#filebody").append("<tr class='fileinfo'><td class='listcheckbox'></td><td class=\"listfilename\"><a onclick=\"hashchanged('#path={path}')\" href=\"#path={path}\">{filename}</a><td class=\"filecontrol\"></td><td class=\"listsize\"></td><td class=\"listdate\"></td></tr>".format({filename:'回到上层',path:current_path.replace(/[^\/]*\/$/,'')}));
    }
    for(var i = 0; i < data.length; i++){
        if(valid_dir(data[i].object_name) && '/'+data[i].bucket_name+'/'+data[i].object_name != current_path){
            $("#filebody").append("<tr class='fileinfo'><td class='listcheckbox'><input type='checkbox' class='checkboxset'/></td><td class=\"listfilename\"><a onclick=\"hashchanged('#path={path}')\" href=\"#path={path}\">{filename}</a><td class=\"filecontrol\"></td><td class=\"listsize\">{size}KB</td><td class=\"listdate\">{date}</td></tr>".format({path:'/'+data[i].bucket_name+'/'+data[i].object_name,filename:get_file_name(data[i].object_name),size:data[i].size,date:data[i].last_modified})
            );
        }
    }
    for(var i = 0; i < data.length; i++){
        if(!valid_dir(data[i].prefix+data[i].object_name)){
            $("#filebody").append("<tr class='fileinfo'><td class='listcheckbox'><input type='checkbox' class='checkboxset'/></td><td class=\"listfilename\"><a  target='new' href='{download_url}'  >{filename}</a><td class=\"filecontrol\"></td><td class=\"listsize\">{size}KB</td><td class=\"listdate\">{date}</td></tr>".format({bucket:data[i].bucket_name,object:data[i].object_name,filename:get_file_name(data[i].object_name),size:data[i].size,date:data[i].last_modified,download_url:data[i].url_with_auth})
            );
        }
    }
}
function valid_dir(object){
    var patten = new RegExp(/^.*\/$/);
    return patten.test(object);
}
var list_object = function(bucket,object){
    $.ajax({
        type:"GET",
        url:"/list_object",
        data:{'bucket':bucket,'object':object}
    }).done(function(data){
        //alert(data);
        parseLIST(eval("("+data+")"));
    });
}
//list the main bucket for user
var list_bucket = function(){
    $.ajax({
        type:"GET",
        url:'/list_bucket'
    }).done(function(data){
        parseLIST(eval("("+data+")"));
    });
}
function hashchanged(hash){
    if(valid_path(hash)){
        parsePATH(hash)
    }
    else if(current_path == ''){
        list_bucket();
    }
    change_file_level();
}
function change_file_level(){
    $("#filelevel").html('');
        $("#filelevel").append("<a href=\"#path=/{current_bucket}/\">全部文件</a>".format({current_bucket:current_bucket}));
    if(current_path != ''){   
    }
    else{
        name_group = current_path.split('/')
        
    }
}
function parsePATH(hash){
    var bucket = hash.match(/^#path=\/[^\/]*/)[0];
    bucket = bucket.replace(/^#path=\//,"");
    current_bucket =bucket
    object = hash.replace(/^#path=\/[^\/]*\//,"")
    var patten = new RegExp(/\/$/);
    if(object == '' || patten.test(object)){
        //end with / this is a direction
        list_object(bucket,object);
        current_path = '/'+bucket+'/'+object
    }
    else{
        //a file, download it
        //download_object(bucket,object);
    }
}
function download_object(bucket,object){
    
    //alert('download bucket '+bucket+' object '+object);
    $.get('/sign_url',{bucket:bucket,object:object,Content_MD5:'',Content_Type:''},function(msg){
        msg = eval("("+msg+")")
        if(msg['permission']!='noPermission'){
        //window.open(msg.url_with_auth)
            $("#download_list").append("<iframe class='download_window' src='{source}'></iframe>".format({source:msg.url_with_auth}))
        }
    });
    //$("#download_list").append("<iframe class='download_window' src='{source}'></iframe>".format({source:'http://www.baidu.com'}))
}
function valid_path(path) {
    var patten = new RegExp(/^#path=(\/\S*)*$/);
    return patten.test(path);
}
