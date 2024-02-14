// Function to send a question
function sendQuestion() {
    var question = document.getElementById("user-input").value.trim();
    if (question === "") return;

    displayUserQuestion(question);

    var xhr = new XMLHttpRequest();
    xhr.open("POST", "/ask", true);
    xhr.setRequestHeader("Content-Type", "application/json");
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE) {
            if (xhr.status === 200) {
                var response = JSON.parse(xhr.responseText).response;
                displayResponse(response);
                saveChat(); // Save the chat after each bot response
            }
        }
    };
    xhr.send(JSON.stringify({ question: question }));
    document.getElementById("user-input").value = "";
}

// Create a mapping between options and responses
var optionResponses = {
    "Direktor/Şöbə Rəisi": "İdarə Heyəti (Maliyyə menecmenti departamentinin təklifi ilə)",
    "Direktor müavini": "Struktur bölmə rəhbəri (Əlavə ƏFG təyin olunmadığı təqdirdə direktorun ƏFG-na bərabər götürülür)",
    "Menecer/Baş Mütəxəssis/Bölmə rəhbəri/Qrup rəhbəri": "Struktur bölmə rəhbəri",
    "Struktur Bölmə Rəhbəri": "Şöbədə çalışan digər əməkdaşlar Çalışdığı strukturun ƏFG və hədəflərinə bərabər götürülür",
    "Şöbədə çalışan digər əməkdaşlar": "Çalışdığı strukturun ƏFG və hədəflərinə bərabər götürülür"
};

function displayResponse(response) {
    var chatBox = document.getElementById("chat-box");

    // Check if the response is a specific message
    if (response === "Təəssüf edirəm, sualınıza cavab verə bilmirəm. FAQ hissəsinə keçə bilərsiniz") {
        // Display the message
        var botLabel = document.createElement("div");
        botLabel.textContent = "Bizdən Biri";
        var botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = response;
        chatBox.appendChild(botLabel);
        chatBox.appendChild(botMessage);

        // Create a FAQ button
        var faqButton = document.createElement("button");
        faqButton.textContent = "FAQ";
        faqButton.onclick = displayCategories;
        chatBox.appendChild(faqButton);
        scrollToBottom();

        // Return from the function
        return;
    }

    // Check if the response includes a certain substring
    if (response.includes("Direktor/ şöbə rəisi")) {
        // Handle this specific response
    } else {
        // If the response does not include the specific substring, display it as usual
        var botLabel = document.createElement("div");
        botLabel.textContent = "Bizdən Biri";
        var botMessage = document.createElement("div");
        botMessage.className = "bot-message";
        botMessage.textContent = response;
        chatBox.appendChild(botLabel);
        chatBox.appendChild(botMessage);
    }

    scrollToBottom();
}

function displaySelectedResponse(option) {
    var chatBox = document.getElementById("chat-box");
    var botLabel = document.createElement("div");
    botLabel.textContent = "Bizdən Biri";
    var botMessage = document.createElement("div");
    botMessage.className = "bot-message";
    botMessage.textContent = option + ": " + optionResponses[option]; // Display the selected option and the corresponding response
    chatBox.appendChild(botLabel);
    chatBox.appendChild(botMessage);
    scrollToBottom();

    
}

// Function to display categories
function displayCategories() {
    var chatBox = document.getElementById("chat-box");

    // Clear the chat box
    chatBox.innerHTML = "";

    // List of categories
    var categories = {
        "Promotion": ["Maaş artımı", "Vəzifə Artımı"],
        "Benefits": ["Sığorta", "Dəyərlisən"],
        "Training": ["ISpring", "Məcburi təlimlər"],
        "Performance review": ["Overall Information"]
    };

    // Create a button for each category and append it to the chat box
    for (var category in categories) {
        var categoryButton = document.createElement("button");
        categoryButton.className = "category-button";
        categoryButton.textContent = category;
        categoryButton.onclick = function() {
            displaySubcategories(this.textContent, categories[this.textContent]);
        };
        chatBox.appendChild(categoryButton);
    }
}
// Function to display the initial message
function displayInitialMessage() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/initial_message", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            var initialMessage = JSON.parse(xhr.responseText).initial_message;
            displayResponse(initialMessage);
        }
    };
    xhr.send();
}

