from aiohttp import web
import socketio
from dotenv import dotenv_values
from scripts.utils.decode_img import save_bytes_as_png, make_video
import os
import json

temp = dotenv_values(".env")
framenum = {}
sio = socketio.AsyncServer()

app = web.Application()

sio.attach(app)

async def index(request):
    with open(os.path.join(os.getcwd(), "frontend", "index.html")) as f:
        return web.Response(text=f.read(), content_type='text/html')


@sio.on('message')
async def print_message(sid, message):
    frame = json.loads(message)

    if frame['frame'] == "start":
        framenum[frame['id']] = 0

    save_bytes_as_png(bytes(frame['frame']), os.path.join(temp['TEMP_VIDEO_PATH'], frame['id'], f"{framenum}.png"))

    framenum[frame['id']] += 1

    if frame == "end":
        framenum[frame['id']] = 0
        make_video(os.path.join(temp['TEMP_VIDEO_PATH'], frame['id']), os.path.join(temp['FINAL_VIDEO_PATH'], frame['id'], f"{frame['id']}.avi"))

app.router.add_get('/', index)


if __name__ == '__main__':
    web.run_app(app)