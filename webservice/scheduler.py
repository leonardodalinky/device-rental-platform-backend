from .models import User


def schedule() -> None:
    with open('test.log', 'w') as fp:
        fp.write('hh')
