from typing import Dict


class TreeNodeUser:
    all_node_users: Dict[str, "TreeNodeUser"] = {}
    def __init__(self,id, label=None):
        self.id = id
        self.label = label or id
        self.all_node_users[id] = self

    
    @staticmethod
    def nick(id):
        return __class__.all_node_users[id].label
    
    @staticmethod
    def profilepic(id):
        return "0"