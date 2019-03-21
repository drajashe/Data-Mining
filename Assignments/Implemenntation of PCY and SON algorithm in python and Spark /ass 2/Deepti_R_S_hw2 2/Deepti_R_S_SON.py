import sysfrom pyspark import SparkContextimport itertoolsfrom  collections import defaultdictimport mathimport csvcandidate_set=frozenset()frequent_item_sets=set()new_global=[]from operator import addsc = SparkContext(appName="SON_Apriori")input_file = sys.argv[1]support_threshold = float(sys.argv[2])def Items_with_minimum_threshold(item_set, baskets):        support_threshold_1 = math.ceil(support_threshold * len(baskets))        frequent_item_set = set()        tot_items = defaultdict(int)        for basket in baskets:            for item in item_set:                if item.issubset(basket):                    tot_items[item]=tot_items[item] + 1        for item, count in tot_items.items():            if count >= support_threshold_1:                frequent_item_set.add(item)        return frequent_item_setdef construct_candidate_sets(frequent_set, kth):        new_candidate_set = set()        for item_k in frequent_set:            for item_j in frequent_set:                new_candidate = item_k.union(item_j)                if len(new_candidate) == kth:                    new_candidate_set.add(new_candidate)        return new_candidate_setdef find_global_frequent_sets(transaction_list):        candidate_set_count = defaultdict(int)        for transaction in transaction_list:            #print transaction            basket = frozenset(transaction.split(','))            #print basket            for candidate in candidate_set:                if candidate.issubset(basket):                    candidate_set_count[candidate] += 1        yield candidate_set_countdef Apriori(file):    item_set=set()    baskets=[]    for each_tran in file:        items = each_tran.split(',')        baskets.append(frozenset(items))        length_of_baskets = len(baskets)        for item in items:            item_set.add(frozenset([item]))    one_frequent_item_set =Items_with_minimum_threshold(item_set, baskets)    frequent_item_sets.update(one_frequent_item_set)    current_frequent_set = one_frequent_item_set    ith_item_set = 2    #length_frq_sets=len(current_frequent_set)    while len(current_frequent_set) > 0:        candidate_set= construct_candidate_sets(current_frequent_set, ith_item_set)        current_frequent_set = Items_with_minimum_threshold(candidate_set, baskets)        frequent_item_sets.update(current_frequent_set)        ith_item_set += 1    return frequent_item_setsglobal_frequent_set = []rdd = sc.textFile(input_file)candidate_set = frozenset(rdd.mapPartitions(Apriori).collect())#print candidate_setc = sc.parallelize(rdd.mapPartitions(find_global_frequent_sets).collect()).flatMap(lambda x: x.items()).reduceByKey(lambda x,y: x+y).collect()#count_1 =rdd.count()s_T= support_threshold * rdd.count()for item,value in c:    if value >= s_T:        global_frequent_set.append(sorted(list(item)))#print global_frequent_setfor eachlist in global_frequent_set:    eachlist=list(map(int, eachlist))    eachlist=sorted(eachlist)    #print eachlist    new_global.append(eachlist)new_global=sorted(new_global)#print new_globaloutput_file = open(sys.argv[3],"w")#file_writer = csv.writer(output_file)max_len =max(len(each) for each in new_global)+1#print max_lenlength_of_each=[]each=[]for i in range(max_len):    for each in new_global:        each=sorted(each)        if len(each)==1==i:            each=str(each).replace("[","").replace("]","")            output_file.write(each+"\n")        if len(each)==i and len(each)!=1:            each=str(each).replace("[","(").replace("]",")")            output_file.write(each+"\n")    # if(len(each)==1):    #     each=str(each)#.replace("[","(").replace("]",")")    #     output_file.write(each+"\n")    # elif(len(each)==2):    #     each=str(each)#.replace("[","(").replace("]",")")    #     output_file.write(each+"\n")    # elif(len(each)==3):    #     each=str(each)#.replace("[","(").replace("]",")")    #     output_file.write(each+"\n")    # elif(len(each)==4):    #     each=str(each)#.replace("[","(").replace("]",")")    #     output_file.write(each+"\n")    # elif(len(each)==5):    #     each=str(each)#.replace("[","(").replace("]",")")    #     output_file.write(each+"\n")    # elif(len(each)==6):    #     each=str(each)#.replace("[","(").replace("]",")")    #     output_file.write(each+"\n")    #each=str(each)#.replace("[","(").replace("]",")")# file_writer = csv.writer(output_file)# for frequent_items in sorted(global_frequent_set):#     file_writer.writerow(frequent_items)