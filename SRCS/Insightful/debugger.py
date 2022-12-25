import inspect
import json
from collections import OrderedDict

class core():

    def __init__(self, obj=None) -> None:

        import sys
        self.modules = sys.modules
        if obj:
            returned = self.unroll(obj, self.actions)
            self.dict = returned
            self.json = json.dumps(returned, indent=2, sort_keys=True)
            # print(json.dumps(returned, indent=2, sort_keys=True))

    def unroll(self, obj, actions):

        if obj:
            returned = None
            for k, v in OrderedDict(actions).items():
                if k(obj):
                    if v == 'unroll_obj':
                        if obj.__class__.__module__ == '__main__' or obj.__class__.__module__ not in self.modules:
                            call_back = getattr(self, v)
                            returned = call_back(obj)
                        else:
                            returned = f"{type(obj).__name__} : can't - unroll"
                    else:                        
                        call_back = getattr(self, v)
                        returned = call_back(obj)
            if returned == None:
                returned = f"{type(obj).__name__} : can't - unroll"
                assert 0, returned
        else:
            returned = obj
        return returned


class crust(core):

    actions = {
        # primitive types
        lambda x: isinstance(x, int): 'ifint',
        lambda x: isinstance(x, float): 'iffloat',
        lambda x: isinstance(x, str): 'ifstr',
        lambda x: isinstance(x, list): 'iflist',
        lambda x: isinstance(x, dict): 'ifdict',
        lambda x: isinstance(x, tuple): 'iftuple',
        lambda x: isinstance(x, set): 'ifset',
        lambda x: isinstance(x, type(None)): 'ifnone',
        # function types
        lambda x: inspect.ismethod(x): 'ifmethod',
        lambda x: inspect.isfunction(x): 'iffunction',
        # custom usage classes
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

class Insightful():

    __probe = False

    def __get_probe(self):
        return Insightful.__probe

    def __set_probe(self, var: bool):
        Insightful.__probe = var

    probe = property(__get_probe, __set_probe)

    def __str__(self):

        if Insightful.__probe:
            obj_as_str = repr(self)
            return json.dumps(eval(obj_as_str), indent=2, sort_keys=True)
        else:
            return super().__repr__()

    def __repr__(self):

        if Insightful.__probe:
            return str( { f"class.{self.__class__.__name__}": crust(self).dict } )
        else:
            return str( { f"class.{self.__class__.__name__}": f"{super().__repr__()}" } )


