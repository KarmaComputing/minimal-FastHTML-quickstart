from fasthtml.common import (
    fast_app,
    serve,
    Div,
    A,
    Ul,
    Li,
    Titled,
    Card,
    Form,
    Group,
    Input,
    Button,
)


def render(todo):
    tid = f"todo-{todo.id}"
    toggle = A("Toggle", hx_get=f"/toggle/{todo.id}", target_id=tid)
    delete = A("Delete", hx_delete=f"{todo.id}", hx_swap="outerHTML", target_id=tid)

    return Li(toggle, delete, todo.title + (" ✅" if todo.done else " ⏳"), id=tid)


app, rt, todos, Todo = fast_app(
    "todos.db", live=True, render=render, id=int, title=str, done=bool, pk="id"
)


def make_input():
    return Input(
        placeholder="Add new todo", id="title", name="title", hx_swap_oob="true"
    )


@rt("/")
def get():
    form = Form(
        Group(make_input(), Button("Add")),
        hx_post="/",
        hx_swap="beforeend",
        target_id="todo-list",
    )
    return Titled("Todos", Card(Ul(id="todo-list", *todos()), header=form))


@rt("/toggle/{tid}")
def get(tid: int):  # noqa: F811
    todo = todos[tid]
    todo.done = not todo.done
    return todos.update(todo)


@rt("/")
def post(todo: Todo):
    return todos.insert(todo), make_input()


@rt("/{tid}")
def delete(tid: int):
    todos.delete(tid)


serve()
