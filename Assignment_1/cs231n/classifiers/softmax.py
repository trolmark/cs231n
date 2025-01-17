from builtins import range
import numpy as np
from random import shuffle
from past.builtins import xrange

def softmax_loss_naive(W, X, y, reg):
    """
    Softmax loss function, naive implementation (with loops)

    Inputs have dimension D, there are C classes, and we operate on minibatches
    of N examples.

    Inputs:
    - W: A numpy array of shape (D, C) containing weights.
    - X: A numpy array of shape (N, D) containing a minibatch of data.
    - y: A numpy array of shape (N,) containing training labels; y[i] = c means
      that X[i] has label c, where 0 <= c < C.
    - reg: (float) regularization strength

    Returns a tuple of:
    - loss as single float
    - gradient with respect to weights W; an array of same shape as W
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using explicit loops.     #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    def soft_max(x, exps):
        exps -= np.max(exps)
        p = np.exp(exps[x]) / np.sum(np.exp(exps))
        return p
    
    num_classes = W.shape[1]
    num_train = X.shape[0]
   
    for i in range(num_train):
        scores = X[i].dot(W)
        for j in range(num_classes):
            p = soft_max(j, scores)
            if j == y[i]:
                loss += -np.log(p)
                dW[:, j] += (p - 1) * X[i]
            else:
                dW[:, j] += p * X[i]
          
    # Add regularization to the loss.
    loss /= num_train
    loss += reg * np.sum(W * W)
    
    dW /= num_train
    dW += reg * W

    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW

def softmax_loss_vectorized(W, X, y, reg):
    """
    Softmax loss function, vectorized version.

    Inputs and outputs are the same as softmax_loss_naive.
    """
    # Initialize the loss and gradient to zero.
    loss = 0.0
    dW = np.zeros_like(W)
    
    num_classes = W.shape[1]
    num_train = X.shape[0]

    #############################################################################
    # TODO: Compute the softmax loss and its gradient using no explicit loops.  #
    # Store the loss in loss and the gradient in dW. If you are not careful     #
    # here, it is easy to run into numeric instability. Don't forget the        #
    # regularization!                                                           #
    #############################################################################
    # *****START OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****
    
    scores = X.dot(W)
    scores -= np.matrix(np.max(scores, axis=1)).T
    scores_y = -scores[np.arange(num_train), y]
    scores_j = np.sum(np.exp(scores), axis = 1)
    loss = scores_y + np.log(scores_j)
    loss = np.mean(loss)
    loss += reg * np.sum(W * W)
    
    derivative = np.exp(scores) / np.matrix(scores_j).T
    derivative[np.arange(num_train), y] -= 1
    dW = X.T.dot(derivative)
    
    dW /= num_train
    dW += reg * W
   
    # *****END OF YOUR CODE (DO NOT DELETE/MODIFY THIS LINE)*****

    return loss, dW
