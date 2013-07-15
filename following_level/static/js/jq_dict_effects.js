jQuery(function($) {

  // Autocompletion
  $('#put_word').typeahead({source: MyGlobal.words});

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
      // Disable the current button
      if( page === current) {
          return;
      } else {
          return "http://localhost:8000/dictionary/show_words/"+page+"/";
      }
    },
    onPageChanged: function(e, oldPage, newPage){
      $('#page-url-alert-content').text(newPage+"/"+options.totalPages/*+'    previous page: '+oldPage*/);
    },
    useBootstrapTooltip: true,
    tooltipTitles: function (type, page, current) {
        //console.log('type: '+type+'| page: '+page+'| current: '+current);
        switch (type) {
        case "first":
            return "Go To First Page <i class='icon-fast-backward icon-white'></i>";
        case "prev":
            return "Go To Previous Page <i class='icon-backward icon-white'></i>";
        case "next":
            return "Go To Next Page <i class='icon-forward icon-white'></i>";
        case "last":
            return "Go To Last Page <i class='icon-fast-forward icon-white'></i>";
        case "page":
            if (page === current) {
                return;
            }
            return "Go to page " + page + " <i class='icon-file icon-white'></i>";
        }
    },
    bootstrapTooltipOptions: {
        html: true,
        placement: 'bottom'
    }
  };
    //console.log(MyGlobal.js_words);
  $('#pagination').bootstrapPaginator(options);
  // Button loading
  $('#load-btn').click(function () {
    var btn = $(this)
    btn.button('loading')
    setTimeout(function () {
        btn.button('reset')
    }, 1000)
  });
//// Inputs should get ready to be checked
//var input = $('input[type="text"]');
//input.wrap('<div class="control-group" />')
//     .parent().css('display', 'inline');
//// Check fields before submitting
//input.focusout(function() {
//    if (!$(this).val()) {
//        $(this).parent().addClass('error');
//    } else {
//        $(this).parent().addClass('success');
//    }
//});

//input.focusin(function() {
//    if ( $(this).parent().hasClass('error') || $(this).parent().hasClass('success') ) {
//        $(this).parent().removeClass('error success');
//    }
//});

//$('#load-btn').click(function() {
//    input.each(function(index, element) {
//        if ($(element).parent().hasClass('error') || !$(element).val()) {
//          if ( !$(element).parent().hasClass('error') ){
//              $(element).parent().addClass('error');
//          }
//          $('#word_dict').submit(function() {
//              return false;
//          });
//        }
//    });
//});
});
