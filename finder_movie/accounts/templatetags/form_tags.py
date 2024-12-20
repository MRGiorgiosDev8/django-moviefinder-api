from django import template

register = template.Library()

@register.filter(name='add_class')
def add_class(field, css_class):
    """
    Фильтр для добавления CSS класса к полю формы.

    Аргументы:
    field -- поле формы, к которому нужно добавить класс
    css_class -- CSS класс, который нужно добавить

    Возвращает:
    Поле формы с добавленным CSS классом.
    """
    return field.as_widget(attrs={"class": css_class})