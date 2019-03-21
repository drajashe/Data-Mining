from __future__ import divisionimport sysimport osimport itertoolsfrequent_item_list = []false_pos_rate = 0.0all_singles=[]bucket_size = 0frq_sets_all=[]candid_pairs=[]singleton_pairs_list={}support_threshold = 0.0def GeneratehashValues(a,b,each_tuple_set):     x,y = each_tuple_set     hash_value=((int(x))*a)+((int(y))*b)     return hash_value % bucket_sizedef calculate_hash(bit_map,hash_bucket,input_file):    with open(input_file) as file:        for transaction in file:            list_transaction = transaction.strip().split(',')            list_transaction = list(map(int, list_transaction))            list_transaction.sort()            subsets_k = itertools.combinations(list_transaction,2)            subset_k_list = list(subsets_k)            for each_subset in subset_k_list:                bucket_number = GeneratehashValues(a,b,each_subset)                hash_bucket.setdefault(bucket_number, 0)                count = hash_bucket[bucket_number]                count = count + 1                hash_bucket[bucket_number] = count    file.close()    for bucket_num, count in hash_bucket.iteritems():        if count >= support_threshold:            bit_map.insert(bucket_num, 1)        else:            bit_map.insert(bucket_num, 0)    return (bit_map,hash_bucket)def calculate_frequent_item_sets(input_file, candidate_item_sets):    candidate_dictionary = {}    with open(input_file) as file:        for each_ele in file:            each_basket = each_ele.strip().split(',')            each_basket = list(map(int, each_basket))            each_basket.sort()            subset_k = itertools.combinations(each_basket,2)            subset_k_list = list(subset_k)            for each_subset in subset_k_list:                if each_subset in candidate_item_sets:                    candidate_dictionary.setdefault(each_subset, 0)                    count = candidate_dictionary.get(each_subset)                    count += 1                    candidate_dictionary[each_subset] = count        file.close()        frequent_item_list = []        infreq_list=[]        #cand_pairs=[]        for candidate_set, count in candidate_dictionary.iteritems():            if count >= support_threshold:                if candidate_item_set not in frequent_item_list:                    frequent_item_list.append(list(candidate_set))    frequent_item_list.sort()    return infreq_list,frequent_item_listdef calculate_candid_itemsets(input_file, bit_map):    candidate_item_set = []    with open(input_file) as file:        for each_ele in file:            each_basket = each_ele.strip().split(',')            each_basket = list(map(int, each_basket))            each_basket.sort()            subset_k = itertools.combinations(each_basket,2)            subset_k_list = list(subset_k)            for each_subset in subset_k_list:                subset_k_1_list = list(itertools.combinations(each_subset,1))                #print "subsets of k-1 length: ", subset_k_1_list                check_flg = 1                for item in subset_k_1_list:                    length = len(item)                    #print length                    if(1 == length):                        for i in range(length):                            if item[i] not in frequent_item_list:                                check_flg = 0                    else:                        if list(item) not in frequent_item_list:                            check_flg = 0                if check_flg == 1:                    bucket_number = GeneratehashValues(a,b,each_subset)                    if(1 == bit_map[bucket_number]):                        if each_subset not in candidate_item_set:                            candidate_item_set.append(each_subset)    file.close()    return subset_k_list,candidate_item_setif __name__ == '__main__':        input_file = sys.argv[1]        a = sys.argv[2]        b = sys.argv[3]        bucket_size = sys.argv[4]        support_threshold = sys.argv[5]        foldername=sys.argv[6]        a=int(a)        b=int(b)        support_threshold = float(support_threshold)        bucket_size = int(bucket_size)        path= foldername        if not os.path.exists(path):            os.makedirs(path)        file = open(input_file,'r')        for transaction in file:            transaction = transaction.strip().split(',')            transaction = list(map(int, transaction))            for each_basket in transaction:                singleton_pairs_list.setdefault(each_basket, 0)                count = singleton_pairs_list.get(each_basket)                count += 1                singleton_pairs_list[each_basket] = count            singleton_dict=singleton_pairs_list        file.close()        for item, count in singleton_dict.iteritems():            if count >= support_threshold:                frequent_item_list.append(int(item))                all_singles.append(int(item))            else:                all_singles.append(int(item))        all_singles=sorted(all_singles)        frequent_item_list.sort()        frq_sets_all.append(frequent_item_list)        while 0 != len(frequent_item_list):            hashBucket = {}            for i in range(bucket_size):                hashBucket[i] = 0            bit_map_list = [0]            bit_map_list,hashBucket= calculate_hash(bit_map_list,hashBucket,input_file)            count_bit_values=0            freq_buckets_hash_values=[]            infreq_buckets_hash_values=[]            for key,value in hashBucket.iteritems():                if value>=support_threshold:                    freq_buckets_hash_values.append(key)                else:                    infreq_buckets_hash_values.append(key)            subset_k_list,candidate_item_set = calculate_candid_itemsets(input_file, bit_map_list)            for pairs in itertools.combinations(all_singles,2):                hash_value_com=((pairs[0]*a + pairs[1]*b) % bucket_size)                #print hash_value_com                if(hash_value_com in infreq_buckets_hash_values ) and pairs[0] in frequent_item_list and pairs[1] in frequent_item_list :                    candid_pairs.append(pairs)            infreq_list,frequent_item_list = calculate_frequent_item_sets(input_file, candidate_item_set)            #            # print infreq_list            frq_sets_all.append(frequent_item_list)            for i in bit_map_list:                if i == 1 :                    count_bit_values=count_bit_values+1            false_pos_rate= count_bit_values/bucket_size            false_pos_rate=round(false_pos_rate,3)        print "False Positive Rate:"+ str(false_pos_rate)        filename1 = 'frequentset.txt'        frq_file = open(os.path.join(path, filename1), "w")        for pairs in frq_sets_all:            for all in pairs:                all=str(all).replace("[","(").replace("]",")")                frq_file.write(str(all))                frq_file.write('\n')        frq_file.close()        filename2 = 'candidates.txt'        cand_file= open(os.path.join(path, filename2), "w")        for items in candid_pairs:            cand_file.write(str(items)+'\n')        cand_file.close()