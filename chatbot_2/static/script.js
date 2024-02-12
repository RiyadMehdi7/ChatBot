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
            }
        }
    };
    xhr.send(JSON.stringify({ question: question }));
    document.getElementById("user-input").value = "";
}

// Function to display a user question
function displayUserQuestion(question) {
    var chatBox = document.getElementById("chat-box");
    var userLabel = document.createElement("div");
    var userMessage = document.createElement("div");
    userMessage.className = "user-message";
    userMessage.textContent = question;
    chatBox.appendChild(userLabel);
    chatBox.appendChild(userMessage);
}

// Function to display a bot response
function displayResponse(response) {
    var chatBox = document.getElementById("chat-box");
    var botLabel = document.createElement("div");
    botLabel.textContent = "Bizdən Biri";
    var botMessage = document.createElement("div");
    botMessage.className = "bot-message";
    botMessage.textContent = response;
    chatBox.appendChild(botLabel);
    chatBox.appendChild(botMessage);

    // Check if the response is a specific message
    if (response === "Təəssüf edirəm, sualınıza cavab verə bilmirəm. FAQ hissəsinə keçə bilərsiniz") {
        // Create a FAQ button
        var faqButton = document.createElement("button");
        faqButton.textContent = "FAQ";
        faqButton.onclick = displayCategories;
        chatBox.appendChild(faqButton);
    }
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

// Function to display subcategories
function displaySubcategories(category, subcategories) {
    var chatBox = document.getElementById("chat-box");

    // Clear the chat box
    chatBox.innerHTML = "";

    // Create a header for the selected category
    var categoryHeader = document.createElement("div");
    categoryHeader.className = "category-header";
    categoryHeader.textContent = category;
    chatBox.appendChild(categoryHeader);

    // Display the ready answer for the selected category
    var readyAnswer = "Ready answer for " + category; // You can replace this with the actual answer
    var readyAnswerDiv = document.createElement("div");
    readyAnswerDiv.className = "bot-message";
    readyAnswerDiv.textContent = "Bizdən Biri: " + readyAnswer;
    chatBox.appendChild(readyAnswerDiv);

    // Display the initial message again
    displayInitialMessage();
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

// Function to save a chat
function saveChat() {
    // Get the chat box
    var chatBox = document.getElementById("chat-box");

    // Get the chat messages
    var chatMessages = Array.from(chatBox.children).map(function(message) {
        return {
            sender: message.className,
            message: message.textContent
        };
    });

    // Generate a name for the chat
    var chatName;
    if (chatMessages.length > 0) {
        var firstMessage = chatMessages[0].message;
        var firstKeyword = firstMessage.split(" ")[0]; // Get the first keyword
        chatName = firstKeyword ? firstKeyword : "Chat";
    } else {
        chatName = "Chat";
    }

    // Save the chat messages to localStorage
    localStorage.setItem(chatName, JSON.stringify(chatMessages));

    // Add the chat to the list of saved chats
    var savedChatsList = document.getElementById("saved-chats-list");
    var listItem = document.createElement("li");
    listItem.textContent = chatName;
    listItem.onclick = function() {
        loadChat(chatName);
    };
    savedChatsList.appendChild(listItem);
}

// Function to load a chat
function loadChat(chatId) {
    // Get the saved chat messages from localStorage
    var chat = JSON.parse(localStorage.getItem(chatId));

    // Get the chat box
    var chatBox = document.getElementById("chat-box");

    // Clear the chat box
    chatBox.innerHTML = "";

    // Display the saved chat messages
    for (var i = 0; i < chat.length; i++) {
        var messageDiv = document.createElement("div");
        messageDiv.className = chat[i].sender;
        messageDiv.textContent = chat[i].message;
        chatBox.appendChild(messageDiv);
    }
}

// Call the displayInitialMessage function when the window loads
window.onload = function() {
    displayInitialMessage();

    // Add event listener for the "New Chat" button
    document.getElementById("new-chat-button").addEventListener("click", function() {
        // Clear the chat box for a new chat
        document.getElementById("chat-box").innerHTML = "";
        displayInitialMessage();
    });

    // Add event listener for each saved chat item
    var savedChatsItems = document.getElementById("saved-chats-list").children;
    for (var i = 0; i < savedChatsItems.length; i++) {
        savedChatsItems[i].addEventListener("click", function() {
            loadChat(this.textContent);
        });
    }

    // Add event listener for the "Save Chat" button
    document.getElementById("save-chat-button").addEventListener("click", saveChat);
};

// Add event listener for the "New Chat" button
document.getElementById("new-chat-button").addEventListener("click", function() {
    // Clear the chat box for a new chat
    document.getElementById("chat-box").innerHTML = "";
    displayInitialMessage();
});

// Add event listener for each saved chat item
var savedChatsItems = document.getElementById("saved-chats-list").children;
for (var i = 0; i < savedChatsItems.length; i++) {
    savedChatsItems[i].addEventListener("click", function() {
        loadChat(this.textContent);
    });
}

// Add event listener for the "Save Chat" button
document.getElementById("save-chat-button").addEventListener("click", saveChat);
