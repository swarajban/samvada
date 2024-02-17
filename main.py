from fastapi import FastAPI
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse

app = FastAPI()


@app.get("/health")
async def read_root():
    return {"health": "ok"}


@app.post("/incoming_call")
async def handle_incoming_call():
    response = VoiceResponse()
    response.say("You are a bagel.")
    response.hangup()
    return Response(content=str(response), media_type="application/xml")
