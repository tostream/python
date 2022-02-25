class Solution:
    def replaceElements(self, arr: List[int]) -> List[int]:
        max_from_right = arr[-1]
        arr[-1] = -1
        for i in range(len(arr)-2,-1,-1):
            cur = arr[i]
            arr[i] = max_from_right
            max_from_right = max(cur,max_from_right)
        return arr
