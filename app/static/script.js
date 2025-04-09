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
    msg.innerHTML = marked.parse(text.trim());
    //msg.textContent = text.trim();
  } else {
    msg.textContent = text; // ingen HTML för user
  }

  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}


async function sendMessage() {
  const input = document.getElementById("chat-text");
  const message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";

  const loadingIndicator = document.getElementById("loading-indicator");
  loadingIndicator.style.display = "block";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message }),
    });

    if (!res.ok) {
      throw new Error("HTTP-fel: " + res.status);
    }

    const data = await res.json();
    addMessage("bot", data.reply || "Inget svar.");
  } catch (err) {
    console.error("🛑 FEL:", err);
    addMessage("bot", "Det gick inte att kontakta servern.");
  } finally {
    loadingIndicator.style.display = "none";
  }
}


  
  