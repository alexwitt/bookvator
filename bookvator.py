from PIL import Image
from math import e

class Neuron:
    def __init__(self, name, activation = 0.55, normalizer = 200, image_size = (15,20)):
        self.name = name
        self.normalizer = normalizer
        self.img_size = image_size
        self.activation = activation
        self.memory = [[0]*self.img_size[1] for y in range(self.img_size[0])]
        
    def predict(self, img_file):
        img = Image.open(img_file).resize(self.img_size)
        
        X = 0
        for x in range(self.img_size[0]):
            for y in range(self.img_size[1]):
                pixel = 0 if sum(img.getpixel((x,y))) else 1
                X += pixel * self.memory[x][y]
        
        X = X/self.normalizer
        result = 1/(1 + e**(-X))
        
        return (True if result > self.activation else False , result)

    def learn(self, img_file, right_name):
        if right_name == self.name: right_answer = True
        else:  right_answer = False
        
        answer = self.predict(img_file)[0]
        cff = 1
        
        if answer != right_answer:
            if answer: cff = -1
            
            img = Image.open(img_file).resize(self.img_size)
            
            for x in range(self.img_size[0]):
                for y in range(self.img_size[1]):
                    pixel = 0 if sum(img.getpixel((x,y))) else 1
                    self.memory[x][y] += pixel*cff      
        
class NeuronNetwork:
    def __init__(self, activation = 0.55, normalizer = 180, image_size = (15,20)):
        self.net = []
        self.normalizer = normalizer
        self.image_size = image_size
        self.activation = activation 
        
    def add_neuron(self,name):
        self.net.append(Neuron(name, 
                               activation = self.activation, 
                               normalizer = self.normalizer, 
                               image_size = self.image_size))
    
    def learning(self, img_file, answer):
        for neuron in self.net:
            neuron.learn(img_file, answer)
    
    def prediction(self, img_file):
        for neuron in self.net:
            answer = neuron.predict(img_file)
            if answer[0]: return (neuron.name, answer[1]*100//1)
        return None