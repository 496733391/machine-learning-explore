#! /usr/bin/python

from sklearn import neighbors, linear_model, datasets

digits = datasets.load_digits()
print digits.data.shape
print digits.target.shape
print digits.data.max()
print digits.data / digits.data.max()
x_digits = digits.data / digits.data.max()
y_digits = digits.target

x_train = x_digits[:-180]
x_test = x_digits[-180:]
y_train = y_digits[:-180]
y_test = y_digits[-180:]

knn_model = neighbors.KNeighborsClassifier()
knn_model.fit(x_train, y_train)
print knn_model.predict(x_test)
print y_test

temp = y_test - knn_model.predict(x_test)
print temp

log = linear_model.LogisticRegression(solver='lbfgs', C=1e5, multi_class='multinomial')
log.fit(x_train, y_train)
print log.predict(x_test)
print y_test

temp1 = y_test - log.predict(x_test)
print temp1
