# Definition for singly-linked list.
# class ListNode:
#     def __init__(self, val=0, next=None):
#         self.val = val
#         self.next = next
class Solution:
    def reverseList(self, head: Optional[ListNode]) -> Optional[ListNode]:
        result = []
        while(head):
            result.append(head.val)
            head = head.next
        itr_ans = ans  = ListNode()
        for i in range(len(result)-1,-1,-1):
            ans.next = ListNode()
            ans = ans.next
            ans.val = result[i]
        
        return itr_ans.next
