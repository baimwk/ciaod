#вариант БГА

В задании необходимо реализовать класс линейной динамической структуры согласно варианту.
Структура должна иметь public методы добавления элемента согласно условию,
удаления элемента согласно условию и поиска по структуре.
Тип хранимых данных – строка (класс String в Java). 
По желанию можно сделать шаблонную структуру для хранения объектов любых типов, но не обязательно.
Необходимо также реализовать механизм общения конечного пользователя со структурой. 

Пользователь должен выбрать одно из доступных действий:
  1. Добавить данные в список (после осуществления добавления содержимое списка должно выводиться на экран)
  2. Удалить данные из списка (после осуществления удаления содержимое списка должно выводиться на экран)
  3. Искать данные в списке
  4. Завершить работу программы (для C/C++ после завершения работы программы выделенная память должна быть освобождена)
  _____________________________________________________________________________________________________________________
  
  Задание задается тремя буквами. Первая буква – тип списка. Вторая буква – тип добавления. Третья буква – тип удаления.
  
  Б – Односвязный список.
  
  Г – в качестве аргумента передается значение before (имеющее тот же тип, что и хранимые данные). 
Необходимо добавить элемент перед первым элементом в списке, содержащем значение before. Если такого элемента нет, 
добавить в конец списка.     void addBefore(String before, String value)

  А – передается индекс элемента, необходимо удалить элемент с данным индексом. 
Значение индекса должно быть в диапазоне [0, n), где n – количество элементов в списке.   void remove(int index)

