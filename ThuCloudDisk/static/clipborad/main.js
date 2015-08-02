// main.js
var client = new ZeroClipboard( $("#target-to-copy"), {
  moviePath: "/static/clipborad/ZeroClipboard.swf"
} );


  client.on( "load", function(clientTarget)
{
    $('#flash-loaded').fadeIn();

    clientTarget.on( "complete", function(clientTarget, args) {
        clientTarget.setText( args.text );
        $('#target-to-copy-text').fadeIn();
    } );
} );