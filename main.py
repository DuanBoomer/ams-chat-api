from fastapi import FastAPI
import motor.motor_asyncio
import socketio
import datetime
import requests

app = FastAPI()

STATIC_API_URL = "https://ams-backend-bdx5.onrender.com"

origins = [
    "http://localhost:3000", "https://alumni-mapping-system.vercel.app", "https://ams-backend-bdx5.onrender.com"
]

uri = "mongodb+srv://chirag1292003:12092003Duan@alumni-mapping-system-d.iryfq1v.mongodb.net/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
database = client.alumni_mapping_system
chat_collection = database.chat

sio = socketio.AsyncServer(cors_allowed_origins=origins, async_mode='asgi')
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)


@app.get("/")
def read_root():
    return {"Chat": "Opened"}


@sio.on('msg')
async def client_side_receive_msg(sid, msg, student, alumni):
    await sio.enter_room(sid, alumni)
    try:
        chat_collection.update_one(
            {"alumni": alumni}, {"$push": {
                "chat": {"time": datetime.datetime.now(), "text": msg, "sender": student}}}
        )
        await sio.emit("msg", {"text": msg, "sender": student}, to=alumni)
    except:
        pass


@sio.on('event_updates')
async def client_side_event_update(sid, alumni):
    r = requests.get(url=f"{STATIC_API_URL}/event/history/{alumni}")
    data = r.json()
    await sio.emit("event_updates", data, to=alumni)
