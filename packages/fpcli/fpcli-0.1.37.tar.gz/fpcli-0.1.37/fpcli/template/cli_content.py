from pydoc import classname


def get_views_content(name: str):
    class_name = f"{''.join([text.capitalize() for text in name.split('_')])}View"
    return f'''
from fastapi import Request

class {class_name}:

    async def index(self):
        """Get all the data"""
        
        return " Get all the data."

    async def create(self, request: Request):
        """Create new data based on the request."""
        return f"Create new data based on the request."


    async def edit(self, uuid: str):
        """Read or edit the data based on the given UUID. """
        
        return "Read or edit the data based on the given UUID. "

    async def update(self, request: Request, uuid: str):
        """Update the data based on the given UUID."""
        
        return f"fUpdate the data based on the given UUID."

    async def destroy(self, uuid: str):
        """ Delete the data based on the given UUID."""
        
        return "for delete the data"
        '''


def get_model_content(name: str, app_name: str = "app"):
    class_name = f"{''.join([text.capitalize() for text in name.split('_')])}Model"
    table_name = f"{app_name.lower()}_{name.lower()}"

    return f'''from typing import List
from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .. import BaseModel


class {class_name}(BaseModel):
    \"\"\"
    {class_name} represents the schema for {table_name}.
    \"\"\"

    __tablename__ = "{table_name}"

    name: Mapped[str] = mapped_column(String, nullable=False)

    # Example relationship: adjust or remove as needed
    # related_items: Mapped[List["RelatedModel"]] = relationship(
    #     back_populates="{name.lower()}s", secondary=SomeLinkModel.__table__
    # )
'''


def get_validator_content(name: str):
    class_name = f"{''.join([text.capitalize() for text in name.split('_')])}Schema"
    return f'''
from pydantic import BaseModel, Field
from typing import Optional

class {class_name}(BaseModel):
    """
    {class_name} is used to validate {name} data.
    """
    uuid: Optional[str] = Field(None, description="Unique identifier for the data")
    name: str = Field(..., description="Name field")
    '''


def get_service_content(name: str):
    class_name = f"{''.join([text.capitalize() for text in name.split('_')])}Service"
    model_name = f"{''.join([text.capitalize() for text in name.split('_')])}Model"
    lower_name = name.lower()

    return f'''from typing import List, Optional
from uuid import UUID
from datetime import datetime
from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from ..models.{lower_name}_model import {model_name}


class {class_name}:
    \"\"\"
    {class_name} handles the business logic and database operations for {name.capitalize()}.
    \"\"\"

    @staticmethod
    async def create(data: dict, session: AsyncSession) -> {model_name}:
        """Create a new {name.capitalize()}."""
        instance = {model_name}(**data)
        session.add(instance)
        await session.commit()
        await session.refresh(instance)
        return instance

    @staticmethod
    async def get_all(session: AsyncSession) -> List[{model_name}]:
        """Fetch all active and non-deleted {name.capitalize()}s."""
        statement = select({model_name}).where(
            {model_name}.deleted_at.is_(None), {model_name}.is_active.is_(True)
        )
        result = await session.execute(statement)
        return result.scalars().all()

    @staticmethod
    async def get_by_id(uuid: UUID, session: AsyncSession) -> Optional[{model_name}]:
        """Fetch an active and non-deleted {name.capitalize()} by its UUID."""
        statement = select({model_name}).where(
            {model_name}.id == uuid,
            {model_name}.deleted_at.is_(None),
            {model_name}.is_active.is_(True),
        )
        result = await session.execute(statement)
        return result.scalars().first()

    @staticmethod
    async def update(uuid: UUID, data: dict, session: AsyncSession) -> Optional[{model_name}]:
        """Update an existing {name.capitalize()} if it is active and not deleted."""
        async with session.begin():
            data.pop("id", None)
            statement = (
                update({model_name})
                .where(
                    {model_name}.id == uuid,
                    {model_name}.deleted_at.is_(None),
                    {model_name}.is_active.is_(True),
                )
                .values(**data)
            )
            await session.execute(statement)
        return await {class_name}.get_by_id(uuid, session)

    @staticmethod
    async def delete(uuid: UUID, session: AsyncSession) -> bool:
        """Soft delete a {name.capitalize()} if it is active and not already deleted."""
        instance = await session.get({model_name}, uuid)
        if instance and instance.deleted_at is None and instance.is_active:
            instance.deleted_at = datetime.now()
            await session.commit()
            return True
        return False

    @staticmethod
    async def is_unique(field_value: str, session: AsyncSession) -> bool:
        """Check if a {name.capitalize()} with the same unique field already exists."""
        statement = select({model_name}).where(
            {model_name}.access == field_value,  # Change 'access' as needed
            {model_name}.deleted_at.is_(None)
        )
        result = await session.execute(statement)
        return result.scalars().first() is not None
'''


