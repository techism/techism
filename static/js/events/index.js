$(document).ready(function(){

  $(".detail").hide(); 

  // clicks for touch interface
  $('article.vevent > header')
    .live('click', function() {
      $(this)
        .parent()
        .children(".detail")
        .slideToggle(300, renderEventDetailMap);
    });

});
