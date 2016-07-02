# -*- coding: utf-8 -*- ?
import config
import codecs 

class Neuron:
    def __init__(self,lit):
        self.lit = lit
        self.memory = [[0]*config.img_size for i in range(config.img_size)]
        self.weight = 0
    
    def process_img(self, mtrx):
        self.weight = 0
        for x in range(config.img_size):
            for y in range(config.img_size):
                if mtrx[x][y]:
                    self.weight += 1  if (10 - self.memory[x][y]) < 4 else 0
                else:
                    self.weight -= 1  if self.memory[x][y] > 4 else 0
    
    def learn(self,mtrx):
        for x in range(config.img_size):
            for y in range(config.img_size):
                if mtrx[x][y] and self.memory[x][y] <= 10: self.memory[x][y] += 1


def convert_img(img_url):
    img_file = codecs.open(img_url,"r","utf-8")
    weight_mtrx = []
    for i in range(config.img_size):
        line = img_file.readline().strip()
        row = []
        for ch in line:
            if ch == "█": row.append(True)
            else: row.append(False)
        weight_mtrx.append(row)
    return weight_mtrx
    
    
def main():
    nn = []
    for i in range(33): 
        nn.append(Neuron(chr(ord("А")+i)))
    
    for i in range(11):
        for j in range(10):
            weight_mtrx = convert_img("learning/%s.txt" % chr(ord("А")+i))
            nn[i].learn(weight_mtrx)        
    while True:
        weight_mtrx = convert_img(input("Введите путь до файла: "))
        for neuron in nn: neuron.process_img(weight_mtrx)
        
        max_weight = 0 
        max_indx = 0
        for neuron_indx in range(33):
            if nn[neuron_indx].weight > max_weight:
                max_weight = nn[neuron_indx].weight
                max_indx = neuron_indx
        
        print("Я считаю, что это буква: %s" % nn[max_indx].lit)
        right_neuron = ord(input("Введите верный ответ: ")) - ord("А")
        nn[right_neuron].learn(weight_mtrx)
        
if __name__ == "__main__": main()