const editor = document.getElementById("editor");
const htmlOutput = document.getElementById("htmlOutput");
const hiddenInput = document.getElementById("emailHtml");

// Simple function to convert plain text to HTML
function convertToHtml(text) {
  // Escape HTML characters first
  const escaped = text
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;");

  // Split by double newlines to create paragraphs
  const paragraphs = escaped.split(/\n\s*\n/);

  let html = paragraphs
    .map((paragraph) => {
      if (paragraph.trim() === "") return "";

      // Convert single newlines to <br> within paragraphs
      const content = paragraph.replace(/\n/g, "<br>");

      return `<p>${content}</p>`;
    })
    .filter((p) => p !== "")
    .join("\n");

  return html || "<p></p>";
}

// Update preview and hidden input
function updateOutput() {
  const text = editor.value;
  const html = convertToHtml(text);

  htmlOutput.textContent = html;
  hiddenInput.value = html;
}

// Update output as user types
editor.addEventListener("input", updateOutput);

// Initialize
updateOutput();

// Handle form submission
/*
document
    .getElementById("templateForm")
    .addEventListener("submit", async function (e) {
      e.preventDefault();

      const form = document.getElementById("templateForm");
      const formData = new FormData(form);

      try {
        const response = await fetch("/templates/new", {
          method: "POST",
          body: formData,
        });

        if (response.ok) {
          // Optionally redirect or show success popup
          alert("Template saved successfully!");
          window.location.href = "/templates/all";
        } else {
          const errorText = await response.text();
          console.error("Error:", errorText);
          alert("Failed to save template.");
        }
      } catch (error) {
        console.error("Network error:", error);
        alert("An error occurred.");
      }
    });
*/