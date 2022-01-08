from channels.consumer import SyncConsumer, AsyncConsumer, StopConsumer
from time import sleep
import asyncio
import json
from asgiref.sync import async_to_sync



# ###############################################################################################
# FOLLOWING class is sync
class MySyncConsumer(SyncConsumer):
    def websocket_connect(self, event):
        print("websocket connect", event)

        print("channel layer", self.channel_layer) 
        print("channel name", self.channel_name) 

        # print(self.scope["url_route"]["kwargs"]["groupkname"])
        self.groupName = self.scope["url_route"]["kwargs"]["groupkname"]    # this is the group name we are getting from frontend

        # adding channel to new or existing Group
        async_to_sync(self.channel_layer.group_add)(
            self.groupName,     # this is group name
            self.channel_name
        ) # here we are making it sync becuase defaultly it is async

        self.send({
            'type':'websocket.accept'    
        })

    def websocket_receive(self, event):
        print("message receive", event)
        print("message received from client", event['text']) 

        async_to_sync(self.channel_layer.group_send)(
            self.groupName, {
            'type':"chat.message",    # here we are using following defined function
            'message':event['text']   # <---------------------------|
        })                            # ----------------------------|
                                      # ----------------------------|
    def chat_message(self, event):    # ----------------------------|
        print("chat_message .....  ", event) # ---------------------|
        print("actual data  ", event["message"])  # which is defined above 
        self.send({
            'type':"websocket.send",
            'text':event["message"]
        })

    
    def websocket_disconnect(self, event):
        print("websocket disconnect", event)

        print("channel layer", self.channel_layer)  # get default channel layer
        print("channel name", self.channel_name)  # get channel name

        # removing channel from Group if it exits
        async_to_sync(self.channel_layer.group_discard)(
            self.groupName,     # this is group name
            self.channel_name
        ) # here we are making it sync becuase defaultly it is async

        raise StopConsumer()            # to stop client from sending data after disconnect
        




# ###############################################################################################
# FOLLOWING class is async
class MyAsyncConsumer(AsyncConsumer):
    async def websocket_connect(self, event):
        print("websocket connect", event)

        print("channel layer", self.channel_layer)  # get default channel layer
        print("channel name", self.channel_name)  # get channel name

        self.groupName = self.scope["url_route"]["kwargs"]["groupkname"]

        # adding channel to new or existing Group
        await self.channel_layer.group_add(
            self.groupName,     # this is group name
            self.channel_name
        ) # here we are making it sync becuase defaultly it is async

        await self.send({
            'type':'websocket.accept'    
        })

    async def websocket_receive(self, event):
        print("message receive", event)
        print("message received from client", event['text']) 

        await self.channel_layer.group_send(self.groupName, {
            'type':"chat.message",    # here we are using following defined function
            'message':event['text']   # <---------------------------|
        })                            # ----------------------------|
                                      # ----------------------------|
    async def chat_message(self, event):    # ----------------------------|
        print("chat_message .....  ", event) # ---------------------|
        print("actual data  ", event["message"])  # which is defined above 
        
        await self.send({
            'type':"websocket.send",
            'text':event["message"]
        })

    
    async def websocket_disconnect(self, event):
        print("websocket disconnect", event)

        print("channel layer", self.channel_layer)  # get default channel layer
        print("channel name", self.channel_name)  # get channel name

        # removing channel from Group if it exits
        await self.channel_layer.group_discard(
            self.groupName,     # this is group name
            self.channel_name
        ) # here we are making it sync becuase defaultly it is async

        raise StopConsumer()            # to stop client from sending data after disconnect
        
