import asyncio
import json
import threading
import logging
import traceback
import uuid
import aiohttp

logger = logging.getLogger(__name__)

class KlipperClient:
    def __init__(self):
        self.session = None
        self.ws_url = ""
        self.ws_connect = None
        self.receive_task = None
        self.pending_requests = {}
        self.original_method_process = {}
        self.loop = None
    async def connect(self, host, port):

        self.session = aiohttp.ClientSession()
        self.ws_url = f"ws://{host}:{port}/websocket"
        self.ws_connect = await self.session.ws_connect(self.ws_url)

        self.receive_task = asyncio.create_task(self.receive_process())

    async def receive_process(self):
        async for msg in self.ws_connect:
            if msg.type == aiohttp.WSMsgType.TEXT:
                try:
                    message_data = json.loads(msg.data)
                    # requestに対してresponse
                    if "id" in message_data:
                        req_id = message_data["id"]
                        if req_id in self.pending_requests:
                            self.pending_requests[req_id]["response"] = message_data
                            self.pending_requests[req_id]["event"].set()
                    else:
                        method = message_data["method"]
                        if method in self.original_method_process:
                            self.original_method_process[method](message_data)
                        #methodに対しての処理
                except Exception:
                    logger.error(traceback.format_exc())
            elif msg.type == aiohttp.WSMsgType.CLOSED:
                break
            elif msg.type == aiohttp.WSMsgType.ERROR:
                break
    
    async def async_send_request(self, method, params=None):
        req_id = str(uuid.uuid4())
        request_data = {"jsonrpc":"2.0", "method":method, "id": req_id}
        if params != None:
            request_data["params"] = params
        # イベントを作成
        event = asyncio.Event()
        self.pending_requests[req_id] = {"event": event, "method":method, "response": None}
        await self.ws_connect.send_str(json.dumps(request_data))

        await event.wait()
        result = self.pending_requests[req_id]["response"]

        # 登録したエントリを削除
        del self.pending_requests[req_id]

        return result


    def add_method_process(self, method, func):
        self.original_method_process[method] = func

    async def close(self):
        if self.ws_connect is not None:
            await self.ws_connect.close()
        if self.session is not None:
            await self.session.close()
        if self.receive_task is not None:
            self.receive_task.cancel()
            try:
                await self.receive_task
            except asyncio.CancelledError:
                pass

    # サブスレッドのループ上でコルーチンを実行するラッパー
    def run_coroutine(self, coro):
        return asyncio.run_coroutine_threadsafe(coro, self.loop)

    def sync_connect(self, host, port):
        fut = self.run_coroutine(self.connect(host, port))
        fut.result()

    def sync_send_request(self, method, params=None):
        fut = self.run_coroutine(self.async_send_request(method, params))
        return fut.result()

    def sync_close(self):
        fut = self.run_coroutine(self.close())
        fut.result()
        self.loop = None
        self.thread = None
    
    def sync_send_gcode(self, gcodes):
        params = {"script": "\n".join(gcodes)}
        logger.debug(f"send gcode params: {params}")
        return self.sync_send_request("printer.gcode.script", params)
        
    def run(self, host, port):
        self.loop = asyncio.new_event_loop()
        self.thread = threading.Thread(target=self._start_loop, args=(self.loop,), daemon=True)
        self.thread.start()
        self.sync_connect(host, port)

    def _start_loop(self, loop):
        asyncio.set_event_loop(loop)
        loop.run_forever()
    
    
if __name__ == '__main__':
    import sys
    import time
    args = sys.argv
    host = args[1]
    port = int(args[2])

    kc = KlipperClient()

    def original_method(data):
        print(data["method"])
    
    # 1回目の接続
    print("First connection")
    kc.run(host, port)
    try:
        kc.add_method_process("notify_proc_stat_update", original_method)
        res = kc.sync_send_request("printer.info")
        print(res)
        time.sleep(3)
    finally:
        kc.sync_close()
    
    time.sleep(5)
    # 2回目の接続
    print("Second connection")
    kc.run(host, port)
    try:
        kc.add_method_process("notify_proc_stat_update", original_method)
        kc.sync_send_gcode(["G28 X Y"])
        res = kc.sync_send_request("printer.info")
        print(res)
        time.sleep(3)
    finally:
        kc.sync_close()
