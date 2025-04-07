from django.db import models


class General(models.Model):
    """Meta model for app permissions"""

    class Meta:
        managed = False
        default_permissions = ()
        permissions = (
            ("basic_waitlist", "Can Access The Incursion Waitlist Tool"),  # All
            ("waitlist_alts_view", "Can View all of a users Alts ! Danger?"),  # Leadership
            ("waitlist_announcements_manage", "can manage announcements"),  # Leadership
            ("waitlist_bages_view", "Can View Badges"),  # FC
            ("waitlist_badges_manage", "Can Manage Badges"),  # Leadership
            ("waitlist_bans_view", "Can View Bans"),  # FC
            ("waitlist_bans_manage", "Can Manage Bans"),  # Leadership
            ("waitlist_commanders_view", "can view commanders"),  # FC
            ("waitlist_commanders_manage", "can manage commanders"),  # Leadership
            ("waitlist_documentation_view", "can view documentation"),  # Jr FC
            ("waitlist_fleet_view", "Can View Active Fleet composition"),  # FC
            ("waitlist_implants_view", "Can View Implants"),  # FC
            ("waitlist_history_view", "Can View History"),  # Leadership
            ("waitlist_notes_view", "Can View Notes"),  # FC
            ("waitlist_notes_manage", "Can Manage notes"),  # Leadership
            ("waitlist_search", "Can Search"),  # FC
            ("waitlist_stats_view", "Can View Fleet Stats"),  # Leadership
            ("waitlist_skills_view", "Can view Skills"),  # Leadership
            # Add extra context to the Waitlist for Non-FCs
            ("waitlist_context_a", "Add Context to Waitlist: Number of Pilots"),
            ("waitlist_context_b", "Add Context to Waitlist: Ship Types"),
            ("waitlist_context_c", "Add Context to Waitlist: Time in Waitlist"),
            ("waitlist_context_d", "Add Context to Waitlist: Pilot Names"),

            ("waitlist_manage_waitlist", "Manage Waitlist"),  # FC
            ("waitlist_manage_waitlist_approve_fits", "Can Approve and Deny Fits on the WL"),  # FC

            # ESI Calls, Limit these maybe?
            ("waitlist_esi_show_info", "Can open a Show Info Window ingame"),
            ("waitlist_esi_search", "Will search ESI when using Search"),
        )
