import hashlib
import math
import tree
import proof as p
import block
import treelib


class Blockchain:
    def __init__(self, genesis):
        self.genesis = genesis
        self.tree = tree.Tree(genesis)
        self.pending_tree_blocks = []
        self.blkid_list = []
        self.blockchain = {0:[{'block':genesis,'weight':0}]}
        self.highest_block_num = 0


    def create_block(self, list_trans, blkid, timestamp, version, creator, block_num, prev_hash=None):
        '''Create temp block with proof of work but not added to chain'''
        if prev_hash is None:
            chain=self.get_chain()
            last_block=chain[-1]
            prev_hash = last_block.header['block_hash']
        new_block = block.Block(prev_hash, list_trans, blkid, timestamp, version, creator, block_num)
        p.proof_of_work(new_block)
        return True, new_block

    def add_block_to_chain(self, block, timestamp, chain=None):
        '''takes temp block add to chain'''
        blkid=block.header['blkid']
        if blkid not in self.blkid_list:
            status_b = self.check_block(block)
            if status_b:
                block_num = block.header['block_num']
                prev_block_num = block_num - 1
                prev_hash = block.header['prev_hash']
                if prev_block_num in self.blockchain.keys():
                    prev_blocks = self.blockchain[prev_block_num]
                    for prev_block in prev_blocks:
                        if prev_block['block'].header['block_hash'] == prev_hash:
                            node = {'block': block, 'weight': 0}
                            if block_num in self.blockchain.keys():
                                self.blockchain[block_num].append(node)
                            else:
                                self.blockchain[block_num] = []
                                self.blockchain[block_num].append(node)
                            self.blkid_list.append(blkid)
                            if block_num > self.highest_block_num:
                                self.highest_block_num = block_num
                            self.update_chain_weight()
                            return True,"Block Added"
                    return False, "Block couldnt be Added"
            return False, "Block couldnt be Added because check block failed"
        return False, "Block couldnt be Added because block already exist"

    def get_chain(self):
        chain = []
        li=[]
        next_block = None
        for i in range(0, self.highest_block_num + 1):
            if i in self.blockchain.keys():
                li = self.blockchain[i]
                weight = -1
                if chain:
                    last_block = chain[-1]
                    for node in li:
                        if last_block.header['block_hash'] == node['block'].header['prev_hash'] and node['weight'] > weight:
                            next_block = node['block']
                            weight = node['weight']
                    chain.append(next_block)
                else:
                    chain.append(li[0]['block'])
        return chain

    def visualize_chain(self):
        li=[]
        for i in range(0, self.highest_block_num + 1):
            if i in self.blockchain.keys():
                li = self.blockchain[i]
                print("Height = ",i,end=" - ")
                for node in li:
                    blk=node['block']
                    print(blk.header['blkid'], blk.header['block_num'], "weight", node['weight'], end=" ---")
                print("")




    def update_chain_weight(self):
        current_nodes = []
        for i in range(self.highest_block_num, -1, -1):
            li = self.blockchain[i]
            prev_nodes = current_nodes
            current_nodes = []
            for node in li:
                prev = {}
                for i in prev_nodes:
                    if node['block'].header['block_hash'] == i['prev_hash']:
                        node['weight'] += i['weight']
                node['weight'] += 1
                prev['prev_hash'] = node['block'].header['prev_hash']
                prev['weight'] = node['weight']
                current_nodes.append(prev)

    def last_block(self, chain):
        return chain[-1]


    def check_block(self, block):
        '''check integrity of recvd block'''
        try:
            is_mkl = self.check_mkl_tree(block.mkl_tree)
            if is_mkl:
                is_pow = p.check_pow(block)
                if is_pow:
                    return True
            return False
        except:
            print(block)
            return False

    def check_trans_block(self, block, chain):
        if chain is None:
            chain = self.get_chain()
        trans_list = []
        for i in chain:
            trans_list.extend(self.get_block_values(i))
            if block.header['prev_hash'] == i.header['block_hash']:
                break
        blk_trans_list = self.get_block_values(block)
        '''for i in blk_trans_list:
            if i in trans_list:
                print("duplicate")
                return False'''

        for i in blk_trans_list:
            if not self.verify_trans_balance(trans_list, i.amount, i.sender):
                print("bal<i", i, False)
                return False
        return True

    def get_chain_trans_list(self, chain):
        trans_list = []
        for i in chain:
            li = self.get_block_values(i)
            trans_list.extend(li)
        return trans_list

    @staticmethod
    def get_block_values(block):
        '''get values of merkle tree leaves sans dummy'''
        block_list = block.mkl_tree.trans_list
        block_list = [i for i in block_list if i != 'dummy']
        return block_list

    def get_block_mkl_tree_index_list(self, block):
        '''get index range of merkle tree leaves incl. dummy'''
        n = len(block.mkl_tree)
        index = (n // 2)
        return index, n

    @staticmethod
    def verify_trans_balance(total_list, amount, node):
        node_id = node.id
        credit = 0
        debit = 0
        total_list = [i for i in total_list if i != 'dummy']
        if total_list:
            for t in total_list:
                if t.sender == node_id:
                    debit += t.amount
                elif t.receiver == node_id:
                    credit += t.amount
        bal = credit - debit
        if amount <= bal:
            return True
        else:
            return False

    def get_blk_object(self, blkid):
        '''get block object from input block id'''
        for i in self.block_list:
            if i.header['blkid'] == blkid:
                return i
        return None

    def get_blk_header(self, blkid):
        '''get block header from input block id'''
        block = self.get_blk_object(blkid)
        if block is None:
            return None
        else:
            return block.header

    def get_blk_hash(self, blkid):
        '''get block hash from input block id'''
        block = self.get_blk_object(blkid)
        if block is None:
            return None
        else:
            return block.header['block_hash']

    def check_mkl_tree(self, mkl_tree):
        '''create intgegrity of merkel tree'''
        trans_list = mkl_tree.trans_list
        tree = mkl_tree.hash_tree
        ln = len(trans_list)
        level = int(math.log2(ln))
        for i in range(ln):
            hash_val = hashlib.sha256(str(trans_list[i]).encode()).hexdigest()
            if tree[ln - 1 + i] != hash_val:
                return False
        while level > 0:
            for k in range(0, 2 ** level, 2):
                index = 2 ** level - 1
                parent = (index + k) // 2
                hash_str = str(tree[index + k]) + str(tree[index + k + 1])
                if tree[parent] != hashlib.sha256(hash_str.encode()).hexdigest():
                    print('Hash Mismatch')
                    return False
            level -= 1
        return True

    def visualize_tree(self):
        tlib = treelib.Tree()
        stack = [self.tree.root]
        tlib.create_node((self.tree.root.header['blkid'], self.tree.root.header['timestamp']),
                         self.tree.root.header['blkid'])
        while stack:
            parent = stack.pop()
            for child in parent.adj_matrix:
                try:
                    tlib.create_node((child.header['blkid'], child.header['creator']), child.header['blkid'],
                                     parent=parent.header['blkid'])
                except:
                    pass
                stack.append(child)
        tlib.show()

    def tree_traverse_blkid(self, print_id=False):
        stack = [self.tree.root]
        blkid_list = []
        while stack:
            parent = stack.pop()
            blkid_list.append(parent.header['blkid'])
            for child in parent.adj_matrix:
                stack.append(child)
        if print_id: print(*blkid_list)
        return blkid_list

    def if_prev_block_child_exists(self, block):
        prev = block.header['prev_hash']
        if self.tree.check_node_hash(prev):
            return True
        else:
            return False
