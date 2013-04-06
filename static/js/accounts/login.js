$(document).ready(function(){

  $("#openid").hide(); 

  $('a.openid')
    .live('click', function() {
    	$("#openid").slideToggle(300);
    });

});

$(function () {
    $('#browserid').click(function (e) {
        e.preventDefault();
        var self = $(this);
        navigator.id.get(function (assertion) {
            if (assertion) {
                self.parent('form')
                        .find('input[type=hidden]')
                            .attr('value', assertion)
                            .end()
                        .submit();
            } else {
                alert('Some error occurred');
            }
        });
    });
});
