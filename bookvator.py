from PIL import Image
from math import e

class Neuron:
    #инициализируем нейрон, указываем имя создаем память и прочие настройки
    def __init__(self, name, activation = 0.55, normalizer = 200, image_size = (15,20)):
        self.name = name
        self.normalizer = normalizer
        self.img_size = image_size
        self.activation = activation
        self.memory = [[0]*self.img_size[1] for y in range(self.img_size[0])]
    
    #создание предсказания на основе памяти нейрона
    def predict(self, img_file):
        img = Image.open(img_file).resize(self.img_size)
        
        #получаем результирующие значение (сумму входного вектора умноженного на коэффициент нейрона)
        X = 0
        for x in range(self.img_size[0]):
            for y in range(self.img_size[1]):
                pixel = 0 if sum(img.getpixel((x,y))) else 1
                X += pixel * self.memory[x][y]
        
        #нормализуем полученое значение
        X = X/self.normalizer
        #проводим его через передаточною функцию (в нашем случае сигматоида)
        result = 1/(1 + e**(-X))

        return (True if result > self.activation else False , result)

    #обучение нейрона
    def learn(self, img_file, right_name):
        #получаем верный ответ для данного нейрона
        if right_name == self.name: right_answer = True
        else:  right_answer = False
        
        answer = self.predict(img_file)[0]
        cff = 1
        
        if answer != right_answer:
            #разбираем две ситуации: ложно положительную и ложно отрицательную, в зависимости от ситуации меняется коэффициент
            if answer: cff = -1
            
            img = Image.open(img_file).resize(self.img_size)
            
            #в зависимости от ситуации прибавляем/вычитаем значение входного вектора
            for x in range(self.img_size[0]):
                for y in range(self.img_size[1]):
                    pixel = 0 if sum(img.getpixel((x,y))) else 1
                    self.memory[x][y] += pixel*cff      
        
class NeuronNetwork:
    #инициализируем нашу сеть
    def __init__(self, activation = 0.55, normalizer = 180, image_size = (15,20)):
        self.net = []
        self.normalizer = normalizer
        self.image_size = image_size
        self.activation = activation 
    
    #добавляем новый нейрон в сеть
    def add_neuron(self,name):
        self.net.append(Neuron(name, 
                               activation = self.activation, 
                               normalizer = self.normalizer, 
                               image_size = self.image_size))
    
    #обучаем сеть
    def learning(self, img_file, answer):
        for neuron in self.net:
            neuron.learn(img_file, answer)
    
    #делаем предсказание
    def prediction(self, img_file):
        for neuron in self.net:
            answer = neuron.predict(img_file)
            if answer[0]: return (neuron.name, answer[1]*100//1)
        return None