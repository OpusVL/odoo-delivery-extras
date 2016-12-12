# -*- coding: utf-8 -*-

##############################################################################
#
# stock_picking_get_purchase_id
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

    purchase_id = fields.One2many('purchase.order', compute="_get_purchase_id")

    @api.depends('group_id', 'origin')
    def _get_purchase_id(self):
        for picking in self:
            po = False
            if picking.origin:
                po = self.return_associated_purchase(picking.origin)
                if not po:
                    po = self.return_associated_purchase_from_return()
            picking.purchase_id = po

    def return_associated_purchase(self, origin):
        return self.env['purchase.order'].search([
            ('name', 'ilike', origin),
        ])

    def return_associated_purchase_from_return(self):
        return self.return_associated_purchase(self.follow_return_chain())

    def follow_return_chain(self):
        """
        Go down the chain of reversed transfers until we meet
        the original document with a PO/SO as the origin
        """
        origin = str(self.origin)
        while origin and ('PO' not in origin):
            source_picking_search = self.env['stock.picking'].search([
                ('name', '=', origin),
            ])
            if len(source_picking_search) > 0:
                origin = str(source_picking_search.origin)
            else:
                break
        return origin



