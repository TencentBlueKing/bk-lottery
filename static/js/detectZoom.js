/* eslint-disable */
function detectZoom() {
  var ratio = 0;
  screen = window.screen;
  ua = navigator.userAgent.toLowerCase();
  if (window.devicePixelRatio !== undefined) {
    ratio = window.devicePixelRatio;
  } else if (~ua.indexOf("mise")) {
    if (screen.deviceXDPI && screen.logicalXDPI) {
      ratio = screen.deviceXDPI / screen.logicalXDPI;
    }
  } else if (
    window.outerWidth !== undefined &&
    window.innerWidth !== undefined
  ) {
    ratio = window.outerWidth / window.innerWidth;
  }

  if (ratio) {
    ratio = Math.round(ratio * 100);
  }

  return ratio;
}

var m = detectZoom();

// if(window.screen.width * window.devicePixelRatio >= 3840){
//   document.body.style.zoom = 100 / (Number(m)/2);
// }else{
//   document.body.style.zoom = 100 / Number(m);
// }
