# Import necessary FastAPI modules
from fastapi import FastAPI, WebSocket
from fastapi.responses import HTMLResponse

# Initialize the FastAPI app
app = FastAPI()

# Define a simple HTML chat interface
html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <!-- Form for sending messages -->
        <form action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <!-- List to display chat messages -->
        <ul id='messages'>
        </ul>
        <script>
            // Establish a WebSocket connection to the server
            var ws = new WebSocket("ws://localhost:8000/ws");
            
            // Event handler for receiving messages from the server
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            
            // Function to send messages to the server
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)             // Send the input value to the server
                input.value = ''                 // Clear the input field after sending
                event.preventDefault()           // Prevent form from refreshing the page
            }
        </script>
    </body>
</html>
"""


# Define a GET route that returns the HTML page
@app.get("/")
async def get():
    return HTMLResponse(html)


# Define a WebSocket endpoint for chat communication
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()  # Accept the WebSocket connection
    while True:
        data = await websocket.receive_text()  # Receive message from the client
        # Send a response back to the client with the received message
        await websocket.send_text(f"Message text was: {data}")
