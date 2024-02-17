from typing import Annotated

from fastapi import FastAPI, Form, WebSocket
from fastapi.responses import Response
from twilio.twiml.voice_response import Connect, VoiceResponse, Stream, Parameter

BASE_HOST = 'samvada.ngrok.app'

app = FastAPI()


@app.get("/health")
async def read_root():
    return {"health": "ok"}


async def _say_something_twiml_response() -> VoiceResponse:
    response = VoiceResponse()
    n = 3
    h = ". ".join(["airplane"] * n)
    response.say(f"Hi Amaya? - what are some of your other favorite movies now? ", voice='woman')
    response.hangup()
    return response


@app.post("/incoming_call")
async def handle_incoming_call(CallSid: Annotated[str, Form()]):
    response = VoiceResponse()
    connect = Connect()
    ws_url = f"wss://{BASE_HOST}/ws"
    stream = Stream(name=CallSid, url=ws_url)
    stream.append(Parameter(name='test_name', value='test_value'))
    connect.append(stream)
    response.append(connect)
    # response = await _say_something_twiml_response()
    print(CallSid)
    return Response(content=str(response), media_type="application/xml")


@app.websocket("/ws")
async def websocket_handler(websocket: WebSocket):
    await websocket.accept()
    print('ws connection connected')
    while True:
        data = await websocket.receive_json()
        event = data.get('event')
        if event in ('connected', 'start'):
            print(f'Event: {event}')
        elif event == 'media':
            print(f"Received media: {data}")
        elif event == 'stop':
            print('ws connection stopped')
            break
    print('ws connection disconnected')
