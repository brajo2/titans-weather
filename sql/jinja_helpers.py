from copy import deepcopy
from six import string_types
from jinja2 import meta
from jinjasql import JinjaSql

"""
jinja helpers that I commonly use with my projects
"""

def quote_sql_string(value):
    '''
    If `value` is a string type, escapes single quotes in the string
    and returns the string enclosed in single quotes.
    '''
    if isinstance(value, string_types):
        new_value = str(value)
        new_value = new_value.replace("'", "''")
        return "'{}'".format(new_value)
    return value


def get_sql_from_template(query, bind_params):
    '''
    Given a query and binding parameters produced by JinjaSql's prepare_query(),
    produce and return a complete SQL query string.
    '''
    if not bind_params:
        return query
    params = deepcopy(bind_params)
    for key, val in params.items():
        # print('val', val)
        params[key] = val if not isinstance(val, list) else [quote_sql_string(v) for v in val]
    return query % params


def apply_sql_template(template,
                       parameters,
                       j = JinjaSql(param_style='pyformat'),
                       func_list=None):
    '''
    Apply a JinjaSql template (string) substituting parameters (dict) and return
    the final SQL. Use the func_list to pass any functions called from the template.
    '''
    if func_list:
        for func in func_list:
            j.env.globals[func.__name__] = func
    query, bind_params = j.prepare_query(template, parameters)
    return get_sql_from_template(query, bind_params)


def generate_templated_sql(sql_template,
                           jsql: JinjaSql = JinjaSql(param_style='pyformat'),
                           **kwargs):
    '''
    Generate SQL from a template and parameters.
    '''
    undeclared_variables = meta.find_undeclared_variables(jsql.env.parse(sql_template))
    missing_variables = [template_var for template_var in undeclared_variables if template_var not in kwargs.keys()]
    if missing_variables:
        raise ValueError(
            # f-string for value error declaring missing variables, kwargs, undeclared_variables
            f"""Missing variables in template: {missing_variables}.
            Template variables: {undeclared_variables}.
            Parameters: {kwargs}."""
        )
    return apply_sql_template(sql_template, kwargs, j=jsql)