#!/usr/bin/python3
"""HBNB console"""
import cmd
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.place import Place
from models.state import State
from models.city import City
from models.amenity import Amenity
from models.review import Review
import shlex

classes = {
    'BaseModel': BaseModel,
    'User': User,
    'Place': Place,
    'State': State,
    'City': City,
    'Amenity': Amenity,
    'Review': Review
}

class HBNBCommand(cmd.Cmd):
    """HBNB command interpreter"""
    prompt = '(hbnb) '

    def do_quit(self, arg):
        """Quit command to exit the program"""
        return True

    def do_EOF(self, arg):
        """EOF command to exit the program"""
        print()
        return True

    def emptyline(self):
        """Empty line"""
        pass

    def do_create(self, arg):
        """Create a new instance"""
        args = shlex.split(arg)
        if not args:
            print("** class name missing **")
            return
        if args[0] not in classes:
            print("** class doesn't exist **")
            return

        new_dict = {}
        for param in args[1:]:
            key_value = param.split('=')
            if len(key_value) != 2:
                continue
            key = key_value[0]
            value = key_value[1]

            if value.startswith('"') and value.endswith('"'):
                value = value[1:-1].replace('_', ' ')
            elif '.' in value:
                try:
                    value = float(value)
                except:
                    continue
            else:
               try:
                   value = int(value)
               except:
                   continue
            new_dict[key] = value

        new_instance = classes[args[0]](**new_dict)
        new_instance.save()
        print(new_instance.id)

def do_show(self, arg):
    """Show an instance based on the class name and id."""
    if not arg:
        print("** class name missing **")
        return
    try:
        class_name, params = arg.split(" ", 1)
    except ValueError:
        class_name, params = arg, ""

    if class_name not in self.classes:
        print("** class doesn't exist **")
        return

    def do_destroy(self, arg):
       """Delete instance"""
       args = shlex.split(arg)
       if not args:
           print("** class name missing **")
           return
       if args[0] not in classes:
           print("** class doesn't exist **")
           return
       if len(args) < 2:
           print("** instance id missing **")
           return
       key = f"{args[0]}.{args[1]}"
       if key not in storage.all():
           print("** no instance found **")
           return
       del storage.all()[key]
       storage.save()

    def do_all(self, arg):
       """Show all instances"""
       args = shlex.split(arg)
       obj_list = []
       if not args:
           for obj in storage.all().values():
               obj_list.append(str(obj))
       elif args[0] in classes:
           for key, obj in storage.all().items():
               if key.split('.')[0] == args[0]:
                   obj_list.append(str(obj))
       else:
           print("** class doesn't exist **")
           return
       print(obj_list)

    def do_update(self, arg):
       """Update instance attributes"""
       args = shlex.split(arg)
       if not args:
           print("** class name missing **")
           return
       if args[0] not in classes:
           print("** class doesn't exist **")
           return
       if len(args) < 2:
           print("** instance id missing **")
           return
       key = f"{args[0]}.{args[1]}"
       if key not in storage.all():
           print("** no instance found **")
           return
       if len(args) < 3:
           print("** attribute name missing **")
           return
       if len(args) < 4:
           print("** value missing **")
           return
       
       obj = storage.all()[key]
       attr_name = args[2]
       attr_value = args[3]
       
       try:
           attr_value = eval(attr_value)
       except:
           pass
           
       setattr(obj, attr_name, attr_value)
       obj.save()

    def default(self, arg):
       """Handle class method calls"""
       args = arg.split('.')
       if len(args) != 2:
           print("*** Unknown syntax:", arg)
           return
           
       class_name = args[0]
       if class_name not in classes:
           print("** class doesn't exist **")
           return
           
       command = args[1].split('(')
       if len(command) != 2:
           print("*** Unknown syntax:", arg)
           return
           
       method_name = command[0]
       params = command[1].rstrip(')')
       
       if method_name == 'all':
           self.do_all(class_name)
       elif method_name == 'count':
           print(len([obj for obj in storage.all().values() 
                     if obj.__class__.__name__ == class_name]))
       elif method_name == 'show':
           self.do_show(f"{class_name} {params.strip('\"')}")
       elif method_name == 'destroy':
           self.do_destroy(f"{class_name} {params.strip('\"')}")
       elif method_name == 'update':
           params = params.split(',')
           if len(params) < 2:
               print("*** Unknown syntax:", arg)
               return
           instance_id = params[0].strip().strip('"')
           if len(params) == 2:  # Update with dictionary
               try:
                   update_dict = eval(params[1])
                   if not isinstance(update_dict, dict):
                       raise ValueError
                   for key, value in update_dict.items():
                       self.do_update(f"{class_name} {instance_id} {key} {value}")
               except:
                   print("*** Unknown syntax:", arg)
           else:  # Normal update
               attr_name = params[1].strip().strip('"')
               attr_value = params[2].strip().strip('"')
               self.do_update(f"{class_name} {instance_id} {attr_name} {attr_value}")
       else:
           print("*** Unknown syntax:", arg)
           
if __name__ == '__main__':
   HBNBCommand().cmdloop()