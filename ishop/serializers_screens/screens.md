1. Создать сериалайзер для обработки данных из 1 задания из лекции про формы (Напишите форму, в которой можно указать имя, пол, возраст и уровень владения английским (выпадающим списком), если введенные данные это парень старше 20-и ( включительно) и уровнем английского B2 выше, или девушка старше 22-ух и уровнем выше чем B1 то перейти на страницу где будет написано, что вы нам подходите, или что не подходит соответственно.)
Зайти в shell. Заполнить сериалайзер через data= данными. Убедиться что валидация работает в соответствии с требованиями. Прислать мне скрины.
    ![Task 1](https://raw.githubusercontent.com/ha020285mdv/shop_module/hw_for_34-35-36_lessons/ishop/serializers_screens/1.png)

2. Создать сериалайзеры для Юзера, Покупки, Товара.
    2.1 Создать объект Юзера, Товара, Покупки, связанных между собой (данные передать через data=), прислать мне скрины
    ![Task 2.1](https://raw.githubusercontent.com/ha020285mdv/shop_module/hw_for_34-35-36_lessons/ishop/serializers_screens/2.png)
    
   
    2.2 Получить объекты из базы, передать в сериалайзер без data=, посмотреть что у них хранится в атрибуте .data
     ![Task 2.2](https://raw.githubusercontent.com/ha020285mdv/shop_module/hw_for_34-35-36_lessons/ishop/serializers_screens/4.png)

3. Написать сериалайзер для Покупки (новый), который будет хранить вложенный сералайзер Юзера.
   3.1 Получить данные любого товара вместе с данными о юзере. Прислать скрины.
     выполнено в п.2 

4. Написать сериалайзер для Юзера, который будет хранить все его Покупки и выдавать их списком из словарей. (many=True)
   4.1 Получить данные любого юзера, прислать скрины.
    ![Task 4.1](https://raw.githubusercontent.com/ha020285mdv/shop_module/hw_for_34-35-36_lessons/ishop/serializers_screens/5.png)

5*. Дописать сериалайзеры из пунктов 4 и 5 так, что бы можно было создавать объекты. (Это сложно)
     ![Task 5](https://raw.githubusercontent.com/ha020285mdv/shop_module/hw_for_34-35-36_lessons/ishop/serializers_screens/6.png)