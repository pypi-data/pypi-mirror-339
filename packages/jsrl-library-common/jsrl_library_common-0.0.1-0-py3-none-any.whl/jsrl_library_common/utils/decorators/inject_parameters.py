import types 
from functools import wraps

def parameters_injection_decorator(*inject_args, **inject_kwargs):
    """Inject in invokation function the required parameters

    Args:
        - inject_args (tuple|list): the args to inject
        - inject_kwargs (dict): the kwargs to inject
    """

    def decorator(func):

        def __extract_needed_resources(resources,
                                       apply_func):
            """Return the resources that apply function define

            Args:
                - resources (dict): param with resources data
                - apply_func (function): function which extract needed resources
            
            Return:
                - dict: the function needed resources
            """
            ans = { k:resources[k] for k in apply_func.__code__.co_varnames if resources.get(k) != None }
            return ans
        

        def __adjust_args_to_class_method(additional_params,
                                            args):
            """Organize dependencies in class method or normal function

            Args:
                - additional_params (list|tuple): the arguments to add
                - args (list|tuple): the function arguments

            Returns:
                - tuple: adjust arguments
            """
            if func.__qualname__ != func.__name__ \
                and len(args) > 0 \
                and func.__qualname__.startswith(args[0].__class__.__name__):
                self, *args = args
                additional_params = (self, *additional_params)

            args = (*additional_params, *args)
            return args


        @wraps(func)
        def wrapper(*args, **kwargs):
            
            exec_func = func
            
            if isinstance(func, types.FunctionType):
                args = __adjust_args_to_class_method(inject_args, args)
            elif isinstance(func, staticmethod):
                exec_func = func.__func__
                args = (*inject_args, *args)

            kwargs = {**__extract_needed_resources(inject_kwargs, exec_func), **kwargs}
            return exec_func(*args, **kwargs)
            
        return wrapper
    
    return decorator
