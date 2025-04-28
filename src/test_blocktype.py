import unittest
from block_type import *

class TestBlockToBlockType(unittest.TestCase):
    def test_headings_blocks(self):
        blocks = ["# heading 1", "## heading 2", "### heading 3", "#### headin 4", "##### headin 5", "###### heading 6", "#paragraph 1", "####### paragraph 2"]
        block_types = []
        
        for block in blocks:
            block_types.append(block_to_block_type(block))
        
        self.assertEqual(block_types,
                         [
                             BlockType.HEADING,
                             BlockType.HEADING,
                             BlockType.HEADING,
                             BlockType.HEADING,
                             BlockType.HEADING,
                             BlockType.HEADING,
                             BlockType.PARAGRAPH,
                             BlockType.PARAGRAPH
                         ],)
        
    def test_code_blocks(self):
        blocks = ["``` some code  ```", "`` some text ``", "```` some text ````", "``` some text ``", "some text ```"]
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
            
        self.assertEqual(block_types,
                             [
                                 BlockType.CODE,
                                 BlockType.PARAGRAPH,
                                 BlockType.CODE,
                                 BlockType.PARAGRAPH,
                                 BlockType.PARAGRAPH
                             ],)
    
    def test_quotes_block(self):
        blocks = ["> This is a quote", "Not a quote", """> This is also\n> a quote""", """> This is \nnot a quote"""]
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        
        self.assertEqual(block_types,
                         [
                             BlockType.QUOTE,
                             BlockType.PARAGRAPH,
                             BlockType.QUOTE,
                             BlockType.PARAGRAPH
                         ])

    def test_unordered_list_block(self):
        blocks = ["- This is a list", "-not a list", """- This is also\n- a list""", """> This is \nnot a list"""]
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        
        self.assertEqual(block_types,
                         [
                             BlockType.UNORDERED_LIST,
                             BlockType.PARAGRAPH,
                             BlockType.UNORDERED_LIST,
                             BlockType.PARAGRAPH
                         ])  
    
    def test_ordered_list_block(self):
        blocks = ["1. This is a list", "1.not a list", """1. This is also\n2. a list""", """1. This is \nnot a list""", """1. Not a\n3. list"""]
        block_types = []
        for block in blocks:
            block_types.append(block_to_block_type(block))
        
        self.assertEqual(block_types,
                         [
                             BlockType.ORDERED_LIST,
                             BlockType.PARAGRAPH,
                             BlockType.ORDERED_LIST,
                             BlockType.PARAGRAPH,
                             BlockType.PARAGRAPH,
                         ]) 