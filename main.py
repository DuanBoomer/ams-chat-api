from fastapi import FastAPI
import motor.motor_asyncio
import socketio
import datetime

app = FastAPI()

origins = [
    "http://localhost:3000", "https://alumni-mapping-system.vercel.app"
]

uri = "mongodb+srv://chirag1292003:12092003Duan@alumni-mapping-system-d.iryfq1v.mongodb.net/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
database = client.alumni_mapping_system
chat_collection = database.chat

sio=socketio.AsyncServer(cors_allowed_origins=origins,async_mode='asgi')
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

@app.get("/")
def read_root():
    return {"Chat": "Opened"}

@sio.on('msg')
async def client_side_receive_msg(sid, msg, student, alumni):
    try:
        chat_collection.update_one(
            {"alumni": alumni}, {"$push": {"chat": {"time": datetime.datetime.now(), "text": msg, "sender": student}}}
        )
        await sio.emit("msg", {"text": msg, "sender": student})
    except:
        pass
