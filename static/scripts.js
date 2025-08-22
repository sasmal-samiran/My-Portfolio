document.addEventListener("DOMContentLoaded", () => {
  const fadeElements = document.querySelectorAll(".lazy-img, .fade-in, .slide-left, .slide-right, .slide-up, .slide-down, .slide-up-right, .zoom-in, .resume-image, .rotate-right, .rotate-left");

  const fadeObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach((entry, index) => {
      if (entry.isIntersecting) {
        const el = entry.target;

        if (el.classList.contains("lazy-img") && el.dataset.src) {
          el.src = el.dataset.src;
          el.onload = () => el.classList.add("loaded");
        }

        const animationMap = {
          "fade-in": "visible",
          "slide-left": "move",
          "slide-right": "move",
          "slide-up": "move",
          "slide-down": "move",
          "slide-up-right": "move",
          "zoom-in": "zoom",
          "resume-image": "flow",
          "rotate-right": "start",
          "rotate-left": "start"
        };

        for (const baseClass in animationMap) {
          if (el.classList.contains(baseClass)) {
            setTimeout(() => {
              el.classList.add(animationMap[baseClass]);
            }, index * 100);
          }
        }

        observer.unobserve(el);
      }
    });
  }, {
    threshold: 0.1,
    rootMargin: "0px 0px 100px 0px"
  });

  fadeElements.forEach(el => fadeObserver.observe(el));

  const alertBox = document.getElementById("custom-alert");
  const messageSpan = document.getElementById("custom-alert-message");
  const closeBtn = document.getElementById("close-alert-btn");

  // Get message from data attribute
  const message = alertBox?.dataset.message || "";

  if (message && messageSpan) {
    messageSpan.textContent = message;
    alertBox.classList.remove("hidden");

    setTimeout(() => {
      alertBox.classList.add("hidden");
    }, 15000);
  }

  // Attach event listener instead of inline onclick
  if (closeBtn) {
    closeBtn.addEventListener("click", () => {
      alertBox.classList.add("hidden");
    });
  }
});

function showCustomAlert(message, duration = 15000) {
  const alertBox = document.getElementById('custom-alert');
  const messageSpan = document.getElementById('custom-alert-message');

  messageSpan.textContent = message;
  alertBox.classList.remove('hidden');

  setTimeout(() => {
    alertBox.classList.add('hidden');
  }, duration);
}

function closeAlert() {
  document.getElementById('custom-alert').classList.add('hidden');
}