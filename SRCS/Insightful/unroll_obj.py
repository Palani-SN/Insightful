
import json
import inspect
import importlib.util
from collections import OrderedDict
import types

# def hello_world(name):
#     return f"hello, {name}"

# class class2:

#     summa = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]


# class Sample_Class(class2):

#     actions = {
#         lambda x: isinstance(x, int): 'unroll_Int',
#         lambda x: isinstance(x, float): 'unroll_Float',
#         lambda x: isinstance(x, str): 'unroll_Str',
#         lambda x: isinstance(x, list): 'unroll_List',
#         lambda x: isinstance(x, dict): 'unroll_Dict',
#         lambda x: isinstance(x, tuple): 'unroll_Tuple',
#         lambda x: isinstance(x, set): 'unroll_Set'
#     }

#     summa_link = class2()
#     func_call_check = hello_world("sathiya")
#     func_ptr_check = hello_world
    
#     def __init__(self) -> None:
#         self.sys_ctrl = [sys.stdin, sys.stderr, sys.stdout]
#         self.unroll_Int_var = 1
#         self.unroll_Float_var = 2.7
#         self.unroll_Str_var = "None"
#         self.unroll_Dict_var = {"unroll_Dict_var": None}
#         self.unroll_List_var = [None, 9, 7, 5]
#         self.unroll_Tuple_var = (None, 2, 3, 5)
#         self.unroll_Set_var = {2, 3, 4, 4, 5, 3}

#     def unroll_Int(self, obj):
#         return obj

#     def unroll_Float(self, obj):

#         return obj

#     def unroll_Str(self, obj):
#         return obj

#     def unroll_Dict(self, obj):
#         dict = {}
#         for k, v in obj.items():
#             dict[self.unroll(k)] = self.unroll(v)
#         return dict

#     def unroll_List(self, obj):
#         list = []
#         for mem in obj:
#             list.append(self.unroll(mem))
#         return list

#     def unroll_Tuple(self, obj):
#         tuple_as_List = list(obj)
#         returned = self.unroll(tuple_as_List)
#         return tuple(returned)

#     def unroll_Set(self, obj):
#         set_as_List = list(obj)
#         returned = self.unroll(set_as_List)
#         return returned

import time
import threading
import sys

class sub_scheduler():

    def __init__(self, val) -> None:
        self.init_val = val
        self.val = val

    def is_non_zero(self):

        return self.val != 0  

    def obj(self):
        cnt = 0
        while self.is_non_zero():
            if cnt == 1:
                self.probe = True
            else:
                self.probe = False
            # print(self)
            # derived(self)
            time.sleep(3)
            cnt += 1

    # def __del__(self):
    #     self.probe = True
    #     derived(self)
    #     self.probe = False


class scheduler():

    def __init__(self, list_input) -> None:
        self.sys_ctrl = [sys.stdin, sys.stderr, sys.stdout]
        start = time.perf_counter()
        self.threads = []
        print(list_input)
        self.sample = sub_scheduler(0)
        self.list_input = [ sub_scheduler(x) for x in list_input ]
        for i in range(len(list_input)):
            t = threading.Thread(target=self.reduction, args=[i])
            t.start()
            self.threads.append(t)
            t = threading.Thread(target=self.list_input[i].obj)
            t.start()
            self.threads.append(t)
        t = threading.Thread(target=self.obj)
        t.start()
        self.threads.append(t)
        for thread in self.threads:
            thread.join()
        finish = time.perf_counter()
        print(f'Finished in {round(finish-start, 2)} seconds')

    def reduction(self, idx):
        while self.list_input[idx].val:
            print(".", end="")
            self.list_input[idx].val -= 1
            time.sleep(0.1)

    def show(self):
        while any([ x.is_non_zero() for x in self.list_input ]):
            print(" ".join([str(x) for x in self.list_input]))
            time.sleep(3)
        
    def obj(self):
        cnt = 0
        while any([ x.is_non_zero() for x in self.list_input ]):
            if cnt == 1:
                self.probe = True
            else:
                self.probe = False
            # print(self)
            # derived(self)
            time.sleep(3)
            cnt += 1

    def __del__(self):
        self.probe = True
        derived(self)
        self.probe = False


class core():

    def __init__(self, obj=None) -> None:

        if obj:
            returned = self.unroll(obj, self.actions)
            print(returned)
            print(json.dumps(returned, indent=2, sort_keys=True))

    def unroll(self, obj, actions):

        if obj:
            returned = None
            for k, v in OrderedDict(actions).items():
                if k(obj):
                    if v == 'unroll_obj':
                        print("->", obj, obj.__class__.__module__)
                        if importlib.util.find_spec(obj.__class__.__module__) == None:
                            # file = inspect.getfile(obj.__class__) 
                            # print("-->", file)
                            call_back = getattr(self, v)
                            returned = call_back(obj)
                        else:
                            returned = f"{type(obj).__name__} : can't - unroll"
                    else:                        
                        call_back = getattr(self, v)
                        returned = call_back(obj)

            # print("returned", returned)
            if returned == None:
                returned = f"{type(obj).__name__} : can't - unroll"
        else:
            returned = obj
        return returned


