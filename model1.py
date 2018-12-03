from collections import defaultdict
import numpy as np
import math 

def parseData(fname):
  for l in open(fname):
    yield eval(l)

print("Reading data...")
data_user_items = list(parseData("./australian_users_items.json"))
print("Done.")

print("Reading the second dataset...")
data_user_reviews = list(parseData("./australian_user_reviews.json"))
print("Done for the second.")

user_item_count = defaultdict(int)
user_items = defaultdict(list)
for d in data_user_items: 
    user = d['user_id']
    count = d['items_count']
    user_item_count[user] = count 
    user_items[user] = d['items']

###########Process to add the item ids into the dictionary###########
def getAllAttributes(user_items): 
    user_items_id = defaultdict(set)
    items_id_user = defaultdict(set)
    user_items_forever = defaultdict(defaultdict)
    for d in user_items.keys(): 
        item_per_user = user_items[d]
        for i in item_per_user:
            user_items_id[d].add(i['item_id'])
            items_id_user[i['item_id']].add(d)
            user_items_forever[d][i['item_id']] = i['playtime_forever']
    return user_items_id, items_id_user, user_items_forever 

user_items_id, items_id_user, user_items_forever = getAllAttributes(user_items)

#########Calculate the Item similarity############
def item_similarity(userItems): 
    N=dict()
    C=defaultdict(defaultdict)
    W=defaultdict(defaultdict)
    for key in userItems: 
        #the items which are purchased by the user
        for i in userItems[key]: 
            if i not in N.keys(): 
                N[i] = 0 
            N[i] += 1 
            for j in userItems[key]: 
                if i == j: 
                    continue
                if j not in C[i].keys(): 
                    C[i][j] = 0 
                C[i][j] += 1 
    print("Finish the first part ")
    for i, related_item in C.items(): 
        for j, cij in related_item.items(): 
            W[i][j] = cij/math.sqrt(N[i]*N[j])
    return W

def norm(user): 
    norm_v = 0 
    for i in user_items_id[user]:
        norm_v += user_items_forever[user][i]
    return norm_v

def allNorms(): 
    N = dict 
    for u in user_items.keys(): 
        N[u] = norm(u)
    return N 
N = allNorms() 
def cosine(items_id_users, user_items_forever, N): 
    C = defaultdict(defaultdict)
    for key in item_id_users: 
        for u1 in item_id_users[key]:
            for u2 in item_id_users[key]: 
                if u1 == u2: 
                    continue 
                if u2 not in C[u1].keys(): 
                    C[u1][u2] = 0
                C[u1][u2] += user_items_forever[u1][key] * user_items_forever[u2][key]

    for key in C:
        for each in C[key]: 
            C[key][each] = C[key][each] / (N[key]*N[each])**0.5
    return C