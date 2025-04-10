import torch.nn as nn
import torch

from nnodely.basic.relation import Stream, NeuObj, ToStream
from nnodely.support.utils import merge, enforce_types, get_inputs, check
from nnodely.basic.model import Model
from nnodely.support.fixstepsolver import Euler, Trapezoidal

SOLVERS = {
    'euler': Euler,
    'trapezoidal': Trapezoidal
}

# Binary operators
int_relation_name = 'Integrate'
der_relation_name = 'Derivate'

class Integrate(Stream, ToStream):
    """
    This operation Integrate a Stream

    Parameters
    ----------
    method : is the integration method
    """
    @enforce_types
    def __init__(self, output:Stream, *, method:str = 'euler') -> Stream:
        from nnodely.layers.input import State, ClosedLoop
        s = State(output.name + "_int" + str(NeuObj.count), dimensions=output.dim['dim'])
        check(method in SOLVERS, ValueError, f"The method '{method}' is not supported yet")
        solver = SOLVERS[method]()
        new_s = s.last() + solver.integrate(output)
        out = ClosedLoop(new_s, s)
        super().__init__(new_s.name, out.json, new_s.dim)

class Derivate(Stream, ToStream):
    """
    This operation Derivate a Stream with respect to time or another Stream

    Parameters
    ----------
    method : is the derivative method
    """
    @enforce_types
    def __init__(self, output:Stream, input:Stream = None, *, method:str = 'euler') -> Stream:
        if input is None:
            check(method in SOLVERS, ValueError, f"The method '{method}' is not supported yet")
            solver = SOLVERS[method]()
            output_dt = solver.derivate(output)
            super().__init__(output_dt.name, output_dt.json, output_dt.dim)
        else:
            super().__init__(der_relation_name + str(Stream.count), merge(output.json,input.json), input.dim)
            self.json['Relations'][self.name] = [der_relation_name, [output.name, input.name]]
            grad_inputs = []
            get_inputs(self.json, input.name, grad_inputs)
            for i in grad_inputs:
                if i in self.json['Inputs']:
                    self.json['Inputs'][i]['type'] = 'derivate'
                elif i in self.json['States']:
                    self.json['States'][i]['type'] = 'derivate'


class Derivate_Layer(nn.Module):
    #: :noindex:
    def __init__(self):
        super(Derivate_Layer, self).__init__()

    def forward(self, *inputs):
        return torch.autograd.grad(inputs[0], inputs[1], grad_outputs=torch.ones_like(inputs[0]), create_graph=True, retain_graph=True, allow_unused=False)[0]

def createAdd(name, *inputs):
    #: :noindex:
    return Derivate_Layer()

setattr(Model, der_relation_name, createAdd)
