from struttureImpiegate.Tree import Tree
from struttureImpiegate.probe_hash_map import ProbeHashMap


class SuffixTree(Tree):
    """class representing the suffix tree"""
    class Position():
        """abstraction used to contain the reference to the tree and the node, whic contains information about the substring stored"""
        __slots__ = '_container', '_node'

        def __init__(self, container, node):
            """initializes the node"""
            self._container = container
            self._node = node

        def element(self):
            """returns the element stored in the node"""
            return self._node._element

        def __eq__(self, other):
            """defines the equal operation"""
            return type(other) is type(self) and other._node is self._node

    class _Node:
        """class which stores infos about the substring in the node"""
        __slots__ = '_element', '_parent', '_children', '_marker'

        def __init__(self, element, parent):
            """initializes the node
                 element: is a type item which contains the infos
                parent: is a position, reference to the father of the node
                marker: is a list used to espress which string the substring belongs to
                children: is an hash table in which references to children nodes are stored"""
            self._element = element
            self._parent = parent
            self._children = ProbeHashMap(5)
            self._marker = set([])

    # item nel quale memorizzo la informazione
    class _Item:
        """class which stores a list that contains """
        __slots__ = '_substring', '_lengthSubstring'

        def __init__(self, index, begin, end, length=0):
            """initializes the item
                :param index: represents the index of the string
                :param begin: represents the beginning character index in the string
                :param end:represents the ending index in the string
                :param length: represents the length of the substring
            """
            self._substring = [index, begin, end]
            self._lengthSubstring = length

    # funzione che permette di verificare se la position è valida, in tal caso ne restituisce il nodo contenuto all'interno
    def _validate(self, position):
        """validates a position by checking its type and the correct initialization of the node within it
            :param position: represents the position to be checked
            :returns the corresponding node if the position is correct otherwise raises an exception
        """
        if not isinstance(position, self.Position):
            raise TypeError("p is not a valid position")
        if self is not position._container:
            raise ValueError("position p does not belong to this tree")

        if position._node._parent is position._node:
            raise ValueError("position p is not valid anymore")
        return position._node

    # funzione che permette di incapsulare un dato nodo in una position
    # se il nodo fornito è valido allora ritorna la position, None altrimenti
    def _make_position(self, node):
        """creates a position froma a node
            :param node: nodes which needs to be wrapped into a position
            :returns the corresponding position if the position is correct otherwise None
        """
        return self.Position(self, node) if node is not None else None

    # metodo costruttore
    def __init__(self, stringSet):
        """
            constructor method for the suffix tree
            :param stringSet: a set of strings from which the suffix tree should be built
        """
        self._root = self._Node(self._Item(0, 0, 0),None)
        #self._root = self._make_position(self._root)
        self._size = 1
        self._stringSet = stringSet
        self._getStringsAndSuffixes()

    def __len__(self):
        return self._size

    def root(self):
        """:returns the root position in the tree"""
        return self._make_position(self._root)

    def parent(self, p):
        """:returns the parent position of a generic position p"""
        node = self._validate(p)
        return self._make_position(node._parent)

    # funzione di inserimento del nodo
    def _getStringsAndSuffixes(self):
        """
        the function is called in the initialization and calls the function
        _initializeSuffix to initialize the suffix tree for each substring in each
        word of the stored stringSet
        """
        count = 0
        for string in self._stringSet:
            suffix = ''
            count += 1
            for letter in reversed(string):
                suffix = letter + suffix
                element = self._Item(count, len(string) - len(suffix),
                                     len(string), len(suffix))
                node = self._Node(element, self.root())
                node._marker.add(count)
                self._initializeSuffix(self._make_position(self._root), self._make_position(node))

    
    def _initializeSuffix(self, rad, n):
        """
        function which stores a particular node in the suffix tree
        :param rad: represents the root of the current subtree on which the function has been called
        :param n: represents the node that has to ben insert into the suffix tree
        """
        root = self._validate(rad)
        node = self._validate(n)
        suffix = self._stringSet[node._element._substring[0] - 1][
                 node._element._substring[1]:node._element._substring[2]]

        childrenNodes = root._children

        if len(suffix) == 0:
            childrenNodes['\0'] = self._make_position(node)
            return

        key = suffix[0:1]

        try:
            keyChild = self._validate(childrenNodes[key])
        except:
            childrenNodes[key] = self._make_position(node)

            return

        inWord = keyChild._element._substring[0]
        inBeg = keyChild._element._substring[1]
        inEnd = keyChild._element._substring[2]
        lengthRoot = keyChild._element._lengthSubstring
        nodeString = self._stringSet[inWord - 1][inBeg:inEnd]

        if suffix.startswith(nodeString):
            # aggiorno il marker del nodo keychlid includendo quello del nodo nuovo

            if len(keyChild._children) == 0:  # creo un nodo con terminatore di stringa
                endingItem = self._Item(inWord, inEnd, inEnd, lengthRoot)
                endingNode = self._Node(endingItem, self._make_position(keyChild))
                endingNode._marker.update(keyChild._marker)

                # attacco il nodo vuoto al nodo keychild con chiamata ricorsiva
                self._initializeSuffix(self._make_position(keyChild), self._make_position(endingNode))

            # creo un nodo con la porzione di suffisso da inserire
            newItem = self._Item(node._element._substring[0], node._element._substring[1] + len(nodeString),
                                 node._element._substring[2], node._element._lengthSubstring)
            newNode = self._Node(newItem, self._make_position(keyChild))
            nodeMarker = set(node._marker)
            newNode._marker.update(nodeMarker)
            keyChild._marker.update(nodeMarker)
            # inserisco il nodo come figlio del nodo keychild
            self._initializeSuffix(self._make_position(keyChild), self._make_position(newNode))

            return

        elif nodeString.startswith(suffix):

            # creo un nodo intermedio che ospita la parte unin comune ai due
            intermediateItem = self._Item(inWord, inBeg, inBeg + len(suffix),
                                          keyChild._element._lengthSubstring - (len(nodeString) - len(suffix)))

            intermediateNode = self._Node(intermediateItem, self._make_position(root))
            keyChildMarker = set(keyChild._marker)
            nodeMarker = set(node._marker)
            intermediateNode._marker.update(keyChildMarker)
            intermediateNode._marker.update(nodeMarker)
            # sostituisco il nodo creato a quello preesistente

            childrenNodes[key] = self._make_position(intermediateNode)

            # il nodo precedente viene modificato e insertio come figlio del nodo intermedio
            keyChild._element._substring[1] += len(suffix)

            self._initializeSuffix(self._make_position(intermediateNode), self._make_position(keyChild))

            # aggiungo un nodo con terminatore di stringa
            endCurrentString = len(self._stringSet[node._element._substring[0] - 1])
            endingItem = self._Item(node._element._substring[0], endCurrentString, endCurrentString,
                                    intermediateNode._element._lengthSubstring)
            endingNode = self._Node(endingItem, self._make_position(intermediateNode))
            endingNode._marker = nodeMarker

            # attacco il nodo vuoto al nodo keychild con chiamata ricorsiva
            self._initializeSuffix(self._make_position(intermediateNode), self._make_position(endingNode))

            return
        else:
            # caso in cui c'è un mismatch
            mismatchIndex = [i for i in range(min(len(suffix), len(nodeString))) if suffix[i] != nodeString[i]][0]

            # creo un nodo intermedio dove salvare la stringa comune e lo attacco al posto di keychild
            nodeMarker = set(node._marker)
            intermediateItem = self._Item(inWord, inBeg, inBeg + len(suffix[0:mismatchIndex]), mismatchIndex + root._element._lengthSubstring)

            intermediateNode = self._Node(intermediateItem, self._make_position(root))
            keyChildMarker=keyChild._marker
            intermediateNode._marker.update(keyChildMarker)
            intermediateNode._marker.update(nodeMarker)

            childrenNodes[key] = self._make_position(intermediateNode)

            # modifico il nodo keychild e lo inserisco come figlio del nodo intermediate
            keyChild._element._substring[1] += len(suffix[0:mismatchIndex])
            keyChild._parent = self._make_position(intermediateNode)

            # inserisco il nodo come figlio di intermediate node
            self._initializeSuffix(self._make_position(intermediateNode), self._make_position(keyChild))

            # formo un nuovo nodo con la parte restante del suffisso da inserire come figlio del nodo intermedio
            newItem = self._Item(node._element._substring[0], node._element._substring[1] + len(suffix[0:mismatchIndex]),
                                 node._element._substring[2], node._element._lengthSubstring)
            newNode = self._Node(newItem, self._make_position(intermediateNode))
            newNode._marker.update(nodeMarker)

            # inserisco il nuovo nodo come figlio del nodo intermediate
            self._initializeSuffix(self._make_position(intermediateNode), self._make_position(newNode))
            return

    def pathString(self, p):
        """
        function used to return the path string from the root to the specified position
        :param p: position whose path string is being calculated
        :return: the path string from the root to the position p
        """
        node = self._validate(p)
        str = ''
        while True:
            str = self._getStringFromSet(node._element._substring) + str
            if node._parent is None:
                return str
            node = self._validate(node._parent)


    def _getStringFromSet(self, list):
        """
        function used to get from the srting set the proper substing according to the specified indexes
        :param list: list where in position 0,1,2 are stored the index oh the string into the string set, the beginning and ending indexes
        :return: the substring [list[1]:list[2]] of string stringSet[list[0]]
        """
        return self._stringSet[list[0] - 1][list[1]:list[2]]

    def getNodeLabel(self, position):
        """
        function that gets the string corresponding to a certain position
        :param position: position whose string is desired
        :return: the corresponding string
        """
        node = self._validate(position)
        return self._getStringFromSet(node._element._substring)

    def getNodeDepth(self, position):
        """
        function that calculates the length of the string until that node
        :param position: the position whose depth is desired
        :return: the length of the substring
        """
        node = self._validate(position)
        return node._element._lengthSubstring

    def getNodeMark(self, position):
        """
        function that accesses to the mark of the node
        :param position: position whose mark is desired
        :return: the list of the strings tho which the substring stored in that node belongs to
        """
        node = self._validate(position)
        return node._marker

    def child(self, position, s):
        """
        the function is used to access to the child position of the specified position whose substring
        -starts with the string s
        -is a prefix for the string s
        :param position(SuffixTree.Position): the position where the function is called
        :param s(str): the string
        :returns the child node if it exists or None if it doesn't
        """
        node = self._validate(position)

        children = node._children

        key = s[0]

        try:
            nextNode = children[key]
        except:
            return None

        nextString = self.getNodeLabel(nextNode)

        if nextString.startswith(s):
            return nextNode
        if s.startswith(nextString):
            return nextNode

        return None


