class LuhnValidations:
    @staticmethod
    def _clean_number(s: str) -> str:
        """Quita espacios y guiones; no permite otros caracteres."""
        cleaned = s.replace(" ", "").replace("-", "")
        if not cleaned.isdigit():
            raise ValueError("La cadena debe contener sólo dígitos, espacios o guiones.")
        return cleaned

    @staticmethod
    def luhn_checksum(number: str) -> int:
        """
        Calcula el Luhn checksum (suma total mod 10) de un número dado SIN incluir
        un dígito de control final (o con él, según uso). Devuelve la suma total % 10.
        Si el resultado es 0, el número es válido según Luhn.
        """
        n = LuhnValidations._clean_number(number)
        total = 0
        # Se itera de derecha a izquierda, alternando la operación de doblar
        reverse_digits = n[::-1]
        for i, ch in enumerate(reverse_digits):
            d = ord(ch) - ord('0')  # dígito como entero
            if i % 2 == 1:
                # posiciones impares (1,3,5...) desde la derecha: doblar
                d *= 2
                if d > 9:
                    d -= 9  # equivalente a sumar los dígitos de d
            total += d
        return total % 10

    @staticmethod
    def is_luhn_valid(number: str) -> bool:
        """
        Devuelve True si el número (incluyendo su dígito de control) es válido según Luhn.
        Acepta espacios y guiones intermedios.
        """
        return LuhnValidations.luhn_checksum(number) == 0

    @staticmethod
    def calculate_luhn_check_digit(partial_number: str) -> str:
        """
        Dado un número sin el dígito de control (por ejemplo, 15 dígitos para tarjetas de 16),
        calcula y devuelve el dígito de control (0-9) que hace que el número completo
        sea válido según Luhn.
        """
        n = LuhnValidations._clean_number(partial_number)
        # Para calcular el dígito de control se añade temporalmente un '0' al final
        # y se calcula qué valor hace que el checksum sea 0.
        checksum_with_zero = LuhnValidations.luhn_checksum(n + "0")
        if checksum_with_zero == 0:
            return "0"
        else:
            return str(10 - checksum_with_zero)

    @staticmethod
    def append_luhn_check_digit(partial_number: str) -> str:
        """Devuelve el número completo añadiendo el dígito de control calculado."""
        d = LuhnValidations.calculate_luhn_check_digit(partial_number)
        return LuhnValidations._clean_number(partial_number) + d