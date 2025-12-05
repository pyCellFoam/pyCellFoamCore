# Super Cells

class SuperBaseCell:
    __slots__ = (
        "__label_text",
        "__label_text_changed",
        "__my_reverse",
    )

    def __init__(self, my_reverse=None):
        self.__my_reverse = my_reverse
        self.__label_text = ""
        self.__label_text_changed = True

    def __get_label_text(self):
        if self.__label_text_changed:
            self.__label_text = "label_text"
            self.__label_text_changed = False
        return self.__label_text

    label_text = property(__get_label_text)

    def __get_my_reverse(self):
        return self.__my_reverse

    my_reverse = property(__get_my_reverse)

    def __neg__(self):
        return self.__my_reverse


class SuperCell(SuperBaseCell):
    __slots__ = ()

    def __init__(self, *args, my_reverse=None, **kwargs):

        if my_reverse is None:
            my_reverse = SuperReversedCell(*args, my_reverse=self, **kwargs)

        super().__init__(*args, my_reverse=my_reverse, **kwargs)

    def __get_my_reverse(self):
        return self.__my_reverse

    my_reverse = property(__get_my_reverse)


class SuperReversedCell(SuperBaseCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

# Cells

class BaseCell(SuperBaseCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

class Cell(BaseCell, SuperCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

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


# Simple Edges

class BaseSimpleEdge(BaseSimpleCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)




class ReversedSimpleEdge(BaseSimpleEdge, ReversedSimpleCell):
    __slots__ = ()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


    def __get_start_node(self):
        return self.my_reverse.end_node

    def __set_start_node(self, n):
        self.my_reverse.end_node = n

    start_node = property(__get_start_node, __set_start_node)

    def __get_end_node(self):
        return self.my_reverse.start_node

    def __set_end_node(self, n):
        self.my_reverse.start_node = n

    end_node = property(__get_end_node, __set_end_node)


class SimpleEdge(BaseSimpleEdge, SimpleCell):
    __slots__ = (
        "__start_node",
        "__end_node",
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


se = SimpleEdge('A', 'B')
mse = -se

print(se.start_node, se.end_node)
print(mse.start_node, mse.end_node)