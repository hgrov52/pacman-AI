# mira.py
# -------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and Pieter 
# Abbeel in Spring 2013.
# For more info, see http://inst.eecs.berkeley.edu/~cs188/pacman/pacman.html

# Mira implementation
import util
PRINT = True

class MiraClassifier:
    """
    Mira classifier.

    Note that the variable 'datum' in this code refers to a counter of features
    (not to a raw samples.Datum).
    """
    def __init__( self, legalLabels, max_iterations):
        self.legalLabels = legalLabels
        self.type = "mira"
        self.automaticTuning = False
        self.C = 0.001
        self.legalLabels = legalLabels
        self.max_iterations = max_iterations
        self.initializeWeightsToZero()

    def initializeWeightsToZero(self):
        "Resets the weights of each label to zero vectors"
        self.weights = {}
        for label in self.legalLabels:
            self.weights[label] = util.Counter() # this is the data-structure you should use

    def train(self, trainingData, trainingLabels, validationData, validationLabels):
        "Outside shell to call your method. Do not modify this method."

        self.features = trainingData[0].keys() # this could be useful for your code later...

        if (self.automaticTuning):
            Cgrid = [0.002, 0.004, 0.008]
        else:
            Cgrid = [self.C]

        return self.trainAndTune(trainingData, trainingLabels, validationData, validationLabels, Cgrid)

    def trainAndTune(self, trainingData, trainingLabels, validationData, validationLabels, Cgrid):
        """
        This method sets self.weights using MIRA.  Train the classifier for each value of C in Cgrid,
        then store the weights that give the best accuracy on the validationData.

        Use the provided self.weights[label] data structure so that
        the classify method works correctly. Also, recall that a
        datum is a counter from features to values for those features
        representing a vector of values.
        """
        "*** YOUR CODE HERE ***"
        import numpy as np
        label = util.Counter()
        num = util.Counter()
        globalWeights = util.Counter()
        n=len(trainingData)
        
        total = 0    
        for current in Cgrid:
            for _ in range(self.max_iterations):
                for data in range(n):
                    for l in self.legalLabels:
                        label[l] = np.multiply(trainingData[data],self.weights[l])
                    if (trainingLabels[data] != label.argMax()):
                        update_data = trainingData[data]
                        update_label = trainingLabels[data]
                        pred = label.argMax()
                        label_num = util.Counter()
                        

                        new_weight = np.subtract(self.weights[pred],self.weights[update_label])
                        new_weight = np.multiply(new_weight,update_data)
                        new_weight = float(new_weight)+1

                        comparison = new_weight / (2.0 / float(np.multiply(update_data,update_data)))
                        minimum = min(current, comparison)
                        for example in trainingData[data].keys():
                            label_num[example] = minimum * trainingData[data][example]
                        
                        maximum = label.argMax()
                        self.weights[maximum] = np.subtract(self.weights[maximum],label_num)
                        self.weights[trainingLabels[data]] = np.add(self.weights[trainingLabels[data]],label_num)

                        
            globalWeights[current] = self.weights
            for dataVal in range(len(validationData)):
                for validationLabel in validationLabels:
                    label[validationLabel] = np.multiply(validationData[dataVal],self.weights[validationLabel])
                if(validationLabels[dataVal] == label.argMax()):
                    total += 1  
            num[current] = total
        self.weights = globalWeights[num.argMax()]

        

    def classify(self, data ):
        """
        Classifies each datum as the label that most closely matches the prototype vector
        for that label.  See the project description for details.

        Recall that a datum is a util.counter...
        """
        guesses = []
        for datum in data:
            vectors = util.Counter()
            for l in self.legalLabels:
                vectors[l] = self.weights[l] * datum
            guesses.append(vectors.argMax())
        return guesses


    def findHighOddsFeatures(self, label1, label2):
        """
        Returns a list of the 100 features with the greatest difference in feature values
                         w_label1 - w_label2

        """
        featuresOdds = []
        
        "*** YOUR CODE HERE ***"

        return featuresOdds
