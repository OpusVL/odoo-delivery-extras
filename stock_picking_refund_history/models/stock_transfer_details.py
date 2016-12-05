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

from openerp import models, fields, api

class StockTransferDetails(models.TransientModel):
    _inherit = 'stock.transfer_details'

    @api.one
    def do_detailed_transfer(self):
        res = super(StockTransferDetails, self).do_detailed_transfer()
        # Update associated refund lines to show lines which have been processed
        self.update_return_processed()
        return res

    def update_return_processed(self):
        for item in self.item_ids:
            if item.destinationloc_id.is_returns_location:
                prod = item.product_id
                qty = item.quantity
                if self.picking_id.refund_line_ids:
                    while qty > 0:
                        for refund_line in self.picking_id.refund_line_ids:
                            qty = self.generic_check_return_processed(
                                prod, qty, refund_line
                            )


    def generic_check_return_processed(self, prod, qty, refund_line):
        # TODO: Make this check generic!
        if prod.is_box:
            if prod.product_variant_id == refund_line.product_id:
                return self.check_return_processed(refund_line, qty)
        elif not prod.is_box:
            if prod == refund_line.product_id:
                return self.check_return_processed(refund_line, qty)

    def check_return_processed(self, refund_line, qty):
        if refund_line.quantity_left - qty <= 0:
            refund_line.write({
                'return_processed': True,
                'quantity_returned': refund_line.quantity_left - qty,
            })
            return qty - refund_line.quantity_left
        else:
            refund_line.write({'quantity_returned': qty})
