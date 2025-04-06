

from typing import List
from typing import Dict
from typing import Optional
from fastapi import APIRouter
from fastapi import Depends

from tendril.authn.users import auth_spec
from tendril.authn.users import authn_dependency
from tendril.authn.users import AuthUserModel

from tendril.libraries import interests
from tendril.interests import type_spec
from tendril.interests import interest_stub_tmodel
from tendril.interests import possible_parents
from tendril.interests import possible_ancestors
from tendril.interests import possible_paths
from tendril.common.states import LifecycleStatus

from tendril.db.controllers.interests import get_interest
from tendril.common.interests.representations import ExportLevel
from tendril.common.interests.representations import rewrap_interest
from tendril.common.interests.representations import get_interest_stub

from tendril.common.interests.memberships import user_memberships
from tendril.common.interests.memberships import UserMembershipsTModel

from tendril.config import INTERESTS_API_ENABLED

from tendril.utils.db import get_session
from tendril.utils import log
logger = log.get_logger(__name__)


interests_router = APIRouter(prefix='/interests',
                             tags=["Common Interests API"],
                             dependencies=[Depends(authn_dependency),
                                           auth_spec(scopes=['interests:common'])]
                             )


@interests_router.get("/libraries", response_model=Dict[str, str])
async def get_interest_libraries():
    return interests.libraries_and_types


@interests_router.get("/types")
async def get_interest_types():
    return type_spec


@interests_router.get("/possible_parents", response_model=Dict[str, List[str]])
async def get_possible_parents():
    return possible_parents


@interests_router.get("/possible_ancestors", response_model=Dict[str, List[str]])
async def get_possible_ancestors():
    return possible_ancestors


@interests_router.get("/possible_paths", response_model=Dict[str, List[List[str]]])
async def get_possible_paths():
    return possible_paths


@interests_router.get("/{id}/stub", response_model=interest_stub_tmodel)
async def interest_stubs(id: int,
                         user: AuthUserModel = auth_spec()):
    with get_session() as session:
        interest = get_interest(id=id, session=session)
        interest = rewrap_interest(interest)

        # We can't expect the user to have permissions on the interest, for
        # instance when looking at platform information from the content
        # interest's perspective for approvals. The stub will have to be
        # treated as public (any logged in user).
        # interest.export(auth_user=user, probe_only=True, session=session)
        return interest.export(export_level=ExportLevel.STUB, session=session)


@interests_router.get("/by_name/{name}/stub", response_model=interest_stub_tmodel)
async def interest_stub_by_name(name: str,
                                user: AuthUserModel = auth_spec()):
    with get_session() as session:
        interest = get_interest(name=name, session=session)
        interest = rewrap_interest(interest)

        # We can't expect the user to have permissions on the interest, for
        # instance when looking at platform information from the content
        # interest's perspective for approvals. The stub will have to be
        # treated as public (any logged in user).
        # interest.export(auth_user=user, probe_only=True, session=session)
        return interest.export(export_level=ExportLevel.STUB, session=session)



@interests_router.post("/memberships", response_model=UserMembershipsTModel)
async def get_user_memberships(user: AuthUserModel = auth_spec(),
                               include_delegated: bool = False,
                               include_inherited: bool = False,
                               interest_types: Optional[List[str]] = [],
                               statuses:Optional[List[LifecycleStatus]] = [],
                               roles:Optional[List[str]] = []):
    kwargs = {}
    if interest_types:
        kwargs['interest_types'] = interest_types
    if statuses:
        kwargs['include_statuses'] = [x.value for x in statuses]
    if roles:
        kwargs['include_roles'] = roles
    return user_memberships(user,
                            include_delegated=include_delegated,
                            include_inherited=include_inherited,
                            **kwargs).render()


@interests_router.get("/name_available", response_model=bool)
async def check_name_available(name: str):
    return interests.name_available(name)


def _generate_routers():
    interest_routers = []
    for libname in interests.libraries:
        ilib = getattr(interests, libname)
        api_generators = ilib.api_generators()
        for generator in api_generators:
            generated_routers = generator.generate(f'{libname}')
            interest_routers.extend(generated_routers)
    return interest_routers


if INTERESTS_API_ENABLED:
    routers = [
        interests_router
    ] + _generate_routers()
else:
    logger.info("Not creating Interest API routers.")
    routers = []
