import re
import sys
from operator import add
from pyspark import SparkContext

sc=SparkContext(appName='average')
#For removing header
menu_data=sc.textFile(sys.argv[1]).map(lambda s:s.encode("ascii","ignore"))
header = menu_data.first()
menu_noHeader=menu_data.filter(lambda line: line != header)

menu_noHeader = menu_noHeader.map(lambda s: s[1:-1].split(",")).map(lambda s: (str(s[3]).strip().strip('').replace("'","").replace("-","").replace("~"," ").replace("`"," ").replace("!"," ").replace("@"," ").replace("#"," ").replace("$"," ").replace("%"," ").replace("^"," ").replace("&"," ").replace("*"," ").replace("("," ").replace(")"," ").replace("_"," ").replace("+"," ").replace("="," ").replace("|"," ").replace("}"," ").replace("{"," ").replace("["," ").replace("]"," ").replace("/"," ").replace(":"," ").replace(";"," ").replace("."," ").replace("<"," ").replace(">"," ").replace("?"," ").lower(),int(s[18])))

#strip off null elements
result = menu_noHeader.filter(lambda s: s[0] !='')



#aggregation and average computation 
agg_out = result.aggregateByKey((0,0), lambda U,v: (U[0] + v, U[1] + 1), lambda U1,U2: (U1[0] + U2[0], U1[1] + U2[1]))
average = agg_out.map(lambda (x, (y, z)): (x,z, (float(y)/z))).sortByKey()

output_rdd = average.collect()

output_rdd = average.saveAsTextFile(sys.argv[2])

