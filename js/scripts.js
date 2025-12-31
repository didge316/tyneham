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