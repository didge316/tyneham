// Highlight the current page in the sidebar menu
document.addEventListener("DOMContentLoaded", function () {
  // Get the current filename (e.g., "map_of_tyneham.html" or "index.html")
  let currentPage = window.location.pathname.split("/").pop();
  if (currentPage === "" || currentPage === "/") {
    currentPage = "index.html";
  }

  // Find all sidebar menu items
  const menuItems = document.querySelectorAll("#sidebar-menu .menu-item");

  menuItems.forEach(function (item) {
    if (item.getAttribute("data-page") === currentPage) {
      item.classList.add("bg-light");                    // Light background
      const link = item.querySelector("a");
      if (link) {
        link.classList.add("fw-bold");                  // Bold text
      }
    }
  });
});


(function() {
  'use strict';
  
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
    [11, 5, 6], [11, 12, 13], [11, 19, 31]
  ];

  function isTynehamOpen(date) {
    if (date.getFullYear() !== 2026) return false;
    
    const month = date.getMonth();
    const day = date.getDate();
    
    return openPeriods2026.some(([m, start, end]) => 
      month === m && day >= start && day <= end
    );
  }

  function getNextOpenDate(today) {
    let next = new Date(today);
    for (let i = 1; i <= 30; i++) { // Look ahead 1 month max
      next.setDate(today.getDate() + i);
      if (isTynehamOpen(next)) {
        return next;
      }
    }
    return null;
  }

  // Initialize on load
document.addEventListener('DOMContentLoaded', function() {
  // List of all status elements by ID
  const statusIds = ['tynehamStatus', 'tynehamStatusSidebar'];

  statusIds.forEach(id => {
    const statusEl = document.getElementById(id);
    if (!statusEl) return; // skip if element not found

    const spinner = statusEl.querySelector('.spinner-border');
    const content = statusEl.querySelector('#statusContent, .statusContent');

    // Show spinner
    spinner.classList.remove('d-none');

    setTimeout(() => { // Simulate quick check
      spinner.classList.add('d-none');
      const today = new Date();
      const openToday = isTynehamOpen(today);
      const nextOpen = getNextOpenDate(today);

      if (openToday) {
        statusEl.className = 'alert alert-success fs-3 fw-bold py-5 shadow-lg border-0 rounded-4 mb-4';
        content.innerHTML = `
          <i class="bi bi-check-circle-fill me-3" style="font-size: 3rem;"></i>
          <strong>✅ Tyneham is OPEN TODAY!</strong><br>
          <small class="text-success-emphasis">9am to dusk (exhibitions 10am-4pm)</small>
        `;
      } else {
        statusEl.className = 'alert alert-danger fs-3 fw-bold py-5 shadow-lg border-0 rounded-4 mb-4';
        content.innerHTML = `
          <i class="bi bi-x-circle-fill me-3" style="font-size: 3rem;"></i>
          <strong>❌ Tyneham is CLOSED TODAY</strong><br>
          ${nextOpen ? `<small class="text-danger-emphasis">Next open: ${nextOpen.toLocaleDateString('en-GB', {
            weekday: 'long',
            day: 'numeric',
            month: 'long',
            year: 'numeric'
          })}</small>` : '<small class="text-danger-emphasis">Check calendar for next open date</small>'}
        `;
      }
    }, 800);
  });
});

})();