class crust(core):

    actions = {
        # var types
        lambda x: isinstance(x, int): 'ifint',
        lambda x: isinstance(x, float): 'iffloat',
        lambda x: isinstance(x, str): 'ifstr',
        lambda x: isinstance(x, list): 'iflist',
        lambda x: isinstance(x, dict): 'ifdict',
        lambda x: isinstance(x, tuple): 'iftuple',
        lambda x: isinstance(x, set): 'ifset',
        lambda x: isinstance(x, type(None)): 'ifnone',
        # func types
        lambda x: inspect.ismethod(x): 'ifmethod',
        lambda x: inspect.isfunction(x): 'iffunction',
        # other usage classes
        # lambda x: type(x) not in [int, float, str, list, dict, tuple, set, type(None), types.MethodType, types.FunctionType]: 'unroll_obj',
        lambda x: x.__class__.__module__ != 'builtins': 'unroll_obj',
        # lambda x : inspect.isabstract(x) : 'ifabstract',
        # lambda x : inspect.isasyncgen(x) : 'ifasyncgen',
        # lambda x : inspect.isasyncgenfunction(x) : 'ifasyncgenfunction',
        # lambda x : inspect.isawaitable(x) : 'ifawaitable',
        # lambda x : inspect.isbuiltin(x) : 'ifbuiltin',
        # lambda x : inspect.isclass(x) : 'ifclass',
        # lambda x : inspect.iscode(x) : 'ifcode',
        # lambda x : inspect.iscoroutine(x) : 'ifcoroutine',
        # lambda x : inspect.iscoroutinefunction(x) : 'ifcoroutinefunction',
        # lambda x : inspect.isdatadescriptor(x) : 'ifdatadescriptor',
        # lambda x : inspect.isframe(x) : 'ifframe',

        # lambda x : inspect.isgenerator(x) : 'ifgenerator',
        # lambda x : inspect.isgeneratorfunction(x) : 'ifgeneratorfunction',
        # lambda x : inspect.isgetsetdescriptor(x) : 'ifgetsetdescriptor',
        # lambda x : inspect.ismemberdescriptor(x) : 'ifmemberdescriptor',

        # lambda x : inspect.ismodule(x) : 'ifmodule',
        # lambda x : inspect.ismethoddescriptor(x) : 'ifmethoddescriptor',
        # lambda x : inspect.isroutine(x) : 'ifroutine',
        # lambda x : inspect.istraceback(x) : 'iftraceback',
    }

    def unroll_obj(self, obj):

        filtered = filter(
            lambda tup: not (tup[0].startswith("__") ^
                             tup[0].startswith("_Insightful__")),
            inspect.getmembers(obj)
        )
        attr_dict = {}
        for name, mem in filtered:
            prefixed_name = f"{type(mem).__name__}.{name}"
            attr_dict[prefixed_name] = self.unroll(mem, self.actions)
        return attr_dict

    def ifmethod(self, obj):
        return str(inspect.signature(obj))

    def iffunction(self, obj):
        if 'lambda' in obj.__name__:
            returned = inspect.getsource(obj).strip().rsplit(':', 1)[0]
        else:
            returned = f"{obj.__name__} {inspect.signature(obj)}"
        return returned

    def ifint(self, obj):
        return obj

    def iffloat(self, obj):
        return obj

    def ifstr(self, obj):
        return obj

    def ifdict(self, obj):
        dict = {}
        for k, v in obj.items():
            dict[str(self.unroll(k, self.actions))
                 ] = self.unroll(v, self.actions)
        return dict

    def iflist(self, obj):
        list = []
        for mem in obj:
            list.append(self.unroll(mem, self.actions))
        return list

    def iftuple(self, obj):
        tuple_as_List = list(obj)
        returned = self.unroll(tuple_as_List, self.actions)
        return tuple(returned)

    def ifset(self, obj):
        set_as_List = list(obj)
        returned = self.unroll(set_as_List, self.actions)
        return returned

    def ifnone(self, obj):
        return obj


# # derived(Sample_Class())
# obj = scheduler([10, 20, 30, 40, 50, 60, 70, 80, 90])
# # list_inp = [1, 3.4, 'S', "hello", {"sample_key_1st_half": {
# #     "sample_key_2nd_half": [(1, 2, 3), {1, 2, 3}]}}, Sample_Class()]
# # derived(list_inp)
