# -*- coding: utf-8 -*-
import random
import numpy as np
import cPickle
import gzip
import json
import sys

class Quadratic(object):
    @staticmethod
    def fn(a,y):
        return (((a-y)**2).sum(axis=1)).mean()
    
    @staticmethod
    def der(a,y):
        return 2. * (a-y)
    
class CrossEntropy(object):
    @staticmethod
    def fn(a,y):
        return (np.nan_to_num(-y*np.log(a)-(1-y)*np.log(1-a)).sum(axis=1)).mean()
    
    @staticmethod
    def der(a,y):
        return np.nan_to_num(-y/a + (1-y)/(1-a))
    
class Sigmoid():
    @staticmethod
    def fn(x):
        return 1./(1.+np.exp(-x))
    
    @staticmethod
    def der(x):
        return Sigmoid.fn(x) * (1.-Sigmoid.fn(x))
    
class Relu():
    @staticmethod
    def fn(x):
        return np.where(x>0,x,0.)
    
    @staticmethod
    def der(x):
        return np.where(x>0,1.,0.)
    
class Softmax():
    @staticmethod
    def fn(x):
        return np.exp(x) / np.expand_dims(np.sum(np.exp(x), axis=1),axis=1)
    
    @staticmethod
    def der(x):
        s = Softmax.fn(x)
        p1 = np.expand_dims(s,axis=2) * np.expand_dims(np.eye(s.shape[1]),axis=0)
        p2 = np.matmul(np.expand_dims(s,axis=2), np.expand_dims(s,axis=1))
        return p1-p2

class Dense(object):
    
    def __init__(self,n_in,n_out,activation=Relu,weights=None,biases=None):
        self.size = n_in,n_out
        if biases is None:
            self.biases = np.zeros(n_out)
        else:
            self.biases = biases
        if weights is None:
            self.weights = np.random.normal(scale=2./np.sqrt(float(n_in)),size=(n_in,n_out))
        else:
            self.weights = weights
        self.activation = activation;
        
    def feed_forward(self,x):
        return (self.activation).fn(np.dot(x,self.weights) + self.biases)
    
    def feed_detail(self,x):
        z = np.dot(x,self.weights) + self.biases
        return (self.activation).fn(z), z
    
    def backprop(self,z,grad):
        tp = (self.activation).der(z)
        if len(tp.shape) == 2:
            delta = grad * tp
        else:
            delta = np.matmul(np.expand_dims(grad,axis=1),tp).reshape(grad.shape)
        return delta, np.dot(delta,self.weights.transpose())
    
    def feed_plus_eps(self,x,i,j,qty):
        z = np.dot(x,self.weights) + self.biases
        if i == -1:
            bc = np.zeros(self.biases.shape)
            bc[j] = qty
            z += bc
        else:
            wc = np.zeros(self.weights.shape)
            wc[i,j] = qty
            z += np.dot(x,wc)
        return self.activation.fn(z)

