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
      addMessage("AI", data.reply || "Inget svar.", "bot");
  
    } catch (err) {
      console.error("🛑 FEL:", err);
      addMessage("Fel", "Det gick inte att kontakta servern: " + err.message, "bot");
    }
  }
  
  function addMessage(sender, text, cls) {
    const chat = document.getElementById("chat-container");
    const msg = document.createElement("div");
    msg.className = `message ${cls}`;
    msg.innerHTML = `<strong>${sender}:</strong><br>${text}`;
    chat.appendChild(msg);
    chat.scrollTop = chat.scrollHeight;
  }
  