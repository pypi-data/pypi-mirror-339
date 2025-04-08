"""
Este es el módulo que incluye la clase 
de reproductor de musica
"""


class Player:
    """

    Esta clase crea un reproductor
    de música
    """

    def play(self, song):
        """

        Reproduce la cancion que recibio
        en el constructor

        Parameters:
        song (str): este es un string con el path de la cancion

        Returns:
        int: 1 si se reprodujo correctamente, 0 si no se reprodujo
        """
        print(f"Reproduciendo canción")

    def stop(self):
        print(f"Deteniendo canción")