class Model(object):
    
    def __init__(self,layers,cost=Quadratic):
        self.layers = layers
        self.cost = cost
    
    def feed_forward(self,x):
        for i in range(0,len(self.layers)):
            x = self.layers[i].feed_forward(x)
        return x
    
    def backprop(self,x,y):
        activ = [x]
        vectorsz = []
        n = x.shape[0]
        for i in range(0,len(self.layers)):
            x,z = self.layers[i].feed_detail(x)
            vectorsz.append(z)
            activ.append(x)
        c = (self.cost).der(activ[-1],y)
        nabla_b = []
        nabla_w= []
        for i in range(1,len(self.layers)+1):
            delta,c = self.layers[-i].backprop(vectorsz[-i],c)
            nabla_b.insert(0,delta.mean(axis=0))
            nabla_w.insert(0, np.tensordot(activ[-i-1],delta,axes = (0,0))/n)
        return activ[-1], nabla_b, nabla_w 
    
    def fit(self, training_data, epochs, batch_size, lr, method = "Adam", validation_data=None):
        n = len(training_data)
        t=0
        if method == "Adam":
                old_grads = [[np.zeros(l.weights.shape) for l in self.layers], [np.zeros(l.biases.shape) for l in self.layers]]
                old_norms = [[np.zeros(l.weights.shape) for l in self.layers], [np.zeros(l.biases.shape) for l in self.layers]]
            
        for j in xrange(epochs):
            minibatches = create_minibatches(training_data,batch_size)
            num = 0
            cos = 0.
            numT = 0
            for i in range(0,len(minibatches)):
                t+=1
                if method=="SGD":
                    dn, dc = self.update_SGD(minibatches[i],lr)
                elif method=="NSGD":
                    dn, dc = self.update_NSGD(minibatches[i],lr)
                elif method == "Adam":
                    old_grads,old_norms,dn, dc = self.update_Adam(minibatches[i],lr,old_grads,old_norms,t)
                num += dn
                cos += dc
                numT += minibatches[i][0].shape[0]
                avg = float(num)/float(numT)
                printProgressBar(numT,n, "Epoch %i" % (j+1), "{:.2f}".format(100. * avg) + "%, cost="+"{:.6f}".format(cos /float(numT)))
            if validation_data:
                avg,cos = self.evaluate(validation_data)
                print "Epoch {0}: {1} %% cost = {2}".format(j+1, avg, cos)
            else:
                print "Epoch {0} complete".format(j+1)
    
    def update_SGD(self,minibatch, lr):
        preds, nabla_b, nabla_w = self.backprop(minibatch[0],minibatch[1])
        for i in range(len(self.layers)):
            self.layers[i].weights -= lr * nabla_w[i]
            self.layers[i].biases -= lr * nabla_b[i]
        num = np.equal(preds.argmax(axis=1),minibatch[1].argmax(axis=1)).sum()
        cos = (self.cost).fn(preds,minibatch[1]) * minibatch[0].shape[0]
        return num, cos
    
    def update_Adam(self, minibatch, lr, old_grads, old_norms,t):
        preds, nabla_b, nabla_w = self.backprop(minibatch[0],minibatch[1])
        old_grads = [[0.9 * onw + 0.1 * nw for (onw,nw) in zip(old_grads[0], nabla_w)],
                     [0.9 * onb + 0.1 * nb for (onb,nb) in zip(old_grads[1], nabla_b)]]
        old_norms = [[0.999 * onw + 0.001 * nw ** 2 for (onw,nw) in zip(old_norms[0], nabla_w)],
                     [0.999 * onb + 0.001 * nb ** 2 for (onb,nb) in zip(old_norms[1], nabla_b)]]
        for i in range(len(self.layers)):
            self.layers[i].weights -= lr * (old_grads[0][i]/(1-0.9**t)) / (np.sqrt(old_norms[0][i]/(1-0.999**t))+1e-8)
            self.layers[i].biases -= lr * (old_grads[1][i]/(1-0.9**t)) / (np.sqrt(old_norms[1][i]/(1-0.999**t))+1e-8)
        num = np.equal(preds.argmax(axis=1),minibatch[1].argmax(axis=1)).sum()
        cos = (self.cost).fn(preds,minibatch[1]) * minibatch[0].shape[0]
        return old_grads, old_norms,num, cos
    
    def update_NSGD(self,minibatch, lr):
        eps = 1e-5
        preds, nabla_b, nabla_w = self.backprop(minibatch[0],minibatch[1])
        na2_b = [np.zeros(nb.shape) for nb in nabla_b]
        na2_w = [np.zeros(nw.shape) for nw in nabla_w]
        for l in range(0,len(self.weights)):
            for j in range(0,self.weights[l].shape[1]):
                t = self.eval_der_sec(minibatch[0],minibatch[1],l,-1,j)
                if t==0.:
                    na2_b[l][j] = eps
                elif np.abs(t) >= eps:
                    na2_b[l][j] = t
                else:
                    na2_b[l][j] = eps * np.sign(t)
                for i in range(0,self.weights[l].shape[0]):
                    t = self.eval_der_sec(minibatch[0],minibatch[1],l,i,j)
                    if t==0.:
                        na2_w[l][i,j] = eps
                    elif np.abs(t) >= eps:
                        na2_w[l][i,j]  = t
                    else:
                        na2_w[l][i,j]  = eps * np.sign(t) 
        self.weights = [w  - lr * nw/nw2 for (w,nw,nw2) in zip(self.weights, nabla_w,na2_w)]
        self.biases = [b - lr * nb/nb2 for (b,nb,nb2) in zip(self.biases, nabla_b, na2_b)]
        num = np.equal(preds.argmax(axis=1),minibatch[1].argmax(axis=1)).sum()
        cos = (self.cost).fn(preds,minibatch[1]) * minibatch[0].shape[0]
        return num, cos
    
    def evaluate(self,tst_data,batch_size=64):
        mbs = create_minibatches(tst_data,batch_size,False)
        num_correct = 0
        coste = 0.
        for mb in mbs:
            z = self.feed_forward(mb[0])
            preds = z.argmax(axis=1)
            num_correct += np.equal(preds,mb[1].argmax(axis=1)).sum()
            coste += (self.cost).fn(z,mb[1]) * z.shape[0]
        return 100.* float(num_correct) /float(len(tst_data)) , coste / float(len(tst_data))
    
    def save(self,filename):
        data = {"cost" : str(self.cost.__name__)}
        c = 0
        for l in self.layers:
            c+=1
            data_l = {"name" : str(l.__class__.__name__),
                "activation" : str(l.activation.__name__),
                "size": list(l.size),
                "weights": l.weights.tolist(),
                "biases": l.biases.tolist()}
            data["layer" + str(c)] =data_l
        f = open(filename, "w")
        json.dump(data, f)
        f.close()
        
    def eval_der(self,x,y,l,i,j):
        eps = 1e-5
        z1 = self.feed_forward(x)
        for cl in range(0,len(self.layers)):
            if cl == l:
                x = self.layers[cl].feed_plus_eps(x,i,j,eps)
            else:
                x = self.layers[cl].feed_forward(x)
        return ((self.cost).fn(x,y)-(self.cost).fn(z1,y))/eps
    
    def eval_der_sec(self,x,y,l,i,j):
        eps = 1e-5
        z = self.feed_forward(x)
        x1 = np.copy(x)
        for cl in range(0,len(self.layers)):
            if cl == l:
                x = self.layers[cl].feed_plus_eps(x,i,j,eps)
                x1 = self.layers[cl].feed_plus_eps(x1,i,j,-eps)
            else:
                x = self.layers[cl].feed_forward(x)
                x1 = self.layers[cl].feed_forward(x1)
        return ((self.cost).fn(x,y)+(self.cost).fn(x1,y)-2.*(self.cost).fn(z,y))/(eps**2)

