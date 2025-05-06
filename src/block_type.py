from enum import Enum
import re

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered list"
    ORDERED_LIST = "ordered list"

def block_to_block_type(block):
    if block.strip().startswith("```") and block.strip().endswith("```"):
        return BlockType.CODE
    if re.findall("\A#+ ", block) :
        max_num = 6
        num = int(re.findall("\A#+ ", block)[0].count("#"))
        if num <= max_num:
            return BlockType.HEADING
    lines = block.split("\n")
    quote_line_count = 0
    unordered_list_line_count = 0
    ordered_list_line_count = 0
    for line in lines:
        if line.startswith(">"):
            quote_line_count += 1
        if line.startswith("- "):
            unordered_list_line_count += 1
        if re.findall("\A\d+. ",line):
            if int(re.findall("\A\d+. ",line)[0][0]) == ordered_list_line_count + 1:
                ordered_list_line_count += 1

    if len(lines) == quote_line_count:
        return BlockType.QUOTE
    if len(lines) == unordered_list_line_count:
        return BlockType.UNORDERED_LIST
    if len(lines) == ordered_list_line_count:
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH 