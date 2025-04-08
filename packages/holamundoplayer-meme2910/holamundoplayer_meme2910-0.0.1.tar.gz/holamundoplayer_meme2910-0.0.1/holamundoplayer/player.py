"""
Esta es la documentación de Player
"""

class Player:
    """
    Esta es la class de Player crea un reproductode musica
    """

    def play(self, song):
        """
        Reproduce la canción que recibe en el constructor.
        Parameters:
        song (str): String con el path de la canción
        Return:
        int: devuelve 1 si se reproduce con exito, en caso de fracaso devuelve 0
        """
        print("Reproducción de canción")

    def stop(self):
        """
        Detiene la reproducción de la canción que se encuentre activa
        """
        print("Detiene canción")