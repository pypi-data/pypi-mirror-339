import time
import threading
import contextvars
import random
from asteval import Interpreter
from concurrent.futures import ThreadPoolExecutor

# Sample evaluation response (string-based values)
evaluation_response = {
    "status": "success",
    "message": "operation completed",
    "priority": "high",
}

def generate_dict():
    return {
        "status": random.choice(["success", "failure"]),
        "message": random.choice(["operation completed", "error occurred"]),
        "priority": random.choice(["high", "medium", "low"]),
    }

# Expression to evaluate (boolean check)
criteria = "status == 'success' and priority == 'high'"

# Large-scale iterations for realistic testing
ITERATIONS = 1000000
THREADS = 20

# Approach 1: Per-call instantiation
def evaluate_per_call(_):
    interpreter = Interpreter()
    interpreter.symtable.update(generate_dict())
    return interpreter(criteria)

# Approach 2: Thread-local storage using contextvars
interpreter_var = contextvars.ContextVar("interpreter", default=None)

def get_context_safe_interpreter():
    interpreter = interpreter_var.get()
    if interpreter is None:
        interpreter = Interpreter()
        interpreter_var.set(interpreter)
    return interpreter

def evaluate_contextvars(_):
    interpreter = get_context_safe_interpreter()
    interpreter.symtable.clear()
    interpreter.symtable.update(generate_dict())
    return interpreter(criteria)

# Approach 3: Shared instance with a lock
shared_interpreter = Interpreter()
lock = threading.Lock()

def evaluate_with_lock(_):
    with lock:
        shared_interpreter.symtable.clear()
        shared_interpreter.symtable.update(generate_dict())
        return shared_interpreter(criteria)

# Benchmarking function
def benchmark(func, iterations=ITERATIONS, threads=THREADS):
    start = time.time()
    with ThreadPoolExecutor(max_workers=threads) as executor:
        list(executor.map(func, range(iterations)))  # Pass dummy argument
    return time.time() - start

# Run benchmarks
time_per_call = benchmark(evaluate_per_call)
time_contextvars = benchmark(evaluate_contextvars)
time_with_lock = benchmark(evaluate_with_lock)

# Print results
print(f"Per-call instantiation: {time_per_call:.4f} seconds")
print(f"Thread-local (contextvars): {time_contextvars:.4f} seconds")
print(f"Shared instance with lock: {time_with_lock:.4f} seconds")
