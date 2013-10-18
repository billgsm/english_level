jQuery(function($) {
  /******************** Useful var ********************/
  var current_url = $(location).attr('href');
  /****************************************************/
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
            'word': rm_word,
          },
          dataType: 'text',
          headers: {
            'X-CSRFToken': $.trim($.cookie('csrftoken')),
          },
          success: function(data) {
            // Remove all word's tracks and update autocompletion source
            current_delete.parent().parent().parent().parent().remove();
            MyGlobal.words.splice(MyGlobal.words.indexOf(rm_word), 1);
            $('#put_word').typeahead({source: MyGlobal.words});
          },
          error: function() {
            console.log($(this).text());
          }
        });
      }
    });
  });

  // User may want to hide some words because
  // he doesn't need to review them anymore
  $('li.hide_word').click(function () {
    var current_delete = $(this);
    hide_word = $.trim(current_delete.parent().parent().parent().prev().text())
    bootbox.confirm('Hide this word "'+hide_word+'", are you sure ?', 'No', 'Yes, I\'m sure', function(result) {
      if (result) {
        $.ajax('/dictionary/hide_words/',
        {
          type: 'POST',
  //timeout: 3000,
          data: {
            'word': hide_word,
          },
          dataType: 'text',
          headers: {
            'X-CSRFToken': $.trim($.cookie('csrftoken')),
          },
          success: function(data) {
            // Remove all word's tracks and update autocompletion source
            current_delete.parent().parent().parent().parent().remove();
            MyGlobal.words.splice(MyGlobal.words.indexOf(hide_word), 1);
            $('#put_word').typeahead({source: MyGlobal.words});
          },
          error: function() {
            console.log($(this).text());
          }
        });
      }
    });
  });

  // Autocompletion
  if ( typeof(MyGlobal) != 'undefined') {
    $('#put_word').typeahead({source: MyGlobal.words});
  }

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
  // ****************************************
  if (typeof(MyGlobal) != "undefined") {
    var last_page = MyGlobal.last_page
        current_page = MyGlobal.current_page;
    if(current_page !== last_page) {
      if(!(current_url.indexOf("?page=") >= 0)) {
        new_url = current_url + "?page=" + (current_page + 1);
      } else {
        new_url = current_url.replace(/page=.*/g, 'page=' + (current_page + 1));
      }
      $('ul.pager li.next').removeClass('disabled')
                           .children('a').attr('href', new_url);
    } else {
      $('ul.pager li.next').children('a').click(function(e){
        e.preventDefault();
      });
    }
    if(current_page !== 1) {
      new_url = current_url.replace(/page=.*/g, 'page=' + (current_page - 1));
      $('ul.pager li.previous').removeClass('disabled')
                               .children('a').attr('href', new_url);
    } else {
      $('ul.pager li.previous').children('a').click(function(e){
        e.preventDefault();
      });
    }
  }

//  if ( typeof(MyGlobal) != 'undefined') {
//    var options = {
//      currentPage: MyGlobal.current_page,
//      totalPages: MyGlobal.num_pages,
//      numberOfPages: 5,
//      pageUrl: function(type, page, current){
//        // Disable the current button
//        if( page === current) {
//            return;
//        } else {
//            return "http://bilousite.alwaysdata.net/dictionary/show_words/"+page+"/";
//        }
//      },
//      onPageChanged: function(e, oldPage, newPage){
//        $('#page-url-alert-content').text(newPage+"/"+options.totalPages/*+'    previous page: '+oldPage*/);
//      },
//      useBootstrapTooltip: true,
//      tooltipTitles: function (type, page, current) {
//          switch (type) {
//          case "first":
//              return "Go To First Page <i class='icon-fast-backward icon-white'></i>";
//          case "prev":
//              return "Go To Previous Page <i class='icon-backward icon-white'></i>";
//          case "next":
//              return "Go To Next Page <i class='icon-forward icon-white'></i>";
//          case "last":
//              return "Go To Last Page <i class='icon-fast-forward icon-white'></i>";
//          case "page":
//              if (page === current) {
//                  return;
//              }
//              return "Go to page " + page + " <i class='icon-file icon-white'></i>";
//          }
//      },
//      bootstrapTooltipOptions: {
//          html: true,
//          placement: 'bottom'
//      }
//    };
//    $('.pagination').bootstrapPaginator(options);
//  }
  // ****************************************
  // Choose the number of rows to show on one single page
  $("#row_number select").change(function(e){
    select_url = current_url + "?&row=" + $(this).val();
    console.log(select_url);
    $(this).closest('form').submit();
  });

  // Button loading
  $('#load-btn').click(function () {
    var btn = $(this)
    btn.button('loading')
    setTimeout(function () {
        btn.button('reset')
    }, 1000)
  });

/**********Make focus on the last hitted title in the nav-bar**********/
  $('div.nav-collapse.collapse > ul.nav > li').click(function() {
    var current_li = this;
    $(this).parent().children().each(function(index, element) {
      if(element!==current_li) {
        $(element).removeClass('active');
      } else {
        $(element).addClass('active');
      }
    });
  });

/* popover when clicking on the word */
  $('div.span2.word_box').popover(
    {
      placement: 'bottom',
      trigger: 'click',
      html: true,
      title: 'Definiton',
      animation: true,
    }
  );
/* tooltip when clicking on the word */
  $('div.span2.word_box').tooltip(
    {
      placement: 'top',
      trigger: 'hover focus',
      title: 'mon titre',
      delay: {
        show: 0,
        hide: 200
          },
    }
  );

  /*generic list: show and hide details*/
  $('h3.toggle-show').next('ul').hide();
  $('h3.toggle-show').click(function(e) {
    $(this).next('ul').toggle(400);
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
