function hashchanged(hash){
    if(valid_path(hash)){
        alert(hash);
    }
}
function valid_path(path) {
    var patten = new RegExp(/^#path=(\/\S*)*$/);
    return patten.test(path);
}
