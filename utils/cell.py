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
        self.create_bit_cell()

    def show_type_cell(self):
        #  1 parede - 2 42 - 0.5 - passagem - 0 - passagem
        match self._type_cell:
            case 1:
                for linha in self.get_ascii_repre(wall_color="\033[34m",
                                                  show_path=False):
                    print(linha)
            case 2:
                for linha in self.get_ascii_repre(wall_color="\033[36m",
                                                  show_path=False):
                    print(linha)
            case 0.5:
                for linha in self.get_ascii_repre(wall_color="\033[90m",
                                                  show_path=False):
                    print(linha)
            case 0:
                for linha in self.get_ascii_repre(wall_color="\033[90m",
                                                  show_path=False):
                    print(linha)

    def translate_cell(self) -> str:
        """
        Traduz a presença de paredes para um dígito hexadecimal (0-F).

        A tradução segue os pesos: Norte(1), Leste(2), Sul(4), Oeste(8). [1]
        """
        value = 0
        if self._west:
            value += 1  # Bit 0
        if self._south:
            value += 2  # Bit 1
        if self._east:
            value += 4  # Bit 2
        if self._north:
            value += 8  # Bit 3

        return hex(value)[2:].upper()

    def get_ascii_repre(self,
                        wall_color: str = "\033[0m",
                        show_path: bool = False) -> list[str]:
        """
        Retorna a representação visual com o centro sólido e colorido.
        As bordas (paredes) são representadas por caracteres ASCII simples.
        """
        reset = "\033[0m"
        # O bloco sólido que antes ficava nas paredes, agora vai para o centro
        solid_center = "\u2588\u2588\u2588"
        #  empty_center = "   "

        # Cores para elementos especiais do subject [3]
        path_color = "\033[94m"    # Azul para o caminho
        pattern_color = "\033[93m"  # Amarelo para o "42"

        # 1. LINHA SUPERIOR: Paredes North agora são traços simples
        # Cantos com "+" e parede com "---"
        north_wall = "---" if self._north else "   "
        top = f"+{north_wall}+"

        # 2. LINHA DO MEIO: Paredes laterais simples e CENTRO SÓLIDO
        west_wall = "|" if self._west else " "
        east_wall = "|" if self._east else " "

        # Lógica do preenchimento central colorido
        # Por padrão, o centro é a cor de 'parede' escolhida pelo usuário [3]
        fill = f"{wall_color}{solid_center}{reset}"

        # Se for o padrão 42, o centro ganha destaque (Capítulo IV.4) [1]
        if self.cell_version_hex == "F":
            fill = f"{pattern_color} 42 {reset}"
        # Se for o caminho da solução, muda a cor do centro (Capítulo V) [2]
        elif show_path and getattr(self, "_is_path", False):
            fill = f"{path_color}{solid_center}{reset}"

        middle = f"{west_wall}{fill}{east_wall}"

        # 3. LINHA INFERIOR: Paredes South simples
        south_wall = "-" if self._south else "   "
        bottom = f"+{south_wall}+"

        return [top, middle, bottom]