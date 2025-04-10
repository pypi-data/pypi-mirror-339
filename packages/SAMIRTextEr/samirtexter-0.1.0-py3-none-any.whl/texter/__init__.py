from colorama import Fore, Style
class Nomen:
    def __init__(self):
        with open("Haeufige_Nomen.txt", "r", encoding="utf-8") as file:
            self.nomen_liste = file.read().splitlines() 
    
    def kontrolliere_Nomen(self, Nomen, return_bei_ja="Ja, das ist ein Nomen.", return_bei_nein="Nein, das ist kein Nomen.", Farbe_ja="GREEN", Farbe_nein="RED", Für_print=True):
        """eine Funktion die Nomen korrigiert.
        param: Nomen = Das Nomen dass korrigiert soll.
        param: return_bei_ja = falls es das Nomen gibt, wird return_bei_ja returniert.
        param: return_bei_nein = das gleiche wie bei return_bei_ja, einfach wenn das Nomen falsch ist.
        param: Farbe_ja und Farbe_nein = Farben die returniert werden.* 
        param: Für_print = das die Funktion weiss dass sie in print() benutzt wird.
        * Funktioniert nur, wenn Für_print True ist.
        """
        Farbe_ja = getattr(Fore, Farbe_ja.upper(), Fore.RESET)
        Farbe_nein = getattr(Fore, Farbe_nein.upper(), Fore.RESET)
        Nomen_korigiert = Nomen.capitalize()
        if Nomen in self.nomen_liste or Nomen_korrigiert in self.nomen_liste:
            if Für_print:
                return Fore.Farbe_ja + return_bei_ja + Style.RESET_ALL
            else:
                return return_bei_ja
        else:
            if Für_print:
                return Fore.Farbe_nein + return_bei_nein + Style.RESET_ALL
            else:
                return return_bei_nein
class Wort_korrektur:
    def __init__(self):
        with open("woerter.txt", "r", encoding="utf-8") as file:
            self.woerter_liste = file.read()
            woerter_liste = self.woerter_liste.split(",")
    def kontrolliere_Wort(self, Wort, return_bei_ja="Ja, das Wort gibt es.", return_bei_nein="Nein, das Wort gibt es nicht.", Farbe_ja="GREEN", Farbe_nein="RED", Für_print=True):
        """eine Funktion die Wörter korrigiert.
        param:  = Das Wort dass korrigiert soll.
        param: return_bei_ja = falls es das Wort gibt, wird return_bei_ja returniert.
        param: return_bei_nein = das gleiche wie bei return_bei_ja, einfach wenn das Wort falsch ist.
        param: Farbe_ja und Farbe_nein = Farben die returniert werden.* 
        param: Für_print = das die Funktion weiss dass sie in print() benutzt wird.
        * Funktioniert nur, wenn Für_print True ist.
        """

       Farbe_ja = getattr(Fore, Farbe_ja.upper(), Fore.RESET)
       Farbe_nein = getattr(Fore, Farbe_nein.upper(), Fore.RESET)
       Wort_korigiert = Wort.capitalize()
       if Wort in self.woerter_liste or Wort_korrigiert in self.woerter_liste:
            if Für_print:
                return Fore.Farbe_ja + return_bei_ja + Style.RESET_ALL
            else:
                return return_bei_ja
        else:
            if Für_print:
                return Fore.Farbe_nein + return_bei_nein + Style.RESET_ALL
            else:
                return return_bei_nein 