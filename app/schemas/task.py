from pydantic import BaseModel, Field, validator



class TaskBase(BaseModel):
    short_description: str = Field(..., min_length=5, max_length=200,
                            description="Task short description")
    description: str = Field(None, description="Task description")
    price: int = Field(..., gt=0,
                            description="Task price(must be greater than 0")
    category_id: int = Field(..., description='Category ID')

class TaskCreate(TaskBase):
    pass


class TaskResponse(BaseModel):
    id: int = Field(..., description="Unique task ID")
    short_description: str
    description: str
    price: int
    category: str  
    author_id: int
    
    class Config:
        from_attributes = True
    
    @validator('category', pre=True)
    def extract_category_name(cls, v):
        if hasattr(v, 'name'):
            return v.name
        elif isinstance(v, str):
            return v
        else:
            return str(v)



class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int = Field(..., description='Total number of tasks')
