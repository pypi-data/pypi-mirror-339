from __future__ import annotations

from typing import Literal, Optional
__all__ = (
    'CustomisedTreeUser',
)



class CustomisedTreeUser:
    """
    A class to hold the custom tree setup for a given user.
    """

    __slots__ = (
        'id',
        'edge',
        'node',
        'font',
        'highlighted_font',
        'highlighted_node',
        'background',
        'direction',
    )
    allctus = {}

    def __init__(
            self,
            user_id: int=0,
            *,
            edge: Optional[int] = None,
            node: Optional[int] = None,
            font: Optional[int] = None,
            highlighted_font: Optional[int] = None,
            highlighted_node: Optional[int] = None,
            background: Optional[int] = None,
            direction: Literal["TB", "LR"] = "TB"):
        self.id = user_id
        self.edge = edge
        self.node = node
        self.font = font
        self.highlighted_font = highlighted_font
        self.highlighted_node = highlighted_node
        self.background = background
        self.direction = direction
        self.allctus[user_id] = self

    def to_json(self) -> dict:

        return {
            "user_id": self.id,
            "edge": self.edge,
            "node": self.node,
            "font": self.font,
            "highlighted_font": self.highlighted_font,
            "highlighted_node": self.highlighted_node,
            "background":self.background,
            "direction":self.direction
        }

    @classmethod
    def from_json(cls, data: dict) -> CustomisedTreeUser:
        """
        Loads an FamilyTreeMember object from JSON.

        Parameters
        ----------
        data : dict
            The JSON object that represent the FamilyTreeMember object.

        Returns
        -------
        FamilyTreeMember
            The new FamilyTreeMember object.
        """

        return cls(**data)


    @classmethod
    def get_by_id(cls, id: int) -> CustomisedTreeUser:
        
        if id in cls.allctus:
            return cls.allctus[id]
        obj = cls(id)
        cls.allctus[id]=obj
        return obj

    @property
    def hex(self) -> dict:
        """
        The conversion of the user's data into some quotes hex strings
        that can be passed directly to Graphviz.
        Provides deafults.
        """

        # Get our defaults
        default_hex = self.get_default_hex()

        # Get our attrs
        attrs = (
            "edge",
            "font",
            "node",
            "highlighted_font",
            "highlighted_node",
            "background",
        )

        # Fill up a dict
        ret = {}
        for i in attrs:
            v = getattr(self, i)
            if v is None:
                v = default_hex[i]
            elif v < 0:
                v = "transparent"
            else:
                v = f'"#{v:0>6X}"'
            ret[i] = v
        ret["direction"] = self.direction

        # And return
        return ret

    @property
    def unquoted_hex(self) -> dict:
        """
        The same as self.hex, but strips out the quote marks from the items.
        Pretty much directly passed into a website's CSS.
        """

        # Just strip the quote marks from the items
        return {
            i: o.strip('"')
            for i, o
            in self.hex.items()
        }

    @staticmethod
    def get_default_hex() -> dict:
        """
        The default hex codes that are used, quoted.
        """

        return {
            'edge': '"#FF0000"',
            'node': '"#FFFFFF00"',#'"#FFB6C1"',
            'font': '"#000000"',
            'highlighted_font': '"#FF0000"',#'"#FFFFFF"',
            'highlighted_node':  '"#FFFFFF00"',#'"#FFFFFF00"',#  '"#0000FF"',
            'background': '"#ADD8E6"',#'"#E5C889"',#
            'direction': '"TB"',
        }

    @classmethod
    def get_default_unquoted_hex(cls) -> dict:
        """
        The default hex codes that are used, unquoted. Pretty much directly passed into a website's CSS.
        """

        return {
            i: o.strip('"')
            for i, o
            in cls.get_default_hex().items()
        }
    


    def get_all(self) -> dict[int, CustomisedTreeUser]:
        return self.allctus


