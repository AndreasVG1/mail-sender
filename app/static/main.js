const editor = document.getElementById("editor");
const hiddenInput = document.getElementById("emailHtml");

// Function to format text
function formatText(command) {
  document.execCommand(command, false, null);
  editor.focus();
}

// Handle keyboard shortcuts
editor.addEventListener("keydown", function (e) {
  // Ctrl+B for bold
  if (e.ctrlKey && e.key === "b") {
    e.preventDefault();
    formatText("bold");
  }
  // Ctrl+I for italic
  else if (e.ctrlKey && e.key === "i") {
    e.preventDefault();
    formatText("italic");
  }
  // Ctrl+U for underline
  else if (e.ctrlKey && e.key === "u") {
    e.preventDefault();
    formatText("underline");
  }
  // Enter for line break
  else if (e.key === "Enter") {
    // Let the default behavior handle this, but update output after
    setTimeout(10);
  }
});

// Handle form submission
document
  .getElementById("templateForm")
  .addEventListener("submit", function (e) {
    e.preventDefault();

    const templateName = document.getElementById("templateName").value;
    const emailHtml = document.getElementById("emailHtml").value;

    // Here you would typically send this data to your Python backend
    console.log("Template Name:", templateName);
    console.log("Email HTML:", emailHtml);

    alert("Template would be saved! Check the console for the data.");
  });

// Add placeholder behavior
editor.addEventListener("focus", function () {
  if (this.textContent.trim() === "" && !this.innerHTML.includes("<")) {
    this.innerHTML = "";
  }
});

editor.addEventListener("blur", function () {
  if (this.textContent.trim() === "") {
    this.innerHTML = `Welcome to our newsletter!<br><br>This is a sample email template. You can:<br>• Type normally and press Enter for new lines<br>• Use Ctrl+B for <strong>bold text</strong><br>• Use Ctrl+I for <em>italic text</em><br>• Use Ctrl+U for <u>underline</u>`;
  }
});
