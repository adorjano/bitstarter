from typing import Dict, Callable, List, Tuple, Any
from nostr.event import Event
from nostr.key import PrivateKey, PublicKey
from nostr.relay_manager import RelayManager
from nostr.filter import Filter, Filters
from nostr.message_type import ClientMessageType
import nostr.relay
import time
import ssl
import json
import inspect

def convert_tags(tags):
    from collections import defaultdict
    d = defaultdict(list)

    for k,v in tags:
        d[k].append(v)
    
    return d

class Bitstarter:
    def __init__(self):
        self.private_key = PrivateKey(b'6\r\xc1\xe4z!p\xc3\xa7G{:@\x1c\x10\x03\x93T\xc0s\x12\x8fog;\xf5\xc9\xd5\xe1)"\xc5')
        self.public_key = self.private_key.public_key
        
        self.kind = 1337
        
        filter = Filter(kinds=[self.kind])
        filters_events = Filters([filter])
        sub_id_events = "global_fetch"

        filter = Filter(authors=[self.public_key.hex()],kinds=[0])
        filters_profile = Filters([filter])
        sub_id_profile = "fetch_profile"

        self.relay_manager = RelayManager()
        #self.relay_manager.add_relay("wss://nostr-pub.wellorder.net")
        self.relay_manager.add_relay("wss://relay.damus.io")
        #self.relay_manager.add_relay("wss://nostramsterdam.vpx.moe")
        self.relay_manager.add_subscription(sub_id_events, filters_events)
        self.relay_manager.add_subscription(sub_id_profile, filters_profile)
        self.relay_manager.open_connections({"cert_reqs": ssl.CERT_NONE}) # NOTE: This disables ssl certificate verification
        time.sleep(1.25) # allow the connections to open

    def post_event(self, kind: int, content: str, tags: List[List[str]] = None) -> str:
        if tags is None:
            tags = []
        tags.append(["plattform", "bitstarter"])
        created_at = int(time.time())
        event = Event(content=content, public_key=self.public_key.hex(), created_at=created_at, kind=kind, tags=tags)
        self.private_key.sign_event(event)
        try:
            self.relay_manager.publish_event(event)
            return event.id
        except Exception as e:
            print("Failed:", e)
            return -1
    
    def get_event(self, event_id: str) -> Event:
        filter = Filter(event_ids=[event_id])
        filters = Filters([filter])
        request = [ClientMessageType.REQUEST, "global_fetch"]
        request.extend(filters.to_json_array())
        message = json.dumps(request)
        
        self.relay_manager.update_subscription("global_fetch", filters)
        self.relay_manager.publish_message(message)
        time.sleep(3)

        events = self.read_events()
        return events[0] if len(events) > 0 else None

    def get_profile(self, public_key: str) -> Dict[str, str]:
        filter = Filter(authors=[public_key],kinds=[0])
        filters_profile = Filters([filter])
        sub_id_profile = "fetch_profile"
        request = [ClientMessageType.REQUEST, sub_id_profile]
        request.extend(filters_profile.to_json_array())
        profile_request = request

        message = json.dumps(profile_request)
        self.relay_manager.update_subscription(sub_id_profile, filters_profile)
        self.relay_manager.publish_message(message)
        time.sleep(2)  # allow the messages to send

        events = self.read_events()
        events = sorted(events, key=lambda x: x.created_at, reverse=True)
            
        return json.loads(events[0].content)
    
    def update_profile(self, profile_data: Dict[str, str]) -> str:
        content = json.dumps(profile_data)
        return self.post_event(0, content)

    def post_idea(self, content:str, tags: Dict[str, str]) -> str:
        tags.append(['p', self.public_key.hex()])
        return self.post_event(self.kind, content, tags)

    def get_ideas(self):
        filter = Filter(kinds=[self.kind])
        filters = Filters([filter])
        request = [ClientMessageType.REQUEST, "global_fetch"]
        request.extend(filters.to_json_array())
        message = json.dumps(request)
        
        self.relay_manager.update_subscription("global_fetch", filters)
        self.relay_manager.publish_message(message)
        time.sleep(2) # allow the messages to send

        events = self.read_events()

        return events

    def post_comment(self, comment, event_id: str, author_pub: str) -> str:
        tags = [['e', event_id],['p', author_pub]]
        return self.post_event(self.kind+1, comment, tags=tags)
    
    def get_comments(self, event_id: str) -> List[Dict[str, str]]:
        filter = Filter(kinds=[self.kind+1], event_refs=[event_id])
        filters = Filters([filter])
        request = [ClientMessageType.REQUEST, "global_fetch"]
        request.extend(filters.to_json_array())
        
        message = json.dumps(request)
        self.relay_manager.update_subscription("global_fetch", filters)
        self.relay_manager.publish_message(message)
        time.sleep(2) # allow the messages to send

        ret = self.read_events()

        return ret

    def like_event(self, event_id: str) -> str:
        tags = [['e', event_id]]
        return self.post_event(self.kind+2, "", tags)

    def get_likes(self, e_id: str) -> int:
        filter = Filter(kinds=[self.kind+2], event_refs=[e_id])
        filters = Filters([filter])
        self.relay_manager.update_subscription("global_fetch", filters)

        request = [ClientMessageType.REQUEST, "global_fetch"]
        request.extend(filters.to_json_array())
        
        message = json.dumps(request)
        self.relay_manager.publish_message(message)
        time.sleep(2) # allow the messages to send

        ret = self.read_events()

        likes = {}
        for e in ret:
            likes[e.public_key] = True

        return len(likes)
            
    def read_events(self):
        ret = []
        while self.relay_manager.message_pool.has_events():
            event_msg = self.relay_manager.message_pool.get_event()
            if ['plattform', 'bitstarter'] in event_msg.event.tags:
                ret.append(event_msg.event)
            
        return ret

    def close_connections(self):
        self.relay_manager.close_connections()

