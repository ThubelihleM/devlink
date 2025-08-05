document.addEventListener("DOMContentLoaded", () => {
  const toggleBtn = document.getElementById("theme-toggle");
  const body = document.body;
  const theme = localStorage.getItem("theme");

  if (theme) {
    body.className = theme;
  }

  toggleBtn.addEventListener("click", () => {
    if (body.classList.contains("light-mode")) {
      body.className = "dark-mode";
      localStorage.setItem("theme", "dark-mode");
    } else {
      body.className = "light-mode";
      localStorage.setItem("theme", "light-mode");
    }
  });
});
