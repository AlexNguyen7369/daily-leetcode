"""Linked lists. Import the node type with:  from dlc.structures import ListNode"""

PROBLEMS = [
    {
        "slug": "reverse-linked-list",
        "title": "Reverse Linked List",
        "difficulty": "Easy",
        "topics": ["Linked List", "Recursion"],
        "url": "https://leetcode.com/problems/reverse-linked-list/",
        "func": "reverse_list",
        "signature": "def reverse_list(head: Optional[ListNode]) -> Optional[ListNode]:",
        "description": (
            "Reverse a singly linked list and return the new head.\n"
            "The test harness passes you a real ListNode chain and reads the result back as a list."
        ),
        "examples": [
            "head = [1,2,3,4,5]  ->  [5,4,3,2,1]",
            "head = [1,2]        ->  [2,1]",
            "head = []           ->  []",
        ],
        "constraints": ["0 <= number of nodes <= 5000", "-5000 <= Node.val <= 5000"],
        "hints": [
            "You need three references: previous, current, and the next node you are about to lose.",
            "Save current.next before you overwrite it.",
            "prev starts as None and ends up being the new head.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["linked"],
        "retspec": "linked",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3, 4, 5]], "expect": [5, 4, 3, 2, 1]},
            {"args": [[1, 2]], "expect": [2, 1]},
            {"args": [[]], "expect": []},
            {"args": [[7]], "expect": [7]},
        ],
        "stress": {"args": lambda: [list(range(50_000))], "budget": 1.5},
        "pitfalls": [
            "Reassigning head.next before saving it drops the rest of the list.",
            "A recursive version costs O(n) stack — fine here, but say so in an interview.",
        ],
        "solution": """
def reverse_list(head):
    prev = None
    while head is not None:
        nxt = head.next
        head.next = prev
        prev = head
        head = nxt
    return prev
""",
    },
    {
        "slug": "merge-two-sorted-lists",
        "title": "Merge Two Sorted Lists",
        "difficulty": "Easy",
        "topics": ["Linked List", "Recursion"],
        "url": "https://leetcode.com/problems/merge-two-sorted-lists/",
        "func": "merge_two_lists",
        "signature": "def merge_two_lists(list1: Optional[ListNode], list2: Optional[ListNode]) -> Optional[ListNode]:",
        "description": (
            "Merge two sorted linked lists into one sorted list by splicing the existing nodes "
            "together, and return the head of the merged list."
        ),
        "examples": [
            "list1 = [1,2,4], list2 = [1,3,4]  ->  [1,1,2,3,4,4]",
            "list1 = [],      list2 = []       ->  []",
            "list1 = [],      list2 = [0]      ->  [0]",
        ],
        "constraints": ["0 <= nodes in each list <= 50", "both lists are sorted ascending"],
        "hints": [
            "A dummy head node removes the 'is this the first element?' special case.",
            "Repeatedly attach whichever current node is smaller and advance that list.",
            "When one list runs out, attach the whole remainder of the other.",
        ],
        "target": {"time": "O(n + m)", "space": "O(1)"},
        "argspec": ["linked", "linked"],
        "retspec": "linked",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 4], [1, 3, 4]], "expect": [1, 1, 2, 3, 4, 4]},
            {"args": [[], []], "expect": []},
            {"args": [[], [0]], "expect": [0]},
            {"args": [[5], [1, 2, 3]], "expect": [1, 2, 3, 5]},
            {"args": [[-9, 3], [5, 7]], "expect": [-9, 3, 5, 7]},
        ],
        "stress": {
            "args": lambda: [list(range(0, 40_000, 2)), list(range(1, 40_000, 2))],
            "budget": 1.5,
        },
        "pitfalls": ["Return dummy.next, not dummy."],
        "solution": """
def merge_two_lists(list1, list2):
    from dlc.structures import ListNode
    dummy = ListNode()
    tail = dummy
    while list1 and list2:
        if list1.val <= list2.val:
            tail.next = list1
            list1 = list1.next
        else:
            tail.next = list2
            list2 = list2.next
        tail = tail.next
    tail.next = list1 or list2
    return dummy.next
""",
    },
    {
        "slug": "linked-list-cycle",
        "title": "Linked List Cycle",
        "difficulty": "Easy",
        "topics": ["Linked List", "Two Pointers"],
        "url": "https://leetcode.com/problems/linked-list-cycle/",
        "func": "has_cycle",
        "signature": "def has_cycle(head: Optional[ListNode]) -> bool:",
        "description": (
            "Return True if the linked list contains a cycle.\n"
            "In the test data a case is written as [values, pos], where pos is the index the tail "
            "connects to (-1 for no cycle). Your function only ever receives the head node."
        ),
        "examples": [
            "head = [3,2,0,-4], pos = 1  ->  True",
            "head = [1,2], pos = 0       ->  True",
            "head = [1], pos = -1        ->  False",
        ],
        "constraints": ["0 <= nodes <= 10^4", "solve it with O(1) memory"],
        "hints": [
            "A set of visited node ids works but costs O(n) memory.",
            "Floyd's algorithm: one pointer moves one step, the other two.",
            "If there is a cycle the fast pointer laps the slow one; otherwise it reaches None.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["linked_cycle"],
        "retspec": "raw",
        "compare": "exact",
        "tests": [
            {"args": [[[3, 2, 0, -4], 1]], "expect": True},
            {"args": [[[1, 2], 0]], "expect": True},
            {"args": [[[1], -1]], "expect": False},
            {"args": [[[], -1]], "expect": False},
            {"args": [[[1, 2, 3], -1]], "expect": False},
            {"args": [[[1], 0]], "expect": True},
        ],
        "stress": {"args": lambda: [[list(range(100_000)), -1]], "budget": 1.5},
        "pitfalls": [
            "Check `fast and fast.next` before stepping twice, or you will hit AttributeError.",
            "Comparing node values instead of node identity gives false positives on duplicates.",
        ],
        "solution": """
def has_cycle(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
        if slow is fast:
            return True
    return False
""",
    },
    {
        "slug": "middle-of-the-linked-list",
        "title": "Middle of the Linked List",
        "difficulty": "Easy",
        "topics": ["Linked List", "Two Pointers"],
        "url": "https://leetcode.com/problems/middle-of-the-linked-list/",
        "func": "middle_node",
        "signature": "def middle_node(head: Optional[ListNode]) -> Optional[ListNode]:",
        "description": (
            "Return the middle node of the list. If there are two middle nodes, return the "
            "second one. (The harness prints the returned node and everything after it.)"
        ),
        "examples": [
            "head = [1,2,3,4,5]    ->  [3,4,5]",
            "head = [1,2,3,4,5,6]  ->  [4,5,6]",
        ],
        "constraints": ["1 <= nodes <= 100"],
        "hints": [
            "Two passes (count, then walk half) is perfectly acceptable.",
            "One pass: move `fast` two steps for every one step of `slow`.",
            "When fast falls off the end, slow sits on the middle.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["linked"],
        "retspec": "linked",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3, 4, 5]], "expect": [3, 4, 5]},
            {"args": [[1, 2, 3, 4, 5, 6]], "expect": [4, 5, 6]},
            {"args": [[1]], "expect": [1]},
            {"args": [[1, 2]], "expect": [2]},
        ],
        "stress": {"args": lambda: [list(range(100_000))], "budget": 1.5},
        "pitfalls": ["For even lengths the answer is the *second* middle — check your loop condition."],
        "solution": """
def middle_node(head):
    slow = fast = head
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    return slow
""",
    },
    {
        "slug": "remove-nth-node-from-end-of-list",
        "title": "Remove Nth Node From End of List",
        "difficulty": "Medium",
        "topics": ["Linked List", "Two Pointers"],
        "url": "https://leetcode.com/problems/remove-nth-node-from-end-of-list/",
        "func": "remove_nth_from_end",
        "signature": "def remove_nth_from_end(head: Optional[ListNode], n: int) -> Optional[ListNode]:",
        "description": "Remove the n-th node counting from the end of the list and return the head.",
        "examples": [
            "head = [1,2,3,4,5], n = 2  ->  [1,2,3,5]",
            "head = [1], n = 1          ->  []",
            "head = [1,2], n = 1        ->  [1]",
        ],
        "constraints": ["1 <= nodes <= 30", "1 <= n <= number of nodes"],
        "hints": [
            "Removing a node requires a reference to the node *before* it.",
            "Send one pointer n steps ahead, then advance both until it reaches the end.",
            "A dummy node in front of the head makes deleting the first element uniform.",
        ],
        "target": {"time": "O(n) one pass", "space": "O(1)"},
        "argspec": ["linked", "raw"],
        "retspec": "linked",
        "compare": "exact",
        "tests": [
            {"args": [[1, 2, 3, 4, 5], 2], "expect": [1, 2, 3, 5]},
            {"args": [[1], 1], "expect": []},
            {"args": [[1, 2], 1], "expect": [1]},
            {"args": [[1, 2], 2], "expect": [2]},
            {"args": [[1, 2, 3], 3], "expect": [2, 3]},
        ],
        "stress": {"args": lambda: [list(range(30_000)), 15_000], "budget": 1.5},
        "pitfalls": [
            "Removing the head is the case everyone forgets — the dummy node handles it.",
            "Off by one: after moving fast n steps, `while fast.next` leaves slow on the predecessor.",
        ],
        "solution": """
def remove_nth_from_end(head, n):
    from dlc.structures import ListNode
    dummy = ListNode(0, head)
    fast = slow = dummy
    for _ in range(n):
        fast = fast.next
    while fast.next is not None:
        fast = fast.next
        slow = slow.next
    slow.next = slow.next.next
    return dummy.next
""",
    },
    {
        "slug": "reorder-list",
        "title": "Reorder List",
        "difficulty": "Medium",
        "topics": ["Linked List", "Two Pointers", "Stack"],
        "url": "https://leetcode.com/problems/reorder-list/",
        "func": "reorder_list",
        "signature": "def reorder_list(head: Optional[ListNode]) -> None:",
        "description": (
            "Reorder the list L0 -> L1 -> ... -> Ln in place to L0 -> Ln -> L1 -> Ln-1 -> ...\n"
            "You may not change node values, only the links. Return nothing."
        ),
        "examples": [
            "head = [1,2,3,4]    ->  [1,4,2,3]",
            "head = [1,2,3,4,5]  ->  [1,5,2,4,3]",
        ],
        "constraints": ["1 <= nodes <= 5 * 10^4", "the reordering must happen in place"],
        "hints": [
            "Three classic sub-problems chained together.",
            "Find the middle (slow/fast), reverse the second half, then interleave the two halves.",
            "Cut the first half's tail (set it to None) before interleaving or you build a cycle.",
        ],
        "target": {"time": "O(n)", "space": "O(1)"},
        "argspec": ["linked"],
        "retspec": "none",
        "compare": "inplace_linked",
        "tests": [
            {"args": [[1, 2, 3, 4]], "expect": [1, 4, 2, 3]},
            {"args": [[1, 2, 3, 4, 5]], "expect": [1, 5, 2, 4, 3]},
            {"args": [[1]], "expect": [1]},
            {"args": [[1, 2]], "expect": [1, 2]},
            {"args": [[1, 2, 3]], "expect": [1, 3, 2]},
        ],
        "stress": {"args": lambda: [list(range(50_000))], "budget": 2.0},
        "pitfalls": [
            "Forgetting to terminate the merged list leaves a cycle — the checker will report it.",
            "Copying values into a list and reassigning them is O(n) space; the problem wants O(1).",
        ],
        "solution": """
def reorder_list(head):
    if head is None or head.next is None:
        return
    slow, fast = head, head.next
    while fast is not None and fast.next is not None:
        slow = slow.next
        fast = fast.next.next
    second = slow.next
    slow.next = None
    prev = None
    while second is not None:
        nxt = second.next
        second.next = prev
        prev = second
        second = nxt
    first, second = head, prev
    while second is not None:
        n1, n2 = first.next, second.next
        first.next = second
        second.next = n1
        first, second = n1, n2
""",
    },
]