if __name__ == '__main__':
    bitstarter = Bitstarter()

    print("Neuer Benutzer erstellt:")
    print(f"Private Key: {bitstarter.private_key.bech32()}")
    print(f"Public Key: {bitstarter.public_key.bech32()}\n")
    print(f"Public Key: {bitstarter.public_key.hex()}\n")
    '''
    '''
    profile_data = {"name": "John Doe", "about": "Softwareentwickler", "picture": "https://example.com/picture.jpg", "github": "https://github.com/bitsperity"}
    up_id = bitstarter.update_profile(profile_data)
    print(f"Profile updated: {up_id}")

    fetched_profile = bitstarter.get_profile(bitstarter.public_key.hex())
    print("Profilinformationen:")
    for key, value in fetched_profile.items():
        print(f"{key}: {value}")
    print()

    '''
    fetched_profile = bitstarter.fetch_profile('93be024443034915604d759b0222a1b7085eda86ee48c8b4a9a765d722a91aec')
    print("Profilinformationen:")
    for key, value in fetched_profile.items():
        print(f"{key}: {value}")
    print()
    '''

    content = "Hier der eigentliche Antrag"
    tags = [["title","Tolle App-Idee"],
            ["description", "Eine App, die das Leben leichter macht."], 
            ["category", "Mobile"]]
    
    idea_id = bitstarter.post_idea(content=content, tags=tags)
    print(f"Idee gepostet: {idea_id}\n")

    comment_id = bitstarter.post_comment("Ich finde diese Idee großartig!", idea_id, bitstarter.public_key.hex())
    print(f"Kommentar gepostet: {comment_id}\n")

    like_id = bitstarter.like_event(idea_id)
    print(f"Idee geliked: {like_id}\n")

    #print(f"Comment: {bitstarter.get_event(comment_id).to_message()}\n")
    #print(f"Like: {bitstarter.get_event(like_id).to_message()}\n")
    
    print("Ideen:")
    ideas = bitstarter.get_ideas()
    for i in ideas:
        tags = convert_tags(i.tags)
        print(f"ID: {i.id}")
        '''
        '''
        print(f"Titel: {tags['title']}")
        print(f"Description: {tags['description']}")
        print(f"Category: {tags['category']}")
        print(i.content)
        print("---")
        comments = bitstarter.get_comments(i.id)
        for c in comments:
            #print the author and the content
            print(f"{c.public_key}: {c.content}")

        print(f"Likes:{bitstarter.get_likes(i.id)}")
        print('-'*20)

        print()

    bitstarter.close_connections()