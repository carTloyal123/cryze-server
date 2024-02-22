import asyncio
import websockets
import json

class CryzeWebsocketServer:
    def __init__(self):
        """
        Initialize the server
        """
        self.max_size = 2**30  # 1GB
        self.server = None
        self.connected = set()
        self.subscriptions = {}  # New: Dictionary to manage subscriptions

    async def handle_subscription(self, message, websocket):
        """"
        This function handles the subscription and unsubscription messages.
        """
        try:
            data = json.loads(message)
            if data['type'] == 'Subscribe':
                topic = data['topic']
                if topic not in self.subscriptions:
                    self.subscriptions[topic] = set()
                self.subscriptions[topic].add(websocket)
                await websocket.send(json.dumps({"type": "Acknowledgement", "message": f"Subscribed to {topic}"}))
            elif data['type'] == 'Unsubscribe':
                topic = data['topic']
                if topic in self.subscriptions and websocket in self.subscriptions[topic]:
                    self.subscriptions[topic].remove(websocket)
                    await websocket.send(json.dumps({"type": "Acknowledgement", "message": f"Unsubscribed from {topic}"}))
        except json.JSONDecodeError:
            pass  # Ignore non-JSON messages or bad format

    async def echo(self, websocket):
        """
        This function handles the echo loop for the server which is the main loop.
        :param websocket: The websocket object
        """
        async for message in websocket:
            try:
                if isinstance(message, bytes):
                    # Handle binary frame data
                    await self.broadcast(websocket, message,  'video-stream', is_binary=True)
                else:
                    data = json.loads(message)
                    topic = data['topic']
                    await self.handle_subscription(message, websocket)
                    await self.broadcast(websocket, message, topic)
            except json.JSONDecodeError:
                print("Bad JSON")
            except KeyError as e:
                print("No topic: " + str(e))
            except Exception as e:
                print("Error in echo: " + str(e))

    async def broadcast(self,websocket, message, topic=None, is_binary=False):
        """
        This function broadcasts a message to all clients subscribed to a topic
        :param websocket: The websocket object
        :param message: The message to broadcast
        :param topic: The topic to broadcast to
        :param is_binary: Whether the message is binary or not
        """
        try:
            if topic in self.subscriptions:
                subscribers = self.subscriptions[topic]
                if is_binary:
                    tasks = [asyncio.create_task(ws.send(message)) for ws in subscribers if ws.open]
                else:
                    print(f"Broadcasting to {topic}")
                    tasks = [asyncio.create_task(ws.send(message)) for ws in subscribers if ws.open and ws != websocket]
                if tasks:
                    await asyncio.wait(tasks)

        except json.JSONDecodeError:
            print("Bad JSON")
        except KeyError as e:
            print("No topic: " + str(e))
        except Exception as e:
            print("Error in broadcast: " + str(e))

    async def on_connect(self, websocket, path):
        """
        This function is called when a new client connects to the server
        :param websocket: The websocket object
        :param path: The path of the connection
        """
        print(f"New connection: {path}")
        self.connected.add(websocket)

    async def on_disconnect(self, websocket, path):
        """
        This function is called when a client disconnects from the server
        :param websocket: The websocket object
        :param path: The path of the connection
        """
        print(f"Disconnected: {path}")
        self.connected.remove(websocket)
        # Remove from all subscriptions
        for subscribers in self.subscriptions.values():
            subscribers.discard(websocket)

    async def handler(self, websocket, path):
        """
        This function is called when a new client connects to the server
        :param websocket: The websocket object
        :param path: The path of the connection
        """
        try:
            await self.on_connect(websocket, path)
            await self.echo(websocket)
        except Exception as e:
            print(f"Echo failed: {e}")
        finally:
            await self.on_disconnect(websocket, path)

    def start(self, url='0.0.0.0', port=3030):
        """
        Start the server
        :param url: The IP address to listen on
        :param port: The port to listen on
        """
        self.server = websockets.serve(self.handler, url, port, max_size=None, max_queue=5)
        print("Running server! with max size: " + str(self.max_size) + " bytes")
        asyncio.get_event_loop().run_until_complete(self.server)
        asyncio.get_event_loop().run_forever()