class Network(object):
    
    def __init__(self,layers, cost = Quadratic):
        self.num_layers = len(layers)
        self.sizes = [l[0] for l in layers]
        self.activations = [l[1] for l in layers[1:]]
        self.biases = [np.random.randn(y) for y in self.sizes[1:]]
        self.weights = [np.random.randn(x,y)/np.sqrt(x) for (x,y) in zip(self.sizes[:-1],self.sizes[1:])]
        self.cost = cost;
    
    def feed_forward(self,x):
        for i in range(0,len(self.weights)):
            x = (self.activations[i]).fn(np.dot(x,self.weights[i]) + self.biases[i])
        return x
    
    def feed_details(self,x):
        activ = [x]
        vectorsz = []
        for i in range(0,len(self.weights)):
            z = np.dot(x,self.weights[i]) + self.biases[i]
            vectorsz.append(z)
            x = (self.activations[i]).fn(z)
            activ.append(x)
        return activ, vectorsz
    
    def fit(self, training_data, epochs, batch_size, lr, method = "Adam", validation_data=None):
        n = len(training_data)
        t=0
        if method == "Adam":
                old_grads = [[np.zeros(w.shape) for w in self.weights], [np.zeros(b.shape) for b in self.biases]]
                old_norms = [[np.zeros(w.shape) for w in self.weights], [np.zeros(b.shape) for b in self.biases]]
            
        for j in xrange(epochs):
            minibatches = create_minibatches(training_data,batch_size)
            num = 0
            cos = 0.
            numT = 0
            for i in range(0,len(minibatches)):
                t+=1
                if method=="SGD":
                    dn, dc = self.update_SGD(minibatches[i],lr)
                elif method=="NSGD":
                    dn, dc = self.update_NSGD(minibatches[i],lr)
                elif method == "Adam":
                    old_grads,old_norms,dn, dc = self.update_Adam(minibatches[i],lr,old_grads,old_norms,t)
                num += dn
                cos += dc
                numT += minibatches[i][0].shape[0]
                avg = float(num)/float(numT)
                printProgressBar(numT,n, "Epoch %i" % (j+1), "{:.2f}".format(100. * avg) + "%, cost="+"{:.6f}".format(cos /float(numT)))
            if validation_data:
                avg,cos = self.evaluate(validation_data)
                print "Epoch {0}: {1} %% cost = {2}".format(j+1, avg, cos)
            else:
                print "Epoch {0} complete".format(j+1)
    
    def update_SGD(self,minibatch, lr):
        preds, nabla_b, nabla_w = self.backprop(minibatch[0],minibatch[1])
        self.weights = [w  - lr * nw for w,nw in zip(self.weights, nabla_w)]
        self.biases = [b - lr * nb for b,nb in zip(self.biases, nabla_b)]
        num = np.equal(preds.argmax(axis=1),minibatch[1].argmax(axis=1)).sum()
        cos = (self.cost).fn(preds,minibatch[1]) * minibatch[0].shape[0]
        return num, cos
    
    def update_Adam(self, minibatch, lr, old_grads, old_norms,t):
        preds, nabla_b, nabla_w = self.backprop(minibatch[0],minibatch[1])
        old_grads = [[0.9 * onw + 0.1 * nw for (onw,nw) in zip(old_grads[0], nabla_w)],
                     [0.9 * onb + 0.1 * nb for (onb,nb) in zip(old_grads[1], nabla_b)]]
        old_norms = [[0.999 * onw + 0.001 * nw ** 2 for (onw,nw) in zip(old_norms[0], nabla_w)],
                     [0.999 * onb + 0.001 * nb ** 2 for (onb,nb) in zip(old_norms[1], nabla_b)]]
        self.weights = [w  - lr * (nw/(1-0.9**t)) / (np.sqrt(vw/(1-0.999**t))+1e-8) for w,nw,vw in zip(self.weights, old_grads[0], old_norms[0])]
        self.biases = [b - lr * (nb/(1.09**t)) / (np.sqrt((vb/(1-0.999**t)))+1e-8) for b,nb, vb in zip(self.biases, old_grads[1], old_norms[1])]
        num = np.equal(preds.argmax(axis=1),minibatch[1].argmax(axis=1)).sum()
        cos = (self.cost).fn(preds,minibatch[1]) * minibatch[0].shape[0]
        return old_grads, old_norms,num, cos
    
    def update_NSGD(self,minibatch, lr):
        eps = 1e-5
        preds, nabla_b, nabla_w = self.backprop(minibatch[0],minibatch[1])
        na2_b = [np.zeros(nb.shape) for nb in nabla_b]
        na2_w = [np.zeros(nw.shape) for nw in nabla_w]
        for l in range(0,len(self.weights)):
            for j in range(0,self.weights[l].shape[1]):
                t = self.eval_der_sec(minibatch[0],minibatch[1],l,-1,j)
                if t==0.:
                    na2_b[l][j] = eps
                elif np.abs(t) >= eps:
                    na2_b[l][j] = t
                else:
                    na2_b[l][j] = eps * np.sign(t)
                for i in range(0,self.weights[l].shape[0]):
                    t = self.eval_der_sec(minibatch[0],minibatch[1],l,i,j)
                    if t==0.:
                        na2_w[l][i,j] = eps
                    elif np.abs(t) >= eps:
                        na2_w[l][i,j]  = t
                    else:
                        na2_w[l][i,j]  = eps * np.sign(t) 
        self.weights = [w  - lr * nw/nw2 for (w,nw,nw2) in zip(self.weights, nabla_w,na2_w)]
        self.biases = [b - lr * nb/nb2 for (b,nb,nb2) in zip(self.biases, nabla_b, na2_b)]
        num = np.equal(preds.argmax(axis=1),minibatch[1].argmax(axis=1)).sum()
        cos = (self.cost).fn(preds,minibatch[1]) * minibatch[0].shape[0]
        return num, cos
        
    def backprop(self,x,y):
        activ = [x]
        vectorsz = []
        n = x.shape[0]
        for i in range(0,len(self.weights)):
            z = np.dot(x,self.weights[i]) + self.biases[i]
            vectorsz.append(z)
            x = (self.activations[i]).fn(z)
            activ.append(x)
        #nabla_b = [np.zeros(b.shape) for b in self.biases]
        #nabla_w = [np.zeros(w.shape) for w in self.weights]
        tp = (self.activations[-1]).der(vectorsz[-1])
        if len(tp.shape) == 2:
            delta = (self.cost).der(activ[-1],y) * tp
        else:
            c = (self.cost).der(activ[-1],y)
            delta = np.matmul(np.expand_dims(c,axis=1),tp).reshape(c.shape)
        nabla_b = [delta.mean(axis=0)]
        nabla_w = [np.tensordot(activ[-2],delta,axes = (0,0))/n]
        for l in xrange(2,self.num_layers):
            delta = np.dot(delta,self.weights[-l+1].transpose()) * (self.activations[-l]).der(vectorsz[-l])
            nabla_b = [delta.mean(axis=0)] + nabla_b
            nabla_w =  [np.tensordot(activ[-l-1],delta,axes = (0,0))/n]+ nabla_w
        return activ[-1], nabla_b, nabla_w 
            
    def evaluate(self,tst_data,batch_size=64):
        mbs = create_minibatches(tst_data,batch_size,False)
        num_correct = 0
        coste = 0.
        for mb in mbs:
            z = self.feed_forward(mb[0])
            preds = z.argmax(axis=1)
            num_correct += np.equal(preds,mb[1].argmax(axis=1)).sum()
            coste += (self.cost).fn(z,mb[1]) * z.shape[0]
        return 100.* float(num_correct) /float(len(tst_data)) , coste / float(len(tst_data))
    
    def save(self,filename):
        data = {"activations" : [str(act.__name__) for act in self.activations],
                "sizes": self.sizes,
                "weights": [w.tolist() for w in self.weights],
                "biases": [b.tolist() for b in self.biases],
                "cost": str(self.cost.__name__)}
        f = open(filename, "w")
        json.dump(data, f)
        f.close()
        
    def eval_der(self,x,y,l,i,j):
        eps = 1e-5
        z1 = self.feed_forward(x)
        for cl in range(0,len(self.weights)):
            z = np.dot(x,self.weights[cl]) + self.biases[cl]
            if cl == l:
                if i == -1:
                    bc = np.zeros(self.biases[cl].shape)
                    bc[j] = eps
                    z += bc
                else:
                    wc = np.zeros(self.weights[cl].shape)
                    wc[i,j] = eps
                    z += np.dot(x,wc)
            x = (self.activations[cl]).fn(z)
        return ((self.cost).fn(x,y)-(self.cost).fn(z1,y))/eps
    
    def eval_der_sec(self,x,y,l,i,j):
        eps = 1e-5
        z = self.feed_forward(x)
        x1 = np.copy(x)
        for cl in range(0,len(self.weights)):
            z1 = np.dot(x,self.weights[cl]) + self.biases[cl]
            z2 = np.dot(x1,self.weights[cl]) + self.biases[cl]
            if cl == l:
                if i == -1:
                    bc = np.zeros(self.biases[cl].shape)
                    bc[j] = eps
                    z1 += bc
                    z2 -= bc
                else:
                    wc = np.zeros(self.weights[cl].shape)
                    wc[i,j] = eps
                    z1 += np.dot(x,wc)
                    z2 -= np.dot(x1,wc)
            x = (self.activations[cl]).fn(z1)
            x1 = (self.activations[cl]).fn(z2)
        return ((self.cost).fn(x,y)+(self.cost).fn(x1,y)-2.*(self.cost).fn(z,y))/(eps**2)

    
