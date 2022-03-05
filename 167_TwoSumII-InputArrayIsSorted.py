class Solution:
    def twoSum(self, numbers: List[int], target: int) -> List[int]:
        arr = {}
        for idx, val in enumerate(numbers):
            temp =  target - val
            if temp in arr:
                return [arr[temp] + 1,idx +1]
            arr[val] = idx
        
        return []
                
