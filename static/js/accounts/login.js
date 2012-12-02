$(document).ready(function(){

  $("#openid").hide(); 

  $('a.openid')
    .live('click', function() {
    	$("#openid").slideToggle(300);
    });

});
