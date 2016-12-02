# -*- coding: utf-8 -*-

##############################################################################
#
# stock_picking_refund_history
# Copyright (C) 2016 OpusVL (<http://opusvl.com/>)
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as
# published by the Free Software Foundation, either version 3 of the
# License, or (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU Affero General Public License for more details.
#
# You should have received a copy of the GNU Affero General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

from openerp import models, api, fields

class AccountInvoiceLine(models.Model):
    _inherit = "account.invoice.line"

    return_processed = fields.Boolean(string="Return Processed", default=False)
    quantity_left = fields.Integer(compute="_compute_quantity_left", default=0)
    quantity_returned = fields.Integer(default=0)

    @api.one
    @api.depends('quantity_returned', 'quantity')
    def _compute_quantity_left(self):
        self.quantity_left = self.quantity - self.quantity_returned
