# -*- coding: utf-8 -*-

##############################################################################
#
# stock_quant_multicurrency
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

from openerp import models, fields, api, SUPERUSER_ID


class StockQuant(models.Model):
    _inherit = "stock.quant"

    secondary_currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        help="Currency which Amount currency is logged against",
    )
    secondary_currency_amount = fields.Float(
        string="Inventory value (in currency)",
        help="Amount in currency which the quant was purchased at",
    )

    @api.model
    def _quant_create(self, qty, move, lot_id=False, owner_id=False,
                      src_package_id=False, dest_package_id=False,
                      force_location_from=False, force_location_to=False):
        res = super(StockQuant, self)._quant_create(qty, move, lot_id, owner_id,
                    src_package_id, dest_package_id, force_location_from,
                    force_location_to
        )
        # Pull the secondary currency info from the original PO line
        sca, scid = move.get_secondary_currency_info()
        res.sudo(SUPERUSER_ID).secondary_currency_amount = sca
        res.sudo(SUPERUSER_ID).secondary_currency_id = scid
        return res


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
