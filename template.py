import os
from pathlib import Path

project_name="sensor"

list_of_files=[

    f'{project_name}/__init__.py',
    f'{project_name}/Components/__init__.py',
     f'{project_name}/Components/data_ingestion.py',
       f'{project_name}/Components/data_transformation.py',
        f'{project_name}/Components/model_evaluation.py',
         f'{project_name}/Components/model_trainer.py',
          f'{project_name}/Components/model_pusher.py',

           f'{project_name}/Configuration/__init__.py',
           f'{project_name}/Constants/__init__.py',
           
           f'{project_name}/entity/__init__.py',
           f'{project_name}/entity/artifact_entity.py',
           f'{project_name}/entity/config_entity.py',

           f'{project_name}/Exception/__init__.py',
           f'{project_name}/logger/__init__.py',

           f'{project_name}/pipeline/__init__.py',
           f'{project_name}/pipeline/prediction_pipeline.py',
           f'{project_name}/pipeline/training_pipeline.py',

           f'{project_name}/utils/__init__.py',
           f'{project_name}/utils/main_utils.py',
           f'{project_name}/utils/__init__.py',

           "app.py",
           "requirements.txt",
           "Dockerfile",
           ".dockerignore",
           "demo.py",
           "setup.py",
           "config/model.yaml",
           "config/schema.yaml"

]

for filepath in list_of_files:
    filepath=Path(filepath)# find info about type of os
    filedir,filename=os.path.split(filepath)#seperate folder and file

    if filedir != "":
        os.makedirs(filedir,exist_ok=True)#create folder
    if (not os.path.exists(filepath)) or(os.path.getsize(filepath)) :
        with open(filepath,"w") as f: #create file inside folder
            pass 
    else:
        print(f"{filepath} already exists")     


    
