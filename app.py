
import flet as ft
import sqlite3

def sql_query(query,update=False):
    connection = sqlite3.connect('Database.db')
    cursor = connection.cursor()
    cursor.execute(query)
    connection.commit()
    return cursor.fetchall()

def main(page: ft.Page):
    page.title = "Справочник"
    print("Initial route:", page.route)

    sql_login = "Select name from Users"
    logins = sql_query(sql_login)
    print(logins)

    login = ft.TextField(label="Логин") #ft.Dropdown(label="Логин", options=[ft.dropdown.Option (','.join(row)) for row in logins])
    password = ft.TextField(label="Пароль")


    page.update()

    def route_change(e):
        page.views.clear()
        page.views.append(
            ft.View(
                "/",
                [
                    ft.AppBar(title=ft.Text("Вход в аккаунт")),
                    login, password,
                    ft.Row([ft.Container(content=ft.ElevatedButton("Выйти", on_click= lambda _:page.window.close())),
                    ft.Container(content=ft.ElevatedButton("Войти", on_click=lambda _: page.go("/main"))),
                    ft.Container(content= ft.ElevatedButton("Создать пользователя", on_click=lambda _: page.go("/registation"))),
                          ] )

                 ],
             )
         )
        if page.route == "/main":
            select_sql = sql_query("SELECT Educationals.name, Educationals.full_name, work_time.work_time, Contacts.contact FROM Educationals INNER JOIN work_time ON work_time.id = Educationals.work_time INNER JOIN Contacts ON Contacts.id = Educationals.contact ")
            page.views.append(
                ft.View(
                    "/main",
                    [
                        ft.AppBar(title=ft.Text("Справочник"),actions=[
                                  ft.IconButton(ft.Icons.ADD,  on_click=lambda _: page.go("/add")),
                              ] ),
                        ft.Container(content= ft.Column([ft.Row([ft.DataTable(
                            vertical_lines=ft.BorderSide(3, "blue"),
                            horizontal_lines=ft.BorderSide(1, "green"),
                            #column_spacing=100,
                            #data_row_max_height=150,
                            columns=[
                                ft.DataColumn(ft.Text("Название учреждения")),
                                ft.DataColumn(ft.Text("Полное наименование")),
                                ft.DataColumn(ft.Text("Время работы")),
                                ft.DataColumn(ft.Text("Контакты")),
                            ],
                            rows=[

                                ft.DataRow(
                                    cells=[
                                        ft.DataCell(ft.Text(select[0])),
                                        ft.DataCell(ft.Text(select[1])),
                                        ft.DataCell(ft.Text(select[2])),
                                        ft.DataCell(ft.Text(select[3])),
                                    ],
                                )
                                for select in select_sql
                            ],
                        )], scroll=ft.ScrollMode.ALWAYS)],
                            scroll=ft.ScrollMode.ALWAYS), expand=2),
                    ]))

        page.update()
        if page.route == "/registation":

            page.views.append(
                ft.View(
                    "/registation",
                    [
                        ft.AppBar(title=ft.Text("Регистрация")),
                        ft.TextField(label="Логин"),
                        ft.TextField(label="Новый пароль"),
                        ft.TextField(label="Повтор пароля"),
                        ft.TextField(label="E-mail"),
                        ft.TextField(label="Телефон"),
                        ft.AppBar(title=ft.Text("Регистрация")),
                        ft.Row([ft.Container(content=ft.ElevatedButton("Назад", on_click=lambda _: page.go("/"))),
                        ft.Container(content=ft.ElevatedButton("Создать пользователя", on_click=lambda _: page.go("/"))),
                                ] )
                    ],
                )
            )
        page.update()
        if page.route == "/add":
            dd=ft.Dropdown(
                            label="Тип",
                            options=[
                                ft.dropdown.Option("СОШ"),
                                ft.dropdown.Option("СПО"),
                                ft.dropdown.Option("ВУЗ"),
                                ft.dropdown.Option("СПО и ВУЗ"),
                            ],
                            autofocus=True,
                        )
            page.views.append(
                ft.View(
                    "/add",
                    [
                        ft.AppBar(title=ft.Text("Создать новое учебное учреждение")),
                        ft.TextField(label="Полное наименование"),
                        ft.TextField(label="Описание"),
                        dd,
                        ft.TextField(label="Время работы"),
                        ft.TextField(label="Контакты"),
                       ft.Row([ft.Container(content=ft.ElevatedButton("Назад", on_click=lambda _: page.go("/main"))),
                        ft.Container(content=ft.ElevatedButton("Создать новое учебное учреждение", on_click=lambda _: page.go("/main"))),

                                ] )
                    ],
                )
            )
        page.update()


    def view_pop(e):
        print("View pop:", e.view)
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)


    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)


ft.app(target=main) #, view=ft.WEB_BROWSER)

