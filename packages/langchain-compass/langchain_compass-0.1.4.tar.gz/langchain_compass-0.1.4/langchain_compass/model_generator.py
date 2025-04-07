from datamodel_code_generator import InputFileType, generate
from datamodel_code_generator.model import PythonVersion
from typing import Any

from pathlib import Path
import tempfile
from pydantic import BaseModel, Field
# # Read the OpenAPI JSON file
# with open('../openapi.json', 'r', encoding='utf-8') as f:
#     openapi_content = f.read()


from datamodel_code_generator import DataModelType, OpenAPIScope

def models_from_openapi(openapi_content: str, path: Any) -> dict[Any]:
    # tmp_file = tempfile.NamedTemporaryFile(delete=False)
    # path = Path(tmp_file.name)

    # Generate Python code (as a string)
    _ = generate(
        input_=openapi_content,
        output=path,
        additional_imports=["numpy"],
        output_model_type=DataModelType.PydanticV2BaseModel,
        input_file_type=InputFileType.OpenAPI,
        openapi_scopes=[OpenAPIScope.Schemas],
        target_python_version=PythonVersion.PY_311,  # Change to your Python version
    )

    return None
    #
    # # Debug: print(generated_code) to see what's being generated
    #
    # # Prepare a namespace to store generated classes
    # local_namespace = {}
    # from pydantic import BaseModel, Field, ConfigDict
    # with open('temp_modelgenerator_in_python.py','w') as f:
    #     f.write(open(path,'r').read())
    # exec(open(path,'r').read(), globals(), local_namespace)
    #
    #
    #
    # return local_namespace