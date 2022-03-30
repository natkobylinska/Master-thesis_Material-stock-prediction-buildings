import numpy as np
import matplotlib.pyplot as plt

data = np.array([[ 1.2, 0.7],
                 [-0.3,-0.5],
                 [ 3.0, 0.1],
                 [-0.1,-1.0],
                 [-1.0, 1.1],
                 [ 2.1,-3.0]])
labels = np.array([ 1,
                   -1,
                    1,
                   -1,
                   -1,
                   +1])

def eval_accuracy(X,Y,A,B,C):
    num_correct = 0;
    data_len = data.shape[0]
    
    for i in range(data_len):
        X,Y = data[i]
        true_label = labels[i]
        
        output = A*X + B*Y + C
        predicted_label = 1 if output > 0 else -1
        
        if (predicted_label == true_label):
            num_correct += 1
    return num_correct / data_len

def create_meshgrid(data):
    h = 0.02
    x_min, x_max = data[:, 0].min() - 1, data[:, 0].max() + 1
    y_min, y_max = data[:, 1].min() - 1, data[:, 1].max() + 1
    xx, yy = np.meshgrid(np.arange(x_min, x_max, h), np.arange(y_min, y_max, h))
    return (xx,yy,np.ones(xx.shape))

def plot_learning_simple(grid,data,A,B,C,iteration, accuracy):
    xx,yy,Z = grid
    
    for i in range(xx.shape[0]): # row
        for j in range(yy.shape[1]): #column
            X, Y = xx[i][j],yy[i][j]
            output = A*X + B*Y + C
            output = 1 if output > 0 else -1
            Z[i][j] = output

    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    plt.title(f'accuracy at the iteration {iteration}: {accuracy}')
    ax.contourf(xx, yy, Z, cmap=plt.cm.binary, alpha=0.1, zorder=15)
    ax.scatter(data[:, 0], data[:, 1], c=labels, s=50,  cmap=plt.cm.bwr,zorder=50)
    ax.set_aspect('equal')
    nudge = 0.08
    for i in range(data.shape[0]):
        d = data[i]
        ax.annotate(f'{i}',(d[0]+nudge,d[1]+nudge))
    plt.xlim(xx.min(), xx.max())
    plt.ylim(yy.min(), yy.max())
    plt.show()

def train_neural_network(data, labels, step_size, no_loops, iter_info):
    #A, B, and C are parameters of the function F. Here, they are set to 1, -2, -1
    A, B, C = 1, -2, -1
    # regularization strenght
    reg_strength = 0.2
    # this function is used for plotting, it can be ignored
    grid = create_meshgrid(data)
    
    # the main training loop
    for i in range(no_loops):
        # we randomly select the data point, and store its info into: x,y,label
        index = np.random.randint(data.shape[0])
        X,Y = data[index]
        label = labels[index]
        # we calculate the output of the function
        output = A*X + B*Y + C
        # We need to define how to affect parameters.
        # If the label is 1 but the output is smaller than 1, we want to push the score up.
        # If the label is -1 but the output is larger than -1, we want to push the score down.
        pull = 0.0
        if (label == 1 and output < 1):
            pull = 1.0
        if (label ==-1 and output > -1):
            pull = -1.0
        # here we update the values with the partial derivatives, and regularization.
        # partial derivative of dF/dA is X, dF/dB is Y, and of dF/dC is 1. 
        # regularization means to pull the parameters A, B, and C towards zero (in the oposite direction)
        A += step_size * (X * pull - A*reg_strength) # -A*reg_strength is from the regularization
        B += step_size * (Y * pull - B*reg_strength) # -A*reg_strength is from the regularization
        C += step_size * pull;
        
        # after a number of iterations, show training accuracy and plot it
        if (i%iter_info==0):
            accuracy = eval_accuracy(X,Y,A,B,C)
            plot_learning_simple(grid,data,A,B,C,i,accuracy)
    # the algorithm returns the learned parameters A, B, and C
    return (A,B,C)

train_1 = train_neural_network(data, labels, 0.01, 1000, 200)

def show_prediction_SVM_simple(train, data, labels):
    a, b, c = train
    for i in range(data.shape[0]):
        x,y = data[i]
        label = labels[i]
        score = a*x + b*y + c
        score = 1 if score > 0 else -1
        print (f'data point {i}: real label : {label}, pred. label: {score}, {(score==label)}')

show_prediction_SVM_simple(train_1,data,labels)