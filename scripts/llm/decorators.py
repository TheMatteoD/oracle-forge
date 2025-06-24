from functools import wraps
import inspect

def add_narration(narration_func):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            flavor = kwargs.pop('flavor', False)
            
            # Get the arguments of the original function (e.g., 'question')
            original_func_args = inspect.signature(func).parameters
            
            # Create a dictionary of the arguments passed to the wrapper
            provided_args = {}
            for i, arg_name in enumerate(original_func_args):
                if i < len(args):
                    provided_args[arg_name] = args[i]
            provided_args.update(kwargs)

            result = func(*args, **kwargs)

            if flavor:
                narration_args = {}
                narration_params = inspect.signature(narration_func).parameters

                # Pass the entire result dictionary if it's expected
                if 'result' in narration_params:
                    narration_args['result'] = result
                elif 'meaning' in narration_params:
                    narration_args['meaning'] = result

                # Pass any of the original function's arguments if the narration function expects them
                for param in narration_params:
                    if param in provided_args:
                        narration_args[param] = provided_args[param]
                
                # Also check the keys in the result dictionary
                if isinstance(result, dict):
                    for param in narration_params:
                        if param in result:
                            narration_args[param] = result[param]


                result['narration'] = narration_func(**narration_args)

            return result
        return wrapper
    return decorator 