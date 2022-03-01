class Solution:
    def plusOne(self, digits: List[int]) -> List[int]:
        num = 0
        for i in range(len(digits)):
          num += digits[i] * pow(10, (len(digits)-1-i))
        return [int(i) for i in str(num+1)]
        result = ''
        for i in digits:
            result = result + str(i)
        result = int(result)+1
        result = str(result)
        result_arr = [i for i in result]
        return result_arr
