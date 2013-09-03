function hashchanged(hash){
    if(valid_path(hash)){
        alert(hash);
    }
}
function valid_path(path) {
    var patten = new RegExp(/^#path=(\/\S*)*$/);
    return patten.test(path);
}
function ini_oss(user_email){
    options = {
        'user_email':user_email,
        'is_security':true,
        'retry_times':5
    }
    var oss = new oss_api(options);
    return oss;
}