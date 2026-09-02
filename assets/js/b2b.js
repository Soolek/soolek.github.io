// B2B call widget (_pages/b2b.*.html).
// A click decodes the phone number from offset parts, so the page source never contains it.
(function () {
  "use strict";
  var button = document.querySelector(".cta__call");
  if (!button) return;

  button.addEventListener("click", function () {
    var parts = [91, 740, 376, 318].map(function (n) { return n - 43; });
    var link = document.createElement("a");
    link.className = "cta__button";
    link.href = "tel:+" + parts.join("");
    link.textContent = "+" + parts.join(" ");
    button.replaceWith(link);
    link.focus();
  });
})();
