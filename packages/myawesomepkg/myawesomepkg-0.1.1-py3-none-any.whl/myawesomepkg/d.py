import math
n=int(input("Enter no of input neurons:"))

print("enter input")
inputs=[]

for i in range(0,n):
    x=float(input())
    inputs.append(x)
print(inputs)

print("enter weight")
weights=[]

for i in range(0,n):
    w=float(input())
    weights.append(w)
print(weights)

print(" the net input is calculated as Yin=x1w1+x2w2+x3w3")

Yin=[]
for i in range(0,n):
    Yin.append(inputs[i]*weights[i])
ynet=round(sum(Yin),3)

print("net input for y neuron",ynet)

print("apply activation function over net input, Binary function")

y=round(1/(1+math.exp(-ynet)),3)
print(y)

print("apply activation function over net input, Bipolar function")
y=round((2/(1+math.exp(-ynet)))-1,3)
print(y)
