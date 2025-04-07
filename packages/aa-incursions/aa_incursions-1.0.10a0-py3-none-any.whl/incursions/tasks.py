from datetime import datetime, timezone

from celery import shared_task
from eveuniverse.models import EveConstellation, EveSolarSystem

from django.db import IntegrityError

from allianceauth.eveonline.models import EveFactionInfo
from allianceauth.services.tasks import QueueOnce

from incursions.helpers import (
    embed_boss_spawned, embed_ended, embed_established,
    embed_established_addendum, embed_mobilizing, embed_waitlist_state,
    embed_withdrawing,
)
from incursions.models.incursion import (
    Incursion, IncursionInfluence, IncursionsConfig,
)
from incursions.models.waitlist import Waitlist
from incursions.providers import get_incursions_incursions


@shared_task(base=QueueOnce)
def update_incursions() -> None:
    incursions, response = get_incursions_incursions()
    actives = []
    for incursion in incursions:
        actives.append(incursion['constellation_id'])
        try:
            # Get, because i need to do more steps than an update_or_create would let me
            # This chunk is purely for when incursions change states.
            # Also incursions have no unique id.... wtf ccp
            i = Incursion.objects.get(
                constellation=EveConstellation.objects.get_or_create_esi(id=incursion['constellation_id'])[0],
                ended_timestamp__isnull=True)
            if incursion['state'] == "established":
                # This is still just an established incursion, nothing to act on
                pass
            elif incursion['state'] == "mobilizing" and i.state != Incursion.States.MOBILIZING:
                i.mobilizing_timestamp = datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)
                i.state = Incursion.States.MOBILIZING
                if i.has_boss == "true":
                    i.has_boss = True
                i.save(update_fields=["mobilizing_timestamp", "state"])
            elif incursion['state'] == "withdrawing" and i.state != Incursion.States.WITHDRAWING:
                i.withdrawing_timestamp = datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)
                i.state = Incursion.States.WITHDRAWING
                if i.has_boss == "true":
                    i.has_boss = True
                i.save(update_fields=["withdrawing_timestamp", "state"])
            else:
                # ????
                pass
            try:
                IncursionInfluence.objects.create(
                    incursion=i,
                    influence=incursion['influence'],
                    timestamp=datetime.strptime(
                        str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc))
            except IntegrityError:
                # If we call this task too often cache will return the same influence
                pass
        except Incursion.DoesNotExist:
            # Create an Incursion, It does not exist.
            i = Incursion.objects.create(
                constellation=EveConstellation.objects.get_or_create_esi(
                    id=incursion['constellation_id'])[0],
                faction=EveFactionInfo.objects.get_or_create(
                    faction_id=incursion['faction_id'])[0],
                has_boss=True if incursion['has_boss'] == "true" else False,
                staging_solar_system=EveSolarSystem.objects.get_or_create_esi(
                    id=incursion['staging_solar_system_id'])[0],
                state=incursion['state'],
                type=incursion['type'],
                established_timestamp=datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)
            )
            # We need to also set the mobilizing and withdrawing state here
            # This is purely for new installs, bcoz partially complete incursions
            if incursion['state'] == "mobilizing":
                i.mobilizing_timestamp = datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)
                i.save(update_fields=["mobilizing_timestamp"])
            elif incursion['state'] == "withdrawing ":
                i.mobilizing_timestamp = datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)
                i.withdrawing_timestamp = datetime.strptime(
                    str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc)
                i.save(update_fields=["withdrawing_timestamp", "mobilizing_timestamp"])
            try:
                IncursionInfluence.objects.create(
                    incursion=i,
                    influence=incursion['influence'],
                    timestamp=datetime.strptime(
                        str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z').replace(tzinfo=timezone.utc))
            except IntegrityError:
                # If we call this task too often cache will return the same influence
                pass

    for ended in Incursion.objects.filter(ended_timestamp__isnull=True).exclude(constellation_id__in=actives):
        # Cant use update here, need to fire signals
        ended.ended_timestamp = datetime.strptime(
            str(response.headers['Last-Modified']), '%a, %d %b %Y %H:%M:%S %Z')
        ended.state = Incursion.States.ENDED
        ended.save(update_fields=["ended_timestamp", "state"])


@shared_task
def incursion_established(incursion_pk: int) -> None:
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        if incursion.staging_solar_system.is_high_sec == webhook.security_high:
            webhook.send_embed(embed=embed_established(incursion))
            webhook.send_embed(embed=embed_established_addendum(incursion))
        elif incursion.staging_solar_system.is_low_sec == webhook.security_low:
            webhook.send_embed(embed=embed_established(incursion))
            webhook.send_embed(embed=embed_established_addendum(incursion))
        elif incursion.staging_solar_system.is_null_sec == webhook.security_null:
            webhook.send_embed(embed=embed_established(incursion))
            webhook.send_embed(embed=embed_established_addendum(incursion))


@shared_task
def incursion_mobilizing(incursion_pk: int) -> None:
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        if incursion.staging_solar_system.is_high_sec == webhook.security_high:
            webhook.send_embed(embed=embed_mobilizing(incursion))
        elif incursion.staging_solar_system.is_low_sec == webhook.security_low:
            webhook.send_embed(embed=embed_mobilizing(incursion))
        elif incursion.staging_solar_system.is_null_sec == webhook.security_null:
            webhook.send_embed(embed=embed_mobilizing(incursion))


@shared_task
def incursion_withdrawing(incursion_pk: int) -> None:
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        if incursion.staging_solar_system.is_high_sec == webhook.security_high:
            webhook.send_embed(embed=embed_withdrawing(incursion))
        elif incursion.staging_solar_system.is_low_sec == webhook.security_low:
            webhook.send_embed(embed=embed_withdrawing(incursion))
        elif incursion.staging_solar_system.is_null_sec == webhook.security_null:
            webhook.send_embed(embed=embed_withdrawing(incursion))


@shared_task
def incursion_ended(incursion_pk: int) -> None:
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        if incursion.staging_solar_system.is_high_sec == webhook.security_high:
            webhook.send_embed(embed=embed_ended(incursion))
        elif incursion.staging_solar_system.is_low_sec == webhook.security_low:
            webhook.send_embed(embed=embed_ended(incursion))
        elif incursion.staging_solar_system.is_null_sec == webhook.security_null:
            webhook.send_embed(embed=embed_ended(incursion))


@shared_task
def incursion_boss_spawned(incursion_pk: int) -> None:
    incursion = Incursion.objects.get(pk=incursion_pk)
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        if incursion.staging_solar_system.is_high_sec == webhook.security_high:
            webhook.send_embed(embed=embed_boss_spawned(incursion))
        elif incursion.staging_solar_system.is_low_sec == webhook.security_low:
            webhook.send_embed(embed=embed_boss_spawned(incursion))
        elif incursion.staging_solar_system.is_null_sec == webhook.security_null:
            webhook.send_embed(embed=embed_boss_spawned(incursion))


@shared_task
def waitlist_state(waitlist_pk: int, is_open: bool) -> None:
    waitlist = Waitlist.get_solo()
    for webhook in IncursionsConfig.get_solo().status_webhooks.all():
        webhook.send_embed(embed=embed_waitlist_state(waitlist=waitlist, is_open=is_open))
