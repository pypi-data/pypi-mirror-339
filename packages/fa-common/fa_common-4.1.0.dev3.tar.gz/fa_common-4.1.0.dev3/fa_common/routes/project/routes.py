import asyncio
from typing import Annotated, Optional

from aiosqlite.core import LOG
from bson import ObjectId
from fastapi import APIRouter, Depends, Query

from fa_common.auth.utils import get_admin_scope
from fa_common.exceptions import NotFoundError, UnauthorizedError
from fa_common.models import Message, PaginationListResponse
from fa_common.routes.user.models import UserDB
from fa_common.routes.user.service import get_current_app_user
from fa_common.utils import validate_id

from . import service
from .models import CreateProject, ProjectDB, ProjectItem, UpdateProject

router = APIRouter()


@router.get("", response_model=PaginationListResponse[ProjectDB] | PaginationListResponse[ProjectItem])
async def list_projects(
    only_mine: bool = True,
    offset: int = 0,
    limit: int = 10,
    search: Optional[str] = None,
    tag: Optional[str] = Query(None, description="Filter by exact tag match (case insensitive)"),
    sort: Annotated[
        list[str], Query(description="The list of fields to sort the projects by using the syntax `['+fieldName', '-secondField']`.")
    ] = [],
    current_user: UserDB = Depends(get_current_app_user),
    as_items: bool = Query(False, description="If True, return a list of ProjectItem instead of ProjectDB."),  # type: ignore
) -> PaginationListResponse[ProjectDB] | PaginationListResponse[ProjectItem]:
    """
    List projects based on the provided filters.

    Parameters
    ----------
    only_mine : bool, optional
        If True, only return projects owned by the current user. If False, return all projects the user has access to. Default is True.
    offset : int, optional
        The number of projects to skip before starting to return results. Default is 0.
    limit : int, optional
        The maximum number of projects to return. Default is 10.
    search : str, optional
        Search string to filter projects by name or tags. Default is None.
    tag : str, optional
        Filter by exact tag match. This is case insensitive and matches against both tags and system_tags. Default is None.
    sort : list[str], optional
        The list of fields to sort the projects by using the syntax `['+fieldName', '-secondField']`.
        See https://beanie-odm.dev/tutorial/finding-documents/
        Default is an empty list.
    current_user : UserDB, optional
        The current authenticated user. Default is obtained using the `get_current_app_user` dependency.
    as_items : bool, optional
        If True, return a list of ProjectItem objects (with owner information) instead of ProjectDB objects. Default is False.

    Returns
    -------
    PaginationListResponse[ProjectDB] | PaginationListResponse[ProjectItem]
        A paginated list of projects that match the provided filters.
    """
    projects, total = await service.get_projects_for_user(
        user=current_user, owner_only=only_mine, offset=offset, limit=limit, sort=sort, search=search, tag=tag
    )

    try:
        if as_items:
            project_items = await asyncio.gather(*[proj.to_project_item() for proj in projects])
            return PaginationListResponse[ProjectItem](total=total, values=project_items, limit=limit, offset=offset)
    except Exception as e:
        LOG.error(f"Error converting projects to ProjectItem: {e}")
    return PaginationListResponse[ProjectDB](total=total, values=projects, limit=limit, offset=offset)


@router.put("", response_model=ProjectDB, response_model_exclude=ProjectDB._api_out_exclude())
async def create_project(
    project: CreateProject,
    current_user: UserDB = Depends(get_current_app_user),
) -> ProjectDB:
    new_project = await service.create_project(current_user, project.model_dump())

    return new_project


@router.patch("/{project_id}", response_model=ProjectDB, response_model_exclude=ProjectDB._api_out_exclude())
async def update_project(
    project_id: str,
    project_update: UpdateProject,
    current_user: UserDB = Depends(get_current_app_user),
) -> ProjectDB:
    project = await ProjectDB.find_one(ProjectDB.id == ObjectId(project_id))

    if project is None:
        raise NotFoundError(f"Project {project_id} not found.")

    if project.user_id != current_user.sub and current_user.sub not in project.project_users:
        raise UnauthorizedError("You do not have access to this project.")

    updated_project = await service.update_project(project, project_update)

    return updated_project


@router.get("/{project_id}", response_model=ProjectDB, response_model_exclude=ProjectDB._api_out_exclude())  # type: ignore
async def get_project(
    project_id: str,
    current_user: UserDB = Depends(get_current_app_user),
) -> ProjectDB:
    """Gets a project given the project_name."""
    _project_id = validate_id(project_id)

    project = await ProjectDB.find_one(ProjectDB.id == _project_id)

    if project is None:
        raise NotFoundError(f"Project {project_id} not found.")

    if get_admin_scope() in current_user.roles:
        return project

    if await project.user_has_access(current_user):
        return project

    raise UnauthorizedError("You do not have access to this project.")


@router.delete("/{project_id}", response_model=Message)
async def delete_project(
    project_id: str,
    current_user: UserDB = Depends(get_current_app_user),
) -> Message:
    """Deletes a project given the project_name."""
    proj_id = ObjectId(project_id)
    user_sub = None
    if get_admin_scope() not in current_user.scopes:
        user_sub = current_user.sub

    delete_outcome = await service.delete(project_id=proj_id, user_sub=user_sub)

    if delete_outcome is False:
        raise NotFoundError()

    return Message(message=f"Deleted project {project_id}.")
