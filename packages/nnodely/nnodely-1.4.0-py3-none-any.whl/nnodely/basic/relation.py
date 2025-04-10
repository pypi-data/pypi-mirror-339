import copy

import numpy as np

from nnodely.support.utils import check, merge, enforce_types, ForbiddenTags

from nnodely.support.logger import logging, nnLogger
log = nnLogger(__name__, logging.CRITICAL)

MAIN_JSON = {
                'Info' : {},
                'Inputs' : {},
                'States' : {},
                'Constants': {},
                'Parameters' : {},
                'Functions' : {},
                'Relations': {},
                'Outputs': {}
            }

CHECK_NAMES = True

def toStream(obj):
    from nnodely.layers.parameter import Parameter, Constant
    if type(obj) in (int,float,list,np.ndarray):
        obj = Constant('Constant'+str(NeuObj.count), obj)
        #obj = Stream(obj, MAIN_JSON, {'dim': 1}) if type(obj) in (int, float) else obj
    if type(obj) is Parameter or type(obj) is Constant:
        obj = Stream(obj.name, obj.json, obj.dim)
    return obj


class NeuObj():
    count = 0
    names = []
    @classmethod
    @enforce_types
    def clearNames(self, names:str|list|None=None):
        if names is None:
            NeuObj.count = 0
            NeuObj.names = []
        else:
            if type(names) is list:
                for name in names:
                    if name in NeuObj.names:
                        NeuObj.names.remove(name)
            else:
                if names in NeuObj.names:
                    NeuObj.names.remove(names)

    def __init__(self, name='', json={}, dim=0):
        NeuObj.count += 1
        if name == '':
            name = 'Auto'+str(NeuObj.count)
        if CHECK_NAMES == True:
            check(name not in NeuObj.names, NameError, f"The name '{name}' is already used change the name of NeuObj.")
            check(name not in ForbiddenTags, NameError, f"The name '{name}' is a forbidden tag.")
            NeuObj.names.append(name)
        self.name = name
        self.dim = dim
        if json:
            self.json = copy.deepcopy(json)
        else:
            self.json = copy.deepcopy(MAIN_JSON)

class Relation():
    def __add__(self, obj):
        from nnodely.layers.arithmetic import Add
        return Add(self, obj)

    def __radd__(self, obj):
        from nnodely.layers.arithmetic import Add
        return Add(obj, self)

    def __sub__(self, obj):
        from nnodely.layers.arithmetic import Sub
        return Sub(self, obj)

    def __rsub__(self, obj):
        from nnodely.layers.arithmetic import Sub
        return Sub(obj, self)

    def __truediv__(self, obj):
        from nnodely.layers.arithmetic import Div
        return Div(self, obj)

    def __rtruediv__(self, obj):
        from nnodely.layers.arithmetic import Div
        return Div(obj, self)

    def __mul__(self, obj):
        from nnodely.layers.arithmetic import Mul
        return Mul(self, obj)

    def __rmul__(self, obj):
        from nnodely.layers.arithmetic import Mul
        return Mul(obj, self)

    def __pow__(self, obj):
        from nnodely.layers.arithmetic import Pow
        return Pow(self, obj)

    def __rpow__(self, obj):
        from nnodely.layers.arithmetic import Pow
        return Pow(obj, self)

    def __neg__(self):
        from nnodely.layers.arithmetic import Neg
        return Neg(self)

