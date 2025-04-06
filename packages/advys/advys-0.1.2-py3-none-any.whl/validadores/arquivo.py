from pydantic import BaseModel, FilePath

class Arquivo(BaseModel):
    caminho: FilePath
