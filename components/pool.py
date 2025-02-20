""" POOL SYSTEM FOR OBJECTS THAT ARE CONSTANTLY ADDED/REMOVED, FOR BETTER PERFORMANCE AND MANAGEMENT """
from assets import init_loading

class Pool:
    def __init__(self, class_type, class_config, amount):
        self.pool = []

        # Adding a predetermined amount of hazzards into the pool
        for index in range(amount):
            init_loading('creating ' + class_config['type'] + ' storage', 1)
            self.pool.append(class_type(class_config, index))

        self.class_type = class_type
        self.class_config = class_config

    # Returns an avaliable object from the pool
    def get(self):
        for obj in self.pool:
            if not obj.alive:
                obj.reset()
                return obj

        # If object is avaliable, create a new one and add it into the pool
        new_obj = self.class_type(self.class_config, len(self.pool) + 1)
        self.pool.append(new_obj)
        return new_obj