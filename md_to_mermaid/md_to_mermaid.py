from dataclasses import dataclass, field
from typing import Union
from file_parser import generate_header, Header

@dataclass
class MermaidNode:
    """
    A Single markdown string produces a single mermaid diagram block
    children: [[Level1, Level2], [Level1a, Level2a]]
    """
    header_level : int
    header_text : str
    parent: "MermaidNode" = None
    children: list["MermaidNode"] = field(default_factory=list)
    format: str = "Flowchart LR"


def build_MermaidNode_from_md_string(md_str: str)-> list[MermaidNode]:
    parent = MermaidNode(
        header_level=0,
        header_text="I am (G)Root"

    )
    mermaid_tree_root = parent

    for header in generate_header(md_str):
        node = MermaidNode(
            header_level=header.level,
            header_text=header.text,
        )

        if header.level > parent.header_level:
            # this header is a child
            node.parent = parent
            parent.children.append(node)

        if header.level <= parent.header_level:
            # these objects are siblings
            grandparent = parent.parent 
            
            while header.level <= grandparent.header_level:
                # keep checking grandparents to find your level
                grandparent = grandparent.parent
            
            node.parent = grandparent
            grandparent.children.append(node)

        parent = node
        
    return mermaid_tree_root



def convert_to_mermaid_code(mermaid_tree: MermaidNode) -> str:
    diagram_lines = [f"graph {mermaid_tree.format}"]
    
    def traverse_node(node: MermaidNode, node_id: int, parent_id: Union[int, None] = None) -> int:
        current_id = node_id
        node_name = f"Node{current_id}"
        diagram_lines.append(f'{node_name}["{node.header_text}"]')

        if parent_id is not None:
            parent_name = f"Node{parent_id}"
            diagram_lines.append(f"{parent_name} --> {node_name}")

        for child in node.children:
            current_id += 1
            current_id = traverse_node(child, current_id, node_id)
        
        return current_id

    # Start traversal from the root (which is usually the first node)
    traverse_node(mermaid_tree, 0)

    return "\n".join(diagram_lines)
