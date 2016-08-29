from bookvator import NeuronNetwork

nn = NeuronNetwork()
nn.add_neuron("A")
nn.add_neuron("T")
for i in range(1,4):
    for j in "AT": 
        img_file = open("learning/%s%s.png" % (j,i), "rb")
        nn.learning(img_file, j)

while True:
    print(nn.prediction(open(input(),"rb")))