from channels.consumer import SyncConsumer, AsyncConsumer, StopConsumer
from time import sleep
import asyncio
import json

class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("websocket connect", event)
        self.send({
            'type':'websocket.accept'    
        })

    def websocket_receive(self, event):
        print("message receive", event)
        print("message received from client", event['text'])   # to accept data from client in server 
        # ####################################################################################################
        # self.send({
        #     'type':'websocket.send',    # to send DATA from server to client
        #     'text':"This is message from Server to Client"
        # })

        # ####################################################################################################
        for i in range(10):
            self.send({
                'type':'websocket.send',    
                # 'text':str(i)
                'text':json.dumps({"counter":i})
            })
            sleep(1)
    
    def websocket_disconnect(self, event):
        print("websocket disconnect", event)
        raise StopConsumer()            # to stop client from sending data after disconnect
        
# #################################
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("websocket connect", event)
        await self.send({
            'type':'websocket.accept'    # to accept data from client in server
        })

    async def websocket_receive(self, event):
        print("message receive", event)
        print("message received from client", event['text'])
        # ####################################################################################################
        # await self.send({
        #     'type':'websocket.send',    # to send DATA from server to client
        #     'text':"This is message from Server to Client"
        # })
        
        # ####################################################################################################
        for i in range(10):
            await self.send({
                'type':'websocket.send',
                'text':str(i)
            })
            await asyncio.sleep(1)
    
    async def websocket_disconnect(self, event):
        print("websocket disconnect", event)
        raise StopConsumer()            # to stop client from sending data after disconnect