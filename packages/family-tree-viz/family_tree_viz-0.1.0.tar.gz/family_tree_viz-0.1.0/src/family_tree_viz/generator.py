from typing import  Optional
from .customised_tree_user import CustomisedTreeUser
from .family_tree_member import FamilyTreeMember
from .renderer import  TreeOutput, TreeRenderer
from .entities import GeneratorOptions, TreeType, IncorrectTreeType



class DotCodeGenerator:
    def __init__(
        self,
        tree_type: TreeType,
        current_user: FamilyTreeMember,
        customised_tree_user: CustomisedTreeUser = None,
        options: GeneratorOptions = None,
    ):
        self.tree_type = tree_type
        self.current_user = current_user
        self.ctu = customised_tree_user or CustomisedTreeUser.get_by_id(current_user.id)
        self.options = options or GeneratorOptions()

    async def generate(self):
        if self.tree_type == TreeType.QUICK:
            return await self.generate_quick()
        elif self.tree_type == TreeType.FAMILY:
            return await self.generate_family()
        elif self.tree_type == TreeType.CUSTOM:
            return await self.generate_custom()
        elif self.tree_type == TreeType.CIRCLE:
            return await self.generate_circle(self.options.radius)

        elif self.tree_type == TreeType.FULL:
            return await self.generate_full()
        else:
            raise IncorrectTreeType

    async def generate_quick(self):
        return await self.current_user.to_dot_script(
            self.ctu, image=self.options.with_images
        )

    async def generate_family(self):
        own_span = self.current_user.generational_span()
        for p in self.current_user.partners:
            partner_span = p.generational_span()
            for i in partner_span.keys():
                if i in own_span.keys():
                    own_span[i].extend(partner_span[i])
                else:
                    own_span[i] = partner_span[i]

        if self.current_user.parent:
            parent_span = self.current_user.parent.generational_span(add_partners=False)
            for i in parent_span.keys():
                if i in own_span.keys():
                    own_span[i].extend(parent_span[i])
                else:
                    own_span[i] = parent_span[i]
        dot_code = await self.current_user.to_dot_script_from_generational_span(
            own_span, self.ctu, image=self.options.with_images
        )
        return dot_code

    async def generate_custom(self):
        dot_code = await self.current_user.to_short_dot_script_from_generational_span(
            self.options.span, self.ctu, image=True, highlight=self.options.highlight
        )
        return dot_code

    async def generate_circle(self, radius):
        circle_span, all_depths = self.current_user.circle_span(max_depth=radius or 500)
        dot_code = await self.current_user.to_dot_script_from_circle_span(
            circle_span, self.ctu, image=True, all_depths=all_depths
        )
        return dot_code

    async def generate_full(self):
        dot_code = await self.current_user.to_full_dot_script(
            self.ctu, image=self.options.with_images
        )
        return dot_code


class FamilyTreeGenerator:
    def __init__(self, options=None):
        self.generational_span = None
        self.options = options or GeneratorOptions()

    async def generate(
        self,
        current_user :FamilyTreeMember,
        tree_type: TreeType,
        image_format=None,
        output_path=None,
        with_images=True,
        span=None,
        highlight=False,
        radius=None,
        font=None
    ) -> Optional[TreeOutput]:
        options = GeneratorOptions(
            image_format= image_format or self.options.image_format,
            output_path=output_path or self.options.output_path,
            with_images=with_images or self.options.with_images,
            span=span or self.options.span,
            highlight=highlight or self.options.highlight,
            radius=radius or self.options.radius,
            font=font or self.options.font,
        )
        ctu = CustomisedTreeUser.get_by_id(current_user.id)

        dot_generator = DotCodeGenerator(tree_type, current_user,ctu, options=options)
        dot_code = await dot_generator.generate()
        renderer = TreeRenderer()

        return await renderer.render(
            tree_type,
            current_user,
            dot_code,
            options,
        )
