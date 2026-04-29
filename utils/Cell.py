class Cell():
    def __init__(self,
                 west: int,
                 south: int,
                 east: int,
                 north: int,
                 type: int):
        self._west: int = west
        self._south: int = south
        self._east: int = east
        self._north: int = north
        self._bit_cell: list[int] = []
        self.cell_version_hex: str | None = None
        self._type_cell = type

    def create_bit_cell(self) -> str | None:
        self._generate_list_bit_initial()
        self.cell_version_hex = self.translate_cell()
        return self.cell_version_hex

    def _generate_list_bit_initial(self) -> None:
        if (self._bit_cell is None
           and self._west is not None
           and self._south is not None
           and self._east is not None
           and self._north is not None):
            self._bit_cell[self._west, self._south, self._east, self._north]

    def set_bit_cell(self,
                     west: int,
                     south: int,
                     east: int,
                     north: int,
                     type: int):

        self._west = west
        self._south = south
        self._east = east
        self._north = north
        self._type_cell = type
        if (self._west == 2):
            self._west = 1
        if (self._east == 2):
            self._east = 1
        if (self._south == 2):
            self._south = 1
        if (self._north == 2):
            self._north = 1
        self.create_bit_cell()

    def translate_cell(self) -> str:
        """
        Traduz a presença de paredes para um dígito hexadecimal (0-F).

        A tradução segue os pesos: Norte(1), Leste(2), Sul(4), Oeste(8). [1]
        """
        value = 0
        if self._west:
            value += 8  # Bit 0
        if self._south:
            value += 4  # Bit 1
        if self._east:
            value += 2  # Bit 2
        if self._north:
            value += 1  # Bit 3
        return hex(value)[2:].upper()

    def get_ascii_repre(self, wall_color: str = "\033[0m") -> list[str]:
        reset = "\033[0m"
        block = "\u2588\u2588\u2588"  # ███ws

        line = f"{wall_color}{block}{reset}"

        # retorna 3 linhas iguais pra manter proporção
        return [line, line, line]
