class Person:
  def __init__(mysillyobject, name, age,x):
    mysillyobject.name = name
    mysillyobject.age = age + x

  def myfunc(self,txt):
    return txt

  def printmyFunc(self):
      return self.myfunc("Azzam")
p1 = Person("John", 36,5)
print(p1.myfunc("Hi"))
print(p1.printmyFunc())
