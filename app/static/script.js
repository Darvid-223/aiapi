// 🔧 Dynamisk viewporthöjd för mobilkompabilitet
function setVH() {
  let vh = window.innerHeight * 0.01;
  document.documentElement.style.setProperty('--vh', `${vh}px`);
}
window.addEventListener('resize', setVH);
window.addEventListener('orientationchange', setVH);
setVH();

// 🧹 Töm chattvyn
function clearChat() {
  document.getElementById("chat-container").innerHTML = "";
}

// 💬 Lägg till ett meddelande i chatten
function addMessage(cls, text) {
  const chat = document.getElementById("chat-container");
  const msg = document.createElement("div");
  msg.className = `message ${cls}`;

  if (cls === "bot") {
    msg.innerHTML = marked.parse(text.trim());
  } else {
    msg.textContent = text;
  }

  chat.appendChild(msg);
  chat.scrollTop = chat.scrollHeight;
}

// 📤 Skicka ett meddelande till servern
async function sendMessage() {
  const input = document.getElementById("chat-text");
  const message = input.value.trim();
  if (!message) return;

  addMessage("user", message);
  input.value = "";

  const loadingIndicator = document.getElementById("loading-indicator");
  loadingIndicator.style.display = "block";

  // 🔍 Hämta användartyp
  const userType = document.querySelector("input[name='user_type']:checked")?.value || "verksamhet";

  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message, user_type: userType }),
    });

    if (!res.ok) throw new Error("HTTP-fel: " + res.status);

    const data = await res.json();
    addMessage("bot", data.reply || "Inget svar.");
  } catch (err) {
    console.error("🛑 FEL:", err);
    addMessage("bot", "Det gick inte att kontakta servern.");
  } finally {
    loadingIndicator.style.display = "none";
  }
}

// 🧠 Initiera event listeners när sidan är klar
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("chat-text");
  const button = document.getElementById("send-btn");
  
  button.addEventListener("click", sendMessage);
  input.addEventListener("keydown", (e) => {
    if (e.key === "Enter") sendMessage();
  });

  // 👥 Byt användartyp och töm chatten
  const userTypeInputs = document.querySelectorAll("input[name='user_type']");
  userTypeInputs.forEach(input => {
    input.addEventListener("change", clearChat);
  });
});
