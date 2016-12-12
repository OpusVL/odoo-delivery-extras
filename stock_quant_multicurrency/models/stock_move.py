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

from openerp import models, fields, api


class StockMove(models.Model):
    _inherit = "stock.move"

    secondary_currency_id = fields.Many2one(
        'res.currency',
        string="Currency",
        help="Currency which Amount currency is logged against",
    )
    secondary_currency_amount = fields.Float(
        string="Inventory value (in currency)",
        help="Amount in currency which the quant was purchased at",
    )


    def get_secondary_currency_info(self):
        if self.purchase_line_id:
            sca = self.purchase_line_id.price_unit
            scid = self.purchase_line_id.order_id.currency_id
            return sca, scid


# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