// Function to display the selected response
function displaySelectedResponse(response) {
    var chatBox = document.getElementById("chat-box");
    var botLabel = createMessageElement("bot-label", "Bizdən Biri");
    var botMessage = createMessageElement("bot-message", response);
    chatBox.appendChild(botLabel);
    chatBox.appendChild(botMessage);
    scrollToBottom();
}

// Function to create a message element
function createMessageElement(className, text) {
    var element = document.createElement("div");
    element.className = className;
    element.textContent = text;
    return element;
}

// Function to display the initial message
function displayInitialMessage() {
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/initial_message", true);
    xhr.onreadystatechange = function() {
        if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
            var initialMessage = JSON.parse(xhr.responseText).initial_message;
            displayResponse(initialMessage);
        }
    };
    xhr.send();
}

// Function to save the chat
function saveChat() {
    // Get the chat name based on the first user message
    var firstUserMessage = document.querySelector(".user-message");
    if (!firstUserMessage) return; // Exit if there are no user messages
    var chatName = firstUserMessage.textContent.trim();

    // Check if a chat with the same name already exists in localStorage
    var savedChat = localStorage.getItem(chatName);
    var chatContent = [];

    // Get the chat box
    var chatBox = document.getElementById("chat-box");

    // Get all chat messages
    var chatMessages = chatBox.querySelectorAll(".user-message, .bot-message");

    // Loop through each chat message and add it to the array
    chatMessages.forEach(function(message) {
        var sender = message.classList.contains("user-message") ? "user" : "bot";
        var content = message.textContent.trim();
        chatContent.push({ sender: sender, content: content });
    });

    // Save or update the chat content in localStorage
    if (savedChat) {
        // If the chat already exists, update its content
        var existingChat = JSON.parse(savedChat);
        existingChat = existingChat.concat(chatContent);
        localStorage.setItem(chatName, JSON.stringify(existingChat));
    } else {
        // If the chat doesn't exist, create a new entry
        localStorage.setItem(chatName, JSON.stringify(chatContent));
        // Update the list of saved chats
        updateSavedChatsList(chatName);
    }
}

// Function to load a saved chat
function loadChat(chatName) {
    // Retrieve the chat messages from localStorage based on the chatName
    var chatMessages = JSON.parse(localStorage.getItem(chatName));

    // Display the chat messages in the chat box
    var chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = ""; // Clear the existing chat messages

    chatMessages.forEach(function(message) {
        var messageElement = document.createElement("div");
        messageElement.className = message.sender === "user" ? "user-message" : "bot-message";
        messageElement.textContent = message.content;
        chatBox.appendChild(messageElement);
    });
}

// Function to update the list of saved chats in the UI
function updateSavedChatsList(chatName) {
    var savedChatsList = document.getElementById("saved-chats-list");

    // Create a new list item for the saved chat
    var chatListItem = document.createElement("li");
    chatListItem.textContent = chatName;

    // Add an event listener to load the chat when the item is clicked
    chatListItem.addEventListener("click", function() {
        loadChat(chatName);
    });

    // Append the new list item to the saved chats list
    savedChatsList.appendChild(chatListItem);
}
// Function to scroll to the bottom of the chat box
function scrollToBottom() {
    var chatBox = document.getElementById("chat-box");
    chatBox.scrollTop = chatBox.scrollHeight;
}

// Function to display a user question
function displayUserQuestion(question) {
    var chatBox = document.getElementById("chat-box");
    var userMessage = createMessageElement("user-message", question);
    chatBox.appendChild(userMessage);
    scrollToBottom();
}

// Initialize the chat when the window loads
window.onload = function() {
    displayInitialMessage();
    
    // Add event listener for the "New Chat" button
    document.getElementById("new-chat-button").addEventListener("click", function() {
        document.getElementById("chat-box").innerHTML = ""; // Clear the chat box for a new chat
        displayInitialMessage();
    });

    // Add event listener for the "Enter" key press in the input field
    document.getElementById("user-input").addEventListener("keydown", function(event) {
        if (event.keyCode === 13) { // Check if the key pressed is "Enter"
            sendQuestion(); // Call the sendQuestion function
        }
    });
};