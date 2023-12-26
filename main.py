from fastapi import FastAPI
import socketio
import motor.motor_asyncio
import datetime

app = FastAPI()

# uri = os.getenv("MONGODB")
uri = "mongodb+srv://chirag1292003:12092003Duan@alumni-mapping-system-d.iryfq1v.mongodb.net/?retryWrites=true&w=majority"
client = motor.motor_asyncio.AsyncIOMotorClient(uri)
database = client.alumni_mapping_system
chat_collection = database.chat

print(datetime.datetime.now())

origins = [
    "http://localhost:3000", "https://alumni-mapping-system.vercel.app"
]

sio=socketio.AsyncServer(cors_allowed_origins=origins,async_mode='asgi')
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

@app.get("/")
async def read_root():
    return {"Chat": "Opened"}

@sio.on('fetch')
async def get_intial_data(sid, alumni):
    data = await chat_collection.find_one({"alumni": alumni})
    print(data)

@sio.on('msg')
async def client_side_receive_msg(sid, msg, alumni, student):
    chat_collection.update_one(
        {"alumni": alumni}, {"$push": {"chat": {
            "time": datetime.datetime.now(),
            "sender": student,
            "chat": msg
        }}}
    )
    await sio.emit("msg", str(msg))