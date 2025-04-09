document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("chat-text");
  const button = document.getElementById("send-btn");

  button.addEventListener("click", sendMessage);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") {
      sendMessage();
    }
  });
});
  
async function sendMessage() {
  const input = document.getElementById("chat-text");
  const message = input.value.trim();
  if (!message) return;

  addMessage("Du", message, "user");
  input.value = "";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message })
    });

    if (!res.ok) {
      throw new Error("HTTP-fel: " + res.status);
    }

    const data = await res.json();
    addMessage("Navigator", data.reply || "Inget svar.", "bot");

  } catch (err) {
    console.error("🛑 FEL:", err);
    addMessage("Fel", "Det gick inte att kontakta servern: " + err.message, "bot");
  }
}

function addMessage(cls, text) {
  const chat = document.getElementById("chat-container");
  const msg = document.createElement("div");
  msg.className = `message ${cls}`;

  if (cls === "bot") {
    msg.innerHTML = marked.parse(text);  // rendera markdown
  } else {
    msg.textContent = text;  // för användare, ingen HTML
  }

  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}


function toggleMenu() {
  const menu = document.getElementById("nav-menu");
  menu.classList.toggle("show");
}


function sendMessage() {
  const input = document.getElementById("chat-text");
  const message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";

  // Visa laddningsindikatorn
  const loadingIndicator = document.getElementById("loading-indicator");
  loadingIndicator.style.display = "block";

  fetch("/chat", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ message })
  })
  .then(response => response.json())
  .then(data => {
    // Dölj laddningsindikatorn
    loadingIndicator.style.display = "none";
    addMessage("bot", data.reply || "Inget svar.");
  })
  .catch(error => {
    console.error("Fel:", error);
    loadingIndicator.style.display = "none";
    addMessage("bot", "Det gick inte att kontakta servern.");
  });
}


  
  