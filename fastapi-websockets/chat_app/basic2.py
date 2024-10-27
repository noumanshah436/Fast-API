from typing import Annotated

from fastapi import (
    Cookie,
    Depends,
    FastAPI,
    Query,
    WebSocket,
    WebSocketDisconnect,
    WebSocketException,
    status,
)
from fastapi.responses import HTMLResponse

app = FastAPI()

html = """
<!DOCTYPE html>
<html>
    <head>
        <title>Chat</title>
    </head>
    <body>
        <h1>WebSocket Chat</h1>
        <form action="" onsubmit="sendMessage(event)">
            <label>Item ID: <input type="text" id="itemId" autocomplete="off" value="foo"/></label>
            <label>Token: <input type="text" id="token" autocomplete="off" value="some-key-token"/></label>
            <button onclick="connect(event)">Connect</button>
            <hr>
            <label>Message: <input type="text" id="messageText" autocomplete="off"/></label>
            <button>Send</button>
        </form>
        <ul id='messages'></ul>

        <script>
            var ws = null;

            // Set a cookie with the name 'session' and a test value
            document.cookie = "session=my-session-cookie-value; path=/";

            // Function to retrieve a cookie value by name
            function getCookie(name) {
                const value = `; ${document.cookie}`;
                const parts = value.split(`; ${name}=`);
                if (parts.length === 2) return parts.pop().split(';').shift();
            }

            function connect(event) {
                var itemId = document.getElementById("itemId").value;
                var token = document.getElementById("token").value;
                var session = getCookie("session");

                // Create the WebSocket URL with query parameters
                var wsUrl = "ws://localhost:8000/items/" + itemId + "/ws?token=" + token + "&session=" + session;
                ws = new WebSocket(wsUrl);

                ws.onopen = function() {
                    console.log("WebSocket connection opened.");
                };

                ws.onmessage = function(event) {
                    var messages = document.getElementById('messages');
                    var message = document.createElement('li');
                    var content = document.createTextNode(event.data);
                    message.appendChild(content);
                    messages.appendChild(message);
                };

                ws.onclose = function() {
                    console.log("WebSocket connection closed.");
                };

                event.preventDefault();
            }

            function sendMessage(event) {
                var input = document.getElementById("messageText");
                ws.send(input.value);
                input.value = '';
                event.preventDefault();
            }
        </script>
    </body>
</html>
"""


@app.get("/")
async def get():
    return HTMLResponse(html)


async def get_cookie_or_token(
    websocket: WebSocket,
    session: Annotated[str | None, Cookie()] = None,
    token: Annotated[str | None, Query()] = None,
    session_from_query: Annotated[str | None, Query(alias="session")] = None,
):
    session = session or session_from_query
    print(f"session ------------------------ {session}")
    print(f"token ------------------------ {token}")
    if session is None and token is None:
        raise WebSocketException(code=status.WS_1008_POLICY_VIOLATION)
    return session or token


@app.websocket("/items/{item_id}/ws")
async def websocket_endpoint(
    *,
    websocket: WebSocket,
    item_id: str,
    q: str | None = None,
    cookie_or_token: Annotated[str, Depends(get_cookie_or_token)],
):
    await websocket.accept()
    try:
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Session cookie or query token value is: {cookie_or_token}")
            if q is not None:
                await websocket.send_text(f"Query parameter q is: {q}")
            await websocket.send_text(f"Message text was: {data}, for item ID: {item_id}")
    except WebSocketDisconnect:
        print("WebSocket disconnect")
