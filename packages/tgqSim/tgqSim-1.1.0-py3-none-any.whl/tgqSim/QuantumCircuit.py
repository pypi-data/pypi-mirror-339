#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
@author: Yuchen He
@contact: heyuchen@tgqs.net
@version: 1.0.1
@file: QuantumCircuit.py
@time: 2024/1/16 17:16

@Modifider: Zhiqiang Wang
@contact: wangzhiqiang@tgqs.net
@version: 0.1.1
@file: QuantumCircuit.py
@time: 2024/04/19 15:36
"""
from .tgqSim.CpuGate import SingleGate, DoubleGate, TripleGate
from .tgqSim.utils import dev_tools
from typing import Union
import random, os, ctypes
import numpy as np
import tgqSim.draw_circuit_tools as tools
import matplotlib.pyplot as plt
import GPUtil, datetime
# from numba import njit, prange

class Float2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_float),
                ("y", ctypes.c_float)]

class Double2(ctypes.Structure):
    _fields_ = [("x", ctypes.c_double),
                ("y", ctypes.c_double)]

class GateInfo(ctypes.Structure):
    _fields_ = [
        ("gateName", ctypes.c_char_p),
        ("actionPos", ctypes.POINTER(ctypes.c_int)),
        ("theta", ctypes.c_double)
    ]


class Qubit:
    def __init__(self, name=None, idx=None, pos=None):
        self.label = 'p' if not name else name
        self.name = f'p_{idx+100}' if not name else f"{name}_{idx}"
        self.pos = pos + idx
        self.idx = idx

    # def __getattr__(self, item):
    #     if item == self.name:
    #         return self.idx
    #     if item == self.label+"["+str(self.pos)+"]":
    #         return self.idx

    def __str__(self):
        return str(self.name)


class SimulationError(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class QuantumCircuit:
    def __init__(self, qbit_number=0):
        self.qbit_list = []
        self.cbit_list = []
        self.gate_list = []
        self.qbit_register = {}
        self.base_single_gate = ['h', 'x', 'y', 'z', 'rx', 'ry', 'rz', 'u3', 's', 'sdg', 't', 'tdg', "damp_I", "pd", "ad"]
        self.base_double_gate = ['cx', 'swap', 'iswap', 'cz', 'cp', 'rxx', 'ryy', 'rzz', 'syc']
        self.base_triple_gate = ['ccx', 'cswap']
        self.noise_mapper = {"bit_flip": "BF", "asymmetric_depolarization": "ADP", "depolarize": "DP", "phase_flip": "PF", "phase_damp": "PD", "amplitude_damp": "AD"}
        self.width = qbit_number
        self.state = []
        self.circuit_diag = []
        self.isgpu = False
        self.deviceid = []
        self.noise_circuit = []
        self.current_gate_info = ()
        self.prob_result = {}

    def add_qubits(self, number: int, name: str = 'p'):
        """
        添加量子比特
        :param number: 比特数量
        :param name: 比特名称
        :return:
        """
        self.width += number
        if name not in self.qbit_register:
            self.qbit_register.update({name: number})
            sub_list = [Qubit(name=name, idx=i, pos=i+self.width) for i in range(number)]
        else:
            former_number = self.qbit_register[name]
            self.qbit_register.update({name: number+former_number})
            sub_list = [Qubit(name=name, idx=i+former_number, pos=i+self.width) for i in range(number)]
        self.qbit_list.append(sub_list)

    def add_single_gate(self, gate_pos: Union[int, str], *gate_info):
        """
        添加单比特门序列
        :param gate_pos:
        :param gate_info: 门类型，门参数
        :return:
        """
        tmp_pos = gate_pos
        if isinstance(gate_pos, list):
            tmp_pos = gate_pos[0]
        if tmp_pos < 0 or tmp_pos >= self.width:
            raise ValueError("添加的位置不能为负数或不能超过线路设置的比特数")
        if len(gate_info) >= 1:
            if gate_info[0] not in self.base_single_gate:
                raise ValueError("添加的门名称在框架支持中，请检查添加门的名称")
        if isinstance(gate_pos, int):
            gatename = gate_info[0].upper()
            self.circuit_diag.append([(gatename, gate_pos)])
        else:
            self.circuit_diag.append([(gatename, int(gate_pos))])

        self.current_gate_info = (gate_pos, gate_info)
        self.noise_circuit.append((gate_pos, gate_info))
        self.gate_list.append((gate_pos, gate_info))
        # print("over")
        return self
        # todo 通过比特名称访问
        # if isinstance(gate_pos, str):
        #     return self.gate_list.append((gate_pos, gate_type))

    def add_double_gate(self, gate_pos_0:int, gate_pos_1:int, *gate_info):
        """
        添加两比特门序列
        :param gate_pos_0: 控制位
        :param gate_pos_1: 目标位
        :param gate_info: 门类型，门参数
        :return:
        """
        min_pos, max_pos = min([gate_pos_0, gate_pos_1]), max([gate_pos_0, gate_pos_1])
        if min_pos < 0 or max_pos >= self.width:
            raise ValueError("添加的位置不能为负数或不能超过线路设置的比特数")
        if len(gate_info) >= 1:
            if gate_info[0] not in self.base_double_gate:
                raise ValueError("添加的门名称在框架支持中，请检查添加门的名称")
        if gate_info[0] in ["rxx", 'ryy', 'rzz', 'iswap', 'syc']:
            self.circuit_diag.append([(gate_info[0].upper(), (gate_pos_1, gate_pos_0))])
        else:
            self.circuit_diag.append([(gate_info[0].upper(), gate_pos_1, gate_pos_0)])
        self.current_gate_info = ([gate_pos_0, gate_pos_1], gate_info)
        self.noise_circuit.append(([gate_pos_0, gate_pos_1], gate_info))
        self.gate_list.append(([gate_pos_0, gate_pos_1], gate_info))
        return self

    def add_triple_gate(self, gate_pos:list, *gate_info):
        """
        添加三比特门序列
        :param gate_pos:
        :param gate_info:
        :return:
        """
        min_pos, max_pos = min(gate_pos), max(gate_pos)
        if min_pos < 0 or max_pos >= self.width:
            raise ValueError("添加的位置不能为负数或不能超过线路设置的比特数")
        if len(gate_info) >= 1:
            if gate_info[0] not in self.base_triple_gate:
                raise ValueError("添加的门名称在框架支持中，请检查添加门的名称")
        self.circuit_diag.append([(gate_info[0].upper(), gate_pos[2], gate_pos[0], gate_pos[1])])
        self.current_gate_info = (gate_pos, gate_info)
        self.noise_circuit.append((gate_pos, gate_info))
        self.gate_list.append((gate_pos, gate_info))
        return self
    
    def setdevice(self, deviceList: Union[int, list]):
        gpus = GPUtil.getGPUs()
        gpuidList = [gpu.id for gpu in gpus]
        if isinstance(deviceList, int):
            deviceList = [deviceList]
        for deviceid in deviceList:
            if deviceid not in gpuidList:
                raise ValueError("设置设备ID不存在")
        self.isgpu = True
        self.deviceid = deviceList

    @staticmethod
    def get_cuda_lib():
        cuda_version = dev_tools.get_cuda_version().replace(".", "-")
        lib_name = f"cuda_{cuda_version}_tgq_simulator.so"
        current_file_path = os.path.abspath(__file__)
        current_directory = os.path.dirname(current_file_path)
        dll_path = os.path.abspath(current_directory + '/lib/' + lib_name)
        lib = ctypes.CDLL(dll_path)
        return lib

    def _run_with_device(self):
        lib = QuantumCircuit.get_cuda_lib()
        lib.execute_circuit.argtypes = [
            ctypes.POINTER(ctypes.POINTER(Double2)),
            ctypes.POINTER(GateInfo),
            ctypes.c_int,
            ctypes.c_int,
            ctypes.POINTER(ctypes.c_int)
        ]
        lib.execute_circuit.restype = None
        gateInfo = []
        for (gate_pos, gate_info) in self.gate_list:
            if isinstance(gate_pos, int):
                length = 2
                gate_pos = [gate_pos]
            elif isinstance(gate_pos, list):
                length = len(gate_pos) + 1
            else:
                raise TypeError("Type of gate_pos must be int or list")
            gate_obj = GateInfo()
            actionPos = gate_pos + [-1]
            gate_obj.actionPos = (ctypes.c_int * length)(*actionPos)
            if len(gate_info) > 0:
                gate_obj.gateName = gate_info[0].encode(encoding='utf-8')
            if len(gate_info) > 1:
                gate_obj.theta = gate_info[1]
            gateInfo.append(gate_obj)
        gateInfoCData = (GateInfo * len(gateInfo))(*gateInfo)
        deviceIdCData = (ctypes.c_int * len(self.deviceid))(*self.deviceid)
        # 申请内存首地址，不在Python端申请内存
        # 在C语言中申请统一内存，减少多次拷贝动作
        self.state = ctypes.POINTER(Double2)()
        lib.execute_circuit(ctypes.byref(self.state), gateInfoCData, len(gateInfo), self.width, deviceIdCData)
        # iStart = datetime.datetime.now()
        # print(f"start time is {iStart}")
        self.state = np.ctypeslib.as_array(self.state, shape=(2**self.width,))
        self.state = self.state.view(np.complex128)
        # print(f"total time of changing type is {(datetime.datetime.now() - iStart).total_seconds()} secs")
        
    # todo:
    def apply_state_space(self):
        self.state = ctypes.POINTER(Double2)()
        return self.state

    def free_state(self):
        if self.isgpu:
            lib = QuantumCircuit.get_cuda_lib()
            lib.freeAllMem.argtypes = [
                np.ctypeslib.ndpointer(dtype=np.complex128)
            ]
            lib.freeAllMem.restype = None
            lib.freeAllMem(self.state)

    def run_with_noise(self, shots:int=1000):
        noise_type = ["bit_flip", "asymmetric_depolarization", "depolarize", "phase_flip", "phase_damp", "amplitude_damp"]
        result_dict = {}
        tmp_circuit = self.gate_list
        for _ in range(shots):
            new_circuit = []
            for (gate_pos, gate_info) in self.noise_circuit:
                if gate_info[0] in noise_type:
                    noise_gate = QuantumCircuit.parse_noise(noise_type=gate_info[0], gate_pos=gate_pos, error_rate=gate_info[1])
                    # print(noise_gate)
                    if noise_gate is not None:
                        new_circuit.append(noise_gate)
                else:
                    new_circuit.append((gate_pos, gate_info))
            # print("new_circuit:", new_circuit)
            self.gate_list = new_circuit
            result = self.measure(measure_bits_list=[i for i in range(self.width)], shots=1000)

            # print(self.state)
            for key in result.keys():
                if key in result_dict:
                    result_dict[key] += result[key]
                else:
                    result_dict[key] = result[key]
        self.gate_list = tmp_circuit
        self.prob_result = dev_tools.get_normalization(frequency=result_dict)

    def run_statevector(self):
        """
        根据线路的门序列计算末态的量子态
        :return:
        """            
        if not self.isgpu:
            self.state = [1 if a == 0 else 0 for a in range(2**self.width)]
            for (gate_pos, gate_info) in self.gate_list:
                gate_type = gate_info[0]
                angle = tuple(gate_info[1:])
                if gate_type in self.base_single_gate:
                    self.state = SingleGate.ActOn_State(self.state, self.width, gate_type, gate_pos, *angle)

                elif gate_type in self.base_double_gate:
                    set_gate_pos = set(gate_pos)
                    if len(set_gate_pos) != len(gate_pos):
                        raise SimulationError(f"Gate position cannot be the same: {gate_pos[0]}, {gate_pos[1]}")
                    self.state = DoubleGate.ActOn_State(self.state, self.width, gate_type, gate_pos, *angle)
                elif gate_type in self.base_triple_gate:
                    set_gate_pos = set(gate_pos)
                    if len(set_gate_pos) != len(gate_pos):
                        raise SimulationError(f"Gate position cannot be the same: "
                                            f"{gate_pos[0]}, {gate_pos[1]} and {gate_pos[2]}")
                    self.state = TripleGate.ActOn_State(self.state, self.width, gate_type, gate_pos, *angle)
                else:
                    raise SimulationError(f"Unkown gate type: {gate_type}")
        else:
            self._run_with_device()
        
    def with_noise(self, noise_type:str, error_rate:Union[float, list]):
        """
        将当前的所有控制门都加上noise_type类型的噪声

        Args:
            noise_type (str): 噪声类型
            error_rate (Union[float, list]): 错误率
        """
        # self.noise_circuit += [self.current_gate_info]
        gate_pos = self.current_gate_info[0]
        if isinstance(gate_pos, int):
            self.noise_circuit += [(gate_pos, (noise_type, error_rate))]
            self.circuit_diag.append([(self.noise_mapper[noise_type], gate_pos)])
        else:
            for gate in gate_pos:
                self.noise_circuit += [(gate, (noise_type, error_rate))]
                self.circuit_diag.append([(self.noise_mapper[noise_type], gate)])
    
    @staticmethod
    def parse_noise(noise_type: str,  gate_pos: int, error_rate: Union[float, list]):
        """
        对于不同的噪声类型，返回不同的信息

        Args:
            noise_type (str): 噪声类型
            error_rate Union[float, list]: 门错误率信息
        """
        gate_name = "I"
        if "bit_flip" == noise_type:
            gate_name = QuantumCircuit.bit_flip(error_rate)
        elif "asymmetric_depolarization" == noise_type:
            gate_name = QuantumCircuit.asymmetric_depolarization(error_rate)
        elif "depolarize" == noise_type:
            gate_name = QuantumCircuit.depolarize(error_rate)
        elif "phase_flip" == noise_type:
            gate_name = QuantumCircuit.phase_flip(error_rate)
        elif "phase_damp" == noise_type:
            gate_name = QuantumCircuit.phase_damp(error_rate)
        elif "amplitude_damp" == noise_type:
            gate_name = QuantumCircuit.amplitude_damp(error_rate)
        else:
            raise ValueError("Please check noise model name")
        if gate_name == "I":
            return None
        return (gate_pos, (gate_name,))
    
    @staticmethod
    def bit_flip(error_rate: float):
        random_value = random.uniform(0, 1)
        gate_name = "I"
        if random_value < error_rate:
            gate_name = "x"
        return gate_name
    
    @staticmethod
    def asymmetric_depolarization(error_rate: Union[list, tuple]):
        if len(error_rate) != 3:
            raise ValueError("Length of error must be 3")
        gate_name = "I"
        thredhold = sum(error_rate)
        random_value = random.uniform(0, 1)
        if random_value < thredhold:
            if random_value < error_rate[0]:
                gate_name = "x"
            elif random_value < sum(error_rate[:2]):
                gate_name = "y"
            else:
                gate_name = "z"
        return gate_name
    
    @staticmethod
    def depolarize(error_rate: float):
        pxyz = [error_rate / 3] * 3
        return QuantumCircuit.asymmetric_depolarization(error_rate=pxyz)

    @staticmethod
    def phase_flip(error_rate: float):
        random_value = random.uniform(0, 1)
        gate_name = "I"
        if random_value < error_rate:
            gate_name = "z"
        return gate_name

    @staticmethod
    def phase_damp(error_rate: float):
        random_value = random.uniform(0, 1)
        gate_name = "damp_I"
        if random_value < error_rate:
            gate_name = "pd"
        return gate_name

    @staticmethod
    def amplitude_damp(error_rate: float):
        random_value = random.uniform(0, 1)
        gate_name = "damp_I"
        if random_value < error_rate:
            gate_name = "ad"
        return gate_name
    
    def random_circuit(self, num_qubits, num_gates: Union[int, list]):
        """
        生成随机线路
        :param num_qubits:
        :param num_gates: 门数量，列表表示单比特，多比特门数量
        :return:
        """
        self.width = num_qubits
        if isinstance(num_gates, int):
            base_gate_list = self.base_single_gate + self.base_double_gate + self.base_triple_gate
            for _ in range(num_gates):
                gate_type = np.random.choice(base_gate_list)
                angle = np.random.uniform(-2*np.pi, 2*np.pi, size=3)
                if gate_type in self.base_single_gate:
                    gate_pos = np.random.choice(np.array(range(num_qubits)), size=1)[0]
                elif gate_type in self.base_double_gate:
                    gate_pos = random.sample(range(num_qubits), 2)
                    gate_pos = list(gate_pos)
                elif gate_type in self.base_triple_gate:
                    gate_pos = random.sample(range(num_qubits), 3)
                    gate_pos = list(gate_pos)
                else:
                    gate_pos = None
                self.gate_list.append([gate_pos, tuple([gate_type]) + tuple(angle)])
        elif isinstance(num_gates, list):
            single_gate_num = num_gates[0]
            multiple_gate_num = num_gates[1]
            for _ in range(single_gate_num):
                gate_type = np.random.choice(self.base_single_gate)
                angle = np.random.uniform(-2*np.pi, 2*np.pi, size=3)
                gate_pos = np.random.choice(np.array(range(num_qubits)), size=1)[0]
                self.gate_list.append([gate_pos, tuple([gate_type]) + tuple(angle)])
            for _ in range(multiple_gate_num):
                base_gate_list = self.base_double_gate+self.base_triple_gate
                gate_type = np.random.choice(base_gate_list)
                angle = np.random.uniform(-2 * np.pi, 2 * np.pi, size=3)
                if gate_type in self.base_double_gate:
                    gate_pos = random.sample(range(num_qubits), 2)
                    gate_pos = list(gate_pos)
                elif gate_type in self.base_triple_gate:
                    gate_pos = random.sample(range(num_qubits), 3)
                    gate_pos = list(gate_pos)
                else:
                    gate_pos = None
                self.gate_list.append([gate_pos, tuple([gate_type]) + tuple(angle)])
                random.shuffle(self.gate_list)

    def h(self, qbit: Union[int, str]):
        return self.add_single_gate(qbit, 'h')

    def x(self, qbit):
        return self.add_single_gate(qbit, 'x')

    def y(self, qbit):
        return self.add_single_gate(qbit, 'y')

    def z(self, qbit):
        return self.add_single_gate(qbit, 'z')

    def rx(self, qbit, theta):
        return self.add_single_gate(qbit, 'rx', theta)

    def ry(self, qbit, theta):
        return self.add_single_gate(qbit, 'ry', theta)

    def rz(self, qbit: Union[int, str], theta):
        return self.add_single_gate(qbit, 'rz', theta)

    def u3(self, qbit, *theta):
        return self.add_single_gate(qbit, 'u3', *theta)
    
    def s(self, qbit:Union[int, str]):
        return self.add_single_gate(qbit, 's')
    
    def sdg(self, qbit:Union[int, str]):
        return self.add_single_gate(qbit, 'sdg')
    
    def t(self, qbit:Union[int, str]):
        return self.add_single_gate(qbit, 't')
    
    def tdg(self, qbit:Union[int, str]):
        return self.add_single_gate(qbit, 'tdg')

    def cx(self, control_qubit, target_qubit):
        return self.add_double_gate(control_qubit, target_qubit, 'cx')

    def swap(self, qubit_1, qubit_2):
        return self.add_double_gate(qubit_1, qubit_2, 'swap')

    def iswap(self, qubit_1, qubit_2):
        return self.add_double_gate(qubit_1, qubit_2, 'iswap')

    def cz(self, control_qubit, target_qubit):
        return self.add_double_gate(control_qubit, target_qubit, 'cz')

    def cp(self, control_qubit, target_qubit, theta):
        return self.add_double_gate(control_qubit, target_qubit, 'cp', theta)

    def rxx(self, qubit_1, qubit_2, theta):
        return self.add_double_gate(qubit_1, qubit_2, 'rxx', theta)

    def ryy(self, qubit_1, qubit_2, theta):
        return self.add_double_gate(qubit_1, qubit_2, 'ryy', theta)

    def rzz(self, qubit_1, qubit_2, theta):
        return self.add_double_gate(qubit_1, qubit_2, 'rzz', theta)

    def ccx(self, control_qubits: list, target_qubits: int):
        return self.add_triple_gate(control_qubits+[target_qubits], 'ccx')
    
    def show_quantum_circuit(self, plot_labels=True, **kwargs):
        """Use Matplotlib to plot a quantum circuit.
        kwargs    Can override plot_parameters
        """
        labels = []
        inits = {}
        for i in range(self.width):
            labels.append(f"q_{i}")
            inits[f"q_{i}"] = i
        plot_params = dict(scale = 1.0, fontsize = 14.5, linewidth = 2.0, 
                            control_radius = 0.05, not_radius = 0.15, 
                            swap_delta = 0.08, label_buffer = 0.8, 
                            rectangle_delta = 0.3, box_pad=0.2)
        plot_params.update(kwargs)
        scale = plot_params['scale']
        
        # Create labels from gates. This will become slow if there are a lot 
        #  of gates, in which case move to an ordered dictionary
        if not labels:
            labels = []
            for i,gate in tools.enumerate_gates(self.circuit_diag, schedule=True):
                for label in gate[1:]:
                    if label not in labels:
                        labels.append(label)
        
        nq = len(labels)
        nt = len(self.circuit_diag)
        wire_grid = np.arange(0.0, nq*scale, scale, dtype=float)
        gate_grid = np.arange(0.0, nt*scale, scale, dtype=float)
        gate_grid_index = [0.0 for _ in range(nq)]
        # print(gate_grid_index)
        
        fig,ax = tools.setup_figure(nq,nt,gate_grid,wire_grid,plot_params)

        measured = tools.measured_wires(self.circuit_diag, labels, schedule=True)
        tools.draw_wires(ax, nq, gate_grid, wire_grid, plot_params, 'k', measured)
        
        if plot_labels: 
            tools.draw_labels(ax, labels, inits, gate_grid, wire_grid, plot_params, 'k')

        tools.draw_gates(ax, self.circuit_diag, labels, gate_grid_index, wire_grid, plot_params, measured, schedule=True)
        plt.show()
        # return ax
    
    def measure(self, measure_bits_list: Union[list, int]=None, shots: int=1000)->dict:
        """
        测量们
        Args:
            measure_bits_list: 测量比特列表，传入比特位置或列表位置
            shots: 测量次数
        Returns:
            返回测量结果
        """
        # 首先通过执行操作得到所有的状态
        # print(self.gate_list)
        self.run_statevector()
        print(self.state)
        state = np.array(self.state)
        prob = np.real(state.conjugate() * state)
        count = {format(i, f'0{self.width}b'): prob[i] for i in range(len(prob))}
        print('old count {}'.format(count))
        distribution = {}

        if isinstance(measure_bits_list, int):
            measure_bits_list = [measure_bits_list]
        if measure_bits_list is None: # 若为空默认测量所有可能
            print('empty measure list')
            # distribution = count
            measure_bits_list = sorted([_ for _ in range(self.width)], reverse=True)
        
        print('old measure bit {}'.format(measure_bits_list))
        # 计算测量分布
        for p in count.keys():
            # key = ''.join(p[pos - 1] for pos in measure_bits_list)
            key = ''.join(p[pos] for pos in measure_bits_list)
            if count[p] == 0:
                continue
            if key not in distribution:
                distribution[key] = count[p]
            else:
                distribution[key] += count[p]
        print('old distribution {}'.format(distribution))
        # 根据分布抽样概率
        result = {}
        cumulate = 0
        sample = np.random.uniform(0,1, size=shots)
        for key in distribution.keys():
            new_cumulate = cumulate + distribution[key]
            result[key] = sum((cumulate<=sample) & (sample<new_cumulate))
            cumulate = new_cumulate
        return result



# 下面这段代码仅限测试使用，不会参与实际工程
if __name__ == '__main__':
    nQubits = 4
    qc = QuantumCircuit()
    qc.add_qubits(nQubits, name='qft')
    # for i in range(nQubits):
    #     if nQubits - 2 == i:
    #         qc.x(i)
    #     else:
    #         qc.h(i)
    # for i in range(nQubits - 1, -1, -1):
    #     for j in range(i, -1, -1):
    #         if j == i:
    #             qc.h(j)
    #         else:
    #             qc.cp(control_qubit=j, target_qubit=i, theta=np.pi / (2 ** (i - j)))
    qc.h(0)
    # qc.x(1)
    # qc.h(3)
    print(qc.gate_list)
    # for i in range(0, nQubits // 2):
    #     qc.swap(qubit_1=i, qubit_2=nQubits - 1 - i)
    # qc.run_statevector()
    # print(qc.state)
    # print(len(qc.state))
    # measure_pos = sorted([1, 0,2,3], reverse=True)
    # print(measure_pos)
    print(qc.measure())
    # print(qc.measure(measure_bits_list=measure_pos))
    # qc.show_quantum_circuit()    


