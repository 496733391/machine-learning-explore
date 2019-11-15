#! /usr/bin/python
# -*- coding: utf-8 -*-

from sklearn import neighbors, linear_model, datasets
from sklearn.preprocessing import MinMaxScaler, minmax_scale
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

digits = datasets.load_digits()

print(digits.data / digits.data.max())
x_digits = digits.data / digits.data.max()

std = StandardScaler()
x_digits2 = std.fit_transform(digits.data)
print (x_digits2)
y_digits = digits.target

x_train = x_digits[:-180]
x_test = x_digits[-180:]
x_train2 = x_digits2[:-180]
x_test2 = x_digits2[-180:]
y_train = y_digits[:-180]
y_test = y_digits[-180:]

knn_model = neighbors.KNeighborsClassifier()
knn_model.fit(x_train, y_train)
print(knn_model.predict(x_test))
print(y_test)

temp = y_test - knn_model.predict(x_test)
print(temp)

log = linear_model.LogisticRegression(solver='lbfgs', C=1e5, multi_class='multinomial')
log.fit(x_train, y_train)
print(log.predict(x_test))
print(y_test)

score = accuracy_score(y_test, log.predict(x_test), normalize=True)
print(score)
