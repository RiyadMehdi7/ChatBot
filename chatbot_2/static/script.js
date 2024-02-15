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
                saveChat(question); // Save the chat after each bot response with the first message as the name
            }
        }
    };
    xhr.send(JSON.stringify({ question: question }));
    document.getElementById("user-input").value = "";
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

// Function to display a bot response
function displayResponse(response) {
    var chatBox = document.getElementById("chat-box");

    // If the response is an object, get the 'response' property
    if (typeof response === 'object' && response !== null && 'response' in response) {
        response = response.response;
    }

    // Create a mapping between options and responses
    var optionResponses = {
        "Direktor/Şöbə Rəisi": "İdarə Heyəti (Maliyyə menecmenti departamentinin təklifi ilə)",
        "Direktor müavini": "Struktur bölmə rəhbəri (Əlavə ƏFG təyin olunmadığı təqdirdə direktorun ƏFG-na bərabər götürülür)",
        "Menecer/Baş Mütəxəssis/Bölmə rəhbəri/Qrup rəhbəri": "Struktur bölmə rəhbəri",
        "Struktur Bölmə Rəhbəri": "Şöbədə çalışan digər əməkdaşlar Çalışdığı strukturun ƏFG və hədəflərinə bərabər götürülür",
        "Şöbədə çalışan digər əməkdaşlar": "Çalışdığı strukturun ƏFG və hədəflərinə bərabər götürülür"
    };

    // Check if the response is a specific message

    if (response === "Təəssüf edirəm, sualınıza cavab verə bilmirəm. FAQ hissəsinə keçə bilərsiniz") {
        // Create a FAQ button
        var faqButton = document.createElement("button");
        // show response
        var botLabel = createMessageElement("bot-label", "Bizdən Biri");
        botLabel.classList.add("with-icon");
        var botMessage = createMessageElement("bot-message", response);
        chatBox.appendChild(botLabel);
        chatBox.appendChild(botMessage);
        faqButton.textContent = "FAQ";
        faqButton.onclick = displayCategories;
        chatBox.appendChild(faqButton);
        scrollToBottom();

    } else if (response.includes("Direktor/ şöbə rəisi")) {
        // Display a specific message
        var specificMessage = document.createElement("div");
        specificMessage.textContent = "Daha dəqiq məlumat almaq üçün vəzifə kategoriyasını seçin :";
        chatBox.appendChild(specificMessage);

        // Create buttons for each option
        var options = Object.keys(optionResponses);
        options.forEach(function(option) {
            var optionButton = document.createElement("button");
            optionButton.textContent = option;
            optionButton.onclick = function() {
                // Handle the user's selection
                var botLabel = createMessageElement("bot-label", "Bizdən Biri");
                botLabel.classList.add("with-icon");
                displaySelectedResponse(optionResponses[option]);
            };
            chatBox.appendChild(optionButton);
        });
    } else {
        // If the response does not include the specific substring, display it as usual
        var botLabel = createMessageElement("bot-label", "Bizdən Biri");
        botLabel.classList.add("with-icon");
        var botMessage = createMessageElement("bot-message", response);
        chatBox.appendChild(botLabel);
        chatBox.appendChild(botMessage);
    }

    scrollToBottom();
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

function displayCategories() {
    // Clear the chat box
    chatBox.innerHTML = '';
    var chatBox = document.getElementById("chat-box");


    // Display the FAQ categories
    var categories = ['Category 1', 'Category 2', 'Category 3']; // Replace with your actual categories
    categories.forEach(function(category) {
        var categoryButton = document.createElement("button");
        categoryButton.textContent = category;
        categoryButton.onclick = function() {
            // Handle the user's selection
            displayFAQ(category);
        };
        chatBox.appendChild(categoryButton);
    });

    scrollToBottom();
}

function displayFAQ(category) {
    // Display the FAQ for the selected category
    // This is just a placeholder. Replace with your actual implementation.
    var faqMessage = document.createElement("div");
    faqMessage.textContent = 'FAQ for ' + category;
    chatBox.appendChild(faqMessage);

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

/// Function to save chat with a specified name
function saveChat(name) {
    // Get the chat messages
    var chatBox = document.getElementById("chat-box");
    var chatMessages = Array.from(chatBox.children).map(function(messageElement) {
        return {
            sender: messageElement.className,
            content: messageElement.textContent,
            timestamp: new Date().toISOString() // Add a timestamp
        };
    });

    // Serialize the chat messages
    var chatData = JSON.stringify(chatMessages);

    // Save the chat data in local storage with the specified name
    localStorage.setItem(name, chatData);
}

// Function to display saved chats
function displaySavedChats() {
    // Get the saved chats from local storage
    var savedChats = Object.keys(localStorage).filter(function(key) {
        return !["chatData", "length"].includes(key); // Exclude keys used for other purposes
    });

    // Sort saved chats by timestamp
    savedChats.sort(function(a, b) {
        return new Date(getTimestamp(b)) - new Date(getTimestamp(a));
    });

    // Display saved chats
    var savedChatsSection = document.getElementById("saved-chats");
    savedChatsSection.innerHTML = ''; // Clear existing saved chats

    // Limit the number of saved chats to 5
    savedChats.slice(0, 5).forEach(function(chatName) {
        var chatData = JSON.parse(localStorage.getItem(chatName));
        var chatTimestamp = new Date(getTimestamp(chatName));
        var chatSquare = document.createElement("div");
        chatSquare.className = "saved-chat";
        chatSquare.textContent = formatTimestamp(chatTimestamp) + " - " + chatName.split(' - ')[0];
        chatSquare.onclick = function() {
            displaySavedChat(chatData);
        };

        // Create a delete button for each chat
        var deleteButton = document.createElement("button");
        deleteButton.textContent = "Delete";
        deleteButton.onclick = function(event) {
            event.stopPropagation(); // Prevent triggering chatSquare's onclick
            deleteChat(chatName);
        };
        chatSquare.appendChild(deleteButton);

        savedChatsSection.appendChild(chatSquare);
    });
}
// Function to delete a saved chat
function deleteChat(chatName) {
    // Remove the chat from local storage
    localStorage.removeItem(chatName);

    // Refresh the display of saved chats
    displaySavedChats();
}
// Function to extract timestamp from chat name
function getTimestamp(chatName) {
    var timestampStr = chatName.split(' - ')[1];
    var timestamp = new Date(timestampStr);
    if (isNaN(timestamp.getTime())) {
        // The string is not a valid date, return current date/time
        return new Date();
    } else {
        return timestamp;
    }
}

// Function to format timestamp
function formatTimestamp(timestamp) {
    var now = new Date();
    var diff = now - timestamp;

    // Calculate the difference in days
    var days = Math.floor(diff / (1000 * 60 * 60 * 24));

    if (days === 0) {
        return "today";
    } else if (days === 1) {
        return "yesterday";
    } else if (days <= 7) {
        return "last week";
    } else if (days <= 30) {
        return "last month";
    } else {
        // Format the timestamp in a custom way if it's more than 30 days ago
        return timestamp.toLocaleDateString();
    }
}

// Function to display a saved chat
function displaySavedChat(chatData) {
    // Clear the chat box
    var chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = '';

    // Display the saved chat messages
    chatData.forEach(function(message) {
        var messageElement = document.createElement("div");
        messageElement.className = message.sender;
        messageElement.textContent = message.content;
        chatBox.appendChild(messageElement);
    });
}


// Function to load chat
function loadChat(chatName) {
    // Get the chat data from local storage
    var chatData = localStorage.getItem(chatName);

    // Check if there's any chat data to load
    if (chatData) {
        // Parse the chat data
        var chatMessages = JSON.parse(chatData);

        // Clear the chat box
        var chatBox = document.getElementById("chat-box");
        chatBox.innerHTML = '';

        // Display the chat messages
        chatMessages.forEach(function(message) {
            var messageElement = document.createElement("div");
            messageElement.className = message.sender;
            messageElement.textContent = message.content;
            chatBox.appendChild(messageElement);
        });
    }
}

// Initialize the chat when the window loads
window.onload = function() {
    loadChat(); // Load the chat
    displayInitialMessage();
    document.getElementById('new-chat-button').addEventListener('click', createNewChat);

    // Add event listener for the "Enter" key press in the input field
    document.getElementById("user-input").addEventListener("keydown", function(event) {
        if (event.keyCode === 13) { // Check if the key pressed is "Enter"
            sendQuestion(); // Call the sendQuestion function
            handleNewMessage(); // Handle the new message
        }
    });

    // Autosave the chat every few minutes
    setInterval(saveChat, 5 * 60 * 1000); // 5 minutes

    // Display saved chats
    displaySavedChats();
};

// Function to handle a new message
function handleNewMessage(message) {
    // Add the new message to the current chat
    currentChat.push(message);

    // Display the new message
    displayMessage(message);
}

// Function to end the chat and save it
function endChat() {
    // Get the current date
    var currentDate = new Date();
  
    // Format the current date as "yyyy-mm-dd"
    var formattedDate = currentDate.toISOString().split('T')[0];

    // Save the current chat in local storage with the formatted date as the chat name
    saveChat(formattedDate);

    // Clear the current chat
    currentChat = [];
}

// Function to create a new chat
function createNewChat() {
    // End the current chat and save it
    endChat();

    // Clear the chat box
    var chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = '';

    // Display the initial message
    displayInitialMessage();
}