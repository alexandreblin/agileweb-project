!function ($) {
  "use strict";
  
  $("#gamegrid td").click(function() {
    var input = $(this).find("> input");
    if (!input.is(":focus")) {
      input.focus();
    }
  });

  $("#gamegrid td > input").focus(function() {
    var input = $(this);
    input.closest('td').addClass('focused');
    setTimeout(function() {
      input.select();
    },1);
  });

  $("#gamegrid td > input").blur(function() {
    $(this).closest('td').removeClass('focused');
  });

  $("#gamegrid td > input").keydown(function(event) {
    if (event.ctrlKey || event.altKey || event.shiftKey || event.metaKey) return;

    var x = $(this).data('x');
    var y = $(this).data('y');

    if (event.keyCode == 39 || event.keyCode == 37) {
      var inputs = $('#gamegrid td > input').filter(function() {
        return $(this).data('y') == y;
      });

      inputs.sort(function(a, b) {
        return $(a).data('x') - $(b).data('x');
      });

      var idx = $.inArray(this, inputs)

      if (event.keyCode == 39) {
        inputs[(idx+1+inputs.length)%inputs.length].focus();
      } else {
        inputs[(idx-1+inputs.length)%inputs.length].focus();
      }
    } else if (event.keyCode == 38 || event.keyCode == 40) {
      var inputs = $('#gamegrid td > input').filter(function() {
        return $(this).data('x') == x;
      });

      inputs.sort(function(a, b) {
        return $(a).data('y') - $(b).data('y');
      });

      var idx = $.inArray(this, inputs)

      if (event.keyCode == 38) {
        inputs[(idx-1+inputs.length)%inputs.length].focus();
      } else {
        inputs[(idx+1+inputs.length)%inputs.length].focus();
      }
    }
  });

}(window.jQuery);
