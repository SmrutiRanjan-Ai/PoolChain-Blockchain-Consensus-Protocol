blockchain={}
blockchain[0]=[{'block':111,'prev':None,'weight':0}]
blockchain[1]=[{'block':121,'prev':111,'weight':0}]
blockchain[2]=[{'block':131,'prev':121,'weight':0},{'block':132,'prev':121,'weight':0}]
blockchain[3]=[{'block':141,'prev':131,'weight':0},{'block':142,'prev':132,'weight':0},{'block':143,'prev':132,'weight':0}]
blockchain[4]=[{'block':151,'prev':141,'weight':0},{'block':152,'prev':142,'weight':0}]
blockchain[5]=[{'block':161,'prev':151,'weight':0},{'block':162,'prev':152,'weight':0},{'block':163,'prev':152,'weight':0}]
blockchain[6]=[{'block':171,'prev':161,'weight':0}]
current_nodes=[]
for i in range(6,-1,-1):
    li=blockchain[i]
    prev_nodes=current_nodes
    current_nodes=[]
    for node in li:
        prev = {}
        leaf=True
        for i in prev_nodes:
            if node['block']==i['prev_hash']:
                node['weight']+=i['weight']
                leaf=False
        node['weight']+=1
        prev['prev_hash']=node['prev']
        prev['weight']=node['weight']
        current_nodes.append(prev)

print(blockchain)