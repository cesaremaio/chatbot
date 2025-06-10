from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse
from sse_starlette.sse import EventSourceResponse
from src.inference.invoke_model import ModelClient
import asyncio
import json
router = APIRouter()

clients = set()

@router.post("/sse/send")
async def sse_send(request: Request):
    data = await request.json()
    user_message = data.get("message")
    if not user_message:
        return JSONResponse({"error": "No message provided"}, status_code=400)
    # Store the message for broadcasting
    for queue in clients:
        await queue.put(user_message)
    return {"status": "sent"}

@router.get("/sse/stream")
async def sse_stream(request: Request):
    queue = asyncio.Queue()
    clients.add(queue)
    chatbot_client = ModelClient()

    async def event_generator():
        try:
            while True:
                user_message = await queue.get()

                # RAG PIPELINE HERE





                bot_response = await chatbot_client.invoke_model(prompt=user_message)
                data = {
                    "type": "response",
                    "message": bot_response.output
                }
                yield {
                    "event": "message",
                    "data": json.dumps(data)
                }
        except asyncio.CancelledError:
            pass
        finally:
            clients.remove(queue)

    return EventSourceResponse(event_generator())


@router.post("/invoke-model")
async def invoke_model(prompt: str):
    client = ModelClient()
    try:
        response = await client.invoke_model(prompt=prompt)
        return response.output
    except Exception as e:
        raise e
    




# @router.websocket("/ws/chat")
# async def websocket_endpoint(websocket: WebSocket):
#     await websocket.accept()
#     chatbot_client = ModelClient()
#     try:
#         while True:
#             # Receive message from client
#             data = await websocket.receive_text()
#             message_data = json.loads(data)
            
#             if message_data["type"] == "message":
#                 user_message = message_data["message"]
                
#                 # Process the message with your chatbot logic here
#                 bot_response = await chatbot_client.invoke_model(prompt=user_message) 
#                 bot_response = bot_response.output
                
#                 # Send response back to client
#                 await websocket.send_text(json.dumps({
#                     "type": "response",
#                     "message": bot_response
#                 }))
                
#     except WebSocketDisconnect:
#         print("Client disconnected")