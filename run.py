from core.controller import Controller
from core.model import Model
from core.view import View

if __name__ == '__main__':
    model = Model(50, 50)
    view = View(model)
    ctrl = Controller(view, model)
    view.set_controller(ctrl)
    ctrl.start()

