

from Insightful.debugger import Insightful

# class sample(Insightful):

#     def __init__(self) -> None:
#         super().__init__()
import sys
import time
import threading

from Insightful.debugger import crust

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


class scheduler(Insightful):

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
            print(crust(self).json)
            # print(self)
            time.sleep(5)
            cnt += 1
    # def __del__(self):
    #     self.probe = True
    #     # print(self)
    #     print(crust(self).json)
    #     self.probe = False


if __name__ == "__main__":

    obj = scheduler([10, 20, 30, 40, 50, 60, 70, 80, 90])
