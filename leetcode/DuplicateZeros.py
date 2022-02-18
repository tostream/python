class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        """
        """
        result = []
        i=0
        while(i < len(arr) and len(result) < len(arr)):
            result.append(arr[i])
            if arr[i] ==0 and i < len(arr):
                result.append(arr[i])
            i += 1
        for j in range(len(arr)):
            arr[j] = result[j]
            
#######################
class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
        arr2 = [i for i in arr]
        i=0
        j = 0
        while i < len(arr):
         if not arr2[j]:
            arr[i] = 0
            i+=1
            if i<len(arr):
               arr[i] = 0
         else:
            arr[i] = arr2[j]
         j+=1
         i+=1
          
          
          
#######################
class Solution:
    def duplicateZeros(self, arr: List[int]) -> None:
    # create our incrementor
    i = 0

    # loop through all dynamic elements
    while i < len(arr)-1:
        # if the character is a zero
        if arr[i]==0:
            # remove the last item from the array
            arr.pop()
            # insert a zero in front of current element
            arr.insert(i+1, 0)
            # move one place forward
            i += 1

        # increment to the next character
        i += 1
