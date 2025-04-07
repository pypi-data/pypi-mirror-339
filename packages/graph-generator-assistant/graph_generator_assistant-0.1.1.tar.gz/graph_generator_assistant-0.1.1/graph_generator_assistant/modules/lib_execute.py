#!/usr/bin/python3

import importlib.util
import os
import tempfile
#temp_dir = tempfile.gettempdir()


def generate_data(  mod_path, # input Path of module
                    img_path  # output image path
                    ):
    module_src_dir  = os.path.dirname(mod_path)    
    module_name     = os.path.splitext(os.path.basename(mod_path))[0]
    
    execute_function_from_string(   module_name, 
                                    module_src_dir, 
                                    img_path)


def execute_function_from_string(module_name, base_path, output_filepath):
    module_path = os.path.join(base_path, f"{module_name}.py")

    # Carrega o módulo dinamicamente
    spec = importlib.util.spec_from_file_location(module_name, module_path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)  # Executa o módulo

    # Obtém a função dinamicamente e executa
    func = getattr(module, module_name)  # Nome da função igual ao nome do módulo
    func(output_filepath=output_filepath)


def save_data(mod_name, mod_str):
    temp_dir = tempfile.gettempdir()
    mod_path = os.path.join(temp_dir, mod_name + ".py")
    img_path = os.path.join(temp_dir, mod_name + ".png")

    with open(mod_path, "w", encoding="utf-8") as arquivo:
        arquivo.write(mod_str)

    generate_data(mod_path, img_path)

    return mod_path, img_path
    
if __name__ == '__main__':
    # Exemplo de uso
    generate_data("../templates/workflow_diagram1.py","salida.pdf")
    #execute_function_from_string("workflow_diagram1", "../templates","salida.pdf")

