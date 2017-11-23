class Move(object):
    """Attribute List
    name     : (string)  name of the move
    power    : (float)   the strength of the move. It affects how much damage will be dealt.
    type     : (string)  type of the move
    gauge    : (int)     how many gauges it needs to perform.
    """
    
    def __init__(self,name_str="Default Attack",power_float=1.0, type_str="normal", gauge_int=0):
        self.name=name_str
        if power_float>=1.0:
            self.power=power_float
        else:
            self.power=1.0
        self.type=type_str
        self.gauge=gauge_int
        
    def __str__(self):
        return self.name