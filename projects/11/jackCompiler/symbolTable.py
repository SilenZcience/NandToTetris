from enum import Enum


class VarKind(Enum):
    FIELD  = 'this'
    STATIC = 'static'
    LOCAL  = 'local'
    ARG    = 'argument'


class SymbolTable:
    VAR_TYPE  = 0
    VAR_KIND  = 1
    VAR_INDEX = 2

    def __init__(self):
        self.class_table = {}
        self.subroutine_table = {}
        self.index_counter = {k.value: 0 for k in VarKind}

    @staticmethod
    def get_segment(kind: VarKind) -> str:
        """
        Returns the segment name for a given variable kind.
        """
        if isinstance(kind, VarKind):
            return kind.value
        raise ValueError(f"Unknown variable kind: {kind}")

    def start_subroutine(self) -> None:
        """
        Resets the subroutine table for a new subroutine.
        """
        self.subroutine_table = {}
        self.index_counter[VarKind.LOCAL.value] = 0
        self.index_counter[VarKind.ARG.value]   = 0

    def add(self, name: str, type_: str, kind: VarKind) -> None:
        """
        Defines a new variable in the current scope.
        """
        if kind in (VarKind.FIELD, VarKind.STATIC):
            self.class_table[name] = (type_, kind, self.index_counter[kind.value])
        else: # local or argument
            self.subroutine_table[name] = (type_, kind, self.index_counter[kind.value])
        self.index_counter[kind.value] += 1


    def get_max_index(self, kind: VarKind) -> int:
        """
        Returns the number of variables of a given kind in the current scope.
        """
        if isinstance(kind, VarKind):
            return self.index_counter[kind.value]
        raise ValueError(f"Unknown variable kind: {kind}")

    def get_info(self, name: str, info_type: int):
        """
        Returns the requested information about a variable.
        info_type can be VAR_TYPE, VAR_KIND, or VAR_INDEX.
        """
        if name in self.class_table:
            return self.class_table[name][info_type]
        if name in self.subroutine_table:
            return self.subroutine_table[name][info_type]
        return None
