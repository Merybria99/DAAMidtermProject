from SuffixTree import SuffixTree
from priority_queue.heap_priority_queue import HeapPriorityQueue



class DNAContamination:

    __slots__ = '_string', '_stringStree', '_contaminants', '_treshold'

    def __init__(self, s, l):
        """
        initializes the DNAContamination object
        :param s:string that is used as reference for all the other strings (contaminants)
        :param l:threshold for the contamination degree
        """
        self._string = s
        self._stringStree = SuffixTree([self._string])
        self._treshold = l
        self._contaminants = HeapPriorityQueue()
#o(len(lunghezza stringa))elevato 2 +log(m)
    def addContaminant(self, c):
        """
        function that adds a contaminant c to the structure implemented to store the information
        about the contaminer and the degree of contamination
        :param c:the contaminant
        """
        self._contaminants.add(-1 * len(self._longestSubstrings(c)), c)

    def _longestSubstrings(self, c):
        """
        For each substring in contaminant c is required to visit the tree and get the longest common substring in it.
        Then it is stored in a list if it is considered maximal
        :param c:the contaminant
        :return: the list that contains the maximal strings
        """
        lista =[]
        tree = self._stringStree
        for i in range(len(c)-(self._treshold-1)):
            substring = c[i:]
            currentMatches = self._visitTree(tree, substring)
            if currentMatches >= self._treshold:
                currentValue = [i, i+currentMatches]
                toBeInsert = True
                if len(lista) !=0:
                    previuosValue=lista[-1]
                    if previuosValue[1] == currentValue[1] and previuosValue[0] < currentValue[0]:
                        toBeInsert = False
                if toBeInsert:
                    lista.append(currentValue)

        return lista

    def _visitTree(self, tree, string):
        """
        The function implements the visit of the tree according to the string.
        :param tree:the tree that has to be visited
        :param string: the string according to which the tree has to be visited
        :return: degree of contamination of the string
        """
        node = tree.root()
        string += 'E' #scelgo di usare il carattere E (end) come valore di fine stringa in quanto non facente parte dell'alfabeto
        counterMatch = 0
        childNode = tree.child(node, string[counterMatch])
        while childNode is not None:
            nodeString = tree.getNodeLabel(childNode)

            for car in nodeString:
                if string[counterMatch] == car:
                    counterMatch += 1
                else:
                    return counterMatch
            childNode = tree.child(childNode, string[counterMatch])
        return counterMatch
#o(k log(m))
    def getContaminants(self, k):
        """
        Function that returns the first k contaminants of the string s.
        :param k: indicdates the k contaminants required
        :return:  a list that contains the k contaminants required
        """
        list = {}
        for i in range(min(k, len(self._contaminants))):
            key, value = self._contaminants.remove_min()
            list[value] = -1 * key

        for key, value in list.items():
            self._contaminants.add(-1 * value, key)
        return list.keys()

