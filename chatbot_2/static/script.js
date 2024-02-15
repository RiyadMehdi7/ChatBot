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

// Function to save chat
function saveChat() {
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

    // Save the chat data in local storage
    localStorage.setItem("chatData", chatData);
}

// Function to load chat
function loadChat() {
    // Get the chat data from local storage
    var chatData = localStorage.getItem("chatData");

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
            saveChat(); // Save the chat
        }
    });

    // Autosave the chat every few minutes
    setInterval(saveChat, 5 * 60 * 1000); // 5 minutes
};


// Function to create a new chat
function createNewChat() {
    // Clear the chat box
    var chatBox = document.getElementById("chat-box");
    chatBox.innerHTML = '';

    // Display the initial message
    displayInitialMessage();
}