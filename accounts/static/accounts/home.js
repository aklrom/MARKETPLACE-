(function () {
    "use strict";

    document.documentElement.classList.add("home-js");

    var revealItems = document.querySelectorAll("[data-reveal]");
    if ("IntersectionObserver" in window) {
        var revealObserver = new IntersectionObserver(function (entries, observer) {
            entries.forEach(function (entry) {
                if (entry.isIntersecting) {
                    entry.target.classList.add("is-visible");
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.12 });

        revealItems.forEach(function (item) {
            revealObserver.observe(item);
        });
    } else {
        revealItems.forEach(function (item) {
            item.classList.add("is-visible");
        });
    }

    var backToTop = document.querySelector(".home-top");
    if (backToTop) {
        var updateBackToTop = function () {
            backToTop.hidden = window.scrollY < 500;
        };

        window.addEventListener("scroll", updateBackToTop, { passive: true });
        updateBackToTop();
        backToTop.addEventListener("click", function () {
            window.scrollTo({
                top: 0,
                behavior: window.matchMedia("(prefers-reduced-motion: reduce)").matches ? "auto" : "smooth"
            });
        });
    }

    document.querySelectorAll(".home-faq details").forEach(function (item) {
        item.addEventListener("toggle", function () {
            if (!item.open) {
                return;
            }
            document.querySelectorAll(".home-faq details[open]").forEach(function (openItem) {
                if (openItem !== item) {
                    openItem.open = false;
                }
            });
        });
    });
})();
