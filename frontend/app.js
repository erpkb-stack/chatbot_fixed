let lastQuestion = "";

function addMessage(text, type = 'bot', confidence = null) {
  const chat = document.getElementById("chat");
  const message = document.createElement("div");
  message.className = `message ${type}-message`;
  
  let content = text;
  if (confidence !== null) {
    content += `<div class="confidence">Confidence: ${(confidence * 100).toFixed(1)}%</div>`;
  }
  
  message.innerHTML = content;
  chat.appendChild(message);
  chat.scrollTop = chat.scrollHeight;
}

async function send() {
  const msgInput = document.getElementById("msg");
  const message = msgInput.value.trim();
  
  if (!message) {
    return;
  }
  
  lastQuestion = message;
  msgInput.value = "";
  
  // Show user message
  addMessage(message, 'user');
  
  try {
    const res = await fetch("/chat", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({message: message})
    });
    
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    
    const data = await res.json();
    
    // Show bot response
    addMessage(data.answer, 'bot', data.confidence);
    
    // Show feedback form if needed
    const feedbackDiv = document.getElementById("feedback");
    if (data.needs_feedback) {
      feedbackDiv.style.display = "block";
      document.getElementById("fb").focus();
    } else {
      feedbackDiv.style.display = "none";
    }
  } catch (error) {
    console.error("Error:", error);
    addMessage("Sorry, I encountered an error. Please try again.", 'bot');
  }
}

async function sendFeedback() {
  const feedbackInput = document.getElementById("fb");
  const feedback = feedbackInput.value.trim();
  
  if (!feedback) {
    alert("Please enter an answer to teach me!");
    return;
  }
  
  if (feedback.length < 3) {
    alert("Please provide a more detailed answer (at least 3 characters).");
    return;
  }
  
  try {
    const res = await fetch("/feedback", {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify({
        question: lastQuestion,
        feedback: feedback
      })
    });
    
    if (!res.ok) {
      throw new Error(`HTTP error! status: ${res.status}`);
    }
    
    const data = await res.json();
    
    // Hide feedback form
    document.getElementById("feedback").style.display = "none";
    feedbackInput.value = "";
    
    // Show confirmation
    addMessage(data.message || "Thanks! I've learned this.", 'info');
  } catch (error) {
    console.error("Error:", error);
    addMessage("Sorry, I couldn't save your feedback. Please try again.", 'bot');
  }
}

// Allow Enter key to send message
document.addEventListener('DOMContentLoaded', function() {
  const msgInput = document.getElementById("msg");
  const fbInput = document.getElementById("fb");
  
  msgInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      send();
    }
  });
  
  fbInput.addEventListener('keypress', function(e) {
    if (e.key === 'Enter') {
      sendFeedback();
    }
  });
  
  // Add welcome message
  addMessage("Hello! I'm your AI learning assistant. Ask me anything, and if I don't know the answer, you can teach me!", 'bot');
});
