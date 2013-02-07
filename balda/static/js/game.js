!function ($) {
  "use strict";

  var letter = null;
  var letterX = -1;
  var letterY = -1;

  function setLetter(l) {
    letter = l.toUpperCase() || null;
    $("#letter").html(letter || $("#letter").data('default'));
  }

  $("#game form").submit(function() {
    $(this).append($("<input>").attr("type", "hidden").attr("name", "letter").val(letter));
    $(this).append($("<input>").attr("type", "hidden").attr("name", "x").val(letterX));
    $(this).append($("<input>").attr("type", "hidden").attr("name", "y").val(letterY));
  });

  function enableAndFocus(input) {
    $(input).prop('disabled', false);
    $(input).focus();
  }

  var isDown = false;

  $("#grid").mousedown(function() {
    // console.log('down');
    isDown = true;
  });

  $(document).mouseup(function() {
    // console.log('up');
    isDown = false;
  });

  $("#grid td").mouseover(function(){
    // console.log('over');
    if(isDown) {
      // console.log('bim');
      $(this).closest('td').css({background:"#333333"});
    }
  });

  $("#grid td").dblclick(function(e) {
    var input = $(this).find("> input");
    if (!input.is(":focus")) {
      input.prop('disabled', false);
      input.focus();
    }
  });

  $("#grid td > input").focus(function() {
    var input = $(this);
    input.closest('td').addClass('focused');
    setTimeout(function() {
      input.select();
    },1);
  });

  $("#grid td > input").blur(function() {
    $(this).closest('td').removeClass('focused');
    $(this).prop('disabled', true);
  });

  $("#grid td > input").change(function() {
    setLetter(this.value);
    if (this.value) {
      letterX = $(this).data('x');
      letterY = $(this).data('y');
    } else {
      letterX = -1;
      letterY = -1;
    }

    var changedInput = this;
    $("#grid td > input").each(function(idx, element) {
      if (element != changedInput) {
        element.value = '';
      }
    });
  });

  $("#grid td > input").keydown(function(event) {
    if (event.ctrlKey || event.altKey || event.shiftKey || event.metaKey) return;

    var x = $(this).data('x');
    var y = $(this).data('y');

    if (event.keyCode == 39 || event.keyCode == 37) {
      var inputs = $('#grid td > input').filter(function() {
        return $(this).data('y') == y;
      });

      inputs.sort(function(a, b) {
        return $(a).data('x') - $(b).data('x');
      });

      var idx = $.inArray(this, inputs);

      if (event.keyCode == 39) {
        enableAndFocus(inputs[(idx+1+inputs.length)%inputs.length]);
      } else {
        enableAndFocus(inputs[(idx-1+inputs.length)%inputs.length]);
      }
    } else if (event.keyCode == 38 || event.keyCode == 40) {
      var inputs = $('#grid td > input').filter(function() {
        return $(this).data('x') == x;
      });

      inputs.sort(function(a, b) {
        return $(a).data('y') - $(b).data('y');
      });

      var idx = $.inArray(this, inputs)

      if (event.keyCode == 38) {
        enableAndFocus(inputs[(idx-1+inputs.length)%inputs.length]);
      } else {
        enableAndFocus(inputs[(idx+1+inputs.length)%inputs.length]);
      }
    }
  });

}(window.jQuery);
