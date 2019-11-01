import asyncio
from aiohttp import web
from aiohttp_sse import sse_response
from models import Chat
import motor.motor_asyncio
import pymongo

routes = web.RouteTableDef()
client = motor.motor_asyncio.AsyncIOMotorClient()
db = client.livechan_db
chat_dbs = db.chat_dbs
serializer = Chat()


@routes.get(r'/messages/{board:\S+}')
async def messages(request):
    board = request.match_info['board']
    cursor = chat_dbs.find({'chat': board}, cursor_type=pymongo.CursorType.TAILABLE)
    async with sse_response(request) as res:
        while True:
            if not cursor.alive:
                await asyncio.sleep(0.1)
                cursor = chat_dbs.find({'chat': board}, cursor_type=pymongo.CursorType.TAILABLE, await_data = True)
                async for message in cursor:
                    data = serializer.dump(message)
                    res.send(data, event='chat')
        return res


@routes.get(r'/last/{board:\S+}/{count:\d+}')
async def last(request):
    board = request.match_info['board']
    count = request.match_info['count']
    limit = request.query.get('limit', '')
    limit = int(limit) if limit.isnumeric() else 50
    cursor = chat_dbs.find({'chat': board, 'count': {'$gt': count}})
    cursor = cursor.sort([('count', pymongo.DESCENDING)]).limit(limit)
    rows = await cursor.to_list(limit)
    res = serializer.dump(rows, many=True)
    return web.json_response(res)


@routes.get(r'/data/{board:\S+}')
async def data(request, ops=False):
    board = request.match_info['board']
    query = {}
    limit = request.query.get('limit', '')
    limit = int(limit) if limit.isnumeric() else 100
    if limit < 1 or limit > 2000:
        limit = 100
    if board != 'all':
        query['chat'] = {'chat': board}
    if ops:
        query['is_convo_op'] = True
        limit = 15
    cursor = chat_dbs.find({'chat': board})
    cursor = cursor.sort([('count', pymongo.DESCENDING)]).limit(limit)
    rows = await cursor.to_list(limit)
    res = serializer.dump(rows, many=True)
    return web.json_response(res)


@routes.get(r'/data_convo/{board:[\w\d]+}')
async def ops(request):
    return await data(request, True)


app = web.Application()
app.add_routes(routes)
web.run_app(app)

