import Pyro4
from multiprocessing import Pool

def func_atom(worker, testStrs):
    results = worker.getSRL_parallel(testStrs)
    return results
    

if __name__ == '__main__':
    testStr1 = "TTTTTTTTTThere are people dying make this world a better place for you and for me."
    testStr2 = "is world a better place for you and for me."
    testStrs1 = [testStr1 for i in range(100)]
    testStrs2 = [testStr2 for i in range(100)]
#     print result.get(timeout=8)
#     worker = Worker_NLP()
#     print worker.getSRL(testStr)
    
    worker1 = Pyro4.Proxy("PYRO:example.worker@192.168.1.18:54315")
    worker2 = Pyro4.Proxy("PYRO:example.worker@192.168.1.2:54315")
#     print worker.getSRL(testStr)
    

    
#     results1 = worker1.getSRL_parallel(testStrs1)
#     print 'server 1 submit'    
#     results2 = worker2.getSRL_parallel(testStrs2)
#     print 'server 2 submit'
#     print results1
#     print results2
#     results = worker.testFunc(testStrs)
#     for result in results:
#         print result

    pool = Pool(4)
    print 'start worker1'
    result1 = pool.apply_async(func_atom, args=(worker1, testStrs1))
    print 'submitted worker1'
    
    print 'start worker2'
    result2 = pool.apply_async(func_atom, args=(worker2, testStrs2))
    print 'submitted worker2'


    print 'obtain result'
    real1 = result1.get()
    real2 = result2.get()
    print real1
    print real2