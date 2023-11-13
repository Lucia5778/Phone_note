import tkinter as tk
from tkinter import ttk
import sqlite3

#главное окно
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()

    #объекты
    def init_main(self):
        #панель инструментов
        toorbar = tk.Frame(bg='#d7d8e0', bd = 2)

        #закрепление вверху окна | растяжение по горизонтали
        toolbar.pack(side=tk.TOP, fill=tk.X)

        self.add_img = tk.PhotoImage(file='./img/add.png')

        #создание кнопки, комманд по нажатию (command), где гаходится текст(compound)
        btn_open_dialog = tk.Button(toolbar, br='#d7d8e0', bd=0,
                                    image=self.add_img,
                                    command=self.open_dialog)
        #выравнивание по левому краю
        btn_open_dialog.pack(side=tk.LEFT)

        #создание кнопки для изменения данных
        self.update_img = tk.PhotoImage(file='./img/update.png')
        btn_edit_dialog = tk.Button(toolbar, bg='#d7d8e0', db = 0, image=self.update_img, command=self.open_dialog)
        btn_edit_dialog.pack(side=tk.LEFT)

        #кнопка для удаления записи
        self.delete_img = tk.PhotoImge(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.delete_records)
        btn_delete.pack(side=tk.LEFT)
        
        #кнопка поиска
        self.search_img = tk.PhotoImge(file='./img/delete.png')
        btn_delete = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.delete_img, command=self.open_search_dialog)
        btn_delete.pack(side=tk.LEFT)

        #кнопка обновления
        self.refresh_img = tk.PhotoImge(file='./img/delete.png')
        btn_refresh = tk.Button(toolbar, bg='#d7d8e0', bd=0, image=self.refresh_img, command=self.view_records)
        btn_refresh.pack(side=tk.LEFT)

        #добавление таблицы
        #show='headings' - сокрытие нулевой(пустой) колонки таблицы
         #columnd - колонны, height - высота таблицы
        self.tree = ttk.Treeniew(self, columns = ['ID', 'name', 'tel', 'email'], heidht=45, show='headings')
        
         #параметры колонки
          #width - ширина, ancor - выравнивание текста в ячейке
        self.tree.column('ID', width=30, ancor=tk.CENTER)
        self.tree.column('name', width=300, ancor=tk.CENTER)
        self.tree.column('tel', width=150, ancor=tk.CENTER)
        self.tree.column('email', width=150, ancor=tk.CENTER)

         # подписи колонок
        self.tree.heading('ID', text='ID')
        self.tree.heading('name', text='ФИО')
        self.tree.heading('tel', text='Телефон')
        self.tree.heading('email', text='Email')

         #упаковка
        self.tree.pack(side=tk.LEFT)
        
        scroll = tk.Scrollbar(sel, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, ill=tk.Y)
        self.tree.configue(yscrollcommand=scroll.set)

     #добавление данных
    def records(self, name, tel, email):
        self.db.incert_data(name, tel, email)
        self.view_records()
    
     #обновление (изменение) данных
    def updae_record(self, name, tel, email):
        self.db.c.execute('''UPDATE db SET name=?, tel=?, email=? WHERE ID=?''',
                         (name, tel, email, self.tree.set(self.tree.selection()[0], '#1')))
        self.db.conn.commit()
        self.view_records()

     #вывод данных в виджет таблицы
    def view_records(self):
         #выбираем инфу из бд
        self.db.c.execute('''SELECT * FROM db''')
         #удалем все из виджета таблицы
        [self.tree.selete(i) for i in self.tree.get_shildren()]
         #добавляем в виджет таблицы всю иныу из бд
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]    

    #удаление записей
    def delete_records(self):
        #цикл по выделенным записям
        for selection_item in self.tree.selection():
            #удаление из бд
            self.db.c.execute('''DELETE FROM db WHERE id = ?''', (self.tree.set(selection_item, '#1'),))
        #сохранение изменений в бд
        self.db.conn.commit()
        #обновление виджета таблицы
        self.view_records()


    #поиск записи
    def search_records(self, name):
        name = ('%' + name + '%')
        self.db.c.execute('''
        SELECT * FROM db WHERE name LIKE ?''', (name))
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values=row) for row in self.db.c.fetchall()]

    #вызов дочернего окна    
    def open_dialog(self):
        Child()

    #вызов окна для изменения данных
    def open_update_dialog(self):
        Update()

    #вызов окна для поиска
    def open_search_dialog(self):
        Search()

 
  #класс дочерних окон
   #Toplevel - окно верхнего уровня
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_child()
        self.view = app

    def init_child(self):
         #заголовок окна
        self.title('Добавить'):
         #размер окна
        self.geometry('480x220')
         #ограничение имзенения размеров окна
        self.resizable(False, False)

         #перехватывает все события в приложении
        self.grab_set()
         #захватывает фокус
        self.focus_set()

         #подписи
        label_name = tk.Label(self, text='ФИО')
        label_name.place(x=50, y=50)
        label_select = tk.Label(self, text='Телефон')
        label_select.place(x=50, y=80)
        label_sum = tk.Label(self, text='Email')
        label_sum.place(x=50, y=110)

         #строка для ввода наименования
        self.entry_name = ttk.Entry(self)
         #меняем координаты объекта
        self.entry_name.place(x=200, y=50)

         #строка для ввода email
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x=200, y=80)

         #строка для ввода телефона
        self.entry_tel = ttk.Entry(self)
        self.entry_tel.place(x=200, y=110)

         #кнопка закрытия дочернего окна
        self.button_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        self.button_cancel.place(x=300, y=170)

         #кнопка добавления
        self.btn_ok = ttk.Button(self, text='Добавить')
        self.btn_ok.place(x=220, y = 170)

        self.btn_ok.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                        self. entry_email.get(), self.entry_tel.get()))

 #класс окна для обновления
