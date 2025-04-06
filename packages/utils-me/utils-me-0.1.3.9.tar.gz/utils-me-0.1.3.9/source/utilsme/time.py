import time


def __duration__(start_time: float, end_time: float):
    
    result = (end_time - start_time) / (60 * 60)
    hour = int(result)
    
    result = (result - hour) * 60
    minute = int(result)
    
    result = (result - minute) * 60
    seconde = round(result, 3)
    
    result = []
    if hour>0:
        result.append(f"{hour}h ")
    if minute>0:
        result.append(f"{minute}min ")
    result.append(f"{seconde}s.")
    print(f"Timing :\n\t{''.join(result)}")

def timing(fun):
    
    def wrapper(*args, **kwargs):
        start = time.time()
        
        result =  fun(*args, **kwargs)
        
        __duration__(start, time.time())
        
        return result
    return wrapper


