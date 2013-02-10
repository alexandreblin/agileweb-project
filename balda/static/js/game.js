!function ($) {
  "use strict";

  var channel = new goog.appengine.Channel(token);
  var socket = channel.open();
  socket.onmessage = function onMessage(message) {
    if (message.data == 'reload') {
      document.location.reload(true);
    }
  };

  if (playerId != currentPlayer) {
    return;
  }

  var word = [];

  $("#game form").submit(function() {
    $(this).append($("<input>").attr("type", "hidden").attr("name", "word").val(JSON.stringify(word)));
  });

  function getCellLetter(td) {
    var x = $(td).data('x');
    var y = $(td).data('y');

    if (word.length > 0) {
      var lastLetter = word[word.length - 1];
      if (Math.abs(lastLetter.x - x) > 1 || Math.abs(lastLetter.y - y) > 1) {
        return false;
      }
    }

    var input = $(td).find('> input');
    var letter;
    var isAddedLetter;
    if (input.length > 0) {
      letter = input.val();
      isAddedLetter = true;
    } else if ($(td).html()) {
      letter = $(td).html().trim();
      isAddedLetter = false;
    }

    if (!letter) {
      return false;
    }

    return {'letter': letter.toLowerCase(), 'x': x, 'y': y, 'isAddedLetter': isAddedLetter};
  }

  function addLetterToWord(letter) {
    for (var i in word) {
      var l = word[i];
      if (l.x == letter.x && l.y == letter.y) {
        return;
      }
    }
    
    if (word.length === 0) {
      $('#word').html('');
    }

    word.push(letter);
    
    $("#word").append(letter.letter.toUpperCase());
  }

  var isDown = false;

  $("#grid td").mousedown(function(e) {
    isDown = true;
    word = [];
    
    $('#word').html('None');
    $('#grid input').blur();
    $('#grid td').removeClass('selected');
    $('#grid').css('cursor','crosshair');
    $(this).trigger('mouseover');

    e.originalEvent.preventDefault();
  });

  $(document).mouseup(function() {
    isDown = false;
    $('#grid').css('cursor','auto');
  });

  $("#grid td").mousemove(function(e){
    if (!isDown || $(this).closest('td').hasClass('selected')) return;

    if (word.length > 0) {
      // we select the letter only if we are in the center of the cell
      // without this, we can't select diagonally because we must pass through the corner of another cell
      var x = e.pageX - this.offsetLeft;
      var y = e.pageY - this.offsetTop;
      var padding = 10;

      if (!(x > padding && x < this.offsetWidth - padding && y > padding && y < this.offsetHeight - padding)) {
        return;
      }
    }

    var letter = getCellLetter(this);
    if(letter) {
      $(this).closest('td').addClass('selected');

      addLetterToWord(letter);
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
    var changedInput = this;
    $("#grid td > input").each(function(idx, element) {
      if (element != changedInput) {
        element.value = '';
      }
    });
  });

}(window.jQuery);
