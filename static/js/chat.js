export class ChatBot {
  constructor(jwtToken) {
    this.jwtToken = jwtToken;
    this.messageInput = document.getElementById("messageInput");
    this.sendButton = document.getElementById("sendButton");
    this.chatMessages = document.getElementById("chatMessages");
    this.connectionStatus = document.getElementById("connectionStatus");

    this.sendButton.addEventListener("click", () => this.sendMessage());
    this.messageInput.addEventListener("keypress", e => {
      if (e.key === "Enter") this.sendMessage();
    });

    this.eventSource = null; // Store the EventSource instance here
    
    this.connect();
    this.setWelcomeTime();
  }

  connect() {
    if (this.eventSource) {
      this.eventSource.close();  // Close previous connection if any
    }

    const eventSource = new EventSource(`/sse/stream?token=${encodeURIComponent(this.jwtToken)}`);

    eventSource.onopen = () => {
      this.updateConnectionStatus("connected", "🟢 Connected");
      this.enableInput();
    };

    eventSource.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === "response") {
        this.addMessage(data.message, "bot");
      } else if (data.type === "error") {
        this.addMessage(`Error: ${data.message}`, "bot");
      }
    };

    eventSource.onerror = () => {
      this.updateConnectionStatus("disconnected", "🔴 Disconnected");
      this.disableInput();
      eventSource.close();
      // setTimeout(() => this.connect(), 3000);
    };
  }

  async sendMessage() {
    const message = this.messageInput.value.trim();
    if (!message) return;

    this.addMessage(message, "user");

    try {
      await fetch("http://localhost:8000/sse/send", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          "Authorization": "Bearer " + this.jwtToken,
        },
        body: JSON.stringify({ message }),
      });
    } catch (err) {
      this.addMessage("Error sending message", "bot");
    }

    this.messageInput.value = "";
  }

  addMessage(message, sender) {
    const wrapper = document.createElement("div");
    wrapper.className = `message ${sender}`;

    const content = document.createElement("div");
    content.className = "message-content";
    content.innerText = message;

    const time = document.createElement("div");
    time.className = "message-time";
    time.innerText = new Date().toLocaleTimeString();

    content.appendChild(time);
    wrapper.appendChild(content);
    this.chatMessages.appendChild(wrapper);
    this.chatMessages.scrollTop = this.chatMessages.scrollHeight;
  }

  enableInput() {
    this.messageInput.disabled = false;
    this.sendButton.disabled = false;
    this.messageInput.focus();
  }

  disableInput() {
    this.messageInput.disabled = true;
    this.sendButton.disabled = true;
  }

  updateConnectionStatus(statusClass, text) {
    this.connectionStatus.className = `connection-status ${statusClass}`;
    this.connectionStatus.innerText = text;
  }

  setWelcomeTime() {
    const timeDiv = document.getElementById("welcomeTime");
    if (timeDiv) timeDiv.innerText = new Date().toLocaleTimeString();
  }
}
