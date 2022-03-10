class Solution:
    def romanToInt(self, s: str) -> int:
        roman_int={'I':1,
        'V':5,
        'X':10,
        'L':50,
        'C':100,
        'D':500,
        'M':1000}
        result = 0
        for i in range(0,len(s)-1):
            if roman_int[s[i]]<roman_int[s[i+1]]:
                result -= roman_int[s[i]]
            else:
                result += roman_int[s[i]]
        return result + roman_int[s[-1]]
class Solution:
    def romanToInt(self, s: str) -> int:
        roman_int={'I':1,
        'V':5,
        'X':10,
        'L':50,
        'C':100,
        'D':500,
        'M':1000}
        result = 0
        temp = 0
        pointer = 1
        for i in range(len(s)-1,0,-1):
            if roman_int[s[i]] > roman_int[s[i-1]]:
                result += temp
                temp = roman_int[s[i]]
                if pointer:
                    pointer = 0
            elif roman_int[s[i]] < roman_int[s[i-1]]:
                if pointer:
                    temp += roman_int[s[i]]
                else:
                    temp -= roman_int[s[i]]
                    result += temp
                    temp = 0
                    pointer = 1
            else:
                if pointer:
                    temp += roman_int[s[i]]
                else:
                    temp -= roman_int[s[i]]
        if pointer:
            temp += roman_int[s[0]]
        else:
            temp -= roman_int[s[0]]
        result += temp
        return result
    
