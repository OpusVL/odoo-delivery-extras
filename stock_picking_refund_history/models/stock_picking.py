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


class StockPicking(models.Model):
    _inherit = "stock.picking"

    refund_line_ids = fields.Many2many(
        comodel_name='account.invoice.line',
        string='Refunded Products',
        help="This field will display any associated refunds",
        compute="compute_refund_line_ids",
    )

    @api.one
    def compute_refund_line_ids(self):
        # Skip <class 'openerp.models.NewId'>
        if isinstance(self.id, int):
            order = self.return_order()
            if order:
                invoices = self.return_associated_invoice(order.name)
                refund_invoice_sets = self.return_associated_refund(invoices)
                self.refund_line_ids = [
                    (6, 0, self.return_refund_line_ids(refund_invoice_sets))
                ]

    def return_order(self):
        """
        A slightly sloppy way of checking whether a PO or SO is the original
        order, so some optimization could be done here
        """
        sale = self.return_associated_sale(self.origin)
        if not sale:
            sale = self.return_associated_sale_from_return()
        purchase = self.return_associated_purchase(self.origin)
        if not purchase:
            purchase = self.return_associated_purchase_from_return()
        return sale if sale else purchase

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

    def return_associated_invoice(self, order_number):
        return self.env['account.invoice'].search([
            ('origin', '=', order_number)
        ])

    def return_refund_line_ids(self, refund_invoice_sets):
        refund_line_ids = []
        for refund_invoice_set in refund_invoice_sets:
            for refund_invoice in refund_invoice_set:
                for refund_line in refund_invoice.invoice_line:
                    refund_line_ids.append(refund_line.id)
        return refund_line_ids

    def return_associated_sale(self, origin):
        return self.env['sale.order'].search([
            ('name', 'ilike', origin),
        ])

    def return_associated_purchase(self, origin):
        return self.env['purchase.order'].search([
            ('name', 'ilike', origin),
        ])

    def return_associated_sale_from_return(self):
        return self.return_associated_sale(self.follow_return_chain())

    def return_associated_purchase_from_return(self):
        return self.return_associated_purchase(self.follow_return_chain())

    def follow_return_chain(self):
        """
        Go down the chain of reversed transfers until we meet
        the original document with a PO/SO as the origin
        """
        origin = str(self.origin)
        while origin and ('SO' not in origin or 'PO' not in origin):
            source_picking_search = self.env['stock.picking'].search([
                ('name', '=', origin),
            ])
            if len(source_picking_search) > 0:
                origin = str(source_picking_search.origin)
            else:
                break
        return origin

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
