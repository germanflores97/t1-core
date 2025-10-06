class BusinessException(Exception):
    mensaje: str
    codigo: int

    def __init__(self, *args: object, mensaje:str, codigo:int) -> None:
        super().__init__(*args)

        self.mensaje = mensaje
        self.codigo = codigo
