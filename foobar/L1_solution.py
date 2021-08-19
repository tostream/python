#from internet
def answer(s):
	cypher = "abcdefghijklmnopqrstuvwxyz"
	rev_cypher = []
	for letter in range(0, len(cypher)):
		rev_cypher.append(cypher[letter])
	listforward = rev_cypher.copy()
	rev_cypher.reverse()
	decoded_list=[]
	for letter in s:
		if ord(letter)>=97 and ord(letter) <= 122:
			index=rev_cypher.index(letter)
			decoded_list.append(listforward[index])
		else:
			decoded_list.append(letter)
	decoded_str="".join(decoded_list)
	return decoded_str
myanswer = answer("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!")
print(myanswer)

#my solution
def solution(x):
	encode='abcdefghijklmnopqrstuvwxyz'
	decode=encode[::-1]
	cypher = dict(zip(decode,encode))
	result = []
	for i in x:
		if cypher.get(i) is None:
			result.append(i)
		else:
			result.append(cypher.get(i))
	result_str="".join(result)
	return result_str
			

myanswer = solution("Yvzs! I xzm'g yvorvev Lzmxv olhg srh qly zg gsv xlolmb!!")
print(myanswer)
