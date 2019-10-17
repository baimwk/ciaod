BLACK = 'BLACK'
RED = 'RED'
NIL = 'NIL'


class Node:
    def __init__(self, value, color, parent, left=None, right=None):
        self.value = value
        self.color = color
        self.parent = parent
        self.left = left
        self.right = right

    def __repr__(self):
        return '{color} {val} Node'.format(color=self.color, val=self.value)

    def __iter__(self):
        if self.left.color != NIL:
            yield from self.left.__iter__()

        yield self.value

        if self.right.color != NIL:
            yield from self.right.__iter__()

    def __eq__(self, other):
        if self.color == NIL and self.color == other.color:
            return True

        if self.parent is None or other.parent is None:
            parents_are_same = self.parent is None and other.parent is None
        else:
            parents_are_same = self.parent.value == other.parent.value and self.parent.color == other.parent.color
        return self.value == other.value and self.color == other.color and parents_are_same

    def has_children(self) -> bool:
        # есть ли у узла дочерние элементы
        return bool(self.get_children_count())

    def get_children_count(self) -> int:
        # кол-во не нулевых дочерних
        if self.color == NIL:
            return 0
        return sum([int(self.left.color != NIL), int(self.right.color != NIL)])


class RedBlackTree:
    NIL_LEAF = Node(value=None, color=NIL, parent=None)

    def __init__(self):
        self.count = 0
        self.root = None
        self.ROTATIONS = {
            'L': self._right_rotation,
            'R': self._left_rotation
        }

    def __iter__(self):
        if not self.root:
            return list()
        yield from self.root.__iter__()

    def add(self, value):
        if not self.root:
            self.root = Node(value, color=BLACK, parent=None, left=self.NIL_LEAF, right=self.NIL_LEAF)
            self.count += 1
            return
        parent, node_dir = self._find_parent(value)
        if node_dir is None:
            return
        new_node = Node(value=value, color=RED, parent=parent, left=self.NIL_LEAF, right=self.NIL_LEAF)
        if node_dir == 'L':
            parent.left = new_node
        else:
            parent.right = new_node

        self._try_rebalance(new_node)
        self.count += 1

    def remove(self, value):
        # node с 0 или 1 дочерним
        node_to_remove = self.find_node(value)
        if node_to_remove is None:
            return
        if node_to_remove.get_children_count() == 2:
            # найти дочерний и заменить значение, удалить родителя
            successor = self._find_in_order_successor(node_to_remove)
            node_to_remove.value = successor.value  # switch the value
            node_to_remove = successor

        # есть 0 или 1 дочерний
        self._remove(node_to_remove)
        self.count -= 1

    def contains(self, value) -> bool:
        # есть ли значение в дереве
        return bool(self.find_node(value))

    def ceil(self, value) -> int or None:
        # есть значение, найти ближайшее >=. None, если такого нет
        if self.root is None: return None
        last_found_val = None if self.root.value < value else self.root.value

        def find_ceil(node):
            nonlocal last_found_val
            if node == self.NIL_LEAF:
                return None
            if node.value == value:
                last_found_val = node.value
                return node.value
            elif node.value < value:
                return find_ceil(node.right)
            else:
                last_found_val = node.value

                return find_ceil(node.left)
        find_ceil(self.root)
        return last_found_val

    def floor(self, value) -> int or None:
        # есть значение, найти ближайшее < =. None, если такого нет
        if self.root is None: return None
        last_found_val = None if self.root.value > value else self.root.value

        def find_floor(node):
            nonlocal last_found_val
            if node == self.NIL_LEAF:
                return None
            if node.value == value:
                last_found_val = node.value
                return node.value
            elif node.value < value:
                last_found_val = node.value

                return find_floor(node.right)
            else:
                return find_floor(node.left)

        find_floor(self.root)
        return last_found_val

    def _remove(self, node):
        left_child = node.left
        right_child = node.right
        not_nil_child = left_child if left_child != self.NIL_LEAF else right_child
        if node == self.root:
            if not_nil_child != self.NIL_LEAF:
                # удаляя корень, сделать дочерний корневым
                self.root = not_nil_child
                self.root.parent = None
                self.root.color = BLACK
            else:
                self.root = None
        elif node.color == RED:
            if not node.has_children():
                # красный узел без детей - самый простой  Удалить
                self._remove_leaf(node)
            else:
            # Поскольку узел красный, у него не может быть ребенка.
                raise Exception('Неожиданное поведение')
        else:  # черный
            if right_child.has_children() or left_child.has_children():
                raise Exception('Красный ребенок черного узла с 0 или 1 ребенком не может иметь детей,'
                                'иначе черная высота дерева становится недействительной!')
            if not_nil_child.color == RED:
                # поменяйте значения с красным потомком и удалите его
                node.value = not_nil_child.value
                node.left = not_nil_child.left
                node.right = not_nil_child.right
            else:  # черный лист
                self._remove_black_node(node)

    def _remove_leaf(self, leaf):
        # удалить листья
        if leaf.value >= leaf.parent.value:
            leaf.parent.right = self.NIL_LEAF
        else:
            leaf.parent.left = self.NIL_LEAF

    def _remove_black_node(self, node):
        # перебрать все листья. последний лист - можно удалить
        self.__case_1(node)
        self._remove_leaf(node)

    def __case_1(self, node):
        # есть черный узел в корне, можем удалить, уменьшив черную высоту дерева
        if self.root == node:
            node.color = BLACK
            return
        self.__case_2(node)

    def __case_2(self, node):
        """
        родитель черный, брат красный. дети братьев и сестер - черные или 0
                         40B                                              60B
                        /   \                                            /   \
                    |20B|   60R                                        40R   80B
                           /   \                                        /   \
                         50B    80B                                |20B|  50B
        """
        parent = node.parent
        sibling, direction = self._get_sibling(node)
        if sibling.color == RED and parent.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
            self.ROTATIONS[direction](node=None, parent=sibling, grandfather=parent)
            parent.color = RED
            sibling.color = BLACK
            return self.__case_1(node)
        self.__case_3(node)

    def __case_3(self, node):
        """
        родитель черный, родной брат черный, дети брата черные. делаем брата красным и проходим двойной черн узел

               ___50B___                                           ___50B___
              /         \                                         /         \
           30B          80B                                     30B        |80B|
          /   \        /   \                                   /  \        /   \
        20B   35R    70B   |90B|                             20B  35R     70R   X
              /  \                                               /   \
            34B   37B                                          34B   37B
        """
        parent = node.parent
        sibling, _ = self._get_sibling(node)
        if (sibling.color == BLACK and parent.color == BLACK
           and sibling.left.color != RED and sibling.right.color != RED):

            sibling.color = RED
            return self.__case_1(parent)  # start again

        self.__case_4(node)

    def __case_4(self, node):
        """
        если родитель красный, а брат черный без красных детей, поменять
                __10R__                   __10B__
               /       \                 /       \
             DB        15B              X        15R
                      /   \                     /   \
                    12B   17B                 12B   17B
        """
        parent = node.parent
        if parent.color == RED:
            sibling, direction = self._get_sibling(node)
            if sibling.color == BLACK and sibling.left.color != RED and sibling.right.color != RED:
                parent.color, sibling.color = sibling.color, parent.color  # switch colors
                return
        self.__case_5(node)

    def __case_5(self, node):
        """
              ___50B___                                                    __50B__
             /         \                                                  /       \
           30B        |80B|                                            35B      |80B|
          /  \        /   \                                           /   \      /
        20B  35R     70R   X                                       30R    37B  70R
            /   \                                                 /   \
          34B  37B                                              20B   34B
        """
        sibling, direction = self._get_sibling(node)
        closer_node = sibling.right if direction == 'L' else sibling.left
        outer_node = sibling.left if direction == 'L' else sibling.right
        if closer_node.color == RED and outer_node.color != RED and sibling.color == BLACK:
            if direction == 'L':
                self._left_rotation(node=None, parent=closer_node, grandfather=sibling)
            else:
                self._right_rotation(node=None, parent=closer_node, grandfather=sibling)
            closer_node.color = BLACK
            sibling.color = RED

        self.__case_6(node)

    def __case_6(self, node):
        """
                    __50B__                                       __35B__
                   /       \                                     /       \
                 35B      |80B|                                30R       50R
                /   \      /                                  /   \     /   \
             30R    37B  70R                               20B   34B 37B    80B
            /   \                                                            /
         20B   34B                                                          70R
        """
        sibling, direction = self._get_sibling(node)
        outer_node = sibling.left if direction == 'L' else sibling.right

        def __case_6_rotation(direction):
            parent_color = sibling.parent.color
            self.ROTATIONS[direction](node=None, parent=sibling, grandfather=sibling.parent)
            # новый родитель
            sibling.color = parent_color
            sibling.right.color = BLACK
            sibling.left.color = BLACK

        if sibling.color == BLACK and outer_node.color == RED:
            return __case_6_rotation(direction)

        raise Exception('Что-то не так')

    def _try_rebalance(self, node):
        # балансировка - если родитель красный, попробовать сбалансировать, дочерний красный.
        parent = node.parent
        value = node.value
        if (parent is None
           or parent.parent is None  # родитель - корень
           or (node.color != RED or parent.color != RED)):  # не нужна балансировка
            return
        grandfather = parent.parent
        node_dir = 'L' if parent.value > value else 'R'
        parent_dir = 'L' if grandfather.value > parent.value else 'R'
        uncle = grandfather.right if parent_dir == 'L' else grandfather.left
        general_direction = node_dir + parent_dir

        if uncle == self.NIL_LEAF or uncle.color == BLACK:
            # rotate
            if general_direction == 'LL':
                self._right_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'RR':
                self._left_rotation(node, parent, grandfather, to_recolor=True)
            elif general_direction == 'LR':
                self._right_rotation(node=None, parent=node, grandfather=parent)
                # благодаря предыдущему повороту наш узел теперь является родительским
                self._left_rotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            elif general_direction == 'RL':
                self._left_rotation(node=None, parent=node, grandfather=parent)
                # благодаря предыдущему повороту наш узел теперь является родительским
                self._right_rotation(node=parent, parent=node, grandfather=grandfather, to_recolor=True)
            else:
                raise Exception("{} is not a valid direction!".format(general_direction))
        else:  # дядя красный
            self._recolor(grandfather)

    def __update_parent(self, node, parent_old_child, new_parent):
        # узел меняет места со старым ребенком, назначает нового родителя
        node.parent = new_parent
        if new_parent:
            # определить позицию старого ребенка, чтобы поместить туда узел
            if new_parent.value > parent_old_child.value:
                new_parent.left = node
            else:
                new_parent.right = node
        else:
            self.root = node

    def _right_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_right = parent.right
        parent.right = grandfather
        grandfather.parent = parent

        grandfather.left = old_right  # сохранить старые правые значения
        old_right.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def _left_rotation(self, node, parent, grandfather, to_recolor=False):
        grand_grandfather = grandfather.parent
        self.__update_parent(node=parent, parent_old_child=grandfather, new_parent=grand_grandfather)

        old_left = parent.left
        parent.left = grandfather
        grandfather.parent = parent

        grandfather.right = old_left  # сохранить старые левые значения
        old_left.parent = grandfather

        if to_recolor:
            parent.color = BLACK
            node.color = RED
            grandfather.color = RED

    def _recolor(self, grandfather):
        grandfather.right.color = BLACK
        grandfather.left.color = BLACK
        if grandfather != self.root:
            grandfather.color = RED
        self._try_rebalance(grandfather)

    def _find_parent(self, value):
        # находит место для нового значения
        def inner_find(parent):
            # возвращает род узел и сторону для нового узла
            if value == parent.value:
                return None, None
            elif parent.value < value:
                if parent.right.color == NIL:  # некуда идти
                    return parent, 'R'
                return inner_find(parent.right)
            elif value < parent.value:
                if parent.left.color == NIL:  # некуда идти
                    return parent, 'L'
                return inner_find(parent.left)

        return inner_find(self.root)

    def find_node(self, value):
        def inner_find(root):
            if root is None or root == self.NIL_LEAF:
                return None
            if value > root.value:
                return inner_find(root.right)
            elif value < root.value:
                return inner_find(root.left)
            else:
                return root

        found_node = inner_find(self.root)
        return found_node

    def _find_in_order_successor(self, node):
        right_node = node.right
        left_node = right_node.left
        if left_node == self.NIL_LEAF:
            return right_node
        while left_node.left != self.NIL_LEAF:
            left_node = left_node.left
        return left_node

    def _get_sibling(self, node):
        # возвращает родного брата узла и сторону лево/право
        parent = node.parent
        if node.value >= parent.value:
            sibling = parent.left
            direction = 'L'
        else:
            sibling = parent.right
            direction = 'R'
        return sibling, direction

