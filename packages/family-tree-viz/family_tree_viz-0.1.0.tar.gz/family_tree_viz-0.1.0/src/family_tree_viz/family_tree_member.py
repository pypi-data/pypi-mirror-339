from __future__ import annotations

import logging
import os
import random
import string
from typing import (
    TYPE_CHECKING,
    Dict,
    Tuple,
    List,
    Optional,
    Iterable,
    Union,
    Set,
    overload,
    Literal,
)
from .relationship_string_simplifier import (
    RelationshipStringSimplifier as Simplifier,
)
from .tree_user import TreeNodeUser as  User
from .customised_tree_user import CustomisedTreeUser



logger = logging.getLogger("log")

if TYPE_CHECKING:

    FamilyTreeMemberSetter = Union[
        "FamilyTreeMember",
        int,
    ]


def get_cluster_name(k: int = 5) -> str:
    return "".join([random.choice(string.ascii_uppercase) for _ in range(k)])




class FamilyTreeMember:
    """
    A class representing a member of a family.
    """

    all_users: Dict[Tuple[int, int], FamilyTreeMember] = {}
    INVISIBLE = "[shape=point,width=0.001,style=invis]"  # For the DOT script

    __slots__ = (
        "id",
        "_children",
        "_parent",
        "_partners",
        "_friends",
        "_guild_id",
        "_user"
    )

    def __init__(
        self,
        id: int,
        children: Optional[List[int]] = None,
        parent_id: Optional[int] = None,
        partners: Optional[List[int]] = None,
        friends: Optional[List[int]] = None,
        guild_id: int = 0,
        label: str = None,
    ):
        self.id: int = id
        self._children: List[int] = children or list()
        self._parent: Optional[int] = parent_id
        self._partners: List[int] = partners or list()
        self._friends: List[int] = friends or list()
        self._guild_id: int = guild_id
        self._user : User = User(id=id,label=label)
        self.all_users[(self.id, self._guild_id)] = self

    @classmethod
    def create_new(cls, uid, chat_id):
        FamilyTreeMember(
            uid,   guild_id=chat_id
        )
        FamilyTreeMember(uid)

    def __hash__(self):
        return hash(
            (
                self.id,
                self._guild_id,
            )
        )

    @overload
    def _get_user_id(self, value: FamilyTreeMemberSetter) -> int: ...

    @overload
    def _get_user_id(self, value: None) -> None: ...

    def _get_user_id(self, value: Optional[FamilyTreeMemberSetter]) -> Optional[int]:
        if value is None:
            return None
        if isinstance(value, int):
            return value
        return value.id


    @classmethod
    def get(cls, id: int, guild_id: int = 0) -> FamilyTreeMember:
        """
        Gives you the object pertaining to the given user ID.

        Parameters
        ----------
        id : int
            The ID of the user we want to get the information off.
        guild_id : int, optional
            The ID of the guild that we want to get the user from.

        Returns
        -------
        FamilyTreeMember
            The family member we've queried for.
        """

        assert id
        v = cls.all_users.get((id, guild_id))
        if v:
            return v
        return cls(
            id=id,
            guild_id=guild_id,
        )
    
    def get_name(cls, id: int):
        """
        Gets the name of the user from the cache.
        """

        return User.nick(id)
    
    @classmethod
    def get_multiple(
        cls, *ids: int, guild_id: int = 0
    ) -> Iterable[FamilyTreeMember]:
        """
        Gets multiple objects from the cache.
        """

        for i in ids:
            yield cls.get(i, guild_id)

    @classmethod
    def get_users_from_guild(cls, guild_id: int = 0) -> Iterable[FamilyTreeMember]:
        for i in cls.all_users.values():
            if i._guild_id == guild_id:
                yield i

    @overload
    def add_child(
        self, child: FamilyTreeMemberSetter, *, return_added: Literal[True]
    ) -> FamilyTreeMember: ...

    @overload
    def add_child(
        self, child: FamilyTreeMemberSetter, *, return_added: Literal[False] = False
    ) -> None: ...

    def add_child(
        self, child: FamilyTreeMemberSetter, *, return_added: bool = False
    ) -> Optional[FamilyTreeMember]:
        """
        Add a new child to this user's children list.
        """

        child_id = self._get_user_id(child)
        if child_id not in self._children:
            self._children.append(child_id)

        if return_added:
            return self.get(child_id, self._guild_id)

    @overload
    def remove_child(
        self, child: FamilyTreeMemberSetter, *, return_added: Literal[True]
    ) -> FamilyTreeMember: ...

    @overload
    def remove_child(
        self, child: FamilyTreeMemberSetter, *, return_added: Literal[False] = False
    ) -> None: ...

    def remove_child(
        self, child: FamilyTreeMemberSetter, *, return_added: bool = False
    ) -> Optional[FamilyTreeMember]:
        """
        Remove a child from this user's children list.
        """

        child_id = self._get_user_id(child)
        while child_id in self._children:
            self._children.remove(child_id)

        if return_added:
            return self.get(child_id, self._guild_id)

    @overload
    def add_partner(
        self, partner: FamilyTreeMemberSetter, *, return_added: Literal[True]
    ) -> FamilyTreeMember: ...

    @overload
    def add_partner(
        self, partner: FamilyTreeMemberSetter, *, return_added: Literal[False] = False
    ) -> None: ...

    def add_partner(
        self, partner: FamilyTreeMemberSetter, *, return_added: bool = False
    ) -> Optional[FamilyTreeMember]:
        """
        Add a new partner to this user's partner list.
        """

        partner_id = self._get_user_id(partner)
        if partner_id not in self._partners:
            self._partners.append(partner_id)

        if return_added:
            return self.get(partner_id, self._guild_id)

    @overload
    def remove_partner(
        self, partner: FamilyTreeMemberSetter, *, return_added: Literal[True]
    ) -> FamilyTreeMember: ...

    @overload
    def remove_partner(
        self, partner: FamilyTreeMemberSetter, *, return_added: Literal[False] = False
    ) -> None: ...

    def remove_partner(
        self, partner: FamilyTreeMemberSetter, *, return_added: bool = False
    ) -> Optional[FamilyTreeMember]:
        """
        Remove a partner from this user's partner list.
        """

        partner_id = self._get_user_id(partner)
        while partner_id in self._partners:
            self._partners.remove(partner_id)

        if return_added:
            return self.get(partner_id, self._guild_id)

    ##
    def add_friend(
        self, friend: FamilyTreeMemberSetter, *, return_added: bool = False
    ) -> Optional[FamilyTreeMember]:
        """
        Add a new partner to this user's partner list.
        """

        friend_id = self._get_user_id(friend)
        if friend_id not in self._friends:
            self._friends.append(friend_id)

        if return_added:
            return self.get(friend_id, self._guild_id)

    def remove_friend(
        self, friend: FamilyTreeMemberSetter, *, return_added: bool = False
    ) -> Optional[FamilyTreeMember]:
        """
        Remove a partner from this user's partner list.
        """

        friend_id = self._get_user_id(friend)
        while friend_id in self._friends:
            self._friends.remove(friend_id)

        if return_added:
            return self.get(friend_id, self._guild_id)

    def to_json(self) -> dict:
        """
        Converts the object to JSON format so you can throw it through Redis.
        """

        return {
            "id": self.id,
            "children": self._children,
            "parent_id": self._parent,
            "partners": self._partners,
            "friends": self._friends,
            "guild_id": self._guild_id,
        }

    @classmethod
    def from_json(cls, data: dict) -> FamilyTreeMember:
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

    def __repr__(self) -> str:
        attrs = (
            (
                "id",
                "id",
            ),
            (
                "children",
                "_children",
            ),
            (
                "parent_id",
                "_parent",
            ),
            (
                "partners",
                "_partners",
            ),
            (
                "guild_id",
                "_guild_id",
            ),
        )
        d = ", ".join(["%s=%r" % (i, getattr(self, o)) for i, o in attrs])
        return f"{self.__class__.__name__}({d})"

    def __eq__(self, other) -> bool:
        if not isinstance(other, self.__class__):
            return False
        return all(
            [
                self.id == other.id,
                self._guild_id == other._guild_id,
            ]
        )

    @property
    def parent(self) -> Optional[FamilyTreeMember]:
        """
        Gets you the instance of this user's parent.
        """

        if self._parent and self._parent != self.id:
            return self.get(self._parent, self._guild_id)
        return None

    @parent.setter
    def parent(self, value: Optional[FamilyTreeMemberSetter]):
        self._parent = self._get_user_id(value)

    @property
    def children(self) -> Iterable[FamilyTreeMember]:
        """
        Gets you the list of children instances for this user.
        """

        for i in sorted(self._children):
            if i == self.id:
                continue
            yield self.get(i, self._guild_id)

    @children.setter
    def children(self, value: Iterable[FamilyTreeMemberSetter]):
        self._children = [self._get_user_id(i) for i in value]

    @property
    def partners(self) -> Iterable[FamilyTreeMember]:
        """
        Gets you the list of partner instances for this user.
        """

        for i in sorted(self._partners):
            if i == self.id:
                continue
            yield self.get(i, self._guild_id)

    @partners.setter
    def partners(self, value: Iterable[FamilyTreeMemberSetter]):
        self._partners = [self._get_user_id(i) for i in value]

    @property
    def friends(self) -> Iterable[FamilyTreeMember]:
        for i in sorted(self._friends):
            if i == self.id:
                continue
            yield self.get(i)

    @friends.setter
    def friends(self, value: Iterable[FamilyTreeMemberSetter]):
        self._friends = [self._get_user_id(i) for i in value]

    def get_direct_relations(self) -> List[int]:
        """
        Gets the direct relation IDs for the given user.
        """

        output = []
        output.extend(self._children)
        output.append(self._parent)
        output.extend(self._partners)
        return [i for i in output if i is not None]

    @property
    def is_empty(self) -> bool:
        """
        Does this instance have any family members? Does not check
        for loops etc, and is only used before a tree generation.
        """

        return not any(
            (len(self._partners) > 0, self._parent is not None, len(self._children) > 0)
        )

    def get_relation(
        self, target_user: FamilyTreeMember, use_all_partners=False
    ) -> Optional[str]:
        """
        Gets your relation to another given FamilyTreeMember object.

        Parameters
        ----------
        target_user : FamilyTreeMember
            The user who we want to get the relationship to.

        Returns
        -------
        Optional[str]
            The family tree relationship string.
        """

        text = self.get_unshortened_relation(
            target_user, use_all_partners=use_all_partners
        )
        if text is None:
            return None
        return Simplifier().simplify(text)

    def get_relation_with_directions(
        self,
        target_user: FamilyTreeMember,
        working_relation: Union[List[tuple[FamilyTreeMember, str]], None] = None,
        added_already: Union[Set[int], None] = None,
    ):
        # Set default values
        if working_relation is None:
            working_relation = []
        if added_already is None:
            added_already = set()

        # You're doing a loop - return None
        if self.id in added_already:
            return None

        # We hit the jackpot - return the made up string
        if target_user.id == self.id:
            # ret_string = "'s ".join(working_relation)
            # return ret_string
            return working_relation

        # Add self to list of checked people
        added_already.add(self.id)

        # Check parent
        if self._parent and self._parent not in added_already:
            parent = self.parent
            assert parent
            x = parent.get_relation_with_directions(
                target_user,
                working_relation=working_relation + [(parent, "parent")],
                added_already=added_already,
            )
            if x:
                return x

        # Check partner
        for i in [o for o in self.partners if o.id not in added_already]:
            x = i.get_relation_with_directions(
                target_user,
                working_relation=working_relation + [(i, "partner")],
                added_already=added_already,
            )
            if x:
                return x

        # Check children
        for i in [o for o in self.children if o.id not in added_already]:
            x = i.get_relation_with_directions(
                target_user,
                working_relation=working_relation + [(i, "child")],
                added_already=added_already,
            )
            if x:
                return x

        return None

    def get_genarational_span_from_relation(self, relation):
        people_dict = {0: [self]}

        # relations = [r.strip() for r in relation.split('\'s')]
        # print(relations)
        depth = 0
        # x = self
        for r in relation:
            user = r[0]
            if r[1] == "parent":
                depth -= 1
                people_dict[depth] = people_dict.get(depth, []) + [user]
                # x = x.parent
            elif r[1] == "child":
                depth += 1
                people_dict[depth] = people_dict.get(depth, []) + [user]
            elif r[1] == "partner":
                people_dict[depth] = people_dict.get(depth, []) + [user]
            else:
                print(r)

        # Remove dupes, should they be in there
        # print(people_dict)
        return people_dict

    @property
    def family_member_count(self) -> int:
        """
        Returns the number of people in the family.
        """

        family_member_count = 0
        for _ in self.span(add_parent=True, expand_upwards=True):
            family_member_count += 1
        return family_member_count

    def span(
        self,
        people_list: Union[set, None] = None,
        add_parent: bool = False,
        expand_upwards: bool = False,
    ) -> Iterable[FamilyTreeMember]:
        """
        Gets a list of every user related to this one
        If "add_parent" and "expand_upwards" are True, then it should
        add every user in a given tree, even if they're related through
        marriage's parents etc.

        Parameters
        ----------
        people_list : set, optional
            The list of users who are currently in the tree (so as to avoid recursion)
        add_parent : bool, optional
            Whether or not to add the parent of this user to the people list
        expand_upwards : bool, optional
            Whether or not to expand upwards in the tree

        Yields
        ------
        Iterable[FamilyTreeMember]
            A list of users that this person is related to.
        """

        # Don't add yourself again
        if people_list is None:
            people_list = set()
        if self in people_list:
            return people_list
        people_list.add(self)
        yield self

        # Add your parent
        if expand_upwards and add_parent and self._parent:
            assert self.parent
            yield from self.parent.span(
                people_list,
                add_parent=True,
                expand_upwards=expand_upwards,
            )

        # Add your children
        for child in self.children:
            yield from child.span(
                people_list,
                add_parent=False,
                expand_upwards=expand_upwards,
            )

        # Add your partner
        for partner in self.partners:
            yield from partner.span(
                people_list,
                add_parent=True,
                expand_upwards=expand_upwards,
            )

    def get_root(self) -> FamilyTreeMember:
        """
        Expands backwards into the tree up to a root user.
        Only goes up one line of family, so it cannot add your spouse's parents etc.
        """

        # Set a default user to look at
        root_user = self
        already_processed = set()

        # Loop until we get someone
        while True:
            # The person we're looking at has been processed before,
            # and as such they should be the top of our tree
            if root_user in already_processed:
                return root_user

            # Keep track of people we've looked at already
            already_processed.add(root_user)

            # If this user has a parent, they must be higher than
            # this instance by default
            if root_user._parent:
                assert root_user.parent
                root_user = root_user.parent

            # If they have any partners, one of THEM could have a parent
            elif root_user._partners:
                # Have to iterate through them to get the cached values
                for p in root_user.partners:
                    # See if a partner has a parent
                    if p._parent:
                        assert p.parent
                        root_user = p.parent
                        break

            # If this user has no parents or partners, they must be the
            # top of our tree
            else:
                return root_user

    def get_unshortened_relation(
        self,
        target_user: FamilyTreeMember,
        working_relation: Union[List[str], None] = None,
        added_already: Union[Set[int], None] = None,
        use_all_partners=False,
    ) -> Optional[str]:
        """
        Gets your relation to the other given user.

        Args:
            target_user (FamilyTreeMember): The user who you want to list the relation to.
            working_relation (list, optional): The list of relation steps it's taking to get.
            added_already (list, optional): So we can keep track of who's been looked at before.

        Returns:
            Optional[str]: The family tree relationship string.
        """

        # Set default values
        if working_relation is None:
            working_relation = []
        if added_already is None:
            added_already = set()

        # You're doing a loop - return None
        if self.id in added_already:
            return None

        # We hit the jackpot - return the made up string
        if target_user.id == self.id:
            ret_string = "'s ".join(working_relation)
            return ret_string

        # Add self to list of checked people
        added_already.add(self.id)

        # Check parent
        if self._parent and self._parent not in added_already:
            parent = self.parent
            assert parent
            x = parent.get_unshortened_relation(
                target_user,
                working_relation=working_relation + ["parent"],
                added_already=added_already,
                use_all_partners=use_all_partners,
            )
            if x:
                return x

        # Check partner
        if not use_all_partners:
            partners = [o for o in self.partners if o.id not in added_already]
        else:
            partners = [
                o
                for o in self.get_all_partners(self, set())
                if o.id not in added_already
            ]
        for i in partners:
            x = i.get_unshortened_relation(
                target_user,
                working_relation=working_relation + ["partner"],
                added_already=added_already,
                use_all_partners=use_all_partners,
            )
            if x:
                return x

        # Check children
        for i in [o for o in self.children if o.id not in added_already]:
            x = i.get_unshortened_relation(
                target_user,
                working_relation=working_relation + ["child"],
                added_already=added_already,
                use_all_partners=use_all_partners,
            )
            if x:
                return x

        return None

    def get_all_partners(
        self, u: FamilyTreeMember, lst: Set[FamilyTreeMember]
    ) -> Set[FamilyTreeMember]:
        if u in lst:
            return set()  # Return an empty set instead of a list
        lst.add(u)  # Use add() method to add partners to the set
        for p in u.partners:
            lst.update(
                self.get_all_partners(p, lst)
            )  # Use update() method to add partners to the set
        return lst

    def generational_span(
        self,
        people_dict: Union[Dict[int, List[FamilyTreeMember]], None] = None,
        depth: int = 0,
        add_parent: bool = False,
        add_partners: bool = True,
        expand_upwards: bool = False,
        all_people: Union[set, None] = None,
        recursive_depth: int = 0,
        use_all_partners=False,
    ) -> Dict[int, List[FamilyTreeMember]]:
        """
        Gets a list of every user related to this one.
        If "add_parent" and "expand_upwards" are True, then it
        should add every user in a given tree, even if they're
        related through marriage's parents etc.

        Parameters
        ----------
        people_dict : Union[dict, None], optional
            The dict of users who are currently in the tree
            (to avoid recursion).
        depth : int, optional
            The current generation of the tree span.
        add_parent : bool, optional
            Whether to add the parent of this user to the
            people list.
        expand_upwards : bool, optional
            Whether to expand upwards in the tree.
        all_people : Union[set, None], optional
            A set of all people who this recursive function would
            look at.
        recursive_depth : int, optional
            How far into the recursion you have gone - this is so we
            don't get recursion errors.

        Returns
        -------
        Dict[int, List[FamilyTreeMember]]
            A dictionary of each generation of users.
        """

        # Don't add yourself again
        if people_dict is None:
            people_dict = {}
        if all_people is None:
            all_people = set()
        if self.id in all_people:
            return people_dict
        if recursive_depth >= 500:
            return people_dict
        all_people.add(self.id)

        # Add to dict
        x = people_dict.setdefault(depth, list())
        x.append(self)

        # Add your children
        for child in self.children:
            people_dict = child.generational_span(
                people_dict,
                depth=depth + 1,
                add_parent=False,
                add_partners=True,
                expand_upwards=expand_upwards,
                all_people=all_people,
                recursive_depth=recursive_depth + 1,
                use_all_partners=use_all_partners,
            )

        # Add your partner
        if add_partners:
            partners = self.partners
            if use_all_partners:
                partners = self.get_all_partners(self, set())
            for partner in partners:  # get_all_partners(self,set()):#self.partners:
                people_dict = partner.generational_span(
                    people_dict,
                    depth=depth,
                    add_parent=True,
                    add_partners=False,
                    expand_upwards=expand_upwards,
                    all_people=all_people,
                    recursive_depth=recursive_depth + 1,
                    use_all_partners=use_all_partners,
                )

        # Add your parent
        if expand_upwards and add_parent and self._parent:
            parent = self.parent
            assert parent
            people_dict = parent.generational_span(
                people_dict,
                depth=depth - 1,
                add_parent=True,
                add_partners=True,
                expand_upwards=expand_upwards,
                all_people=all_people,
                recursive_depth=recursive_depth + 1,
                use_all_partners=use_all_partners,
            )

        # Remove dupes, should they be in there
        # print(people_dict)
        return people_dict

    def circle_span(
        self,
        people_dict=None,
        all_people: Union[set, None] = None,
        recursive_depth: int = 0,
        max_depth=500,
        all_depths: dict[int, int] = None,
    ) -> Tuple[List[FamilyTreeMember], Dict[int, int]]:
        # Don't add yourself again
        if people_dict is None:
            people_dict = []
        if all_people is None:
            all_people = []
        if all_depths is None:
            all_depths = {}
        if self.id in all_people:
            return people_dict, all_depths
        if recursive_depth >= max_depth:
            return people_dict, all_depths
        all_people.append(self.id)

        people_dict.append(self)
        if self.id not in all_depths:
            all_depths[self.id] = recursive_depth
        # Add your children
        for friend in self.friends:
            people_dict, all_depths = friend.circle_span(
                people_dict,
                all_people=all_people,
                recursive_depth=recursive_depth + 1,
                max_depth=max_depth,
                all_depths=all_depths,
            )
        return people_dict, all_depths

    async def to_dot_script(
        self,
        customised_tree_user: CustomisedTreeUser,
        image=False,
    ) -> str:
        """
        Gives you a string of the current family tree that will go through DOT.

        Parameters
        ----------
        bot : types.Bot
            The bot instance that should be used to get the names of users.
        customised_tree_user : CustomisedTreeUser
            The customised tree object that should be used to alter how the
            dot script looks.

        Returns
        -------
        str
            The generated DOT code.
        """

        root_user = self.get_root()
        gen_span = root_user.generational_span()
        return await self.to_dot_script_from_generational_span(
            gen_span, customised_tree_user, image=image
        )

    async def to_full_dot_script(
        self, customised_tree_user: CustomisedTreeUser, image=False
    ) -> str:
        """
        Gives you the string of the FULL current family.

        Parameters
        ----------
        bot : types.Bot
            The bot instance that should be used to get the names of users.
        customised_tree_user : CustomisedTreeUser
            The customised tree object that should be used to alter how the
            dot script looks.

        Returns
        -------
        str
            The generated DOT code.
        """

        root_user = self.get_root()
        gen_span = root_user.generational_span(expand_upwards=True, add_parent=True)
        # print(gen_span)
        return await self.to_dot_script_from_generational_span(
            gen_span, customised_tree_user, image=image
        )

    async def to_graphviz_label(
        self,
        name: str,
        customised_tree_user: CustomisedTreeUser | None = None,
        image=False,
    ) -> str:
        """
        Convert the current family tree member into a label applicable for Graphviz.
        """

        # Generate dot for both ourselves and others
        # print("CALL-",self.id)
        if str(self.id).startswith("1000"):
            return (
                f'{self.id}[label="{name}",style="invis"]'
                # f'fillcolor="#b720d9",'
                # f'fontcolor="#ffffff"];'
            )

        if image and os.path.exists(f"pfps/{self.id}_{User.profilepic(self.id)}.png"):
            image_path = f"pfps/{self.id}_{User.profilepic(self.id)}.png"
            if customised_tree_user:
                return (
                    f'{self.id}[fillcolor={customised_tree_user.hex["highlighted_node"]},fontcolor={customised_tree_user.hex["highlighted_font"]},label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD>{name}</TD></TR><TR><TD ALIGN="CENTER"><IMG SRC="{image_path}" /></TD></TR></TABLE>>,imagepos="mc"]'
                    # f'{self.id}[fillcolor={customised_tree_user.hex["highlighted_node"]},label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD>{name}</TD></TR><TR><TD ALIGN="CENTER"><IMG SRC="{image_path}" /></TD></TR></TABLE>>,imagepos="mc"]'
                )
            else:
                # with open(image_path, "rb") as f:
                #     image_data = binascii.hexlify(f.read()).decode("utf-8")
                return (
                    f'{self.id}[color="#FFFFFF00",label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD>{name}</TD></TR><TR><TD ALIGN="CENTER"><IMG SRC="{image_path}" /></TD></TR></TABLE>>,imagepos="mc"]'
                    # f'{self.id}[color="#FFFFFF00",label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD>{name}</TD></TR><TR><TD ALIGN="CENTER"><IMG SRC="data:image/png;base64,{image_data}" /></TD></TR></TABLE>>,imagepos="mc"]'
                )
                # return (
                #     f'{self.id}[color="#FFFFFF00",fillcolor="#FFFFFF00",label=<<TABLE BORDER="0" CELLBORDER="0" CELLSPACING="0"><TR><TD>{name}</TD></TR><TR><TD ALIGN="CENTER"><IMG SRC="{image_path}" /></TD></TR></TABLE>>,imagepos="mc"]'
                # )

        # print(u_name)
        # if int(self.id) == 1217088375:
        #     return (
        #         f'{self.id}[label="{name}",'
        #         f'fillcolor="#b720d9",'
        #         f'fontcolor="#ffffff"];'
        #     )
        if customised_tree_user:
            return (
                f'{self.id}[label="{name}",'
                f"fillcolor={customised_tree_user.hex['highlighted_node']},"
                f"fontcolor={customised_tree_user.hex['highlighted_font']}];"
            )
        return f'{self.id}[label="{name}"];'

    async def to_dot_script_from_generational_span(
        self,
        gen_span: Dict[int, List[FamilyTreeMember]],
        customised_tree_user: CustomisedTreeUser,
        image=False,
        paired_children=False,
    ) -> str:
        """
        Generates the DOT script from a given generational span.

        Parameters
        ----------
        bot : types.Bot
            The bot instance that should be used to get the names of users.
        gen_span : Dict[int, List[FamilyTreeMember]]
            The generational span.
        customised_tree_user : CustomisedTreeUser
            The customised tree object that should be used to alter how the
            dot script looks.

        Returns
        -------
        str
            The generated DOT code.
        """

        # Find my own depth
        my_depth: int = 0
        for depth, depth_list in gen_span.items():
            if self in depth_list:
                my_depth = depth
                break

        # Add my partner and parent
        for partner in self.partners:
            if partner not in (x := gen_span.get(my_depth, [])):
                x.append(partner)
                gen_span[my_depth] = x
        if parent := self.parent:
            if parent not in (x := gen_span.get(my_depth - 1, [])):
                x.append(parent)
                gen_span[my_depth - 1] = x

        # MY EDIT
        # if self.parent:
        #     for child in self.parent.children:
        #         if child not in (x := gen_span.get(my_depth, [])):
        #             x.append(child)
        #             gen_span[my_depth] = x
        #             for childchild in child.children:
        #                 if childchild not in (y := gen_span.get(my_depth+1, [])):
        #                     y.append(childchild)
        #                     gen_span[my_depth+1] = y

        # Long var names suck
        ctu = customised_tree_user
        pc = paired_children
        if pc:
            splines = "splines=false;"
        else:
            splines = ""  # 'splines=ortho;'

        # Make some initial digraph stuff
        caption = f'"{User.nick(self.id)}: Family Tree"'
        # Change below line for remote rendering support
        all_text: str = (
            "digraph {"
            f"{splines}"
            f"node [shape=box,fontcolor={ctu.hex['font']},"
            f"color={ctu.hex['edge']},"
            f"fillcolor={ctu.hex['node']},style=filled];"
            f"edge [dir=none,color={ctu.hex['edge']}];"
            f"bgcolor={ctu.hex['background']};"
            f"rankdir={ctu.hex['direction']};"
        )

        # The ordered list of generation numbers -
        # just a list of sequential numbers
        # Done so we can make sure we have each generation in the
        # right order
        generation_numbers: List[int] = sorted(list(gen_span.keys()))

        # Go through the members for each generation
        for generation_number in generation_numbers:
            if (generation := gen_span.get(generation_number)) is None:
                continue

            # Make sure you don't add a spouse twice (as they will
            # be added both by the partner loop and they'll be in the
            # generation list)
            added_already: List[FamilyTreeMember] = []

            # # Add a ranking for this generation; only necessary if this
            # # if our first runthrough (the child adding section adds this
            # # on subsequent loops)
            # all_text += "{rank=same;"

            junctions_by_ppl = {}
            # Go through each person in the generation
            for person in generation:
                # Don't add a person twice
                if person in added_already:
                    continue
                added_already.append(person)

                # Work out who the user's partners are
                previous_partner = None
                filtered_possible_partners = [*person.partners]
                for p in filtered_possible_partners.copy():
                    filtered_possible_partners.extend(p.partners)
                filtered_possible_partners = [*list(set(filtered_possible_partners))]
                try:
                    filtered_possible_partners.remove(person)
                except ValueError:
                    pass
                filtered_possible_partners.insert(0, person)

                # Add the user's partners
                all_text += (
                    f"subgraph cluster{get_cluster_name()}{{ peripheries=0;{{rank=same;"
                )

                # def fetch_ctu_by_id(id):
                # return data[str(id)]['ctu']
                for partner in filtered_possible_partners:
                    name = (
                        # (
                        #     fetch_name_by_id(partner.id)
                        # )
                        (User.nick(partner.id)).replace('"', '\\"')
                    )
                    ctu = CustomisedTreeUser.get_by_id(partner.id)
                    if partner == self:  # or ctu!="":
                        all_text += await partner.to_graphviz_label(
                            name, ctu, image=image
                        )
                    else:
                        all_text += await partner.to_graphviz_label(name, image=image)
                    if previous_partner is None:
                        previous_partner = partner
                        continue
                    partner_link = (
                        f'{previous_partner.id} -> {partner.id}[color="deeppink"];'
                    )
                    alt_partner_link = (
                        f'{partner.id} -> {previous_partner.id}[color="deeppink"];'
                    )
                    if (
                        partner_link not in all_text
                        and alt_partner_link not in all_text
                        and partner != previous_partner
                    ):
                        all_text += partner_link
                    added_already.append(partner)
                    previous_partner = partner

                all_text += "}"
                if pc:
                    junc_name = get_cluster_name() + "_junction"
                    all_text += f"{junc_name} [shape=point];"
                    total_children = [
                        c for p in [person] + list(person.partners) for c in p._children
                    ]
                    if len(total_children) > 0:
                        for partner in filtered_possible_partners:
                            all_text += f"{partner.id}:s->{junc_name}:n;"
                            junctions_by_ppl[partner.id] = junc_name
                        for c in total_children:
                            # print(c)
                            junctions_by_ppl[c] = junc_name

                all_text += "}"

                # # Close off the generation and open a new ranking for
            # # adding children links
            # all_text += "}"

            # Go through the people in the generation and see if they have
            # any children to add
            for person in generation:
                if person._children and not pc:
                    all_text += f"p{person.id} {self.INVISIBLE};"

            # Add the lines from parent to node to child
            for person in generation:
                if person._children and not pc:
                    new_text = f"{person.id}:s -> p{person.id}:c;"
                    if new_text not in all_text:
                        all_text += new_text
                for child in person.children:
                    if not pc:
                        new_text = f"p{person.id}:c -> {child.id}:n;"
                    else:
                        junc = junctions_by_ppl[person.id]
                        new_text = f"{junc}:c -> {child.id}:n;"
                    if new_text not in all_text:
                        all_text += new_text

        # And we're done!
        all_text += "}"
        return all_text

    async def to_dot_script_from_circle_span(
        self,
        circle_span: List[FamilyTreeMember],
        customised_tree_user: CustomisedTreeUser,
        all_depths: dict[int, int],
        image=False,
    ) -> str:
        # Add my partner and parent
        # for friend in self.friends:
        #     if friend not in circle_span:
        #         circle_span.append(friend)

        ctu = customised_tree_user

        # Make some initial digraph stuff
        all_text: str = (
            "digraph {"
            f"node [shape=box,fontcolor={ctu.hex['font']},"
            f"color={ctu.hex['edge']},"
            f"fillcolor={ctu.hex['node']},style=filled];"
            f"edge [dir=none,color={ctu.hex['edge']}];"
            f"bgcolor={ctu.hex['background']};"
            f"rankdir={ctu.hex['direction']};"
        )

        added_already: List[FamilyTreeMember] = []
        # print(len(all_depths),len(circle_span))
        i = 0
        for person in circle_span:
            i += 1
            all_text += "\n"
            # if person in added_already:
            #     continue
            # print(i,all_depths[person.id],person)
            added_already.append(person)
            filtered_possible_partners = [*person.friends]
            try:
                filtered_possible_partners.remove(person)
            except ValueError:
                pass
            filtered_possible_partners.insert(0, person)
            # let's say this person is at depth x

            depth_of_this = all_depths[person.id]
            # now we should only add partners which are of depth x+1
            for partner in filtered_possible_partners:
                if partner not in circle_span:
                    continue
                # in this version, this is off by default
                # if (
                #     all_depths[partner.id] != depth_of_this + 1
                #     and self.id != partner.id
                # ):
                #     continue
                name = (User.nick(partner.id)).replace('"', '\\"')
                if partner == self:  # or ctu!="":
                    all_text += await partner.to_graphviz_label(name, ctu, image=image)
                else:
                    # if depth_of_this > 1:
                    #     all_text += partner.to_graphviz_label(name, image=False)
                    # else:
                    all_text += await partner.to_graphviz_label(name, image=image)
                partner_link = f"{person.id} -> {partner.id};"
                alt_partner_link = f"{partner.id} -> {person.id};"
                if (
                    partner_link not in all_text
                    and alt_partner_link not in all_text
                    and partner != person
                ):
                    all_text += partner_link
                    # print(partner_link)
                added_already.append(partner)
        all_text += "}"
        return all_text

    async def to_short_dot_script_from_generational_span(
        self,
        gen_span: Dict[int, List[FamilyTreeMember]],
        customised_tree_user: CustomisedTreeUser,
        image=False,
        highlight=None,
    ) -> str:
        # Find my own depth
        total_ppl = set([item for sublist in gen_span for item in gen_span[sublist]])
        my_depth: int = 0
        for depth, depth_list in gen_span.items():
            if self in depth_list:
                my_depth = depth
                break
        # Long var names suck
        ctu = customised_tree_user

        # Make some initial digraph stuff
        all_text: str = (
            "digraph {"
            f"node [shape=box,fontcolor={ctu.hex['font']},"
            f"color={ctu.hex['edge']},"
            f"fillcolor={ctu.hex['node']},style=filled];"
            f"edge [dir=none,color={ctu.hex['edge']}];"
            f"bgcolor={ctu.hex['background']};"
            f"rankdir={ctu.hex['direction']};"
        )

        # The ordered list of generation numbers -
        # just a list of sequential numbers
        # Done so we can make sure we have each generation in the
        # right order
        generation_numbers: List[int] = sorted(list(gen_span.keys()))

        # Go through the members for each generation
        for generation_number in generation_numbers:
            if (generation := gen_span.get(generation_number)) is None:
                continue

            # Make sure you don't add a spouse twice (as they will
            # be added both by the partner loop and they'll be in the
            # generation list)
            added_already: List[FamilyTreeMember] = []

            # # Add a ranking for this generation; only necessary if this
            # # if our first runthrough (the child adding section adds this
            # # on subsequent loops)
            # all_text += "{rank=same;"

            # Go through each person in the generation
            for person in generation:
                # Don't add a person twice
                if person in added_already:
                    continue
                added_already.append(person)

                # Work out who the user's partners are
                previous_partner = None
                filtered_possible_partners = [*person.partners]
                for p in filtered_possible_partners.copy():
                    filtered_possible_partners.extend(p.partners)
                filtered_possible_partners = [*list(set(filtered_possible_partners))]
                try:
                    filtered_possible_partners.remove(person)
                except ValueError:
                    pass
                filtered_possible_partners.insert(0, person)

                # Add the user's partners
                all_text += (
                    f"subgraph cluster{get_cluster_name()}{{peripheries=0;{{rank=same;"
                )

                # def fetch_ctu_by_id(id):
                # return data[str(id)]['ctu']
                for partner in filtered_possible_partners:
                    if partner not in total_ppl:
                        continue
                    name = (
                        # (
                        #     fetch_name_by_id(partner.id)
                        # )
                        (User.nick(partner.id)).replace('"', '\\"')
                    )
                    # ctu = fetch_ctu_by_id(partner.id)
                    if partner == self or partner == highlight:  # or ctu!="":
                        all_text += await partner.to_graphviz_label(
                            name, ctu, image=image
                        )
                    else:
                        all_text += await partner.to_graphviz_label(name, image=image)
                    if previous_partner is None:
                        previous_partner = partner
                        continue
                    partner_link = f"{previous_partner.id} -> {partner.id};"
                    alt_partner_link = f"{partner.id} -> {previous_partner.id};"
                    if (
                        partner_link not in all_text
                        and alt_partner_link not in all_text
                        and partner != previous_partner
                    ):
                        all_text += partner_link
                    added_already.append(partner)
                    previous_partner = partner
                all_text += "}" + "}"

            # # Close off the generation and open a new ranking for
            # # adding children links
            # all_text += "}"

            # Go through the people in the generation and see if they have
            # any children to add
            for person in generation:
                if person._children:
                    all_text += f"p{person.id} {self.INVISIBLE};"

            # Add the lines from parent to node to child
            for person in generation:
                if [x for x in person.children if x in total_ppl]:
                    new_text = f"{person.id}:s -> p{person.id}:c;"
                    if new_text not in all_text:
                        all_text += new_text
                for child in person.children:
                    if child not in total_ppl:
                        continue
                    new_text = f"p{person.id}:c -> {child.id}:n;"
                    if new_text not in all_text:
                        all_text += new_text

        # And we're done!
        all_text += "}"
        return all_text

    async def to_dot_script_from_waifu_span(
        self,
        waifu_span: Dict[int, int],
        customised_tree_user: CustomisedTreeUser,
    ) -> str:
        ctu = customised_tree_user
        all_text: str = (
            "digraph {"
            f"node [shape=box,fontcolor={ctu.hex['font']},"
            f"color={ctu.hex['edge']},"
            f"fillcolor={ctu.hex['node']},style=filled];"
            f"edge [color={ctu.hex['edge']}];"
            f"bgcolor={ctu.hex['background']};"
            f"rankdir={ctu.hex['direction']};"
        )
        all_people = list(waifu_span.keys()) + list(waifu_span.values())
        for p in all_people:
            person = FamilyTreeMember.get(p)
            if person == self: 
                all_text += await person.to_graphviz_label(
                    User.nick(p), ctu, image=True
                )
            else:
                all_text += await person.to_graphviz_label(
                    User.nick(p), image=True
                )
        for person in waifu_span:
            all_text += "\n"
            waifu = FamilyTreeMember.get(waifu_span[person])
            name = (User.nick(waifu_span[person])).replace('"', '\\"')
            partner_link = f"{person} -> {waifu.id};"
            all_text += partner_link
        all_text += "}"
        return all_text

