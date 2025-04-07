# jfr_1/modules.py

# Store algorithms in a list
algorithms = []

def register_algorithm(name, function, description):
    """Register a new algorithm."""
    algorithms.append({
        'name': name,
        'function': function,
        'description': description
    })

def list_algorithms():
    """List all registered algorithms."""
    return [algo['name'] for algo in algorithms]

def get_algorithm(name):
    """Retrieve an algorithm by name."""
    for algo in algorithms:
        if algo['name'] == name:
            return algo
    raise ValueError(f"Algorithm '{name}' not found.")

