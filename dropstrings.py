def solution(S):
    return process_string(S, 'A', 'B')
    #return replacestring(S, 'AB')
    # pass


def replacestring(S, A):
    result = S
    for i in A:
        for j in A:
            if i != j:
                result = result.replace(i + j, '')
    return result


def process_string(S, basechar, nearchar):
    i = 0
    while (len(S) > i):
        if S[i] == basechar:
            if i == 0 and S[i + 1] == nearchar:
                S = S[i + 2:]
                print(S + '1')
            elif i != len(S) - 1 and S[i + 1] == nearchar:
                S = S[0:i] + S[i + 2:]
                print(S + '2')
            elif i != len(S) - 1 and S[i - 1] == nearchar:
                S = S[0:i - 1] + S[i + 1:]
                print(S + '3')
                i -= 1
            elif S[i - 1] == nearchar:
                S = S[0:i - 1] + S[i + 1:]
                print(S + '4')
            else:
                i += 1
        else:
            i += 1
    return S


s = 'ABDEFAHABCBSABFBACCCABBAABBA'
print(solution(s))
