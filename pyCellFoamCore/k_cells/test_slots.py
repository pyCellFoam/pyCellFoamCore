# Super Cells

class SuperBaseCell:
    __slots__ = (
        "__slot_super_base_cell",
        "__my_reverse",
    )

    def __init__(self, slot_super_base_cell=None, my_reverse=None):
        self.__slot_super_base_cell = slot_super_base_cell
        self.__my_reverse = my_reverse

    def __get_slot_super_base_cell(self):
        return self.__slot_super_base_cell

    def __set_slot_super_base_cell(self, value):
        self.__slot_super_base_cell = value

    slot_super_base_cell = property(
        __get_slot_super_base_cell,
        __set_slot_super_base_cell,
    )

    def __get_my_reverse(self):
        return self.__my_reverse

    def __set_my_reverse(self, value):
        self.__my_reverse = value

    my_reverse = property(
        __get_my_reverse,
        __set_my_reverse,
    )


class SuperCell(SuperBaseCell):
    __slots__ = (
        "__slot_super_cell",
    )

    def __init__(self, slot_super_cell, *args, **kwargs):

        self.__slot_super_cell = slot_super_cell
        super().__init__(*args, **kwargs)

    def __get_slot_super_cell(self):
        return self.__slot_super_cell
    def __set_slot_super_cell(self, value):
        self.__slot_super_cell = value
    slot_super_cell = property(
        __get_slot_super_cell,
        __set_slot_super_cell,
    )

class SuperReversedCell(SuperBaseCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# Cells

class BaseCell(SuperBaseCell):
    __slots__ = (
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




class Cell(BaseCell, SuperCell):
    __slots__ = (
        "__slot_cell",
    )

    def __init__(self, slot_cell, *args, **kwargs):
        self.__slot_cell = slot_cell
        super().__init__(*args, **kwargs)

    def __get_slot_cell(self):
        return self.__slot_cell

    def __set_slot_cell(self, value):
        self.__slot_cell = value

    slot_cell = property(
        __get_slot_cell,
        __set_slot_cell,
    )

class ReversedCell(BaseCell, SuperReversedCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class DualCell(Cell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Simple Cells

class BaseSimpleCell(SuperBaseCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SimpleCell(BaseSimpleCell, SuperCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class ReversedSimpleCell(BaseSimpleCell, SuperReversedCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# Edges

class BaseEdge(BaseCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


class Edge(BaseEdge, Cell):
    __slots__ = (
        "__slot_edge"
    )

    def __init__(self, slot_edge, *args, **kwargs):
        self.__slot_edge = slot_edge
        super().__init__(
            *args,
            my_reverse=ReversedEdge(my_reverse=self),
            **kwargs,
        )

    def __get_slot_edge(self):
        return self.__slot_edge

    def __set_slot_edge(self, value):
        self.__slot_edge = value

    slot_edge = property(
        __get_slot_edge,
        __set_slot_edge,
    )



class ReversedEdge(BaseEdge, ReversedCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def __get_slot_edge(self):
        return self.my_reverse.slot_edge

    def __set_slot_edge(self, value):
        self.my_reverse.slot_edge = value

    slot_edge = property(
        __get_slot_edge,
        __set_slot_edge,
    )


class DualEdge1D(Edge, DualCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DualEdge2D(Edge, DualCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class DualEdge3D(Edge, DualCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


# Simple Edges

class BaseSimpleEdge(BaseSimpleCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)





class ReversedSimpleEdge(BaseSimpleEdge, ReversedSimpleCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class SimpleEdge(BaseSimpleEdge, SimpleCell):
    __slots__ = (
        "__slot_simple_edge"
    )

    def __init__(self, start_node, end_node, *args, **kwargs):
        super().__init__(
            *args,
            my_reverse=ReversedSimpleEdge(my_reverse=self),
            **kwargs,
        )
        self.__start_node = start_node
        self.__end_node = end_node

    def __get_start_node(self):
        return self.__start_node

    def __set_start_node(self, n):
        self.__start_node = n

    start_node = property(__get_start_node, __set_start_node)

    def __get_end_node(self):
        return self.__end_node

    def __set_end_node(self, n):
        self.__end_node = n

    end_node = property(__get_end_node, __set_end_node)


de = DualEdge3D(slot_edge="edge_slot",
                slot_cell="cell_slot",
                slot_super_cell="super_cell_slot",
                slot_super_base_cell="super_base_cell_slot")


print("DualEdge3D:", de.slot_super_base_cell)
print("DualEdge3D slot_edge:", de.slot_edge)

e = Edge(slot_edge="edge_slot",
         slot_cell="cell_slot",
         slot_super_cell="super_cell_slot",
         slot_super_base_cell="super_base_cell_slot")

print("Edge:", e.slot_super_base_cell)
print("Edge slot_edge:", e.slot_edge)

re = e.my_reverse
print("ReversedEdge:", re.slot_super_base_cell)
print("ReversedEdge slot_edge:", re.slot_edge)

try:
    re.test = 5
    print("ReversedEdge test attribute:", re.test)
except AttributeError as e:
    print("Caught AttributeError as expected:", e)