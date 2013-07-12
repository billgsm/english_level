jQuery(function($) {
  // Table sortable setup
  $("table#sortTable").tablesorter({ sortList: [[1,0]] });
  // Modal setup
/*          $(".modal .close").bind("click", function(){
      $(".modal-backdrop").fadeOut();
      return false;
  });*/

  // Carousel setup
  $('.carousel').carousel({
    interval: 5000
  })

  // pagination setup
  var options = {
    currentPage: MyGlobal.current_page,
    totalPages: MyGlobal.num_pages,
    numberOfPages: 5,
    pageUrl: function(type, page, current){
      return "http://localhost:8000/dictionary/show_words/"+page+"/";
    }
  };
  $('#pagination').bootstrapPaginator(options);
});
