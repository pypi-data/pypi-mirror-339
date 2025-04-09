from ninja import NinjaAPI, Schema

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils.timezone import now

from allianceauth.eveonline.models import EveCharacter
from allianceauth.framework.api.evecharacter import get_user_from_evecharacter
from allianceauth.framework.api.user import get_all_characters_from_user
from allianceauth.services.hooks import get_extension_logger

from incursions.api.bans import PublicBanSchema
from incursions.api.schema import CharacterSchema
from incursions.models.waitlist import Ban, CharacterBadges, CharacterRoles


class CharacterAndLevelSchema(Schema):
    character: CharacterSchema
    tags: list[str] | None
    active_bans: list[PublicBanSchema] | None


logger = get_extension_logger(__name__)
api = NinjaAPI()


def setup(api: NinjaAPI) -> None:
    PilotAPIEndpoints(api)


class PilotAPIEndpoints:

    tags = ["Pilot"]

    def __init__(self, api: NinjaAPI) -> None:

        @api.get("/pilot/info", response={200: CharacterAndLevelSchema, 403: dict}, tags=self.tags)
        def pilot_info(request, character_id: int):
            character = get_object_or_404(EveCharacter.objects.only("pk"), character_id=character_id)

            if not (character in get_all_characters_from_user(request.user) or request.user.has_perm("incursions.waitlist_pilot_view")):
                logger.warning(f"User {request.user} denied access to pilot info for character {character_id}")
                return 403, {"error": "Permission denied"}

            character = get_object_or_404(EveCharacter.objects.only("pk", "character_id", "character_name"), character_id=character_id)

            badge_tags = CharacterBadges.objects.filter(character__pk=character.pk).values_list("badge__name", flat=True)
            role_tags = CharacterRoles.objects.filter(character__pk=character.pk).values_list("role__name", flat=True)
            bans = Ban.objects.filter(Q(revoked_at__isnull=True) | Q(revoked_at__gt=now()), entity_character_id=character.pk)

            logger.info(f"User {request.user} fetched pilot info for character {character_id}")
            return CharacterAndLevelSchema(
                character=CharacterSchema.from_orm(character),
                tags=list(badge_tags) + list(role_tags),
                active_bans=[PublicBanSchema.from_orm(ban) for ban in bans]
            )

        @api.get("/pilot/alts", response={200: list[CharacterSchema], 403: dict}, tags=self.tags)
        def alt_info(request, character_id: int):
            character = get_object_or_404(EveCharacter.objects.only("pk"), character_id=character_id)
            if not (character in get_all_characters_from_user(request.user) or request.user.has_perm("incursions.waitlist_alts_view")):
                logger.warning(f"User {request.user} denied access to alts for character {character_id}")
                return 403, {"error": "Permission denied"}

            character = get_object_or_404(EveCharacter.objects.only("pk", "character_id"), character_id=character_id)
            user = get_user_from_evecharacter(character)
            alts = get_all_characters_from_user(user)
            filtered_alts = [alt for alt in alts if alt.character_id != character_id]

            logger.info(f"User {request.user} fetched {len(filtered_alts)} alts for character {character_id}")
            return [CharacterSchema.from_orm(alt) for alt in filtered_alts]
