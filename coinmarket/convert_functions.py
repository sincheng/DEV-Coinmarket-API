
import re
import dateparser

#A function to convert string to number
def convertNumber(inputString,convert_type):
    #Check input string is not none and contain number
    while inputString and bool(re.search(r'\d',inputString)):
        #Remove \n
        s = inputString.replace("\n","")
        n = re.sub(r'[,$%]',"",s)
        return convert_type(n)
    return "NA"

#A function to convert string to formatted_date yyyymmdd
def convertDate(date):
  formatted_date = dateparser.parse(date, date_formats=['%d %B, %Y'])
  return str(formatted_date.date()).replace("-","")
