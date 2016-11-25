# -*- coding: utf-8 -*-

##############################################################################
#
# sale_order_show_cancelled_moves
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

    cancelled_move_ids = fields.Many2many(
        comodel_name='stock.move',
        string='Cancelled Moves',
        help="This field will display any associated stock moves which are in a state of 'Cancelled'",
        compute="compute_cancelled_move_ids",
    )

    def compute_cancelled_move_ids(self):
        # Skip <class 'openerp.models.NewId'>
        if isinstance(self.id, int):
            pickings = self.return_associated_pickings(self.name)
            self.cancelled_move_ids = [
                (6, 0, self.return_cancelled_move_ids(pickings))
            ]

    def return_cancelled_move_ids(self, pickings):
        cancelled_move_ids = []
        for picking in pickings:
            for move_line in picking.move_lines:
                if move_line.state == 'cancel':
                    cancelled_move_ids.append(move_line.id)
        return cancelled_move_ids

    def return_associated_pickings(self, so_number):
        return self.env['stock.picking'].search([
            ('origin', 'ilike', so_number),
        ])

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
