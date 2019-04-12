# Creating Field Files from Input String: 
# : it takes in the string of sequence (professor name + professor fields)
#	and creates files for each field, and the content being all the 
# 	professor names that are associated with that field. 

import sys 
import os
import re

def createFieldFiles(inputStr):
	try: 
		os.mkdir('fields')
	except OSError: 
		pass
	
	tempStr = re.sub(r'\d+\.\d+|\d+', '', inputStr)
	strList = tempStr.split()
	profName = []
	for word in strList: 
		if word[0].islower(): 
			if len(profName) > 3: 
				if '.' in profName[-4]:
					profName = profName[-2:]
				else: 
					profName = profName[-3:]

			if ',' in word: 
				print(profName)
				fieldList = word.split(',')
				for field in fieldList:
					output = fieldFile_helper('fields/'+field)
					for name in profName: 	
						output.write(name + ' ')
					output.write('\n')
					output.close()
				profName = []
			else: 
				output = fieldFile_helper('fields/'+word)
				for name in profName: 	
					output.write(name + ' ')
				output.write('\n')
				output.close()
				profName = []
		else: 
			profName.append(word)

# Helper Function for createFieldFiles, returns correct file object, 
# either for creating new files or appending data to existing files	
def fieldFile_helper(fname):
	if os.path.isfile(fname): 
		return open(fname, 'a')
	else: 
		temp = open(fname, 'w')
		temp.close()
		return open(fname, 'a')
