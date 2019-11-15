#! /usr/bin/python
# -*- coding: utf-8 -*-

from pyomo.environ import *
import pandas as pd


def model_construct():
    main_model = ConcreteModel()
    return main_model


def set_list(main_model):

    return main_model


def var_list(main_model):

    return main_model


def param_list(main_model):

    return main_model


def con_list(main_model):

    return main_model


def obj_list(main_model):

    return main_model


if __name__ == '__main__':
    main_model = model_construct()
    main_model = set_list(main_model)
    main_model = var_list(main_model)
    main_model = con_list(main_model)
    main_model = obj_list(main_model)
    opt = SolverFactory('cplex', solver_io='nl')
    opt.options['timelimit'] = 180
    opt.options['thread'] = 16
    opt.solve(main_model, tee=True, warmstart=True)
