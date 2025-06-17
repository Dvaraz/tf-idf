from collections import Counter
from itertools import chain

from core.tfidf_app.utils import clean_text


class Node:
    def __init__(self, char, frequency, left_node=None, right_node=None):
        self.char = char
        self.frequency = frequency
        self.left_node = left_node
        self.right_node = right_node

    def __lt__(self, other):
        return self.frequency < other.frequency


def search_insert_place(array: list[Node], freq):
    if not array:
        return 0

    left, right = 0, len(array) - 1

    while left < right:

        mid = left + (right - left) // 2

        if array[mid].frequency < freq:
            left = mid + 1

        else:
            right = mid
    return left + 1 if array[left].frequency < freq else left


def create_huffman_tree(chars_frequency: dict):

    list_of_nodes = [Node(char=char, frequency=frequency) for char, frequency in chars_frequency.items()]

    list_of_nodes.sort(key=lambda x: x.frequency)

    while len(list_of_nodes) > 1:

        left_node = list_of_nodes.pop(0)
        right_node = list_of_nodes.pop(0)

        new_node_frequency = left_node.frequency + right_node.frequency

        node = Node(None, new_node_frequency, left_node=left_node, right_node=right_node)

        insert_index = search_insert_place(list_of_nodes, node.frequency)

        list_of_nodes.insert(insert_index, node)

    return list_of_nodes[0]


def create_codes_for_tree(root_node: Node):
    codes = {}

    stack = [(root_node, "")]

    while stack:
        node, current_code = stack.pop()

        if node.char is not None:
            codes[node.char] = current_code

        if node.right_node:
            stack.append((node.right_node, current_code + "1"))

        if node.left_node:
            stack.append((node.left_node, current_code + "0"))

    return codes


def encode_huffman_algo(text):
    clean_doc = clean_text(text)
    chars_frequency = Counter(chain(clean_doc))
    root = create_huffman_tree(chars_frequency)

    huffman_codes = create_codes_for_tree(root)

    encoded_text = ''.join(huffman_codes[char] for char in clean_doc)

    return encoded_text, huffman_codes
