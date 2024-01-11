/* eslint-disable */
$(function () {
  // var setAwardBoxWidth = function() {
  //     var $box = $('.award-container .award-box');
  //     var height = $box.height();
  //     $box.css('width', height + 'px');
  // };
  // setAwardBoxWidth();

  // ------------------预加载部分 start------------------
  // 加载资源路径 使用 preload.js 来实现预加载 用到的每个资源都应该写上
  // var staticImgUrl = static_url + 'avatars/';
  var staticImgUrl = "";
  var loader = document.querySelector(".loader");
  var preloadItemMap = {};
  var isLoading = false;
  var ErrorItemMap = {};
  var resourceList = rtxs.map(function (item) {
    return { src: staticImgUrl + item.avatar, id: item.name, type: "image" };
  });

  function startPreload() {
    if (localStorage.getItem("isPreload")) {
      $(".loading").hide();
      isLoading = true;
      return false;
    } else {
      $(".loading").show();
    }
    preload = new createjs.LoadQueue();
    preload.setMaxConnections(100);
    // preload.installPlugin(createjs.Sound); //加载音频文件需要调用
    preload.addEventListener("progress", handleFileProgress);
    preload.addEventListener("complete", loadComplete);
    preload.addEventListener("error", loadError);
    preload.loadManifest(resourceList);
  }

  var ErrorItem = {};

  //处理加载错误
  function loadError(evt) {
    ErrorItem[evt.data.id] = evt.data.src;
    localStorage.setItem("ErrorItem", JSON.stringify(ErrorItem));
    // alert("加载出错！");
  }

  //已加载完毕进度
  function handleFileProgress(event) {
    loader.innerHTML = ((preload.progress * 100) | 0) + "%";
  }

  //全部资源加载完毕
  function loadComplete(event) {
    // init();
    ErrorItemMap = JSON.parse(localStorage.getItem("ErrorItem"));
    if (ErrorItemMap === null) {
      ErrorItemMap = {};
    }
    localStorage.setItem("isPreload", true);
    $(".loading").hide();
    preload.getItems().forEach(function (item) {
      if (!preloadItemMap[item.item.id]) {
        // preloadItemMap[item.item.id] = item.result
        preloadItemMap[item.item.id] = item.item.src;
      }
    });
    isLoading = true;
  }

  // 加载
  startPreload();
  ErrorItemMap = JSON.parse(localStorage.getItem("ErrorItem"));
  if (ErrorItemMap === null) {
    ErrorItemMap = {};
  }
  // ------------------预加载部分 end------------------

  var background = document.getElementById("background");
  var audio_play = document.getElementById("audio_play");
  var canvas = document.getElementById("space");
  canvas.width = $(window).width();
  canvas.height = $(window).height();
  var context = canvas.getContext("2d");
  context.drawImage(background, 0, 0, windowWidth, windowHeight);
  context.textAlign = "center";
  context.fillStyle = "white";

  var windowWidth = canvas.width;
  var windowHeight = canvas.height;
  var avatarShowPercent = 0.4;
  var avatarFocalLength = 10;
  var winnerFocalLength = 7;
  var sizeFactor = 100;
  if (windowWidth > 2000) {
    sizeFactor = 200;
    winnerFocalLength = 8;
  }
  var speed = 1.5;
  var winnerTick = 11; // 抽中中奖者时，中奖者将在n个tick后到达
  // var winnerSize = 400;
  var zRange = 400;
  var globalAlpha = 0.6;
  var clickInterval = 1000;
  if (award_number > 5) {
    clickInterval = 200;
    winnerTick = 6;
    winnerFocalLength = 2;
  }
  var max_avatar_n = Math.min(1000, rtxs.length); // 动画显示头像的最大个数

  var is_reward = false;
  var isStopButtonShow = true;
  var isPausing = false;
  var intervalId;
  var allIntervalId;
  var shockIntervalId;

  var avatars = [];
  var winners = [];
  var fontSizes = [
    1, 2, 4, 6, 8, 10, 12, 14, 16, 18, 20, 22, 24, 26, 28, 30, 32, 34, 36, 38,
    40,
  ];

  var Avatar = function (name, name_zh, url, x, y, z, focalLength) {
    this.image = document.createElement("img");
    // if (ErrorItemMap[name]) {
    //     this.image.src = site_url + "static/avatars/default.png";
    // } else {
    //     this.image.src = url;
    // }
    this.image.src = url;
    this.image.onerror = function () {
      this.src = site_url + "static/avatars/default.png";
    };
    this.name = name;
    this.name_zh = name_zh;
    this.x = x || Math.random() * windowWidth - windowWidth / 2;
    this.y = y || Math.random() * windowHeight - windowHeight / 2;
    this.z = z || Math.random() * zRange - zRange / 2;
    this.focalLength =
      focalLength || avatarFocalLength || Math.random() * 10 + 5;
    this.isWinner = false;
    this.display = Math.random() > avatarShowPercent ? false : true;
    this.showName = "";
    this.tick;

    // 随机色
    // var color = "#" + Math.floor(Math.random() * 0xffffff).toString(16).padEnd(6, "0");

    this.render = function () {
      var scale = this.focalLength / (this.focalLength + this.z);
      var size = Math.max(1, Math.floor(scale * sizeFactor));
      var halfSize = size / 2;
      var x2d = this.x * scale + windowWidth / 2;
      var y2d = this.y * scale + windowHeight / 2;
      if (this.isWinner) {
        var lastAlpha = context.globalAlpha;
        context.globalAlpha = 1.0;
        context.drawImage(
          this.image,
          x2d - halfSize,
          y2d - halfSize,
          size,
          size
        );
        this.drawNameBySize(size, x2d, y2d);
        this.tick -= 1;
        if (this.tick == 0) {
          clearInterval(intervalId);
          this.isWinner = false;
          isStopButtonShow = false;
          context.globalAlpha = 0;

          if (allIntervalId != undefined) {
            if (winners.length === award_number) {
              allIntervalId = setTimeout(function () {
                $("#comfirmButton").trigger("click");
              }, clickInterval);
            } else {
              allIntervalId = setTimeout(function () {
                $("#nextButton").trigger("click");
              }, clickInterval);
            }
          }
        } else {
          context.globalAlpha = lastAlpha - globalAlpha / winnerTick;
          if (context.globalAlpha < 0 || context.globalAlpha > globalAlpha) {
            context.globalAlpha = 0;
          }
        }
      } else {
        context.drawImage(
          this.image,
          x2d - halfSize,
          y2d - halfSize,
          size,
          size
        );
      }
      this.nextTick();
    };

    this.nextTick = function () {
      this.z -= speed;
      if (this.z < -this.focalLength) {
        this.z += zRange;
        this.x = Math.random() * windowWidth - windowWidth / 2;
        this.y = Math.random() * windowHeight - windowHeight / 2;
        this.display = Math.random() > avatarShowPercent ? false : true;
      }
    };

    this.drawNameBySize = function (size, x2d, y2d) {
      var fontSize = 1;
      context.font = fontSize + "px 微软雅黑";
      var measure = context.measureText(this.showName);
      while (size - measure.width > 1) {
        fontSize += 0.5;
        context.font = fontSize + "px 微软雅黑";
        measure = context.measureText(this.showName);
      }
      context.fillText(this.showName, x2d, y2d + size / 2 + fontSize);
    };
  };

  var initAvatar = function () {
    //        for (var i = 0; i < rtxs.length; i++) {
    if (avatar_head_portrait) {
      var avatarHeadPortrait = eval(avatar_head_portrait);
      for (var i = 0; i < max_avatar_n; i++) {
        avatars.push(
          new Avatar(
            rtxs[i].name,
            rtxs[i].name_zh,
            "/static/avatars/" +
              avatarHeadPortrait[Math.trunc(i % avatarHeadPortrait.length)]
          )
        );
      }
    } else {
      for (var i = 0; i < max_avatar_n; i++) {
        avatars.push(
          new Avatar(
            rtxs[i].name,
            rtxs[i].name_zh,
            "/static/avatars/default.png"
          )
        );
      }
    }

    avatars.sort(function (a, b) {
      return b.z - a.z;
    });
  };

  var renderAll = function () {
    context.save();
    context.globalAlpha = 1.0;
    context.drawImage(background, 0, 0, windowWidth, windowHeight);
    context.restore();
    for (var i = 0; i < avatars.length; i++) {
      if (avatars[i].display) {
        avatars[i].render();
      } else {
        avatars[i].nextTick();
      }
    }
  };

  var start = function () {
    if (is_reward) {
      context.globalAlpha = globalAlpha;
    }
    renderAll();
    return setInterval(function () {
      renderAll();
    }, 50);
  };

  // ------------------------展示中奖人员名单和风格--------------------------
  var layout = null;
  var winnerPageSize = null;
  if (award_number > 1000) {
    layout = 5;
    winnerPageSize = 150;
  } else if (award_number <= 1000 && award_number > 60) {
    layout = 4;
    winnerPageSize = 100;
  } else if (award_number <= 60 && award_number > 20) {
    layout = 3;
    winnerPageSize = 60;
  } else if (award_number <= 20 && award_number > 10) {
    layout = 2;
    winnerPageSize = 20;
  } else {
    layout = 1;
    winnerPageSize = 10;
  }
  var layoutMap = {
    1: {
      width: 278,
      height: 222,
      font_size: 24,
      line_height: 40,
      margin: "5px 20px",
    },
    2: {
      width: 232,
      height: 130,
      font_size: 20,
      line_height: 34,
      margin: "0 30px",
    },
    3: {
      width: 150,
      height: 80,
      font_size: 16,
      line_height: 28,
      margin: "8px 16px",
    },
    4: {
      width: 136,
      height: 58,
      font_size: 13,
      line_height: 22,
      margin: "10px 14px",
    },
    5: {
      width: 100,
      height: 55,
      font_size: 12,
      line_height: 20,
      margin: "8px 12px",
    },
  };
  var layoutConfig = layout ? layoutMap[layout] : layoutMap[1];

  var showWinners = function (winners) {
    if (winners.length == 0) return; // 中奖人员已经展示过了

    if (winners.length != award_number) {
      //修改了中奖者人数，添加删除dom元素
      var winner_box = $(".winners-boxs").children().first();
      if (winners.length > award_number) {
        for (var i = 0; i < winners.length - award_number; i++) {
          winner_box.after(winner_box.clone(true));
        }
      } else {
        for (var i = 0; i < award_number - winners.length; i++) {
          winner_box.siblings().first().remove();
        }
      }
      award_number = winners.length;
    }

    var effect_vul = effect;
    var effects = ["default", "fade", "cube", "coverflow", "flip", "cards"];

    //var interval = 0;
    //var showPages = Math.ceil(winners.length/winner_nums);
    if (-1 === effects.indexOf(effect_vul)) showWinnerLists(winners);
    else {
      ///////////////////////////轮播效果开始//////////////////////////////////
      var init = {
        stopTime: 3,
      };
      var effectMap = {
        fade: {
          effect: "fade",
          fadeEffect: {
            crossFade: true,
          },
        },
        cube: {
          effect: "cube",
          cubeEffect: {
            slideShadows: true,
            shadow: true,
            shadowOffset: 100,
            shadowScale: 0.6,
          },
        },
        coverflow: {
          effect: "coverflow",
          coverflowEffect: {
            rotate: 30,
            stretch: 10,
            depth: 60,
            modifier: 2,
            slideShadows: true,
          },
        },
        flip: {
          effect: "flip",
          flipEffect: {
            slideShadows: true,
            limitRotation: true,
          },
        },
        cards: {
          effect: "cards",
          cardsEffect: {
            slideShadows: true,
            //transformEl:'.text',
          },
        },
      };
      var mySwiper;
      var swiperSlides;
      var showPages = Math.ceil(award_number / winnerPageSize);

      // 构造中奖者页面
      var swiper_wrapper = "";
      for (let i = 0; i < showPages; i++) {
        swiper_wrapper += `<div class="swiper-slide"></div>`;
      }
      var innerHtml =
        `<div class="swiper-wrapper">` + swiper_wrapper + "</div>";
      $(".winners-boxs").html(innerHtml);

      var headPortraitHTML =
        "head_portrait" === head_portrait_style
          ? '<img src="' +
            static_url +
            '/avatars/default.png" alt=".." class="avatar">'
          : "";
      var awardHTML =
        award_takeinscene === "True"
          ? `<img src="${static_url}/images/refresh.png" class="redraw">`
          : "";

      // 内容填充
      function generateSwiper() {
        // 翻页风格
        var curSetting = {
          direction: "horizontal",
          loop: true,
          autoplay: true,
          delay: init.stopTime * 1000,
        };
        if ("true" === is_end_play)
          curSetting = {
            direction: "horizontal",
            delay: init.stopTime * 1000,
            on: {
              slideChangeTransitionStart: function () {
                if (this.activeIndex + 1 === showPages) {
                  this.autoplay.stop();
                }
              },
            },
          };
        const params = Object.assign(curSetting, effectMap[effect_vul]);

        mySwiper = new Swiper(".winners-boxs", params);
        swiperSlides = document.querySelectorAll(".swiper-slide");
        var winnerFirstHTML = "";
        Array.from(swiperSlides).forEach((item, index) => {
          var step = 0;
          var winnerHTML = "";
          var winner = winners.shift(0);
          while (step < winnerPageSize && winner) {
            if (winner != undefined) {
              if ("non_head_portrait" === head_portrait_style) {
                var lineString =
                  '<div class="line1"></div><div class="line2"></div><div class="line3"></div>';
                winnerHTML += `<div class="winner-box" style="width:${
                  layoutConfig.width
                }px; height: ${layoutConfig.height}px;">
                                    <div class="line-common line-top">
                                      ${lineString}
                                    </div>
                                    <div class="line-common line-bottom">
                                      ${lineString}
                                    </div>
                                    <div class="line-common line-right" style="width: ${
                                      layoutConfig.height - 4
                                    }px;right: -${
                  (layoutConfig.height + 2) / 2
                }px; top: ${(layoutConfig.height - 2) / 2}px">
                                      ${lineString}
                                    </div>
                                    <div class="line-common line-left" style="width: ${
                                      layoutConfig.height - 4
                                    }px;left: -${
                  (layoutConfig.height + 2) / 2
                }px; top: ${(layoutConfig.height - 2) / 2}px">
                                      ${lineString}
                                    </div>
                                   <div class="content" style="background-color: ${
                                     version_config.background_color
                                   };" >
                                        <div style="font-size: ${
                                          layoutConfig.font_size
                                        }px; color: ${
                  version_config.p_color
                }; font-family: ${font_family};"> 
                                            <div class="name-en" style="line-height: ${
                                              layoutConfig.line_height
                                            }px">${winner.name}</div>
                                            <div class="name-zh" style="line-height: ${
                                              layoutConfig.line_height
                                            }px">${winner.chinese_name}</div>
                                            ${headPortraitHTML}
                                            ${awardHTML}
                                        </div>
                                   </div>
                                </div>`;
              } else if ("head_portrait" === head_portrait_style) {
                winnerHTML += `<div class="winner-box" style="width:${layoutConfig.width}px; height: ${layoutConfig.height}px; background-color:  ${version_config.background_color}; font-size: 13px;">
                                    <div class="winner-avatar" style="width:${layoutConfig.width}px; height: ${layoutConfig.height}px;">
                                        <div class="profile_bg"></div>
                                            ${headPortraitHTML}
                                            ${awardHTML}
                                    <p class="rtx-name" style="font-family:${font_family}; color: ${version_config.p_color}; height:28px; 
                                    line-height: 28px;font-size: 16px;">${winner.name}</p>
                                    <p class="rtx-chinese-name" style="font-family:${font_family}; color: ${version_config.p_color}; height:28px; 
                                    line-height: 28px;font-size: 20px;text-overflow: clip">${winner.chinese_name}</p>
                                    </div>
                                </div>`;
              }
            }
            switch (index) {
              case 0:
                winnerFirstHTML = winnerHTML;
                break;
            }
            step += 1;
            if (step >= winnerPageSize) {
              break;
            }
            winner = winners.shift(0);
          }
          if (winnerHTML) item.innerHTML = winnerHTML;
          else item.innerHTML = winnerFirstHTML;
          item.setAttribute("data-swiper-autoplay", params.delay);
        });
      }

      generateSwiper();

      // 是否轮播
      if ("true" === is_play && 1 != showPages) mySwiper.autoplay.start();
      else mySwiper.autoplay.stop();

      // 控制上下、左右
      var pageturning_vul = pageturning;
      let pageturnings = ["vertical", "horizontal"];
      if (!pageturnings.includes(pageturning_vul))
        pageturning_vul = "horizontal";
      mySwiper.changeDirection(pageturning_vul);

      const curTime = time_presentation * 1000;
      init.stopTime = time_interval;
      swiperSlides.forEach((item) => {
        item.setAttribute("data-swiper-autoplay", curTime);
      });

      ///////////////////////////轮播效果结束//////////////////////////////////
    }
  };

  var currentPage = 0;
  var showWinnerLists = function (winners, showWinnerInterval) {
    if (showWinnerInterval != undefined) {
      console.log("showWinnerInterval", showWinnerInterval);
      clearInterval(showWinnerInterval);
    }
    currentPage += 1;
    var showPages = Math.ceil(award_number / winner_nums);
    $(".winner-box").each(function (index) {
      var winner = winners.shift(0);
      if (winner != undefined) {
        for (let i = 0; i < rtxs.length; i++) {
          if (winner.name == rtxs[i]["name"]) {
            avatar_path = rtxs[i]["avatar"];
            // var tempAvatarNode = $(this).children().first();
            var image_dom = $(this).find("img.avatar").first();
            if (ErrorItemMap[rtxs[i]["name"]]) {
              image_dom.attr("src", static_url + "/avatars/default.png");
            } else {
              image_dom.attr("src", avatar_path);
            }
            $(this).css("opacity", "1");
            $(this).show();
          }
        }
        $(this).find(".rtx-name").html(winner.name);
        $(this)
          .find(".rtx-chinese-name")
          .html("（" + winner.chinese_name + "）");
        //var thisDom = $(this);
      } else {
        clearInterval(showWinnerInterval);
        $(this).hide();
      }
      if (index === winner_nums) {
        if (currentPage < showPages) {
          // 如果当前非最后一页， 需要隐藏
          flashScreenHideWinners(winners);
        }
        return false;
      }
    });
  };

  var hideWinners = function () {
    $(".winner-box").each(function (index) {
      $(this).css("opacity", "1");
      if (index === winner_nums) {
        return false;
      }
    });
  };

  //TODO 轮播方式
  var flashScreenHideWinners = function (winners) {
    var controlDisplay = setInterval(function () {
      // 定时 1s 之后hide()
      //  $('.winner-box').hide();
      $(".winner-box").each(function (index) {
        $(this).css("opacity", "0");
      });
      var showWinnerInterval = setInterval(function () {
        showWinnerLists(winners, showWinnerInterval);
      }, time_interval * 500);

      clearInterval(controlDisplay);
    }, time_presentation * 2000);
  };

  //结束时隐藏背景并展示最后的背景
  var endBghide = function () {
    // $('#lotteryModal').modal('hide');
    $("#background-img").hide();
    $("#background-img-end").show();
    $("#lucky-title").hide();
    $("#play-button").hide();
    $("#award-img").hide();
    $(".top-div").show();
  };

  // 48区间风格(原始默认)
  var styleFor48 = function (width, height) {
    var maxNum = 48;
    if (award_number <= maxNum) {
      let wh = 193 / 143;
      // 每行个数
      // 最大行数 12
      // 最小行数 5  5：最大5个  6 最大6个  7  最大14个 8 最大16个 9 最大 18个 10 最大 30个  11 最大 33个  12 最大48个
      let lineNum = 0;
      if (award_number > 0 && award_number <= 5) {
        lineNum = 5;
      } else if (award_number > 5 && award_number <= 6) {
        lineNum = 6;
      } else if (award_number > 6 && award_number <= 14) {
        lineNum = 7;
      } else if (award_number > 14 && award_number <= 16) {
        lineNum = 8;
      } else if (award_number > 16 && award_number <= 18) {
        lineNum = 9;
      } else if (award_number > 18 && award_number <= 30) {
        lineNum = 10;
      } else if (award_number > 30 && award_number <= 33) {
        lineNum = 11;
      } else if (award_number > 33 && award_number <= 48) {
        lineNum = 12;
      }
      // 每个方块的宽度
      let boxWidth = width / lineNum - 28;
      // 每个方块的高度
      let boxHeight = boxWidth * wh;
      $(".winners-boxs .profile_bg").css("box-sizing", "content-box");
      $(".winners-boxs .profile_bg").css("border", "2px solid #ddb775");
      $(".winners-boxs")
        .find(".winner-box, img.profile_bg, .winner-avatar")
        .each(function (index, value) {
          $(value).css("width", boxWidth + "px");
          $(value).css("height", boxHeight + "px");
          $(value).css(
            "font-size",
            boxHeight / 30 < 5 ? 5 : boxHeight / 30 + "px"
          );
        });
    } else {
      let boxWidth = 147;
      let boxHeight = 78;
      let scale = 1.7;
      $(".winners-boxs .winner-box").css("margin", "7px");
      $(".winners-boxs .profile_bg").attr(
        "src",
        static_url + "/images/bg2/profile_bg.png"
      );
      $(".winners-boxs .avatar").css("display", "none");
      $(".winners-boxs .rtx-name").css("height", "30%");
      $(".winners-boxs .rtx-name").css("bottom", "50%");
      $(".winners-boxs .rtx-chinese-name").css("height", "30%");
      $(".winners-boxs .rtx-chinese-name").css("bottom", "20%");
      $(".winners-boxs")
        .find(".winner-box, img.profile_bg, .winner-avatar")
        .each(function (index, value) {
          $(value).css("width", boxWidth / scale + "px");
          $(value).css("height", boxHeight / scale + "px");
          $(value).css("font-size", 5 + "px");
        });
      // if (isautoScrollSee) {
      //     isautoScrollSee = false;
      //     autoScrollSee();
      // }
    }
  };

  // 纯无头像风格
  var styleForNonHeadPortrait = function (width, height) {
    let boxWidth = width / winner_line_nums - 28;
    let boxHeight = height / Math.ceil(winner_nums / winner_line_nums);
    let fontSize = 5;
    if (winner_nums > 150) fontSize = 5;
    else if (100 < winner_nums && winner_nums <= 150) fontSize = 6;
    else if (48 < winner_nums && winner_nums <= 100) fontSize = 7;
    else if (winner_nums <= 48) fontSize = 8;
    if (boxHeight < 80 || boxHeight > 100) boxHeight = 70;

    $(".winners-boxs .winner-box").css("margin", `${layoutConfig.margin}`);
    $(".winners-boxs .profile_bg").attr(
      "src",
      static_url + "/images/bg2/profile_bg.png"
    );
    $(".winners-boxs .avatar").css("display", "none");
    $(".winners-boxs .rtx-name").css("height", "30%");
    $(".winners-boxs .rtx-name").css("bottom", "50%");
    $(".winners-boxs .rtx-chinese-name").css("height", "30%");
    $(".winners-boxs .rtx-chinese-name").css("bottom", "20%");
    $(".winners-boxs")
      .find(".winner-box, img.profile_bg, .winner-avatar")
      .each(function (index, value) {
        // $(value).css('width', boxWidth + 'px');
        // $(value).css('min-width',  '100px');
        // $(value).css('height', boxHeight + 'px');
        // $(value).css('max-height', 70 + 'px');
        $(value).css("font-size", fontSize + "px");
      });
  };

  // 纯头像+中奖者名称风格
  var styleForHeadPortrait = function (width, height) {
    $(".winners-boxs")
      .find("img.avatar")
      .each(function (index, value) {
        $(value).css("margin-top", "5%");
      });
  };

  // 根据中奖人数改变中奖人卡片尺寸
  var autoWinnerSize = function () {
    var width = parseInt($(".winners-boxs").css("width"));
    var height = parseInt($(".winners-boxs").css("height"));
    var len = Math.floor($(".winners-boxs").children().length);
    // var maxRowCount = windowWidth > 4000 ? 16 : 5;
    // var minRowCount = windowWidth > 4000 ? 6 : 3;
    // var eachWidth, eachHeight, rows, eachMarginBottom;

    if ("non_head_portrait" === head_portrait_style) {
      styleForNonHeadPortrait(width, height);
    } else if ("head_portrait" === head_portrait_style) {
      styleForHeadPortrait(width, height);
    } else {
      styleFor48(width, height);
    }
    redrawAward();
  };
  // ------------------------展示中奖人员名单和风格结束--------------------------

  var isautoScrollSee = true;
  var autoScrollSee = function () {
    let timeOut = 1000;
    let timeStep = 10;
    let timer = null;
    let curHeight = 0;
    let timeHeight = 1;
    let winnersBoxs = $(".winners-boxs");
    let winnersBoxsHeight = $(".winners-boxs")[0].scrollHeight;
    setTimeout(function () {
      timer = setInterval(function () {
        if (winnersBoxsHeight - curHeight <= timeHeight) {
          winnersBoxs.scrollTop(0);
          clearInterval(timer);
        }
        curHeight = curHeight + timeHeight;
        winnersBoxs.scrollTop(curHeight);
      }, timeStep);
    }, timeOut);
  };
  var adjustWidthFowWinner = function () {
    autoWinnerSize();
  };

  var getWinnerFromServer = function () {
    if (!is_reward) {
      return;
    }
    is_reward = false;
    $.post(
      site_url + "lottery/award/" + award_id + "/winner/",
      function (data) {
        if (data["result"]) {
          for (var i = 0; i < avatars.length; i++) {
            if (avatars[i].name === data["rtx"].name) {
              winners.push(data["rtx"]);
              avatars[i].isWinner = true;
              avatars[i].x = 0;
              avatars[i].y = 0;
              avatars[i].z = winnerFocalLength;
              avatars[i].tick = winnerTick;
              avatars[i].showName =
                data["rtx"].name + " (" + data["rtx"].chinese_name + ")";
              avatars[i].display = true;
              break;
            }
          }
        } else {
          toastr.info(data["message"]);
        }
      },
      "json"
    );
  };

  // 去掉输入框、style奖品title
  var stylePrize = function () {
    $("#prize_bg p, #prize_bg").addClass("drew");
  };

  var pauseAudio = function () {
    if (need_pause_audio === "on") {
      audio_play.pause(); //暂停音乐
    } else {
      console.log("Pause audio if forbidden");
    }
  };

  var getAllWinnersFromServer = function () {
    endBghide();

    $.ajax({
        url: site_url + "lottery/award/" + award_id + "/winners/",
        data: {"is_reward": is_reward, absent_winner: absent_winner},
        dataType: "json",
        type: "POST",
        success: function (data) {
        if (data["result"]) {
          pauseAudio();
          winners = data["winners"];
          setTimeout(function () {
            // TOOD 为何这里要做一次确认？？
            $("#comfirmButton").trigger("click");
          }, 0);
          stylePrize();
          $("#background-img").attr(
            "src",
            static_url + "/images/animation_bg_0.jpg"
          );
          // 设定下次抽奖就为重新抽奖了
          is_reward = true

        } else {
          toastr.info(data["message"]);
        }
      },
        error: function () {
          toastr.error(JSON.parse(data.responseText)["message"]);
        },
      });
  };

  var awardFadeOut = function () {
    $(".award-box").addClass("award-fadeOut");
    //        $('.modal-button').css('opacity', '0.8');
  };

  var shockImage = function (image, x, y, size) {
    var xs = [0, 0, -2, 2, 0, 0, -2, 2];
    var ys = [2, -2, 0, 0, 2, -2, 0, 0];
    shockIntervalId = setInterval(function () {
      var offsetx = xs.shift();
      var offsety = ys.shift();
      if (offsetx === undefined) {
        clearInterval(shockIntervalId);
      } else {
        var lastAlpha = context.globalAlpha;
        context.globalAlpha = 1.0;
        context.drawImage(image, offsetx + x, offsety + y, size, size);
        context.globalAlpha = lastAlpha;
      }
    }, 50);
  };

  // $('.award-box').on('click', function() {
  //     if (award_times > 0) {
  //         $('#lotteryModal').modal('show');
  //     }
  // });

  $("#play-button").on("click", function () {
    if (isLoading) {
      if (award_times > 0) {
        $("#play-button").modal("hide")
        $("#lotteryModal").modal("show");
      }
      var audio_start_time =
        version_config.audio_start_time === "undefined"
          ? 0
          : version_config.audio_start_time;
      console.log(audio_start_time);
      audio_play.currentTime = audio_start_time;
      console.log(audio_play.currentTime);
      audio_play.play();
      console.log(audio_play.currentTime);
    }
  });

  // 暂停按钮和继续按钮
  $("#pauseButton").on("click", function () {
    clearInterval(intervalId);
    isPausing = true;
    $("#pauseButton").hide();
    $("#continueButton").show();
  });

  $("#continueButton").on("click", function () {
    if (isStopButtonShow && isPausing) {
      intervalId = start();
      isPausing = false;
      $("#continueButton").hide();
      $("#pauseButton").show();
    }
  });
  $("#continueButton").hide();
  $("#draw-again").hide();

  $("#stopButton").on("click", function () {
    getWinnerFromServer();
    // $('#stopButton').hide();
    // $('#nextButton').show();
  });

  $("#nextButton").on("click", function () {
    if (
      !isStopButtonShow &&
      !is_reward &&
      winners.length < award_number
    ) {
      isStopButtonShow = true;
      is_reward = true;
      intervalId = start();

      if (allIntervalId == undefined) {
        $("#nextButton").hide();
        $("#stopButton").show();
      }
    }

    if (allIntervalId != undefined) {
      allIntervalId = setTimeout(function () {
        $("#stopButton").trigger("click");
      }, 500);
    }
  });
  $("#nextButton").hide();

  $("#allButton").on("click", function () {
    if (allIntervalId == undefined) {
      allIntervalId = setTimeout(function () {
        $("#stopButton").trigger("click");
      }, 0);
    }
  });

  $("#multiWinnersButton").on("click", function () {
    getAllWinnersFromServer();
  });

  $("#comfirmButton").on("click", function () {
    //         if (!isChangeNumber && winners.length !== award_number)
    //         {
    // //            console.log('请打开更改人数开关');
    //             console.log(`winners length: ${winners.length}, award_number: ${award_number}`)
    //         }else{
    if (true) {
      $(".award-box").addClass("awarded");
      showWinners(winners);
      $(".winners-boxs").show();
      adjustWidthFowWinner();

      //     var winner_boxs = $('.winners-boxs').get(0)
      //     if (winner_boxs.clientHeight < winner_boxs.scrollHeight && award_number > 12){

      //         scrollSpeed = winner_boxs.scrollHeight/30000;
      //         var marginDiv = $("<div class='margin'></div>");
      //         marginDiv.height(winner_boxs.clientHeight);
      //         var $box1 = $('.winners-boxs');
      //         $box1.append(marginDiv.clone());
      //         $box1.prepend(marginDiv.clone());

      //         $box1[0].scrollTop = $box1.height();

      //         var offsetToScroll = $box1[0].scrollHeight - $box1.height()*2;
      //         var offsetToReset = $box1[0].scrollHeight - $box1.height();

      //         var $box2;
      //         var box1Ready = false;
      //         var loop = function(){
      //             if (!$box2){
      //                 $box2 = $box1.clone();
      //                 $box2.insertAfter($box1);
      //                 $box2.css("top", -$box1.height())
      //             }
      //             $box2[0].scrollTop = 0;
      //             box1Ready = false;

      //             $box2.animate({scrollTop:offsetToScroll}, (offsetToScroll-$box2.scrollTop())/scrollSpeed,
      //             "linear", function(){
      //                 $box2.animate({scrollTop: offsetToReset}, (offsetToReset-$box2.scrollTop())/scrollSpeed, "linear", function(){
      //                     $box2.scrollTop(0);
      //                 })

      //                 $box1.scrollTop(0);
      //                 $box1.animate({scrollTop: offsetToScroll}, offsetToScroll/scrollSpeed, "linear", loop);
      //             });

      //             $box1.animate({scrollTop:offsetToReset}, (offsetToReset-$box1[0].scrollTop)/scrollSpeed,
      //              "linear",
      //              function(){$box1.scrollTop(0);})
      //         }

      //         $box1.animate({scrollTop:offsetToScroll}, (offsetToScroll-$box1[0].scrollTop)/scrollSpeed,
      //          "linear"
      //          , loop)
      //     }
      // }
      $(".awarded-number").html(winners.length);
      $("#lotteryModal").modal("hide");
      $("#play-button").hide()
      if (need_input) {
        $("#draw-again").fadeIn("slow");
      }
    }
  });

  // 再抽一次
  $("#draw-again").on("click", function () {
    $.ajax({
      url: site_url + "lottery/award/more/",
      data: { award_id: award_id },
      dataType: "json",
      success: function (data) {
        if (data.result) {
          $("body").html(data.html);
          // window.location.href = site_url + "lottery/award/" + data.award_id + "/"
        } else {
        }
      },
    });
  });

  function randomSort(a, b) {
    return Math.random() > 0.5 ? -1 : 1;
  }

  var $redraw_icon;
  var absent_winner;

  function redrawAward() {
    $(".redraw").on("click", function (event) {
      absent_winner = $(event.currentTarget.parentElement).find('p.rtx-name').text();
      if (!absent_winner)
        absent_winner = $(event.currentTarget.parentElement).context.firstElementChild.textContent;
      $redraw_icon = $(event.currentTarget);
      $("#lotteryModal").modal("show");
      audio_play.currentTime =
        version_config.audio_start_time === "undefined"
          ? 0
          : version_config.audio_start_time;
      audio_play.play();
      console.log(audio_play.currentTime);

    });
  }

  $("#lotteryModal").on("hide.bs.modal", function () {
    clearInterval(intervalId);
    $(".operate-button").hide();
    if (award_times > 0) $("#play-button").show();
    else $("#play-button").hide();
  });

  $("#lotteryModal").on("show.bs.modal", function () {
    if (isStopButtonShow) {
      intervalId = start();
    }
    if (award_times > 0) {
      hideWinners();
    }
  });

  $("#lotteryModal").on("shown.bs.modal", function () {
    $("#play-button").parent().addClass("shown");
    $("#play-button").hide();
    $(".operate-button").show();
  });

  $("input.award-prize").on("click", function (e) {
    e.stopPropagation();
  });

  var award_prize = $("#award-input").val();

  $("input.award-prize").on("focusout", function (e) {
    var awardID = $(this).attr("data-award");
    var value = $(this).val();
    if (award_prize != value) {
      $.post(
        site_url + "lottery/award/" + awardID + "/update/",
        {
          prize: value,
        },
        function (data) {
          if (!data.result) {
            toastr.error(data.message);
          }
        },
        "json"
      );
    }
  });

  $(window).on("resize", function () {
    setTimeout(function () {
      adjustWidthFowWinner();
    }, 300);
  });

  var checkWinners = function () {
    $.ajax({
      url: site_url + "lottery/check_winners/",
      type: "post",
      data: {
        name: award_id,
      },
      dataType: "json",
      success: function (data, status) {
        if (data.status == 2) {
          $("#play-button").hide();
          // $("#award_not").show()
          winners = data.winner_list;
          $("#comfirmButton").trigger("click");
          $("#award-forbidden").show();
          endBghide();
          window.isDrew = true;
        } else {
          $("#play-button").show();
          $("#award-forbidden").hide();
        }
      },
    });
  };
  checkWinners();
  initAvatar();
  awardFadeOut();

  // var wheel = new Wheel();
  // wheel.show();
  //getAllWinnersFromServer();
});
