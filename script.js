(function () {
  "use strict";

  function initLogoFallback() {
    var imgs = document.querySelectorAll(".site-logo img");
    imgs.forEach(function (img) {
      img.addEventListener("error", function () {
        var link = img.closest(".site-logo");
        if (!link) return;
        link.classList.add("site-logo--text");
        link.setAttribute("aria-label", "Eva Casino — главная");
        link.innerHTML = "<span>Eva Casino</span>";
      });
    });
  }

  function initMenu() {
    var toggle = document.querySelector(".menu-toggle");
    var nav = document.querySelector(".site-nav");
    if (!toggle || !nav) return;

    function closeMenu() {
      nav.classList.remove("is-open");
      toggle.classList.remove("is-open");
      toggle.setAttribute("aria-expanded", "false");
    }

    function openMenu() {
      nav.classList.add("is-open");
      toggle.classList.add("is-open");
      toggle.setAttribute("aria-expanded", "true");
    }

    toggle.setAttribute("aria-expanded", "false");
    toggle.addEventListener("click", function () {
      if (nav.classList.contains("is-open")) {
        closeMenu();
      } else {
        openMenu();
      }
    });

    document.addEventListener("keydown", function (e) {
      if (e.key === "Escape") closeMenu();
    });

    document.addEventListener("click", function (e) {
      var target = e.target;
      if (!(target instanceof Node)) return;
      if (toggle.contains(target) || nav.contains(target)) return;
      closeMenu();
    });

    window.addEventListener("resize", function () {
      if (window.matchMedia("(min-width: 992px)").matches) {
        closeMenu();
      }
    });
  }

  function init() {
    initLogoFallback();
    initMenu();
  }

  if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", init);
  } else {
    init();
  }
})();
