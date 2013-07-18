jQuery(function($) {

  // take into account user's preferences on displayed words
  $('li.delete_word').click(function () {
    var current_delete = $(this);
    rm_word = $.trim(current_delete.parent().parent().parent().prev().text())
    bootbox.confirm('Removing this word "'+rm_word+'", are you sure ?', 'No', 'Yes, I\'m sure', function(result) {
      if (result) {
        $.ajax('/dictionary/remove_words/',
        {
          type: 'POST',
  //timeout: 3000,
          data: {
            'word_id': $.trim(current_delete.parent().parent().parent().prev().prev().text()),
            'word': rm_word,
          },
          dataType: 'text',
          headers: {
            'X-CSRFToken': $.trim($.cookie('csrftoken')),
          },
          success: function(data) {
            current_delete.parent().parent().parent().parent().remove();
            console.log(data);
          },
          error: function() {
            console.log($(this).text());
          }
        });
      }
    });
  });

  // Autocompletion
  $('#put_word').typeahead({source: MyGlobal.words});

  // Visibility of the settings button over each word
  //var can_hide = false;
  //var can_display = true;
  //$('body').click(function(){console.log('c_h: '+can_hide+'|c_d: '+can_display)});
  $('table#sortTable tbody tr').hover(function () {
      //if ( can_display ) {
          $(this).find('.word_settings').removeClass('non_visible');
      //}
      //$(this).find('.word_settings').click(function () {
      //    console.log('here');
      //});
  },
  function () {
      //if ( can_hide ) {
          $(this).find('.word_settings').addClass('non_visible');
      //}
  });

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
