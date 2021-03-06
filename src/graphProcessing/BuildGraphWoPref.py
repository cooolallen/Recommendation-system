import pandas as pd
import json
from tqdm import tqdm

#Table 1: product ID, string of tag ID
#Table 2: user id ,product id, rating

class TriGraphWoPref():
    def __init__(self, df_tag=None, df_pref=None, dict=None, userNum=None, userCount=None, 
                 prodUCount=None, prodDCount=None, tagUCount=None, tagDCount=None, NodeList=None):
        print("Initializing Graph...")
        if df_tag is not None and df_pref is not None: 
            self.dict = {}
            self.userNum = 0
            self.userCount = -1
            #self.prefCount = -1
            self.prodUCount = -1
            self.prodDCount = -1
            self.tagUCount = -1
            self.tagDCount = -1
        
            self.users = {}
            #self.prefs = {}
            self.products_U = {}
            self.products_D = {}
            self.tags_U = {}
            self.tags_D = {}
            self.NodeList = {}
            self.buildGraghFromProduct(df_tag)
            self.buildGraghFromUser(df_pref)
        else:
            self.dict = None
            self.userNum = userNum
            self.userCount = userCount
            #self.prefCount = prefCount
            self.prodUCount = prodUCount
            self.prodDCount = prodDCount
            self.tagUCount = tagUCount
            self.tagDCount = tagDCount
        
            self.users = None
            #self.prefs = None
            self.products_U = None
            self.products_D = None
            self.tags_U = None
            self.tags_D = None
            self.NodeList = NodeList
        print("Initializing Graph Done")

    def buildGraghFromUser(self, df):
        prev = ""
        prev_id = -1
        products = []
        count = 0
        print('Building Users...')
        pbar = tqdm(total=len(df.index))
        for _, row in df.iterrows():
            rating = row['rating']
            product = row['product']
            if count == 0: 
                prev = row['user']
                prev_id = self.hashID('user', row['user'])
            count += 1
            #print(row['user'])
            #print('P', prev)
            if row['user'] != prev:
                #construct the graph by prev user
                #print(prev)
                products.sort(key = lambda x: x[1], reverse=True)
                self.dict[prev_id] = []
                if products[0] != products[-1]: 
                    rating_mean = sum([pair[1] for pair in products])/len(products)
                    for item in products:
                        if item[1] > rating_mean:
                            product_id_d = self.hashID('product', item[0], 'D')
                            self.dict[prev_id].append(product_id_d)
                            if product_id_d not in self.dict:
                                self.dict[product_id_d] = [prev_id]
                            else: self.dict[product_id_d].append(prev_id)
                        elif item[1] < rating_mean:
                            product_id_u = self.hashID('product', item[0], 'U')
                            self.dict[prev_id].append(product_id_u)
                            if product_id_u not in self.dict:
                                self.dict[product_id_u] = [prev_id]
                            else: self.dict[product_id_u].append(prev_id)
                    '''
                    for i in range(len(products)-1):
                        for j in range(i+1, len(products)):
                            a = products[i][0]
                            b = products[j][0]
                            if products[i][1] > products[j][1]: 
                                product_id_d = self.hashID('product', a, 'D')
                                product_id_u = self.hashID('product', b, 'U')
                                self.dict[prev_id].append(product_id_d)
                                self.dict[prev_id].append(product_id_u)
                                if product_id_d not in self.dict:
                                    self.dict[product_id_d] = [prev_id]
                                else: self.dict[product_id_d].append(prev_id)
                                if product_id_u not in self.dict:
                                    self.dict[product_id_u] = [prev_id]
                                else: self.dict[product_id_u].append(prev_id)
                    '''
                #Start new user
                prev = row['user']
                prev_id = self.hashID('user', row['user'])
                products = [(product, rating)]
            else: 
                products.append((product, rating))
            pbar.update(1)
        pbar.close()

        products.sort(key = lambda x: x[1], reverse=True)
        self.dict[prev_id] = []
        if products[0] != products[-1]:
            rating_mean = sum([pair[1] for pair in products])/len(products)
            for item in products:
                if item[1] > rating_mean:
                    product_id_d = self.hashID('product', item[0], 'D')
                    self.dict[prev_id].append(product_id_d)
                    if product_id_d not in self.dict:
                        self.dict[product_id_d] = [prev_id]
                    else: self.dict[product_id_d].append(prev_id)
                elif item[1] < rating_mean:
                    product_id_u = self.hashID('product', item[0], 'U')
                    self.dict[prev_id].append(product_id_u)
                    if product_id_u not in self.dict:
                        self.dict[product_id_u] = [prev_id]
                    else: self.dict[product_id_u].append(prev_id)
            '''
            for i in range(len(products)-1):
                for j in range(i+1, len(products)):
                    a = products[i][0]
                    b = products[j][0]
                    if products[i][1] > products[j][1]:
                        product_id_d = self.hashID('product', a, 'D')
                        product_id_u = self.hashID('product', b, 'U')
                        self.dict[prev_id].append(product_id_d)
                        self.dict[prev_id].append(product_id_u)
                        if product_id_d not in self.dict:
                            self.dict[product_id_d] = [prev_id]
                        else: self.dict[product_id_d].append(prev_id)
                        if product_id_u not in self.dict:
                            self.dict[product_id_u] = [prev_id]
                        else: self.dict[product_id_u].append(prev_id)
            '''
    def buildGraghFromProduct(self, df):
        products = []
        print('Building Products and Tags...')
        pbar = tqdm(total=len(df.index))
        for _, row in df.iterrows():
            product = row['product']
            products.append(product)
            product_id_d = self.hashID('product', product, 'D')
            product_id_u = self.hashID('product', product, 'U')
            self.dict[product_id_d] = []
            self.dict[product_id_u] = []
            tags = row['tag'].split(',')
            tagsD = [self.hashID('tag', tag, 'D') for tag in tags]
            tagsU = [self.hashID('tag', tag, 'U') for tag in tags]
            
            for tag_id in tagsD:
                self.dict[product_id_d].append(tag_id)
                if tag_id in self.dict:
                    self.dict[tag_id].append(product_id_d)
                else:
                    self.dict[tag_id] = [product_id_d] 
                
            for tag_id in tagsU:
                self.dict[product_id_u].append(tag_id)
                if tag_id in self.dict:
                    self.dict[tag_id].append(product_id_u)
                else:
                    self.dict[tag_id] = [product_id_u] 
            pbar.update(1)
        pbar.close()
                   
    def hashID(self, type, id, desire = None):

        if type == 'user':
            if id not in self.users:
                self.userCount+=1
                self.users[id] = 'user_' + str(self.userCount)
            return self.users[id]
        
        if type == 'product':
            if desire == 'D':
                if id not in self.products_D:
                    self.prodDCount+=1
                    self.products_D[id] = 'product_D_' + str(self.prodDCount)
                return self.products_D[id]
            if desire == 'U':
                if id not in self.products_U:
                    self.prodUCount+=1
                    self.products_U[id] = 'product_U_' + str(self.prodUCount)
                return self.products_U[id]
        
        if type == 'tag':
            if desire == 'D':
                if id not in self.tags_D:
                    self.tagDCount+=1
                    self.tags_D[id] = 'tags_D_' + str(self.tagDCount)
                return self.tags_D[id]
            if desire == 'U':
                if id not in self.tags_U:
                    self.tagUCount+=1
                    self.tags_U[id] = 'tags_U_' + str(self.tagUCount)
                return self.tags_U[id]
        
        return    
    
    def buildMapping(self, outfileName):
        print('Building the mapping')
        mapping = {'old2new':{},'new2old':{}}
        dl = [self.users, self.products_D, self.products_U, self.tags_D, self.tags_U]
        for idx, name in enumerate(['user', 'item_D', 'item_U', 'tag_D', 'tag_U' ]):
            mapping['old2new'][name] = dl[idx]
            dd = dict((value, key) for key, value in dl[idx].items())
            mapping['new2old'][name] = dd
        outJsonfileName = './corpus/' + outfileName + '.json'
        with open(outJsonfileName, 'w') as outfile:
            json.dump(mapping, outfile)
        return  
            
    def buildNodeList(self, remove = True):
        print("Building the NodeList")
        self.userNum = self.userCount+1
        for key in tqdm(self.dict):
            if remove and not self.dict[key]:
                self.userNum -=1
                continue
            self.NodeList[key] = {}
            self.NodeList[key]['next_user'] = []
            self.NodeList[key]['next_prod'] = []
            self.NodeList[key]['next_tags'] = []
            self.NodeList[key]['Type'] = key.split('_')[0][:4]  
            self.NodeList[key]['Id'] = key
            for item in self.dict[key]:
                s = 'next_' + item[:4]
                self.NodeList[key][s].append(item)   
    
    def getCount(self, remove = True):
        if not remove:
            return [self.userCount+1, 0, self.prodUCount+1, self.prodDCount+1, self.tagUCount+1, self.tagDCount+1]
        return [self.userNum, 0, self.prodUCount+1, self.prodDCount+1, self.tagUCount+1, self.tagDCount+1]

    