def load_data():
    f = gzip.open("D:/Temp/Deeplearning/neural-networks-and-deep-learning/data/mnist.pkl.gz", 'rb')
    tr_d, va_d, te_d = cPickle.load(f)
    f.close()
    training_results = [vectorized_result(y) for y in tr_d[1]]
    training_data = zip(tr_d[0] , training_results)
    val_results = [vectorized_result(y) for y in va_d[1]]
    validation_data = zip(va_d[0],val_results)
    test_results = [vectorized_result(y) for y in te_d[1]]
    test_data = zip(te_d[0], test_results)
    return (training_data, validation_data, test_data)

def load_databis():
    f = gzip.open("D:/Temp/Deeplearning/neural-networks-and-deep-learning/data/mnist.pkl.gz", 'rb')
    tr_d, va_d, te_d = cPickle.load(f)
    f.close()
    return tr_d

def create_minibatches(data,size,shuffle=True):
    n = len(data)
    L = list(range(0,n))
    if shuffle:
        L = np.random.permutation(L)
    if n%size != 0:
        last_X = np.array([data[L[n//size + j]][0] for j in range(0,n%size)])
        last_Y = np.array([data[L[n//size + j]][1] for j in range(0,n%size)])
    else:
        last_X = np.array([data[L[n//size + j]][0] for j in range(0,size)])
        last_Y = np.array([data[L[n//size + j]][1] for j in range(0,size)])
    minibatches = [(np.array([data[L[i + j]][0] for j in range(0,size)]),np.array([data[L[i + j]][1] for j in range(0,size)])) for i in range(0,n-size,size)] + [(last_X,last_Y)]
    return minibatches

def get_one():
    tr_d = load_databis()
    f = open("D:/Temp/Deeplearning/digit.csv",'w')
    L = tr_d[0][0]
    for i in range(0,28):
        line = ""
        for j in range(0,28):
            line += str(L[j+28*i]) + ";"
        line = line[:-1] + "\n"
        f.write(line)
    f.close()

def vectorized_result(j):
    e = np.zeros(10)
    e[j] = 1.0
    return e

def loadnetwork(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data["cost"])
    activs = [getattr(sys.modules[__name__], act) for act in data["activations"]]
    L = [[data["sizes"][0]]] + [[dat,act] for (dat,act) in zip(data["sizes"][1:], activs)]
    net = Network(L, cost=cost)
    net.weights = [np.array(w) for w in data["weights"]]
    net.biases = [np.array(b) for b in data["biases"]]
    return net

def load_model(filename):
    f = open(filename, "r")
    data = json.load(f)
    f.close()
    cost = getattr(sys.modules[__name__], data["cost"])
    c = 1
    L = []
    while "layer" + str(c) in data:
        data_l = data["layer" + str(c)]
        size = data_l["size"]
        layer = getattr(sys.modules[__name__], data_l["name"])(size[0],size[1],
                activation = getattr(sys.modules[__name__], data_l["activation"]),
                weights = np.array(data_l["weights"]),
                biases = np.array(data_l["biases"]))
        L.append(layer)
        c+=1
    model = Model(L,cost=cost)
    return model

def printProgressBar (iteration, total, prefix = '', suffix = '', length = 50, fill = '-'):
    percent = "%i/%i" % (iteration,total)
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '>' + ' ' * (length - filledLength-1)
    print '\r%s %s |%s| %s' % (prefix, percent, bar, suffix),
    # Print New Line on Complete
    if iteration >= total: 
        print

def gen_rd_data(n_in,n_out,n_samp):
    X = np.random.normal(size=(n_samp,n_in))
    A = np.random.normal(size=(n_in,n_out))
    noise = np.random.normal(size=(n_samp,n_out),scale=0.01)
    Y = np.dot(X,A) + noise
    Y = np.where(Y>0.,np.zeros(Y.shape),np.ones(Y.shape))
    return [(X[i,:],Y[i,:]) for i in range(n_samp)]

def check_zeros(L1,L2):
    L1 = [np.where(X==0.,np.ones(X.shape),np.zeros(X.shape)) for X in L1]
    L2 = [np.where(X==0.,np.ones(X.shape),np.zeros(X.shape)) for X in L2]
    L1 = [np.sum(X) for X in L1]
    L2 = [np.sum(X) for X in L2]
    if sum(L1) != 0.:
        l=0
        while L1[l]==0.:
            l+=1
        print("Zero in L1 layer " + str(l))
    if sum(L2) != 0.:
        l=0
        while L1[2]!=0.:
            l+=1
        print("Zero in L2 layer " + str(l))

def copy_mod(net):
    L = []
    for i in range(0,len(net.weights)):
        dense = Dense(net.weights[i].shape[0],net.weights[i].shape[1],net.activations[i],net.weights[i],net.biases[i])
        L.append(dense)
    return Model(L,net.cost)