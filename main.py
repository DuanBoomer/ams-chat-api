from fastapi import FastAPI
import socketio

app = FastAPI()

origins = [
    "http://localhost:3000", "https://alumni-mapping-system.vercel.app"
]

sio=socketio.AsyncServer(cors_allowed_origins=origins,async_mode='asgi')
socket_app = socketio.ASGIApp(sio)
app.mount("/", socket_app)

@app.get("/")
def read_root():
    return {"Chat": "Opened"}

@sio.on('msg')
async def client_side_receive_msg(sid, msg):
    await sio.emit("msg", str(msg))