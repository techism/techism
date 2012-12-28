$(function(){
  // masonry: fluent boxes
  $('#contentorganizations').masonry({
    itemSelector : '.organizations'
  });

  // infinite scrolling
  $('#contentorganizations').infinitescroll({
    navSelector  : ".next",  // selector for the paged navigation (it will be hidden)
    nextSelector : ".next",  // selector for the NEXT link (to page 2)
    itemSelector : ".organizations", // selector for all items you'll retrieve
    errorCallback: function(){ $('#infscr-loading').remove() }
    },
    function(newElements){
      // hide new items while they are loading
      var $newElems = $( newElements ).css({ opacity: 0 });
      // ensure that images load before adding to masonry layout
      $newElems.imagesLoaded(function(){
        // show elems now they're ready
        $newElems.animate({ opacity: 1 });
        $('#contentorganizations').masonry('reload');
      });
      // add ajax click handler to more link
      var pagina = newElements[newElements.length - 1];
      // add click handler or remove pagina when there is no next page
      var next = $('.next', pagina);
      if (next.length > 0){
        next.bind('click', moreHandler);
      }
  });

  function moreHandler(e){
    e.preventDefault();

    // remove old pagina
    $(this).parent().parent().parent().remove();

    $(document).trigger('retrieve.infscr');
  }

  // kill scroll binding
  $(window).unbind('.infscr');

  // hook up the manual click guy.
  $('.next').bind('click', moreHandler);

});