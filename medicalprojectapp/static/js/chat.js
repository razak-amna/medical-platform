// document.addEventListener('DOMContentLoaded', function() {
//     const chatForm = document.getElementById('chat-form');
//     const userMessageInput = document.getElementById('user-message');
//     const chatContainer = document.getElementById('chat-container');
    
//     // Check if chatContainer exists
//     if (!chatContainer) {
//         console.error("chat-container not found!");
//         return;
//     }

//     // CSRF token for POST requests
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//     chatForm.addEventListener('submit', function(event) {
//         event.preventDefault();
//         const userMessage = userMessageInput.value;
//         userMessageInput.value = '';

//         // Display the user's message in the chat container
//         const userMessageElement = document.createElement('div');
//         userMessageElement.textContent = 'You: ' + userMessage;
//         chatContainer.appendChild(userMessageElement);

//         // Send the message to the server and get a response
//         fetch('/chatbot/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded',
//                 'X-CSRFToken': csrftoken,  // CSRF token for security
//             },
//             body: `message=${encodeURIComponent(userMessage)}`,  // Send the message in URL-encoded format
//         })
//         .then(response => response.json())  // Parse the response as JSON
//         .then(data => {
//             // Display the bot's response in the chat container
//             const botMessageElement = document.createElement('div');
//             botMessageElement.textContent = 'Bot: ' + data.bot_response;  // Use the bot response from the JSON data
//             chatContainer.appendChild(botMessageElement);
//         })
//         .catch(error => console.error('Error:', error));  // Log any errors
//     });
// });

// document.addEventListener('DOMContentLoaded', function() {
//     const chatForm = document.getElementById('chat-form');
//     const userMessageInput = document.getElementById('user-message');
//     const chatContainer = document.getElementById('chat-container');
    
//     // CSRF token for POST requests
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//     chatForm.addEventListener('submit', function(event) {
//         event.preventDefault();
//         const userMessage = userMessageInput.value;
//         userMessageInput.value = '';  // Clear input field

//         // Display the user's message in the chat container
//         const userMessageElement = document.createElement('div');
//         userMessageElement.textContent = 'You: ' + userMessage;
//         chatContainer.appendChild(userMessageElement);

//         // Send the message to the server and get a response
//         fetch('/chatbot/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded',
//                 'X-CSRFToken': csrftoken,  // CSRF token for security
//             },
//             body: `user_message=${encodeURIComponent(userMessage)}`,  // Send the message in URL-encoded format
//         })
//         .then(response => response.json())  // Parse the response as JSON
//         .then(data => {
//             // Display the bot's response in the chat container
//             const botMessageElement = document.createElement('div');
//             botMessageElement.textContent = 'Bot: ' + data.bot_response;  // Use the bot response from the JSON data
//             chatContainer.appendChild(botMessageElement);
//         })
//         .catch(error => console.error('Error:', error));  // Log any errors
//     });
// });
// document.addEventListener('DOMContentLoaded', function() {
//     const chatForm = document.getElementById('chat-form');
//     const userMessageInput = document.getElementById('user-message');
//     const chatContainer = document.getElementById('chat-container');
    
//     // CSRF token for POST requests
//     const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

//     chatForm.addEventListener('submit', function(event) {
//         event.preventDefault();
//         const userMessage = userMessageInput.value;
//         userMessageInput.value = '';  // Clear input field

//         // Display the user's message in the chat container
//         const userMessageElement = document.createElement('div');
//         userMessageElement.textContent = 'You: ' + userMessage;
//         chatContainer.appendChild(userMessageElement);

//         // Send the message to the server and get a response
//         fetch('/chatbot/', {
//             method: 'POST',
//             headers: {
//                 'Content-Type': 'application/x-www-form-urlencoded',
//                 'X-CSRFToken': csrftoken,  // CSRF token for security
//             },
//             body: `user_message=${encodeURIComponent(userMessage)}`,  // Send the message in URL-encoded format
//         })
//         .then(response => response.json())  // Parse the response as JSON
//         .then(data => {
//             // Check if data has bot_response
//             console.log(data);  // Log the response to see the structure

//             if (data.bot_response) {
//                 // Display the bot's response in the chat container
//                 const botMessageElement = document.createElement('div');
//                 botMessageElement.textContent = 'Bot: ' + data.bot_response;  // Use the bot response from the JSON data
//                 chatContainer.appendChild(botMessageElement);
//             } else {
//                 // If bot_response is missing
//                 console.error('Bot response missing from the data:', data);
//             }
//         })
//         .catch(error => console.error('Error:', error));  // Log any errors
//     });
// });
document.addEventListener('DOMContentLoaded', function() {
    const chatForm = document.getElementById('chat-form');
    const userMessageInput = document.getElementById('user-message');
    const chatContainer = document.getElementById('chat-container');

    // CSRF token for POST requests
    const csrftoken = document.querySelector('[name=csrfmiddlewaretoken]').value;

    chatForm.addEventListener('submit', function(event) {
        event.preventDefault();

        const userMessage = userMessageInput.value.trim();

        // Validate input
        if (!userMessage) {
            alert('Please enter a message!');
            return;
        }

        // Clear input field and disable inputs
        userMessageInput.value = '';
        userMessageInput.disabled = true;
        chatForm.querySelector('button').disabled = true;

        // Display the user's message in the chat container
        const userMessageElement = document.createElement('div');
        userMessageElement.className = 'chat-message user-message';
        userMessageElement.textContent = 'You: ' + userMessage;
        chatContainer.appendChild(userMessageElement);

        // Auto-scroll to the bottom
        chatContainer.scrollTop = chatContainer.scrollHeight;

        // Send the message to the server and get a response
        fetch('/chatbot/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
                'X-CSRFToken': csrftoken, // CSRF token for security
            },
            body: `user_message=${encodeURIComponent(userMessage)}`, // Send the message in URL-encoded format
        })
        .then(response => response.json()) // Parse the response as JSON
        .then(data => {
            console.log(data); // Log the response to see the structure

            // Check if data has bot_response
            if (data.bot_response) {
                const botMessageElement = document.createElement('div');
                botMessageElement.className = 'chat-message bot-response';
                botMessageElement.textContent = 'Bot: ' + data.bot_response; // Use the bot response from the JSON data
                chatContainer.appendChild(botMessageElement);
            } else {
                console.error('Bot response missing from the data:', data);
                const errorElement = document.createElement('div');
                errorElement.className = 'chat-message bot-response';
                errorElement.textContent = 'Bot: Sorry, I didn’t understand that.';
                chatContainer.appendChild(errorElement);
            }

            // Auto-scroll to the bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
        })
        .catch(error => {
            console.error('Error:', error);
            const errorElement = document.createElement('div');
            errorElement.className = 'chat-message bot-response';
            errorElement.textContent = 'Bot: Sorry, there was an error processing your message. Please try again.';
            chatContainer.appendChild(errorElement);

            // Auto-scroll to the bottom
            chatContainer.scrollTop = chatContainer.scrollHeight;
        })
        .finally(() => {
            // Re-enable input and button
            userMessageInput.disabled = false;
            chatForm.querySelector('button').disabled = false;
        });
    });
});

