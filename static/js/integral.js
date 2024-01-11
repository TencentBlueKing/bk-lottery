/* eslint-disable */
$(function () {
  // var initializeIntegralBox = function() {
  //     var count = $('.integral-box').length;
  //     $('.integral-box').css('width', (100 / count - 1) + '%');
  // };

  // renderDiagram = function() {
  //     $('.integral-diagram').each(function() {
  //         var count = $(this).attr('data-count');
  //         var height = count / 12 * 100;
  //         var marginTop = 100 - height;
  //         $(this).css('height', height + '%');
  //         $(this).css('top', marginTop + '%');
  //     });
  // };

  // initializeIntegralBox();

  // renderDiagram();

  var itemHeight = parseInt($(".integral-list>.integral-item").css("height"));
  var marginBottom = parseInt(
    $(".integral-list>.integral-item").css("marginBottom")
  );
  integrals = {};

  var translate = function (
    id,
    srcIndex,
    destIndex,
    offset,
    newCount,
    game1,
    game2,
    game3
  ) {
    var element = $("#integral-" + id);
    var obj = {
      index: srcIndex + 1,
      count: parseInt(element.find(".integral-count").text()),
      game1: parseInt(element.find(".integral-game1").text()),
      game2: parseInt(element.find(".integral-game2").text()),
      game3: parseInt(element.find(".integral-game3").text()),
    };
    TweenMax.to(obj, 0.7, {
      index: destIndex + 1,
      count: newCount,
      game1: game1,
      game2: game2,
      game3: game3,
      onUpdate: function () {
        var nowCount = Math.floor(obj.count).toString();
        element.find(".integral-count").text(nowCount);

        var nowIndex = Math.floor(obj.index).toString();
        element.find(".integral-index").text(nowIndex);

        var nowGame1 = Math.floor(obj.game1).toString();
        element.find(".integral-game1").text(nowGame1);

        var nowGame2 = Math.floor(obj.game2).toString();
        element.find(".integral-game2").text(nowGame2);

        var nowGame3 = Math.floor(obj.game3).toString();
        element.find(".integral-game3").text(nowGame3);
      },
      ease: Expo.easeOut,
    });
    if (srcIndex === destIndex) {
      return;
    }
    if (destIndex < srcIndex) {
      TweenMax.to(element, 0.25, {
        scale: 1.1,
      });
      TweenMax.to(element, 0.6, {
        y: (itemHeight + marginBottom) * (destIndex - srcIndex + offset),
        delay: 0.1,
      });
      TweenMax.to(element, 0.5, {
        scale: 1,
        delay: 0.6,
        ease: Elastic.easeOut.config(1, 0.3),
      });
    } else {
      TweenMax.to(element, 0.6, {
        y: (itemHeight + marginBottom) * (destIndex - srcIndex + offset),
        ease: Expo.easeOut,
        delay: 0.1,
      });
    }
  };

  var initialize = function () {
    setTimeout(function () {
      TweenMax.staggerTo(
        $(".integral-list>.integral-item"),
        5,
        {
          autoAlpha: 1,
          y: 0,
          ease: Expo.easeOut,
        },
        0.1
      );
    }, 500);

    $(".integral-list>.integral-item").each(function (index, element) {
      var id = $(element).attr("data-id");
      var integral = {
        id: id,
        count: parseInt($(element).find(".integral-count").text()),
        index: index,
        offset: 0,
      };
      integrals[id] = integral;
    });
  };

  $(window).on("resize", function () {
    itemHeight = parseInt($(".integral-list>.integral-item").css("height"));
    marginBottom = parseInt(
      $(".integral-list>.integral-item").css("marginBottom")
    );
  });

  setInterval(function () {
    $.get(
      site_url + "integral/query/",
      {},
      function (data) {
        if (data.result) {
          for (var i = 0; i < data.integrals.length; i++) {
            var id = data.integrals[i].id;
            var count = data.integrals[i].count;
            var game1 = data.integrals[i].game1;
            var game2 = data.integrals[i].game2;
            var game3 = data.integrals[i].game3;
            translate(
              id,
              integrals[id].index,
              i,
              integrals[id].offset,
              count,
              game1,
              game2,
              game3
            );
            integrals[id].offset -= integrals[id].index - i;
            integrals[id].index = i;
          }
        } else {
          toastr.info(data.message);
        }
      },
      "json"
    );
  }, 1000);

  initialize();
});