class Stream(Relation):
    """
    Represents a stream of data inside the neural network. A Stream is automatically create when you operate over a Input, State, Parameter, or Constant object.
    """
    count = 0
    @classmethod
    def resetCount(self):
        Stream.count = 0

    def __init__(self, name, json, dim, count = 1):
        Stream.count += count
        check(name not in ForbiddenTags, NameError, f"The name '{name}' is a forbidden tag.")
        self.name = name
        self.json = copy.deepcopy(json)
        self.dim = dim

    def __str__(self):
        from nnodely.visualizer.visualizer import color, GREEN
        from pprint import pformat
        stream = f" Stream "
        stream_name = f" {self.name} {self.dim} "

        title = color((stream).center(80, '='), GREEN, True)
        json = color(pformat(self.json), GREEN)
        stream = color((stream_name).center(80, '-'), GREEN, True)
        return title + '\n' + json + '\n' + stream

    def __repr__(self):
        return self.__str__()

    @enforce_types
    def tw(self, tw:float|int|list, offset:float|int|None = None) -> "Stream":
        """
        Selects a time window on Stream. It is possible to create a smaller or bigger time window on the stream.
        The Time Window must be in the past not in the future.

        Parameters
        ----------
        tw : float, int, list
            The time window represents the time in the past. If a list, it should contain the start and end times, both indexes must be in the past.
        offset : float, int, optional
            The offset for the sample window. Default is None.

        Returns
        -------
        Stream
            A Stream representing the TimePart object with the selected time window.

        """
        from nnodely.layers.input import State, Connect
        if type(tw) is list:
            check(0 >= tw[1] > tw[0] and tw[0] < 0, ValueError, "The dimension of the sample window must be in the past.")
        s = State(self.name+"_tw"+str(NeuObj.count),dimensions=self.dim['dim'])
        out_connect = Connect(self, s)
        win_state = s.tw(tw, offset)
        return Stream(win_state.name, merge(win_state.json, out_connect.json), win_state.dim,0 )

    @enforce_types
    def sw(self, sw:int|list, offset:int|None = None) -> "Stream":
        """
        Selects a sample window on Stream. It is possible to create a smaller or bigger window on the stream.
        The Sample Window must be in the past not in the future.

        Parameters
        ----------
        sw : int, list
            The sample window represents the number of steps in the past. If a list, it should contain the start and end indices, both indexes must be in the past.
        offset : int, optional
            The offset for the sample window. Default is None.

        Returns
        -------
        Stream
            A Stream representing the SamplePart object with the selected samples.

        """
        from nnodely.layers.input import State, Connect
        if type(sw) is list:
            check(0 >= sw[1] > sw[0] and sw[0] < 0, ValueError, "The dimension of the sample window must be in the past.")
        s = State(self.name+"_sw"+str(NeuObj.count),dimensions=self.dim['dim'])
        out_connect = Connect(self, s)
        win_state = s.sw(sw, offset)
        return Stream(win_state.name, merge(win_state.json, out_connect.json), win_state.dim,0 )

    @enforce_types
    def z(self, delay:int|float) -> "Stream":
        """
        Considering the Zeta transform notation. The function is used to delay a Stream.
        The value of the delay can be only positive.

        Parameters
        ----------
        delay : int
            The delay value.

        Returns
        -------
        Stream
            A Stream representing the delayed Stream
        """
        check(delay > 0, ValueError, "The delay must be a positive integer")
        check('sw' in self.dim, TypeError, "The stream is not defined in samples but in time")
        return self.sw([-self.dim['sw']-delay,-delay])

    @enforce_types
    def delay(self, delay:int|float) -> "Stream":
        """
        The function is used to delay a Stream.
        The value of the delay can be only positive.

        Parameters
        ----------
        delay : int, float
            The delay value.

        Returns
        -------
        Stream
            A Stream representing the delayed Stream
        """
        check(delay > 0, ValueError, "The delay must be a positive integer")
        check('tw' in self.dim, TypeError, "The stream is not defined in time but in sample")
        return self.tw([-self.dim['tw']-delay,-delay])

    @enforce_types
    def s(self, order:int, method:str = 'euler') -> "Stream":
        """
        Considering the Laplace transform notation. The function is used to operate an integral or derivate operation on a Stream.
        The order of the integral or the derivative operation is indicated by the order parameter.

        Parameters
        ----------
        order : int
            Order of the Laplace transform
        method : str, optional
            Integration or derivation method

        Returns
        -------
        Stream
            A Stream of the signal represents the integral or derivation operation.
        """
        from nnodely.layers.timeoperation import Derivate, Integrate
        check(order != 0, ValueError, "The order must be a positive or negative integer not a zero")
        if order > 0:
            for i in range(order):
                o = Derivate(self, method = method)
        elif order < 0:
            for i in range(-order):
                o = Integrate(self, method = method)
        return o

    def connect(self, obj) -> "Stream":
        """
        Connects the current stream to a given state object.

        Parameters
        ----------
        obj : State
            The state object to connect to.

        Returns
        -------
        Stream
            A new Stream object representing the connected state.

        Raises
        ------
        TypeError
            If the provided object is not of type State.
        KeyError
            If the state variable is already connected.
        """
        from nnodely.layers.input import State
        check(type(obj) is State, TypeError,
              f"The {obj} must be a State and not a {type(obj)}.")
        self.json = merge(self.json, obj.json)
        check('closedLoop' not in self.json['States'][obj.name] or 'connect' not in self.json['States'][obj.name], KeyError,
              f"The state variable {obj.name} is already connected.")
        self.json['States'][obj.name]['connect'] = self.name
        return Stream(self.name, self.json, self.dim,0 )

    def closedLoop(self, obj) -> "Stream":
        """
        Creates a closed loop connection with a given state object.

        Parameters
        ----------
        obj : State
            The state object to create a closed loop with.

        Returns
        -------
        Stream
            A new Stream object representing the closed loop state.

        Raises
        ------
        TypeError
            If the provided object is not of type State.
        KeyError
            If the state variable is already connected.
        """
        from nnodely.layers.input import State
        check(type(obj) is State, TypeError,
              f"The {obj} must be a State and not a {type(obj)}.")
        self.json = merge(self.json, obj.json)
        check('closedLoop' not in self.json['States'][obj.name] or 'connect' not in self.json['States'][obj.name],
              KeyError,
              f"The state variable {obj.name} is already connected.")
        self.json['States'][obj.name]['closedLoop'] = self.name
        return Stream(self.name, self.json, self.dim,0 )

class ToStream():
    def __new__(cls, *args, **kwargs):
        out = super(ToStream,cls).__new__(cls)
        out.__init__(*args, **kwargs)
        return Stream(out.name,out.json,out.dim,0)

class AutoToStream():
    def __new__(cls, *args,  **kwargs):
        if len(args) > 0 and (issubclass(type(args[0]),NeuObj) or type(args[0]) is Stream):
            instance = super().__new__(cls)
            #instance.__init__(**kwargs)
            instance.__init__()
            return instance(args[0])
        instance = super().__new__(cls)
        return instance
