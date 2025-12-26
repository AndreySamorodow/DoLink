from pydantic import BaseModel, Field



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
    price: float
    category: str

    class Config:   
        from_attributes = True



class TaskListResponse(BaseModel):
    tasks: list[TaskResponse]
    total: int = Field(..., description='Total number of tasks')
