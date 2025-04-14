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

function resetTextarea(textarea) {
  textarea.value = "";
  const lineHeight = parseInt(getComputedStyle(textarea).lineHeight);
  textarea.style.height = lineHeight + "px";
}

// 📤 Skicka ett meddelande till servern
async function sendMessage() {
  const textarea = document.getElementById("chat-text");
  const message = textarea.value.trim();
  if (!message) return;

  addMessage("user", message);
  resetTextarea(textarea); // 🧹 återställ direkt efter att användaren skickat

  const loadingIndicator = document.getElementById("loading-indicator");
  loadingIndicator.style.display = "block";

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
  resetTextarea(document.getElementById("chat-text"));

}


// 🧹 Töm chatten visuellt
function clearChat() {
  const chat = document.getElementById("chat-container");
  chat.innerHTML = "";
}

// 🧠 Initiera event listeners när sidan är klar
document.addEventListener("DOMContentLoaded", () => {
  const input = document.getElementById("chat-text");
  const button = document.getElementById("send-btn");

  button.addEventListener("click", sendMessage);

  // 👥 När användartyp ändras – töm både frontend och backend-minnet
  const userTypeInputs = document.querySelectorAll("input[name='user_type']");
  userTypeInputs.forEach(input => {
    input.addEventListener("change", async () => {
      clearChat();
      const userType = input.value;

      try {
        await fetch("/reset_memory", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ user_type: userType }),
        });
      } catch (err) {
        console.error("Kunde inte rensa serverminnet:", err);
      }
    });
  });
});



const textarea = document.getElementById("chat-text");

// 🟢 Dynamisk höjdanpassning
textarea.addEventListener("input", () => {
  textarea.style.height = "auto"; // återställ
  textarea.style.height = textarea.scrollHeight + "px"; // väx
});

// 🟢 Skicka på Enter (utan Shift), radbryt på Shift+Enter
textarea.addEventListener("keydown", function (event) {
  if (event.key === "Enter" && !event.shiftKey) {
    event.preventDefault();       // stoppa ny rad
    sendMessage();                // skicka
  }
  // Shift+Enter: inget event.preventDefault → ny rad fungerar!
});

// 🟢 Återställ höjd efter skickat
function resetTextarea(textarea) {
  textarea.value = "";
  textarea.style.height = "auto"; // återställ
  textarea.style.height = textarea.scrollHeight + "px"; // sätt korrekt 1-radshöjd
}