def get_middleware_content(name: str):
    class_name = f"{''.join([text.capitalize() for text in name.split('_')])}Middleware"

    return f'''
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
import logging

class {class_name}(BaseHTTPMiddleware):
    """
    {class_name} is a custom middleware for processing requests and responses.
    """
    async def dispatch(self, request: Request, call_next):
        """
        Intercept the incoming request, process it, then call the next handler.
        
        Args:
            request (Request): The incoming request.
            call_next (Callable): The function to call the next middleware or route handler.
        
        Returns:
            Response: The final response to be returned.
        """


        # Call the next middleware or route handler
        response = await call_next(request)


        return response
    '''


def get_seeder_content(name: str, app_name: str):
    class_name = f"{''.join([text.capitalize() for text in name.split('_')])}Seeder"
    service_name = f"{''.join([text.capitalize() for text in name.split('_')])}Service"
    return f'''
from ..services.{name.lower()}_service import {service_name}

class {class_name}:
    """
    Seeder for {name.capitalize()}Model to populate initial data.
    """

    @staticmethod
    async def run():
        """
        Run the seeder to insert sample data into the database.
        """
        records = [
            {{
                "name": "{name.capitalize()}1",
               
            }},
            {{
                "name": "{name.capitalize()}2",

            }}
        ]

        # Insert the data into the database using a loop
        for record in records:
            await {service_name}.create(record)

        print(f"{class_name} seed successfully!")
    '''


def get_router_content(name: str):
    model = name.lower()
    Model = "".join([text.capitalize() for text in name.split("_")])
    model_plural = f"{model}s"

    return f'''
from uuid import UUID
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas.{model}_schema import {Model}Schema
from ..utils import error_response, response
from ..services.{model}_service import {Model}Service
from .. import get_db

{model}_router = APIRouter(prefix="/{model_plural}", tags=["{model_plural}"])


@{model}_router.get("", status_code=status.HTTP_200_OK)
async def index(session: AsyncSession = Depends(get_db)):
    """Get all {{model_plural}}"""
    data = await {Model}Service.get_all(session)
    if not data:
        return await error_response(message="Data not found", status_code=404)
    return await response(data=data, message="Data fetched successfully")


@{model}_router.post("", status_code=status.HTTP_201_CREATED)
async def create({model}: {Model}Schema, session: AsyncSession = Depends(get_db)):
    """Create a new {model}"""
    is_unique = await {Model}Service.is_unique({model}.name, session)  # Change `name` to unique field
    if is_unique:
        return await error_response(message="{Model} already exists", status_code=422)
    response_data = await {Model}Service.create({model}.model_dump(), session)
    return await response(data=response_data, message="Data created successfully")


@{model}_router.get("/{"{uuid}"}", status_code=status.HTTP_200_OK)
async def edit(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Get {model} by UUID"""
    data = await {Model}Service.get_by_id(uuid, session)
    if not data:
        return await error_response(message="Data not found", status_code=404)
    return await response(data=data, message="Data fetched successfully")


@{model}_router.put("/{"{uuid}"}", status_code=status.HTTP_200_OK)
async def update({model}: {Model}Schema, uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Update {model} by UUID"""
    data = await {Model}Service.update(uuid, {model}.model_dump(), session)
    return await response(data=data, message="Data updated successfully")


@{model}_router.delete("/{"{uuid}"}", status_code=status.HTTP_204_NO_CONTENT)
async def destroy(uuid: UUID, session: AsyncSession = Depends(get_db)):
    """Delete {model} by UUID"""
    data = await {Model}Service.delete(uuid, session)
    if data:
        return await response(data=data, message="Data deleted successfully")
    else:
        return await error_response(message="Data not found", status_code=404)

'''


def get_test_case_content(name: str):
    from ..fpcli_settings import CONFIG_FOLDER

    return f"""
from fastapi.testclient import TestClient
from {CONFIG_FOLDER.lower()}.main import app  

client = TestClient(app)

async def test_list_{name}(self):
    response = client.get("/{name}s")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

async def test_create_{name}(self):
    response = client.post("/{name}s", json={{"name": "test"}})
    assert response.status_code == 201
    assert response.json()["name"] == "test"

async def test_get_{name}(self):
    response = client.get("/{name}s/1")
    assert response.status_code == 200
    assert response.json()["name"] == "test"

async def test_update_{name}(self):
    response = client.put("/{name}s/1", json={{"name": "updated"}})
    assert response.status_code == 200
    assert response.json()["name"] == "updated"

async def test_delete_{name}(self):
    response = client.delete("/{name}s/1")
    assert response.status_code == 200"""
