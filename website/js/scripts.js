
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


// Live weather widget — fetches current conditions + 3-day forecast for Tyneham
// from Open-Meteo (free, no API key) and injects a card above the sidebar menus.
(function () {
  "use strict";

  // WMO weather code → [emoji, short description]
  var WMO = {
    0:  ["☀️",  "Clear sky"],
    1:  ["🌤️", "Mainly clear"],
    2:  ["⛅",  "Partly cloudy"],
    3:  ["☁️",  "Overcast"],
    45: ["🌫️", "Fog"],
    48: ["🌫️", "Freezing fog"],
    51: ["🌦️", "Light drizzle"],
    53: ["🌦️", "Drizzle"],
    55: ["🌧️", "Heavy drizzle"],
    61: ["🌧️", "Light rain"],
    63: ["🌧️", "Rain"],
    65: ["🌧️", "Heavy rain"],
    71: ["🌨️", "Light snow"],
    73: ["🌨️", "Snow"],
    75: ["❄️",  "Heavy snow"],
    80: ["🌦️", "Rain showers"],
    81: ["🌧️", "Heavy showers"],
    82: ["⛈️",  "Violent showers"],
    95: ["⛈️",  "Thunderstorm"],
    96: ["⛈️",  "Thunderstorm"],
    99: ["⛈️",  "Thunderstorm"]
  };

  function wmo(code) {
    return WMO[code] || ["🌡️", "Unknown"];
  }

  function initWeather() {
    var menuUl = document.getElementById("sidebar-menu");
    if (!menuUl) return;
    var menuCard = menuUl.closest(".card");
    if (!menuCard) return;
    var col = menuCard.parentNode;

    var weatherCard = document.createElement("div");
    weatherCard.className = "card mt-3 mb-4 shadow-sm";
    weatherCard.id = "sidebar-weather";
    weatherCard.innerHTML =
      '<div class="card-header bg-primary text-white">' +
        "<strong>Tyneham Weather</strong>" +
      "</div>" +
      '<div class="card-body p-3" id="sw-body">' +
        '<div class="text-center text-muted py-2">Loading…</div>' +
      "</div>";

    col.insertBefore(weatherCard, col.firstElementChild);

    var url =
      "https://api.open-meteo.com/v1/forecast" +
      "?latitude=50.6239&longitude=-2.1601" +
      "&current=temperature_2m,weathercode,windspeed_10m" +
      "&daily=weathercode,temperature_2m_max,temperature_2m_min" +
      "&timezone=Europe%2FLondon&forecast_days=4";

    fetch(url)
      .then(function (r) { return r.json(); })
      .then(renderWeather)
      .catch(function () {
        var b = document.getElementById("sw-body");
        if (b) b.innerHTML =
          '<div class="text-center text-muted small py-2">Weather unavailable</div>';
      });
  }

  function renderWeather(data) {
    var body = document.getElementById("sw-body");
    if (!body) return;

    var cur = data.current;
    var daily = data.daily;
    var w = wmo(cur.weathercode);
    var temp = Math.round(cur.temperature_2m);
    var wind = Math.round(cur.windspeed_10m);

    var DAYS = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"];
    var forecastHtml = "";
    for (var i = 1; i <= 3; i++) {
      if (!daily.time[i]) break;
      var d = new Date(daily.time[i] + "T12:00:00");
      var fw = wmo(daily.weathercode[i]);
      var hi = Math.round(daily.temperature_2m_max[i]);
      var lo = Math.round(daily.temperature_2m_min[i]);
      forecastHtml +=
        '<div class="d-flex justify-content-between align-items-center border-top pt-2 mt-2">' +
          '<span class="text-muted" style="width:2.8rem;font-size:1rem">' + DAYS[d.getDay()] + "</span>" +
          '<span style="font-size:1.5rem">' + fw[0] + "</span>" +
          '<span style="font-size:1rem">' + hi + "\xb0" +
            '<span class="text-muted">/' + lo + "\xb0</span></span>" +
        "</div>";
    }

    body.innerHTML =
      '<div class="text-center mb-3">' +
        '<div style="font-size:3rem;line-height:1.2">' + w[0] + "</div>" +
        '<div class="fw-bold" style="font-size:2rem">' + temp + "\xb0C</div>" +
        '<div class="text-muted" style="font-size:1.1rem">' + w[1] + "</div>" +
        '<div class="text-muted" style="font-size:1rem">Wind: ' + wind + " km/h</div>" +
      "</div>" +
      forecastHtml +
      '<div class="text-end mt-2" style="font-size:0.65rem;color:#aaa">' +
        "Near Tyneham \xb7 Open-Meteo</div>";
  }

  document.addEventListener("DOMContentLoaded", initWeather);
}());
