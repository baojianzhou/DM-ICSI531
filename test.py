import numpy as np
import matplotlib.pyplot as plt
from numpy import genfromtxt
import pickle


def test():
    my_data = genfromtxt('slice_localization_data.csv', delimiter=',')

    patients = dict()
    for i in range(1, len(my_data)):
        if int(my_data[i][0]) not in patients:
            patients[int(my_data[i][0])] = []
        else:
            patients[int(my_data[i][0])].append(my_data[i][1:])
    for i in patients:
        pickle.dump(patients[i], open('patient_%02d.pkl' % int(i), 'wb'))
    pass


patient = pickle.load(open('patient_95.pkl', 'r'))
plt.imshow(np.asarray(patient)[:, 0:383])
plt.show()
pass
