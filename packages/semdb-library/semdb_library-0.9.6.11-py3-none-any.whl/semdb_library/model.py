import numpy as np
import bisect
from enum import Enum

class NeuralNet:
    def __init__(self, config: object, input_size: int):
        self._input_size = input_size
        self._second_layer = config['second_layer']
        self._third_layer = config['third_layer']

        bias_size = [ self._second_layer, self._third_layer, 1 ]

        self._bias = []
        for i in range(0, 3):
            bias_vec = np.empty([bias_size[i], 1])
            for j in range(0, bias_size[i]):
                bias_vec[j, 0] = config['bias'][i][j]
            self._bias.append(bias_vec)

        weight_size = [
            (self._second_layer, self._input_size),
            (self._third_layer, self._second_layer),
            (1, self._third_layer)
        ]

        self._weight = []
        for i in range(0, 3):
            weight = np.empty([weight_size[i][0], weight_size[i][1]])
            for x in range(0, weight_size[i][0]):
                for y in range(0, weight_size[i][1]):
                    weight[x, y] = config['weight'][i][x][y]
            self._weight.append(weight)

    def activate(self, x):
        len = x.shape[0]
        for i in range(0, len):
            # LeakyReLU activation
            if x[i, 0] < 0:
                x[i, 0] *= 0.25
    
    def run(self, input: list) -> float:
        input_layer = np.empty([self._input_size, 1])
        for i in range(0, self._input_size):
            input_layer[i, 0] = input[i]

        second_layer = np.matmul(self._weight[0], input_layer)
        second_layer += self._bias[0]
        self.activate(second_layer)

        third_layer = np.matmul(self._weight[1], second_layer)
        third_layer += self._bias[1]
        self.activate(third_layer)

        output = np.matmul(self._weight[2], third_layer)
        output += self._bias[2]

        return output[0, 0]
    
class QuadraticModel:
    def __init__(self, config: object, input_size: int):
        self._input_size = input_size
        self._dim = input_size + 1

        self._weight = np.empty([self._dim, self._dim])
        for x in range(0, self._dim):
          for y in range(0, self._dim):
            self._weight[x, y] = config["coeff"][x][y]

    def run(self, input: list) -> float:
        input_layer = []
        for i in range(0, self._input_size):
            input_layer.append(input[i])
        input_layer.append(1)

        output = 0
        for x in range(0, self._dim):
          for y in range(0, self._dim):
            output += input_layer[x] * self._weight[x, y] * input_layer[y]

        return output

class Normalizer:
    def __init__(self, config: object, input_size: int):
        self._input_size = input_size
        self._mean = []
        self._std = []
        for i in range(0, self._input_size):
            self._mean.append(config['mean'][i])
            self._std.append(config['std'][i])

    def normalize(self, input: list) -> list:
        output = []
        for i in range(0, self._input_size):
            output.append((input[i] - self._mean[i]) / self._std[i])
        return output
    
CalType = Enum('CalType', ['PLATT', 'ISOTONIC'])

class Calibrator:
    def __init__(self, config: object):
        if config['type'] == 'platt':
            self._type = CalType.PLATT
        elif config['type'] == 'isotonic':
            self._type = CalType.ISOTONIC
        else:
            raise Exception('unknown keyword: ' + config['type'])
        
        if self._type == CalType.PLATT:
            self._a = config['a']
            self._b = config['b']
        else:
            size = len(config['score'])
            self._segs = []
            for i in range(0, size):
                self._segs.append(( config['score'][i], config['prob'][i] ))

    def calibrate(self, score: float):
        if self._type == CalType.PLATT:
            pre = self._a * score + self._b

            # sigmoid
            if pre > 0:
                return 1 / (1 + np.exp(-pre))
            else:
                return np.exp(pre) / (1 + np.exp(pre))
        else:
            l = 0
            r = len(self._segs) - 1
            while l < r:
                mid = (l + r) / 2
                if self._segs[mid][0] >= score:
                    r = mid
                else:
                    l = mid + 1

            return self._segs[l][1]
        
class ClassificationModel:
    def __init__(self, config: object):
        self._input_size = config['input_dimension']
        self._output_size = len(config['induce_label'])

        self._base = []
        self._normalizer = []
        self._calibrator = []
        for i in range(0, self._output_size):
            state = config['state'][i]

            if config['base_model_type'] == 'forward_network':
                self._base.append(NeuralNet(state['base'], self._input_size))
            elif config['base_model_type'] == 'quadratic_momentum':
                self._base.append(QuadraticModel(state['base'], self._input_size))
            else:
                raise Exception('unknown keyword: ' + state['base_model_type'])
            self._normalizer.append(Normalizer(state['normalizer'], self._input_size))
            self._calibrator.append(Calibrator(state['calibrator']))

    def run(self, input: list):
        result = []
        for i in range(0, self._output_size):
            normalized = self._normalizer[i].normalize(input)
            base_output = self._base[i].run(normalized)
            calibrated = self._calibrator[i].calibrate(base_output)
            result.append(calibrated)
        return result
    
class RankingModel:
    def __init__(self, config: object):
        self._input_size = config['input_dimension']
        
        state = config['state']
        if config['base_model_type'] == 'forward_network':
            self.base_ = NeuralNet(state['base'], self._input_size)
        elif config['base_model_type'] == 'quadratic_momentum':
            self.base_ = QuadraticModel(state['base'], self._input_size)
        else:
            raise Exception('unknown keyword: ' + state['base_model_type'])
        self.normalizer_ = Normalizer(state['normalizer'], self._input_size)

        self._percentile = state['percentile']
        if config['output'] == 'value':
            self._value = state['value']
            if len(self._value) == 0:
                raise Exception('empty value list')
        else:
            self._value = None

    # evaluate percentile value
    def eval_pval(self, input: float) -> float:
        normalized = self.normalizer_.normalize(input)
        score = self.base_.run(normalized)

        if len(self._percentile) == 0:
            return 0
        if len(self._percentile) == 1:
            return 0.5

        idx = bisect.bisect_left(self._percentile, score)
        if idx < len(self._percentile):
            if idx == 0:
                return 0
            
            size = float(len(self._percentile) - 1)
            total_value_range = self._percentile[idx] - self._percentile[idx - 1]
            bucket_range = 1.0 / size
            upper_percentile = idx / size
            
            if total_value_range < 1e-3:
                return upper_percentile - bucket_range / 2
            else:
                return upper_percentile - (self._percentile[idx] - score) / total_value_range * bucket_range
        else:
            return 1

    # execute the model
    def run(self, input: list):
        pval = self.eval_pval(input)
        if self._value == None:
            return pval
        else:
            # recover value
            fid = pval * len(self._value) - 1
            
            id = int(fid)
            if id < 0:
                id = 0
            if id >= len(self._value):
                id = len(self._value) - 1

            est_val = self._value[id]
            if id < len(self._value) - 1:
                est_val += (self._value[id + 1] - self._value[id]) * (fid - id)

            return est_val
