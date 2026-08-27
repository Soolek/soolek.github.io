// Developer / driver image comparison (_includes/choose.html).
// The invisible snap scroller's position is the single source of truth: hover, arrow keys, resize and init
// move the scroller, and the scroll handler is the only thing that writes data-pos (which drives the CSS).
(function () {
  "use strict";
  var root = document.querySelector(".choose");
  if (!root) return;
  var stage = root.querySelector(".choose__stage");
  var scroller = root.querySelector(".choose__scroller");
  var stops = scroller.children;
  var POS = ["left", "center", "right"];
  var current = 1;   // target position index; data-pos lags behind until the (asynchronous) scroll event fires

  function step() { return stops[1].offsetLeft; }   // 160/720 of the stage width, in px
  function go(i) {
    current = Math.max(0, Math.min(2, i));
    scroller.scrollLeft = current * step();
  }

  // Phones: the nearest snap stop is the position, so the divider starts sliding as soon as a swipe passes the midpoint
  scroller.addEventListener("scroll", function () {
    var s = step();
    if (!s) return;
    current = Math.max(0, Math.min(2, Math.round(scroller.scrollLeft / s)));
    if (root.getAttribute("data-pos") !== POS[current]) root.setAttribute("data-pos", POS[current]);
  }, { passive: true });

  // Mouse/pen: hover a half, leave the image to go back to the centre.
  // Touch is left to the scroller (its pointer events carry pointerType "touch").
  stage.addEventListener("pointermove", function (e) {
    if (e.pointerType === "touch") return;
    var r = stage.getBoundingClientRect();
    go(e.clientX - r.left < r.width / 2 ? 0 : 2);
  });
  stage.addEventListener("pointerleave", function (e) {
    if (e.pointerType !== "touch") go(1);
  });
  stage.addEventListener("keydown", function (e) {
    if (e.key !== "ArrowLeft" && e.key !== "ArrowRight") return;
    e.preventDefault();   // a focused scroller would otherwise scroll 40px and snap straight back
    go(current + (e.key === "ArrowLeft" ? -1 : 1));
  });
  // The stops are percentages but scrollLeft is pixels: keep the current position on resize / rotation
  window.addEventListener("resize", function () { go(current); });

  go(1);   // start centred
})();
