#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Nov 18 09:41:21 2018

@author: zibinchen
"""

X = X_right
y = y_right
hello = DecisionTree()
hello.learn(X, y)
hello.classify(record)
tree = test_learn(X, y)

def test_learn(X, y):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        entropy_y = entropy(y)
        if entropy_y == 0:
            return np.atleast_2d(['Leaf', y[0], 'NA', 'NA'])
        
        else:
            best_info = 0
            best_i = -1
            best_j = 0
            for i in range(0, len(X[0])):
                split_range = [item[i] for item in X]
                type_x = split_range[0]
                if (isinstance(type_x,int) or isinstance(type_x,float)):
                    unique = np.unique(split_range)[1:-1]
                else:
                    unique = np.unique(split_range)
                    if len(unique) == 1:
                        unique = unique[1:-1]
                    
                for j in unique:
                    [X_left, X_right, y_left, y_right] = partition_classes(X, y, i, j)
                    current_y = list()
                    current_y.append(y_left)
                    current_y.append(y_right)
                    info_gain = information_gain(y, current_y)
                    
                    if info_gain > best_info:
                        best_info = info_gain
                        best_i = i
                        best_j = j
           
            if (best_i == -1):
                counts = np.bincount(y)
                return np.atleast_2d(['Leaf', np.argmax(counts), 'NA', 'NA'])
            else:
                [X_left, X_right, y_left, y_right] = partition_classes(X, y, best_i, best_j)
                lefttree = test_learn(X_left, y_left)
                righttree = test_learn(X_right,y_right)
                root = np.atleast_2d([best_i, best_j, 1, np.atleast_2d(lefttree).shape[0] + 1])
                root_left = np.append(root, lefttree, axis = 0)
                root_right = np.append(root_left, righttree, axis = 0)
                
        tree = root_right
        return(tree)
        pass
    
    
    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        i = 0
        start_feature = int(float(tree[i][0]))
        
        while True:
            start_feature = int(float(start_feature))
            if (isinstance(record[start_feature],int) or isinstance(record[start_feature],float)):
                start_spilt = float(tree[i][1])
                if record[start_feature] <= start_spilt:
                    i = i + int(float(tree[i][2]))
                else:
                    i = i + int(float(tree[i][3]))
            else:
                if record[start_feature] == start_spilt:
                    i = i + int(float(tree[i][2]))
                else:
                    i = i + int(float(tree[i][3]))
                          
            start_feature = tree[i][0]
            
            if start_feature == "Leaf":
                break
        
        return(float(self.tree[i][1]))
        pass
    
