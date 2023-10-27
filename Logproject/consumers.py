# consumers.py

from channels.generic.websocket import AsyncWebsocketConsumer
from alertlog.models import Filterlog

class DataConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        # Accept the WebSocket connection
        await self.accept()

        # Retrieve data from the SQLite database
        data = Filterlog.objects.all().values()

        # Send the data to the frontend
        await self.send_json(list(data))