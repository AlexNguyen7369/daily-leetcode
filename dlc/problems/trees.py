"""Binary trees. Import the node type with:  from dlc.structures import TreeNode

Trees are written in LeetCode level-order form, using None for a missing child:
[3, 9, 20, None, None, 15, 7]
"""


def _perfect_bst(levels: int):
    """Level-order encoding of a perfect BST holding 0 .. 2**levels - 2."""
    size = 2 ** levels - 1
    out = [0] * size
    def fill(index, lo, hi):
        if lo > hi or index >= size:
            return
        mid = (lo + hi) // 2
        out[index] = mid
        fill(2 * index + 1, lo, mid - 1)
        fill(2 * index + 2, mid + 1, hi)
    fill(0, 0, size - 1)
    return out


PROBLEMS = [
    {
        "slug": "invert-binary-tree",
        "title": "Invert Binary Tree",
        "difficulty": "Easy",
        "topics": ["Tree", "DFS", "BFS", "Binary Tree"],
        "url": "https://leetcode.com/problems/invert-binary-tree/",
        "func": "invert_tree",
        "signature": "def invert_tree(root: Optional[TreeNode]) -> Optional[TreeNode]:",
        "description": "Mirror the binary tree — swap every node's left and right child — and return the root.",
        "examples": [
            "root = [4,2,7,1,3,6,9]  ->  [4,7,2,9,6,3,1]",
            "root = [2,1,3]          ->  [2,3,1]",
            "root = []               ->  []",
        ],
        "constraints": ["0 <= nodes <= 100", "-100 <= Node.val <= 100"],
        "hints": [
            "Inverting a tree means inverting both subtrees and then swapping them.",
            "The base case is an empty node — return None.",
            "Python lets you swap in one line: node.left, node.right = node.right, node.left",
        ],
        "target": {"time": "O(n)", "space": "O(h)"},
        "argspec": ["tree"],
        "retspec": "tree",
        "compare": "exact",
        "tests": [
            {"args": [[4, 2, 7, 1, 3, 6, 9]], "expect": [4, 7, 2, 9, 6, 3, 1]},
            {"args": [[2, 1, 3]], "expect": [2, 3, 1]},
            {"args": [[]], "expect": []},
            {"args": [[1, 2]], "expect": [1, None, 2]},
        ],
        "stress": {"args": lambda: [list(range(30_000))], "budget": 2.0},
        "pitfalls": ["Swapping after recursing or before recursing both work — just don't do it twice."],
        "solution": """
def invert_tree(root):
    if root is None:
        return None
    root.left, root.right = invert_tree(root.right), invert_tree(root.left)
    return root
""",
    },
    {
        "slug": "maximum-depth-of-binary-tree",
        "title": "Maximum Depth of Binary Tree",
        "difficulty": "Easy",
        "topics": ["Tree", "DFS", "BFS"],
        "url": "https://leetcode.com/problems/maximum-depth-of-binary-tree/",
        "func": "max_depth",
        "signature": "def max_depth(root: Optional[TreeNode]) -> int:",
        "description": (
            "Return the maximum depth: the number of nodes along the longest path from the root "
            "down to a leaf."
        ),
        "examples": ["root = [3,9,20,None,None,15,7]  ->  3", "root = [1,None,2]  ->  2", "root = []  ->  0"],
        "constraints": ["0 <= nodes <= 10^4"],
        "hints": [
            "The depth of a node is 1 + the depth of its deeper subtree.",
            "An empty tree has depth 0 — that is your base case.",
            "A BFS that counts levels is the iterative equivalent.",
        ],
        "target": {"time": "O(n)", "space": "O(h)"},
        "argspec": ["tree"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[3, 9, 20, None, None, 15, 7]], "expect": 3},
            {"args": [[1, None, 2]], "expect": 2},
            {"args": [[]], "expect": 0},
            {"args": [[1]], "expect": 1},
            {"args": [[1, 2, 3, 4, None, None, 5, 6]], "expect": 4},
        ],
        "stress": {"args": lambda: [list(range(50_000))], "budget": 2.0},
        "pitfalls": ["Depth counts nodes, not edges."],
        "solution": """
def max_depth(root):
    if root is None:
        return 0
    return 1 + max(max_depth(root.left), max_depth(root.right))
""",
    },
    {
        "slug": "same-tree",
        "title": "Same Tree",
        "difficulty": "Easy",
        "topics": ["Tree", "DFS", "Binary Tree"],
        "url": "https://leetcode.com/problems/same-tree/",
        "func": "is_same_tree",
        "signature": "def is_same_tree(p: Optional[TreeNode], q: Optional[TreeNode]) -> bool:",
        "description": "Return True if two binary trees have identical structure and identical values.",
        "examples": [
            "p = [1,2,3], q = [1,2,3]      ->  True",
            "p = [1,2],   q = [1,None,2]   ->  False",
            "p = [1,2,1], q = [1,1,2]      ->  False",
        ],
        "constraints": ["0 <= nodes <= 100", "-10^4 <= Node.val <= 10^4"],
        "hints": [
            "Two trees match when the roots match and both pairs of subtrees match.",
            "Handle the None cases first: both None -> True, exactly one None -> False.",
            "Then compare values and recurse on left/left and right/right.",
        ],
        "target": {"time": "O(n)", "space": "O(h)"},
        "argspec": ["tree", "tree"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3], [1, 2, 3]], "expect": True},
            {"args": [[1, 2], [1, None, 2]], "expect": False},
            {"args": [[1, 2, 1], [1, 1, 2]], "expect": False},
            {"args": [[], []], "expect": True},
            {"args": [[1], []], "expect": False},
        ],
        "stress": {"args": lambda: [list(range(30_000)), list(range(30_000))], "budget": 2.0},
        "pitfalls": ["Serialising both trees and comparing strings can confuse structure — "
                     "[1,2] and [1,None,2] must differ."],
        "solution": """
def is_same_tree(p, q):
    if p is None and q is None:
        return True
    if p is None or q is None:
        return False
    if p.val != q.val:
        return False
    return is_same_tree(p.left, q.left) and is_same_tree(p.right, q.right)
""",
    },
    {
        "slug": "balanced-binary-tree",
        "title": "Balanced Binary Tree",
        "difficulty": "Easy",
        "topics": ["Tree", "DFS", "Binary Tree"],
        "url": "https://leetcode.com/problems/balanced-binary-tree/",
        "func": "is_balanced",
        "signature": "def is_balanced(root: Optional[TreeNode]) -> bool:",
        "description": (
            "Return True if the tree is height-balanced: for every node, the depths of its two "
            "subtrees differ by at most 1."
        ),
        "examples": [
            "root = [3,9,20,None,None,15,7]         ->  True",
            "root = [1,2,2,3,3,None,None,4,4]       ->  False",
            "root = []                              ->  True",
        ],
        "constraints": ["0 <= nodes <= 5000"],
        "hints": [
            "Calling a separate height() at every node is O(n^2).",
            "Compute the height and the balanced flag in the same traversal.",
            "Return -1 (or None) upward as a sentinel meaning 'already unbalanced' and short-circuit.",
        ],
        "target": {"time": "O(n)", "space": "O(h)"},
        "argspec": ["tree"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[3, 9, 20, None, None, 15, 7]], "expect": True},
            {"args": [[1, 2, 2, 3, 3, None, None, 4, 4]], "expect": False},
            {"args": [[]], "expect": True},
            {"args": [[1, 2, 2, 3, None, None, 3, 4, None, None, 4]], "expect": False},
            {"args": [[1, None, 2, None, 3]], "expect": False},
        ],
        "stress": {"args": lambda: [list(range(20_000))], "budget": 2.0},
        "pitfalls": ["Checking only the root's two subtree heights is not enough — every node must balance."],
        "solution": """
def is_balanced(root):
    def height(node):
        if node is None:
            return 0
        left = height(node.left)
        if left < 0:
            return -1
        right = height(node.right)
        if right < 0:
            return -1
        if abs(left - right) > 1:
            return -1
        return 1 + max(left, right)

    return height(root) >= 0
""",
    },
    {
        "slug": "diameter-of-binary-tree",
        "title": "Diameter of Binary Tree",
        "difficulty": "Easy",
        "topics": ["Tree", "DFS", "Binary Tree"],
        "url": "https://leetcode.com/problems/diameter-of-binary-tree/",
        "func": "diameter_of_binary_tree",
        "signature": "def diameter_of_binary_tree(root: Optional[TreeNode]) -> int:",
        "description": (
            "Return the length of the longest path between any two nodes, measured in edges. "
            "The path does not have to pass through the root."
        ),
        "examples": ["root = [1,2,3,4,5]  ->  3   (4-2-1-3)", "root = [1,2]  ->  1"],
        "constraints": ["1 <= nodes <= 10^4", "-100 <= Node.val <= 100"],
        "hints": [
            "The best path through a given node is leftHeight + rightHeight edges.",
            "Do one post-order traversal that returns heights and updates a running maximum.",
            "The answer is in edges, so a single node contributes 0.",
        ],
        "target": {"time": "O(n)", "space": "O(h)"},
        "argspec": ["tree"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3, 4, 5]], "expect": 3},
            {"args": [[1, 2]], "expect": 1},
            {"args": [[1]], "expect": 0},
            {"args": [[1, 2, 3, 4, None, None, 5, 6, None, None, 7]], "expect": 6},
        ],
        "stress": {"args": lambda: [list(range(20_000))], "budget": 2.0},
        "pitfalls": [
            "The longest path may not include the root.",
            "Edges, not nodes — off by one is the usual mistake here.",
        ],
        "solution": """
def diameter_of_binary_tree(root):
    best = 0

    def height(node):
        nonlocal best
        if node is None:
            return 0
        left = height(node.left)
        right = height(node.right)
        best = max(best, left + right)
        return 1 + max(left, right)

    height(root)
    return best
""",
    },
    {
        "slug": "binary-tree-level-order-traversal",
        "title": "Binary Tree Level Order Traversal",
        "difficulty": "Medium",
        "topics": ["Tree", "BFS", "Binary Tree"],
        "url": "https://leetcode.com/problems/binary-tree-level-order-traversal/",
        "func": "level_order",
        "signature": "def level_order(root: Optional[TreeNode]) -> List[List[int]]:",
        "description": "Return the values of the tree level by level, left to right, as a list of lists.",
        "examples": [
            "root = [3,9,20,None,None,15,7]  ->  [[3],[9,20],[15,7]]",
            "root = [1]  ->  [[1]]",
            "root = []   ->  []",
        ],
        "constraints": ["0 <= nodes <= 2000"],
        "hints": [
            "BFS with a queue visits nodes in exactly this order.",
            "To know where a level ends, record len(queue) before you start draining it.",
            "Process exactly that many nodes, collecting their children for the next round.",
        ],
        "target": {"time": "O(n)", "space": "O(n)"},
        "argspec": ["tree"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[3, 9, 20, None, None, 15, 7]], "expect": [[3], [9, 20], [15, 7]]},
            {"args": [[1]], "expect": [[1]]},
            {"args": [[]], "expect": []},
            {"args": [[1, 2, 3, 4, None, None, 5]], "expect": [[1], [2, 3], [4, 5]]},
        ],
        "stress": {"args": lambda: [list(range(50_000))], "budget": 2.0},
        "pitfalls": [
            "list.pop(0) is O(n) — use collections.deque.popleft().",
            "Do not append an empty list for a level that has no nodes.",
        ],
        "solution": """
def level_order(root):
    from collections import deque
    if root is None:
        return []
    out = []
    queue = deque([root])
    while queue:
        level = []
        for _ in range(len(queue)):
            node = queue.popleft()
            level.append(node.val)
            if node.left:
                queue.append(node.left)
            if node.right:
                queue.append(node.right)
        out.append(level)
    return out
""",
    },
    {
        "slug": "validate-binary-search-tree",
        "title": "Validate Binary Search Tree",
        "difficulty": "Medium",
        "topics": ["Tree", "DFS", "BST"],
        "url": "https://leetcode.com/problems/validate-binary-search-tree/",
        "func": "is_valid_bst",
        "signature": "def is_valid_bst(root: Optional[TreeNode]) -> bool:",
        "description": (
            "Return True if the tree is a valid binary search tree: every node in a left subtree "
            "is strictly less than its ancestor, every node in a right subtree strictly greater."
        ),
        "examples": [
            "root = [2,1,3]              ->  True",
            "root = [5,1,4,None,None,3,6]  ->  False   (4 sits right of 5)",
        ],
        "constraints": ["1 <= nodes <= 10^4", "-2^31 <= Node.val <= 2^31 - 1"],
        "hints": [
            "Comparing each node only with its direct children is not enough.",
            "Push an allowed (low, high) range down the recursion.",
            "Going left tightens the upper bound to node.val; going right raises the lower bound.",
        ],
        "target": {"time": "O(n)", "space": "O(h)"},
        "argspec": ["tree"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[2, 1, 3]], "expect": True},
            {"args": [[5, 1, 4, None, None, 3, 6]], "expect": False},
            {"args": [[1]], "expect": True},
            {"args": [[5, 4, 6, None, None, 3, 7]], "expect": False},
            {"args": [[2, 2, 2]], "expect": False},
            {"args": [[10, 5, 15, None, None, 6, 20]], "expect": False},
        ],
        "stress": {"args": lambda: [_perfect_bst(14)], "budget": 2.0},
        "pitfalls": [
            "[10,5,15,null,null,6,20] is the trap: 6 is a valid child of 15 but invalid under 10.",
            "Equal values are not allowed on either side.",
        ],
        "solution": """
def is_valid_bst(root):
    def check(node, low, high):
        if node is None:
            return True
        if not (low < node.val < high):
            return False
        return check(node.left, low, node.val) and check(node.right, node.val, high)

    return check(root, float('-inf'), float('inf'))
""",
    },
    {
        "slug": "kth-smallest-element-in-a-bst",
        "title": "Kth Smallest Element in a BST",
        "difficulty": "Medium",
        "topics": ["Tree", "DFS", "BST"],
        "url": "https://leetcode.com/problems/kth-smallest-element-in-a-bst/",
        "func": "kth_smallest",
        "signature": "def kth_smallest(root: Optional[TreeNode], k: int) -> int:",
        "description": "Return the k-th smallest value (1-indexed) in a binary search tree.",
        "examples": [
            "root = [3,1,4,None,2], k = 1            ->  1",
            "root = [5,3,6,2,4,None,None,1], k = 3   ->  3",
        ],
        "constraints": ["1 <= k <= nodes <= 10^4"],
        "hints": [
            "What order does an in-order traversal of a BST produce?",
            "In-order gives the values sorted, so you want the k-th one emitted.",
            "Use an explicit stack and stop as soon as you have popped k nodes — no need to visit the rest.",
        ],
        "target": {"time": "O(h + k)", "space": "O(h)"},
        "argspec": ["tree", "raw"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[3, 1, 4, None, 2], 1], "expect": 1},
            {"args": [[5, 3, 6, 2, 4, None, None, 1], 3], "expect": 3},
            {"args": [[1], 1], "expect": 1},
            {"args": [[3, 1, 4, None, 2], 4], "expect": 4},
            {"args": [[5, 3, 6, 2, 4, None, None, 1], 6], "expect": 6},
        ],
        "stress": {"args": lambda: [_perfect_bst(14), 9_000], "budget": 2.0},
        "pitfalls": ["k is 1-indexed."],
        "solution": """
def kth_smallest(root, k):
    stack = []
    node = root
    while stack or node:
        while node:
            stack.append(node)
            node = node.left
        node = stack.pop()
        k -= 1
        if k == 0:
            return node.val
        node = node.right
    return -1
""",
    },
    {
        "slug": "lowest-common-ancestor-of-a-binary-search-tree",
        "title": "Lowest Common Ancestor of a BST",
        "difficulty": "Medium",
        "topics": ["Tree", "DFS", "BST"],
        "url": "https://leetcode.com/problems/lowest-common-ancestor-of-a-binary-search-tree/",
        "func": "lowest_common_ancestor",
        "signature": "def lowest_common_ancestor(root: 'TreeNode', p: 'TreeNode', q: 'TreeNode') -> 'TreeNode':",
        "description": (
            "Given a BST and two of its nodes `p` and `q`, return their lowest common ancestor — "
            "the deepest node having both as descendants (a node may be a descendant of itself).\n"
            "The harness gives you real nodes and reads `.val` off whatever you return; the test "
            "data lists p and q by value."
        ),
        "examples": [
            "root = [6,2,8,0,4,7,9,None,None,3,5], p = 2, q = 8  ->  6",
            "root = [6,2,8,0,4,7,9,None,None,3,5], p = 2, q = 4  ->  2",
        ],
        "constraints": ["2 <= nodes <= 10^5", "all values unique", "p != q and both exist in the tree"],
        "hints": [
            "Use the BST ordering instead of searching the whole tree.",
            "If both values are smaller than the current node, the answer is in the left subtree; "
            "if both are larger, it is in the right.",
            "The first node that splits them (or equals one of them) is the LCA.",
        ],
        "target": {"time": "O(h)", "space": "O(1)"},
        "argspec": ["tree", "node_in_0", "node_in_0"],
        "retspec": "node_val",
        "compare": "exact",
        "tests": [
            {"args": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 8], "expect": 6},
            {"args": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 2, 4], "expect": 2},
            {"args": [[2, 1], 2, 1], "expect": 2},
            {"args": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 3, 5], "expect": 4},
            {"args": [[6, 2, 8, 0, 4, 7, 9, None, None, 3, 5], 0, 5], "expect": 2},
        ],
        "stress": {"args": lambda: [_perfect_bst(14), 16_000, 100], "budget": 2.0},
        "pitfalls": ["A node can be its own ancestor — [2,1] with p=2 answers 2."],
        "solution": """
def lowest_common_ancestor(root, p, q):
    node = root
    while node:
        if p.val < node.val and q.val < node.val:
            node = node.left
        elif p.val > node.val and q.val > node.val:
            node = node.right
        else:
            return node
    return None
""",
    },
]
