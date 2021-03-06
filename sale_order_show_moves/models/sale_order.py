# -*- coding: utf-8 -*-

##############################################################################
#
# sale_order_show_moves
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


class SaleOrder(models.Model):
    _inherit = "sale.order"

    move_ids = fields.Many2many(
        comodel_name='stock.move',
        string='Moves',
        help="This field will display any associated stock moves",
        compute="compute_move_ids",
    )
    refund_line_ids = fields.Many2many(
        comodel_name='account.invoice.line',
        string='Refunded Products',
        help="This field will display any associated refunds",
        compute="compute_refund_line_ids",
    )

    def compute_move_ids(self):
        # Skip <class 'openerp.models.NewId'>
        if isinstance(self.id, int):
            pickings = self.picking_ids
            self.move_ids = [
                (6, 0, self.return_move_ids(pickings))
            ]

    def return_move_ids(self, pickings):
        move_ids = []
        for picking in pickings:
            for move_line in picking.move_lines:
                move_ids.append(move_line.id)
        return move_ids

    @api.one
    def compute_refund_line_ids(self):
        # Skip <class 'openerp.models.NewId'>
        if isinstance(self.id, int):
            invoices = self.invoice_ids
            refund_invoice_sets = self.return_associated_refund(invoices)
            self.refund_line_ids = [
                (6, 0, self.return_refund_line_ids(refund_invoice_sets))
            ]

    def return_associated_refund(self, invoices):
        """
        Finds any validated/paid refunds connected with the invoices
        from a sale/purchase order
        """
        refund_ids = []
        for invoice in invoices:
            refund_ids.append(self.env['account.invoice'].search([
                ('origin', '=', invoice.number),
                ('type', 'in', ['in_refund', 'out_refund']),
                ('state', 'in', ['open', 'paid']),
            ]))
        return refund_ids

    def return_refund_line_ids(self, refund_invoice_sets):
        refund_line_ids = []
        for refund_invoice_set in refund_invoice_sets:
            for refund_invoice in refund_invoice_set:
                for refund_line in refund_invoice.invoice_line:
                    refund_line_ids.append(refund_line.id)
        return refund_line_ids

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
