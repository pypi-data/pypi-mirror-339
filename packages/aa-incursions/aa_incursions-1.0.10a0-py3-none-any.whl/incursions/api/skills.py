from corptools.models import CharacterAudit, EveItemGroup, EveItemType, Skill
from ninja import NinjaAPI, Schema

from django.http import HttpRequest
from django.shortcuts import get_object_or_404

from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.user import get_all_characters_from_user
from allianceauth.services.hooks import get_extension_logger

from incursions.app_settings import EVECATEGORY_SKILLS
from incursions.models.waitlist import ApprovedSkills

SKILL_GROUP_GUNNERY = 255
SKILL_GROUP_MISSILES = 256
SKILL_GROUP_SPACESHIP_COMMAND = 257
SKILL_GROUP_ARMOR = 1210
SKILL_GROUP_RIGGING = 269
SKILL_GROUP_SHIELDS = 1209
SKILL_GROUP_DRONES = 273
SKILL_GROUP_NEURAL_ENHANCEMENT = 1220

RELEVANT_SKILL_GROUPS = [SKILL_GROUP_ARMOR, SKILL_GROUP_DRONES, SKILL_GROUP_GUNNERY, SKILL_GROUP_MISSILES, SKILL_GROUP_NEURAL_ENHANCEMENT, SKILL_GROUP_RIGGING, SKILL_GROUP_SHIELDS, SKILL_GROUP_SPACESHIP_COMMAND]


class SkillTierSchema(Schema):
    min: int | None
    elite: int | None
    gold: int | None


class SkillsResponse(Schema):
    current: dict[int, int]
    ids: dict[str, int]
    categories: dict[str, list[int]]
    requirements: dict[str, dict[int, SkillTierSchema]]


logger = get_extension_logger(__name__)
api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    SkillsAPIEndpoints(api)


class SkillsAPIEndpoints:

    tags = ["Skills"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/skills/{character_id}", response={200: SkillsResponse, 403: dict}, tags=self.tags)
        def list_skills(request: HttpRequest, character_id: int):
            character = get_object_or_404(EveCharacter.objects.only("pk"), character_id=character_id)

            if not (character in get_all_characters_from_user(request.user) or request.user.has_perm("incursions.waitlist_skills_view")):
                logger.warning(f"User {request.user} denied access to skills for character {character_id}")
                return 403, {"error": "Permission denied"}

            character_audit = get_object_or_404(CharacterAudit.objects.select_related("character"), character=character)
            skills = Skill.objects.filter(character=character_audit, skill_name__group_id__in=RELEVANT_SKILL_GROUPS).select_related("skill_name")

            requirements = {
                shipskills.ship.name: {
                    x.skill.type_id: SkillTierSchema.from_orm(x)
                    for x in shipskills.skill_checks.all()
                }
                for shipskills in ApprovedSkills.objects.select_related("ship").prefetch_related("skill_checks__skill")
            }

            current_skills = {skill.skill_name.type_id: skill.trained_skill_level for skill in skills}
            ids = {skill.name: skill.type_id for skill in EveItemType.objects.filter(group__category_id=EVECATEGORY_SKILLS).only("name", "type_id")}
            categories = {
                group.name: list(EveItemType.objects.filter(group=group).values_list("type_id", flat=True))
                for group in EveItemGroup.objects.filter(group_id__in=RELEVANT_SKILL_GROUPS).only("name")
            }

            logger.info(f"User {request.user} retrieved skills for character {character_id}")
            return SkillsResponse(current=current_skills, ids=ids, categories=categories, requirements=requirements)
