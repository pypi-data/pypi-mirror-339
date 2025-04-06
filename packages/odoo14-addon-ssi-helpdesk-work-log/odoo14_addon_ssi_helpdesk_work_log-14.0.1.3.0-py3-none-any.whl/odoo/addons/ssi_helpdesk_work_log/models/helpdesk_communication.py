# Copyright 2022 OpenSynergy Indonesia
# Copyright 2022 PT. Simetri Sinergi Indonesia
# License AGPL-3.0 or later (http://www.gnu.org/licenses/agpl-3.0-standalone.html).

from odoo import models


class HelpdeskCommunication(models.Model):
    _name = "helpdesk_communication"
    _inherit = [
        "helpdesk_communication",
        "mixin.work_object",
    ]

    _work_log_create_page = True
