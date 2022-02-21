class Solution:
    def majorityElement(self, nums: List[int]) -> int:
        result = {}
        majority_len = int(len(nums) / 2)
        for item in nums:
            if item in result:
                result[item] += 1
            else:
                result.update({item:1})
            if result[item] > majority_len:
                return item
