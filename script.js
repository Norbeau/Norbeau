document.addEventListener("DOMContentLoaded", function () {
  alert("Welcome to my GitHub website!");

  // ✅ LOGIN PAGE: attach handler to login form if present
  const loginForm = document.querySelector("form#login-form");
  if (loginForm) {
    loginForm.addEventListener("submit", function (event) {
      event.preventDefault();
      const username = document.getElementById("username").value;
      const password = document.getElementById("password").value;

      fetch("https://norbeau.pythonanywhere.com/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ username, password }),
      })
        .then((res) => res.json())
        .then((data) => {
          if (data.status === "success") {
            // ✅ Store user_index in localStorage
            localStorage.setItem("user_index", data.user_index);
            alert(data.message);
            window.location.href = `user_page.html?username=${encodeURIComponent(
              username
            )}&word_count=${data.word_count}`;
          } else {
            alert(data.message || "Login failed.");
          }
        })
        .catch(() => alert("Server error. Please try again later."));
    });
  }

  // ✅ ADD WORD PAGE: attach handler if "Add" button is present
  const addWordButton = document.getElementById("add-word-btn");
  if (addWordButton) {
    addWordButton.addEventListener("click", function () {
      const word = document.getElementById("word").value;
      const user_index = localStorage.getItem("user_index");

      if (!word || !user_index) {
        alert("Missing input or user session.");
        return;
      }

      fetch("https://norbeau.pythonanywhere.com/add_word", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ word, user_index }),
      })
        .then((res) => res.json())
        .then((data) => {
          alert(data.message);
          window.location.href = "user_page.html";
        })
        .catch(() => alert("Error connecting to server."));
    });
  }
});
