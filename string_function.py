# Creating Field Files from Input String: 
# : it takes in the string of sequence (professor name + professor fields)
#	and creates files for each field, and the content being all the 
# 	professor names that are associated with that field. 

import sys 
import os
import re

def createFieldFiles(inputStr, fieldDir):
	res = set()
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
					# //
					find = ''
					for Area, subArea in fieldDir.items():
						if field in subArea:
							find = Area
					if find == '':
						break

					output = fieldFile_helper('fields/'+find+'/'+field)
					tempName  = ' '.join(profName)
					res.add(tempName)

					for name in profName: 	
						output.write(name + ' ')
					output.write('\n')
					output.close()
				profName = []
			else:
				# //
				find = ''
				for Area, subArea in fieldDir.items():
					if word in subArea:
						find = Area
				if find == '':
					break

				output = fieldFile_helper('fields/'+find+'/'+word)

				for name in profName: 	
					output.write(name + ' ')
				tempName = ' '.join(profName)
				res.add(tempName)
				output.write('\n')
				output.close()
				profName = []
		else: 
			profName.append(word)
	return res

# Helper Function for createFieldFiles, returns correct file object, 
# either for creating new files or appending data to existing files	
def fieldFile_helper(fname):
	if os.path.isfile(fname): 
		return open(fname, 'a')
	else: 
		temp = open(fname, 'w')
		temp.close()
		return open(fname, 'a')



if __name__ == "__main__":
	name = ' Carla P. Gomes ai Bart Selman ai,ml Joseph Y. Halpern ai Daniel D. Lee robotics Rafael Pass theory,crypto Kilian Q. Weinberger ml Tanzeem Choudhury hci Siddhartha Banerjee ml,metrics Arpita Ghosh ecom,web+ir Robert D. Kleinberg theory,ecom Volodymyr Kuleshov ml,ai,ecom Jon M. Kleinberg web+ir,ml,ecom David B. Shmoys Karthik Sridharan ml 8 '
	createFieldFiles(name)
