/* =============================================================
    oss_js_sdk.js v1.0.0
    by xiaoh16@gmail.com
 * ============================================================ */
!function ($) {
    oss_api = function (options) {
        this.init(options);
    }
    oss_api.prototype = {
        constructor:oss_api,
        
        host:null,
        access_key_id:null,
        user_email:null,
        is_security:null,
        retry_times:null,
        
        init:function(options){
            this.user_email = options.user_email;
            this.is_security = options.is_security;
            this.retry_times=options.retry_times;
            this.get_host_access_key(this.user_email);
        },
        get_host_access_key:function(user_email){
            $.ajax(url:'/auth/get_host_access_key',
            data:{'user_email':user_email},
            dataType: "json",
            async:false
            )
            .done(function( json ) {
              this.host = json.host;
              this.access_key_id = json.access_key_id;
            })
            .fail(function( jqxhr, textStatus, error ) {
              var err = textStatus + ', ' + error;
              console.log( "get host access key Failed: " + err);
            });
        },
        /*
            list all files in the objectgroup of the host, if this is a valid folder, return
            the list, otherwise return false
        */
        get_object_list:function(){
            $.ajax({
                type: "GET",
                url: this.host,
                dataType: "xml",
                beforesend:setheaders(),
                success: xmlParser(xml)
               });
            setheaders = function(xhr){
                signature = 
                xhr.setRequestHeader('Authorization', 'OSS'+this.access_key_id);
            }
            object_list_Parser = function (xml){
                alert(xml);
            }
            },
        get_authorization_header:function(){
        }
            
            ;
        }
        
    }
}(window.jQuery);