class Conducta():
    ''' clase que contiene las ordenes que se irán cumpliendo a cada paso 
        en los elementos con conducta programada'''
    ordenes        = []          # Listado de ordenes
    nextorden      = False       # Siguiente orden
    activa         = False       # Indica si hay ordenes pendientes.
    activa_cont    = 0
    bloqueado      = False


    def add(self, orden, conducta_programada=False, lista=False, reset=False):
        ''' añade una nueva orden al listado general o un listado de ellas '''
        self.bloqueado = False      # Si el elemento está bloqueado, lo desbloquea si inicia un nuevo comportamiento.
        self.activa = True

        if reset:
            self.ordenes = []
        if listado:
            self.ordenes.extend(self.lista)
        elif conducta_programada:
            self.ordenes.extend(self.conducta_programada(conducta_programada))
        elif orden:
            self.ordenes.append(orden)

        self.activa_cont = len(self.ordenes)


    def delete(self, pos=False, todas=False):
        ''' borra una orden o todas'''
        if pos:
            self.ordenes.pop(pos)
        elif todas:
            self.ordenes = []


    def update (self):
        ''' Actualiza la clase tras cumplir la última orden. '''

        if self.bloqueado:
            None
        else:
            if self.activa:
                self.ordenes.pop(0)
                if len(self.ordenes) > 0:
                    self.nextorden   = self.ordenes[0]
                    self.activa_cont = len(self.ordenes)
                else:
                    self.activa      = False
            else:
                return 'sin conducta planificada'


    def conducta_programada (self, conducta_programada):
        ''' actualizará self.ordenes con un listado de acciones que representa
            una acción programada. '''
        conductas_dict = {}     # {conducta_programada:listadoacciones, ...}
        return conductas_dict[conducta_programada] 



    def calc_nextaction(self, nextaction):
        ''' Gestiona el listado de ordenes 'self.nextaction'''

        # Este método se invoca desde otro módulo por algún evento. Se actualizará la
        # posición con el update tras comprobar que la nueva posicíón es pisable.

        if nextaction == 0:
            self.nextaction = False
            self.nextpos    = self.map_pos

        elif nextaction.startswith('camina'):
            orientacion = (self.orientacion[nextaction[-1]]) ####### Adaptar al cambio a 8 direcciones.
            avance=self.orientacion[nextaction[-1]]
            self.nextpos = (self.map_pos[0] + avance[0], self.map_pos[1] + avance[1])
            self.nextaction = nextaction

