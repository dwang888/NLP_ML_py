import nltk
from nltk.tokenize import sent_tokenize
from practnlptools.tools import Annotator
from multiprocessing import Pool
from multiprocessing import Process
import Pyro4

def compute_task_atom(rawTxt, tokenizer, annotator):
    srls = []
    sents = tokenizer(rawTxt)
    for sent in sents:
        srl = annotator.getAnnotations(sent)['srl']
        srls.append(srl)
    return srls

class Worker_NLP:
    '''
    worker class for NLP
    '''
    nThreads = 4
    pool = None
    ith = 0
    tokenizer_sent = None
    practNLP_annotator = None
    sent_tokenizers = None
    annotators = None    
    
    def __init__(self):
        
        self.practNLP_annotator=Annotator()
        self.tokenizer_sent = nltk.tokenize.sent_tokenize
        self.pool = Pool(self.nThreads)
        self.sent_tokenizers = []
        self.annotators = []
        for i in xrange(self.nThreads):
            self.sent_tokenizers.append(nltk.tokenize.sent_tokenize)
            self.annotators.append(Annotator())
        
    def getSRL(self, rawTxt):
        sents = sent_tokenize(rawTxt)
        srls = []
        for sent in sents:
            srl = self.practNLP_annotator.getAnnotations(sent)['srl']
            srls.append(srl)
        return srls

    def getSRL_parallel(self, rawTxts):
        tasks = []#[rawTxt, tokenizer, annotator]
        for i, rawTxt in enumerate(rawTxts):
            tokenizer_tmp = self.sent_tokenizers[self.ith]
            annotator_tmp = self.annotators[self.ith]
            self.ith = (self.ith+1)%self.nThreads
            tasks.append((rawTxt, tokenizer_tmp, annotator_tmp))
        
        results = []
        for task in tasks:
            result = self.pool.apply_async(compute_task_atom, args=task)
            results.append(result)
            
        srls_results = [item.get() for item in results]
        return srls_results


if __name__ == '__main__':
#     print result.get(timeout=8)
    worker = Worker_NLP()
    daemon = Pyro4.Daemon(host="192.168.1.2", port=54315)
    Pyro4.Daemon.serveSimple(
            {
                worker: "example.worker"
            },
            ns = False,
            daemon=daemon
            )
#     print worker.getSRL("There are people dying make this world a better place for you and for me.")
    
    