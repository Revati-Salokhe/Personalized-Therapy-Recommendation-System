// Function to initialize the chat with a welcome message
function initializeChat() {
    const chatBox = document.getElementById("chat-box");

    // First welcome message
    const welcomeMessage1 = document.createElement("div");
    welcomeMessage1.classList.add("bot-message");
    welcomeMessage1.innerText = "Welcome! How can I assist in your journey toward relaxation and wellness?";
    chatBox.appendChild(welcomeMessage1);

    // Second message asking for age
    const welcomeMessage2 = document.createElement("div");
    welcomeMessage2.classList.add("bot-message");
    welcomeMessage2.innerText = "To recommend the best therapy for you, please share your age and weight";
    chatBox.appendChild(welcomeMessage2);

    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

// Function to send user query and display the bot's response
async function sendQuery() {
    const query = document.getElementById("user_input").value.trim();

    if (!query) {
        alert("Please enter a message.");
        return;
    }

    const chatBox = document.getElementById("chat-box");

    // Append the user's message to the chat box
    const userMessage = document.createElement("div");
    userMessage.classList.add("user-message");
    userMessage.innerText = query;
    chatBox.appendChild(userMessage);

    // Clear the input field while waiting for the bot response
    document.getElementById("user_input").value = "";

    // Add a loading indicator while waiting for the response
    const loadingMessage = document.createElement("div");
    loadingMessage.classList.add("bot-message");
    loadingMessage.innerText = "Typing...";
    chatBox.appendChild(loadingMessage);

    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom

    try {
        const response = await fetch("/ask", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ query }),
        });

        const data = await response.json();
        console.log("Response Data:", data);

        chatBox.removeChild(loadingMessage);

        const botMessage = document.createElement("div");
        botMessage.classList.add("bot-message");

        if (response.ok) {
            botMessage.innerText = data.response || "I couldn't find an answer to that.";
        } else {
            botMessage.innerText = data.error || "An error occurred. Please try again.";
        }

        chatBox.appendChild(botMessage);
    } catch (error) {
        chatBox.removeChild(loadingMessage);
        const errorMessage = document.createElement("div");
        errorMessage.classList.add("bot-message");
        errorMessage.innerText = "Unable to reach the server. Please try again.";
        chatBox.appendChild(errorMessage);
        console.error("Error:", error);
    }

    chatBox.scrollTop = chatBox.scrollHeight; // Scroll to the bottom
}

// Function to clear the chat box
function clearChat() {
    const chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = ""; // Clears all messages from the chat box
    initializeChat(); // Reinitialize with the welcome message
}

// Initialize the chat when the page loads
window.onload = initializeChat;