class Update(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.view = app
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать позицию')
        bth_edit = ttk.Button(self, text='Редактировать')
        bth_edit.place(x=205, y=170)
        bth_edit.blind('<Button-1>', lambda event: self.view.update_record(self.entry_name.get(), self.entry_email.get(), self.entry_tel.get() ))
       
         #закрывает окно редактирования
         # add='+'позваоляет вешатьна одну кнопку более одного события       
        btn_edit.blind('<Button-1>', lambda event: self.destroy(), add='+')
        self.btn_ok.destroy()

    def default_data(self):
        self.db.c.execute('''SELECT * FROM db WHERE id=?''',(self.view.tree.set(self.view.tree.selection()[0], '#1'),))
        row = self.db.c.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_email.insert(0, row[2])
        self.entry_tel.insert(0, row[3])

 #класс поиска записи
class Search(tk.Toplevel):
    def __init__(self):
        super().__init__()
        self.init_search()
        self.view = app

    def init_search(self):
        self.title('Поиск')
        self.geometry('300x100')
        self.resizable(False, False)

        label_search = tk.Label(self, text='Поиск')
        label_search.place(x=50, y=20)

        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x=105, y=20, width=150)

        btn_cancel = ttk.Button(self, text='Закрыть', command=self.destroy)
        btn_cancel.place(x=185, y=50)

        btn_search = ttk.Button(self, text = 'Поиск')
        btn_search.place(x=105, y50)
        btn_search.bind('<Button-1>', lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1', lambda event: self.destroy(), add='+')

class DB:
    def __init__(self):
         #соединение с БД
        self.conn = sqlite3.connect('db.db')
         #объект класса для взаимодействия с бд
        self.c = self.conn_cursor()
        self.c.execute('''CREATE TABLE IF NOT EXISTS dbd (id integer primary key, name text, tel text, email text)''')
        self.conn.commit()

     #метод добавления в БД
    def insert_data(self, name, tel, email):
        self.c.execute('''INSERT INTO db (name, tel, email) VALUES (?, ?, ?)''', (name, tel, email))
        self.conn.commit()


if __name__ == '__main__':
    root = tk.Tk()
    app = Main(root)
    app.psck()
    #заголовок окна
    root.title('Телефонная книга')
     #размер окна
    root.geometry('665x450')
     #ограничения для измнения размеров окна
    root.resizable(False, False)
    root.mainpool()