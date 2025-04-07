import asyncio
import tempfile
from typing import List, Optional
from .family_tree_member import FamilyTreeMember
from .entities import GeneratorOptions, TreeType
from PIL import Image

class TreeRenderer:
    def __init__(self, current_user: FamilyTreeMember=None, tree_type: TreeType=None, options: GeneratorOptions = None):
        self.current_user = current_user
        self.tree_type = tree_type
        self.options = options or None

    async def execute_dot(self, args: List[str], dot_code:str) -> Optional[bytes]:
        dot = await asyncio.create_subprocess_exec(*args,
        stdin = asyncio.subprocess.PIPE,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)
        try:
            stdout, stderr = await asyncio.wait_for(dot.communicate(input=dot_code.encode("UTF-8")), 30.0)
            if dot.returncode != 0:
                raise Exception(f"DOT processing failed: {stderr.decode('utf-8')}")
            return stdout
        
        except asyncio.TimeoutError:
            dot.terminate()
            await dot.wait()  
            raise TimeoutError("DOT processing timed out after 30 seconds")

    def make_dot_args(self, engine, 
        image_format,tmp_path, scale,font, output_path, ):
        final_args = []
        final_args.append(engine)
        final_args.append(f"-T{image_format}")
        final_args.append(tmp_path)
        if scale:
            final_args.append(scale)
        final_args.append(f'-Nfontname="{font}"')
        if output_path:
            final_args.append("-o")
            if not output_path.endswith(image_format):
                output_path = f"{output_path}.{image_format}"
            final_args.append(output_path)
        final_args.append("-Gcharset=UTF-8")
        return final_args



    async def render(self, 
        tree_type: TreeType,
        current_user: FamilyTreeMember,
        dot_code: str,
        options: GeneratorOptions ,
    ) -> Optional["TreeOutput"]: 

        scale = None
        layout_engine = "dot"
        if tree_type == TreeType.CIRCLE:
            layout_engine = "neato"
            # removed since this caused a bug?
            # scale = "-Goverlap=scale"
        else:
            pass
            # if tree_type == TreeType.FULL and current_user.family_member_count > 120:
            #     options.image_format = "-Tpdf"
            #     image_filename = "tree.pdf"
        with tempfile.NamedTemporaryFile(delete=False, suffix='.gz') as tmp:
            tmp.write(dot_code.encode())


        exec_args = self.make_dot_args(
            engine=layout_engine, 
            image_format=options.image_format,tmp_path=tmp.name ,scale=scale,font= options.font, output_path=options.output_path, 
        )
        file_data_or_empty = await self.execute_dot(exec_args,dot_code)
        if file_data_or_empty:
            return TreeOutput(file_data_or_empty, options.image_format)
        return file_data_or_empty
    
class TreeOutput:
    def __init__(self, image: bytes, image_format: str):
        self.image = image
        self.image_format = image_format

    def save(self, output_path: str):
        with open(output_path, "wb") as f:
            f.write(self.image)
    
    def get_image(self) -> bytes:
        return self.image

    def get_image_format(self) -> str:
        return self.image_format
    
    def show(self):
        # use PIL to show image to user
        from io import BytesIO
        image = Image.open(BytesIO(self.image))
        image.show()

    def save_as(self, output_path: str):
        with open(output_path, "wb") as f:
            f.write(self.image)
