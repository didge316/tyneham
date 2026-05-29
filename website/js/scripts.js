// Dark mode: apply stored/OS preference before first paint, toggle on button click.
// Two .dark-mode-btn buttons exist per page: one outside the collapse (mobile),
// one inside the nav list (desktop). Both stay in sync.
(function () {
  var stored = localStorage.getItem('theme');
  var prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  var theme = stored || (prefersDark ? 'dark' : 'light');
  document.documentElement.setAttribute('data-theme', theme);

  document.addEventListener('DOMContentLoaded', function () {
    var btns = document.querySelectorAll('.dark-mode-btn');
    if (!btns.length) return;
    function syncBtns(t) {
      btns.forEach(function (b) {
        b.textContent = t === 'dark' ? '☀️' : '🌙';
        b.title = t === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
      });
    }
    syncBtns(theme);
    btns.forEach(function (btn) {
      btn.addEventListener('click', function () {
        var next = document.documentElement.getAttribute('data-theme') === 'dark' ? 'light' : 'dark';
        document.documentElement.setAttribute('data-theme', next);
        localStorage.setItem('theme', next);
        syncBtns(next);
      });
    });
  });
})();

// Highlight the current page in the sidebar menu.
// Deferred to idle time — it's cosmetic and not on the critical path.
function highlightSidebar() {
  let currentPage = window.location.pathname.split("/").pop();
  if (!currentPage || currentPage === "/") currentPage = "index.html";
  if (!currentPage.includes(".")) currentPage += ".html";

  const menuItems = document.querySelectorAll(
    "#sidebar-menu .menu-item, #sidebar-menu-near .menu-item"
  );

  // Read all links first, then batch the writes (avoids forced reflow).
  const toHighlight = [];
  menuItems.forEach(function (item) {
    if (item.getAttribute("data-page") === currentPage) {
      toHighlight.push({ item, link: item.querySelector("a") });
    }
  });
  toHighlight.forEach(function ({ item, link }) {
    item.classList.add("bg-light");
    if (link) link.classList.add("fw-bold");
  });
}

if (typeof requestIdleCallback !== "undefined") {
  requestIdleCallback(highlightSidebar);
} else {
  setTimeout(highlightSidebar, 0);
}


(function () {
  "use strict";

  // 2026 Tyneham open periods [month, startDate, endDate]
  const openPeriods2026 = [
    // Jan
    [0, 1, 4], [0, 10, 11], [0, 24, 25], [0, 31, 31],
    // Feb
    [1, 1, 1], [1, 7, 8], [1, 14, 15], [1, 21, 22], [1, 28, 28],
    // Mar
    [2, 1, 1], [2, 7, 8], [2, 21, 22], [2, 28, 29], [2, 30, 31],
    // Apr
    [3, 1, 12], [3, 18, 19], [3, 25, 26],
    // May
    [4, 2, 4], [4, 9, 10], [4, 16, 17], [4, 23, 31],
    // Jun
    [5, 6, 7], [5, 20, 21], [5, 27, 28],
    // Jul
    [6, 4, 5], [6, 11, 12], [6, 18, 19], [6, 25, 31],
    // Aug
    [7, 1, 31],
    // Sep
    [8, 5, 6], [8, 19, 20], [8, 26, 27],
    // Oct
    [9, 3, 4], [9, 17, 18], [9, 24, 25], [9, 31, 31],
    // Nov
    [10, 1, 1], [10, 7, 8], [10, 21, 22], [10, 28, 29],
    // Dec
    [11, 5, 6], [11, 12, 13], [11, 19, 31],
  ];

  function isTynehamOpen(date) {
    if (date.getFullYear() !== 2026) return false;
    const month = date.getMonth();
    const day = date.getDate();
    return openPeriods2026.some(([m, start, end]) => month === m && day >= start && day <= end);
  }

  function getNextOpenDate(today) {
    let next = new Date(today);
    for (let i = 1; i <= 30; i++) {
      next.setDate(today.getDate() + i);
      if (isTynehamOpen(next)) return next;
    }
    return null;
  }

  function updateStatus(statusEl) {
    const spinner = statusEl.querySelector(".spinner-border");
    const content = statusEl.querySelector("#statusContent, .statusContent");
    if (!spinner || !content) return;

    const today = new Date();
    const openToday = isTynehamOpen(today);
    const nextOpen = getNextOpenDate(today);

    // Hide spinner and update immediately — no artificial delay.
    spinner.classList.add("d-none");

    if (openToday) {
      statusEl.className =
        "alert alert-success fs-3 fw-bold py-5 shadow-lg border-0 rounded-4 mb-4";
      content.innerHTML =
        "<strong>✅ Tyneham is OPEN TODAY!</strong><br>" +
        '<small class="text-success-emphasis">9am to dusk (exhibitions 10am-4pm)</small>';
    } else {
      statusEl.className =
        "alert alert-danger fs-3 fw-bold py-5 shadow-lg border-0 rounded-4 mb-4";
      const nextStr = nextOpen
        ? nextOpen.toLocaleDateString("en-GB", {
            weekday: "long",
            day: "numeric",
            month: "long",
            year: "numeric",
          })
        : null;
      content.innerHTML =
        "<strong>❌ Tyneham is CLOSED TODAY</strong><br>" +
        '<small class="text-danger-emphasis">' +
        (nextStr ? "Next open: " + nextStr : "Check calendar for next open date") +
        "</small>";
    }
  }

  document.addEventListener("DOMContentLoaded", function () {
    ["tynehamStatus", "tynehamStatusSidebar"].forEach(function (id) {
      const el = document.getElementById(id);
      if (el) updateStatus(el);
    });
  });
})();
