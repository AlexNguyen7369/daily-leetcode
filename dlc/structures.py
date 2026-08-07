"""Data structures used by LeetCode-style problems, plus (de)serializers.

Your solution file can import these:

    from dlc.structures import ListNode, TreeNode
"""

from __future__ import annotations

from typing import Any, List, Optional


class ListNode:
    def __init__(self, val: int = 0, next: "Optional[ListNode]" = None):
        self.val = val
        self.next = next

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        vals, seen, node = [], set(), self
        while node is not None and id(node) not in seen:
            seen.add(id(node))
            vals.append(str(node.val))
            node = node.next
        if node is not None:
            vals.append("...cycle")
        return "ListNode(" + " -> ".join(vals) + ")"


class TreeNode:
    def __init__(
        self,
        val: int = 0,
        left: "Optional[TreeNode]" = None,
        right: "Optional[TreeNode]" = None,
    ):
        self.val = val
        self.left = left
        self.right = right

    def __repr__(self) -> str:  # pragma: no cover - debugging aid
        return f"TreeNode({self.val})"


# --------------------------------------------------------------------------- #
# linked lists
# --------------------------------------------------------------------------- #
def build_linked(values: Optional[List[int]]) -> Optional[ListNode]:
    head = None
    for v in reversed(values or []):
        head = ListNode(v, head)
    return head


def linked_to_list(head: Optional[ListNode], limit: int = 2_000_000) -> List[int]:
    out, seen = [], set()
    while head is not None:
        if id(head) in seen or len(out) > limit:
            raise ValueError("cycle detected in returned list (or list too long)")
        seen.add(id(head))
        out.append(head.val)
        head = head.next
    return out


def build_cycle(spec: List[Any]) -> Optional[ListNode]:
    """spec = [values, pos]; pos == -1 means no cycle."""
    values, pos = spec
    head = build_linked(values)
    if head is None or pos is None or pos < 0:
        return head
    nodes, node = [], head
    while node is not None:
        nodes.append(node)
        node = node.next
    nodes[-1].next = nodes[pos]
    return head


# --------------------------------------------------------------------------- #
# binary trees (LeetCode level-order format, using None for missing children)
# --------------------------------------------------------------------------- #
def build_tree(values: Optional[List[Optional[int]]]) -> Optional[TreeNode]:
    if not values:
        return None
    it = iter(values)
    root = TreeNode(next(it))
    queue = [root]
    i = 0
    while i < len(queue):
        node = queue[i]
        i += 1
        try:
            left = next(it)
        except StopIteration:
            break
        if left is not None:
            node.left = TreeNode(left)
            queue.append(node.left)
        try:
            right = next(it)
        except StopIteration:
            break
        if right is not None:
            node.right = TreeNode(right)
            queue.append(node.right)
    return root


def tree_to_list(root: Optional[TreeNode]) -> List[Optional[int]]:
    if root is None:
        return []
    out: List[Optional[int]] = []
    queue = [root]
    i = 0
    while i < len(queue):
        node = queue[i]
        i += 1
        if node is None:
            out.append(None)
            continue
        out.append(node.val)
        queue.append(node.left)
        queue.append(node.right)
    while out and out[-1] is None:
        out.pop()
    return out


def find_node(root: Optional[TreeNode], val: int) -> Optional[TreeNode]:
    """Locate the node holding `val` (used for problems that take node refs)."""
    stack = [root]
    while stack:
        node = stack.pop()
        if node is None:
            continue
        if node.val == val:
            return node
        stack.append(node.left)
        stack.append(node.right)
    return None
