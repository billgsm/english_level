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

  $('table#sortTable tbody tr').hover(function () {
          $(this).find('.word_settings').removeClass('non_visible');
  },
  function () {
          $(this).find('.word_settings').addClass('non_visible');
  });

  // Table sortable setup
  $("table#sortTable").tablesorter({ sortList: [[1,0]] });

  // Carousel setup
  $('.carousel').carousel({
    interval: 5000
  })


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

  // Model: modify word: do not save
  // and go to the page word
  $('#not_save').click(function(e) {
      e.preventDefault();
      window.location = get_absolute_url;
      });

});
