"""Tree Structure Module

This module provides retrieval algorithms based on tree structures, 
including fuzzy search algorithms that allow for horizontal drift.


"""

class Trie:
    """Tree Structure Class

    This class is used to initialize a tree structure without the 
    need to additionally specify the depth of the tree.

    Attributes:
        dna_dict: dict,The elements contained in the sequence.
        node_nums: int,The number of elements contained in the sequence.
        children: int,Number of tree branches.
        isEnd: int,The value to determine if the tree is terminated.
    
    """

    def __init__(self):
        self.dna_dict = {"A":0,"T":1,"G":2,"C":3}
        self.node_nums = len(self.dna_dict)
        self.children = [None] * self.node_nums
        self.isEnd = False
        self.maxOptimDepth = 3
    #Node retrieval function without drift.
    def searchPrefix(self, prefix: str) -> "Trie":
        dict=self.dna_dict
        node = self
        for ch in prefix:
            ch = dict[ch]
            if not node.children[ch]:
                return None
            node = node.children[ch]
        return node.isEnd

    def insert(self, word: str,label:str) -> None:
        """Add a branch to the tree.
        
        Args:
            word: str,The sequence added to the tree.
            label: str,Sequence of labels.

        """
        node = self
        dict=self.dna_dict
        for ch in word:
            ch = dict[ch]
            if not node.children[ch]:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.isEnd = label

    
    def delete(self,word:str):
        """Deletes a branch from the tree.
        
        Args:
            word: str,Sequences deleted from the tree.

        """
        node = self
        dict=self.dna_dict
        for ch in word:
            ch = dict[ch]
            if not node.children[ch]:
                node.children[ch] = Trie()
            node = node.children[ch]
        node.isEnd = False

    def fuzz_align(self, word):
        """Horizontal drift function

        Args:
            word: Sequence of fuzzy retrieval.
        
        return:
            Returns a list with the positions that need to be drifted 
            laterally and the nodes that can be drifted laterally.
        
        """
        node = self 
        dict = self.dna_dict
        num=0
        tmp_list=[]
        sub_list=[]
        ins_list=[]
        del_list=[]
        len_=len(word)

        for pos, ch in enumerate(word) :

            ch = dict[ch]
            if not node.children[ch]:
                
                for i in range(self.node_nums):
                    if not node.children[i]:
                        pass
                    else:
                        tmp_list.append(i)
                
                maxOptimDepth = self.maxOptimDepth
                traverseNum = min(len_-num-1, maxOptimDepth)
                #print(word,ch,list,num)
                for k in tmp_list:
                    #Deletion
                    depth = 0
                    tmp = node.children[k]
                    while depth < traverseNum:
                        if not tmp.children[dict[word[num+depth]]]:
                            break
                        tmp = tmp.children[dict[word[num+depth]]]
                        depth += 1

                    if depth == traverseNum:
                        del_list.append(k)

                    #Insertion
                    depth = 0
                    tmp = node
                    while depth < traverseNum-1:
                        if not tmp.children[dict[word[num+depth+1]]]:
                            break
                        tmp = tmp.children[dict[word[num+depth+1]]]
                        depth += 1

                    if depth == traverseNum-1:
                        ins_list.append(k)                     

                    #Substitution
                    depth = 0
                    tmp = node.children[k]
                    while depth < traverseNum:                                                
                        if not tmp.children[dict[word[num+depth+1]]]:
                            break
                        tmp = tmp.children[dict[word[num+depth+1]]]
                        depth += 1

                    if depth == traverseNum:
                        sub_list.append(k)

                return [num, sub_list, ins_list, del_list]

            else:
                node = node.children[ch]
            num = num + 1

        return node.isEnd

    def fuzz_fin(self,word,max_value):
        """Fuzzy search with horizontal drift.

        Args:
            word: str,Sequence of search
            max_value: int,The maximum number of horizontal drifts.

        return:
            Returns a list, the first element of which is the index of the final matched 
            core sequence, and the second element is the number of horizontal drifts.
        """

        tmp_list=[[word,0]]
        
        fin_list=["",1000]
        num2dnaDict = {0: 'A', 1: 'T', 2: 'G', 3: 'C'}
        error_list=[]
        while True :
            if tmp_list == [] or fin_list[1] == 0 :

                break
            dna = tmp_list[0]
            
            if dna[1] > max_value :
                break
            del tmp_list[0]
            result = self.fuzz_align(dna[0])
            error_list.append([dna, result])
            if type(result) == int :
                if dna[1] < fin_list[1] :
                    fin_list=[result, dna[1]]
            elif result is False:
                break # To Do...
            elif self.fuzz_align(word)[1] == [] :
                continue
            elif result[0] == len(dna[0])-1:
                for i in range(len(result[1])):
                    chNum = result[1][i]
                    k = dna[0][:result[0]]+num2dnaDict[chNum]
                    tmp_list.append([k,dna[1]+1])
            else:
                for i in range(len(result[1])):
                    chNum = result[1][i]
                    k = dna[0][:result[0]]+num2dnaDict[chNum]+dna[0][result[0]-len(dna[0])+1:]
                    tmp_list.append([k,dna[1]+1])

                # Insertion Fix
                for i in range(len(result[2])):
                    k = dna[0][:result[0]]+dna[0][result[0]-len(dna[0])+1:] + 'A'
                    tmp_list.append([k,dna[1]+1])

                # Deletion Fix
                for i in range(len(result[3])):
                    chNum = result[3][i]
                    k = dna[0][:result[0]]+num2dnaDict[chNum]+dna[0][result[0]-len(dna[0]):]
                    k = k[:16]
                    tmp_list.append([k,dna[1]+1])

        fin_list.append(error_list)
        return fin_list[:2]
    

