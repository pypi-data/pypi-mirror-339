class SortingVisualizer:
    """Klasse zur Visualisierung verschiedener Sortieralgorithmen"""
    
    def __init__(self, arr=None):
        """Initialisiert die Klasse mit einem optionalen Array"""
        self.original = arr.copy() if arr else []
        self.array = arr.copy() if arr else []
        self.steps = []
        
    def reset(self):
        """Setzt das Array auf seinen ursprünglichen Zustand zurück"""
        self.array = self.original.copy()
        self.steps = []
        return self.array
        
    def _record_step(self):
        """Speichert den aktuellen Zustand des Arrays als Schritt"""
        self.steps.append(self.array.copy())
        
    def get_steps(self):
        """Gibt alle aufgezeichneten Schritte zurück"""
        return self.steps
    
    def bubble_sort(self, array=None):
        """Implementiert Bubble Sort"""
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()
        
        self._record_step()  # Anfangszustand
        n = len(self.array)
        
        for i in range(n):
            for j in range(0, n-i-1):
                if self.array[j] > self.array[j+1]:
                    self.array[j], self.array[j+1] = self.array[j+1], self.array[j]
                    self._record_step()
                    
        return self.array, self.steps
    
    def selection_sort(self, array=None):
        """Implementiert Selection Sort"""
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()
        
        self._record_step()  # Anfangszustand
        n = len(self.array)
        
        for i in range(n):
            min_idx = i
            for j in range(i+1, n):
                if self.array[j] < self.array[min_idx]:
                    min_idx = j
                    
            if min_idx != i:
                self.array[i], self.array[min_idx] = self.array[min_idx], self.array[i]
                self._record_step()
                
        return self.array, self.steps
    
    def insertion_sort(self, array=None):
        """Implementiert Insertion Sort"""
        if array:
            self.array = array.copy()
            self.original = array.copy()
        self.reset()
        
        self._record_step()  # Anfangszustand
        n = len(self.array)
        
        for i in range(1, n):
            key = self.array[i]
            j = i-1
            while j >= 0 and key < self.array[j]:
                self.array[j+1] = self.array[j]
                j -= 1
            self.array[j+1] = key
            self._record_step()
            
        return self.array, self.steps
