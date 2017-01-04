# -*- coding: utf-8 -*-

##############################################################################
#
# swoon_purchase_order
# Copyright (C) 2015 OpusVL (<http://opusvl.com/>)
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

from openerp.osv import fields, osv
from openerp import api, exceptions


class wizard_stock_move_cancel_amount(osv.osv_memory):
    _name = "wizard.stock.move.cancel_amount"
    _description = "Cancel a specific amount from a stock move line"

    _columns = {
        'amount': fields.float(string="Amount to Cancel", digits=(16,2))
    }

    def action_cancel_amount(self, cr, uid, ids, context=None):
        active_id = context.get('active_id')
        stock_move_obj = self.pool.get('stock.move')
        wiz_rec = self.browse(cr, uid, ids, context)
        # First, find the amount we will have left over (if any)
        move = stock_move_obj.browse(
            cr, uid, active_id, context=context
        )
        qty_left = move.product_uom_qty - wiz_rec.amount
        # If it's < 0 - we have a problem!
        if qty_left < 0:
            raise exceptions.Warning("You cannot cancel more than there is to be moved!")
        # If it's > 0, we duplicate the move and set the amount to qty_left
        if qty_left > 0:
            # Set the amount on the line we will cancel
            stock_move_obj.write(cr, uid, active_id, {
                'product_uom_qty': wiz_rec.amount,
            }, context=context)
            # Duplicate the stock move and set the amount left on it
            move_duplicate = stock_move_obj.copy(cr, uid, active_id, context=context)
            stock_move_obj.write(cr, uid, move_duplicate, {
                'product_uom_qty': qty_left,
            }, context=context)

            # Then find & duplicate any chained stock moves and set the amount left on it
            group_picking_ids = self.pool.get('stock.picking').search(cr, uid, [
                ('group_id', '=', move.picking_id.group_id.id),
            ], context=context)
            chained_moves = stock_move_obj.search(cr, uid, [
                ('picking_id', 'in', group_picking_ids),
                ('product_id', '=', move.product_id.id),
                ('state', 'in', ['draft', 'waiting', 'confirmed', 'partially_available', 'assigned']),
                ('id', 'not in', [move_duplicate, move.id]),
            ], context=context)
            for chained_move in chained_moves:
                chained_duplicate = stock_move_obj.copy(
                    cr, uid, chained_move, context=context
                )
                stock_move_obj.write(cr, uid, chained_duplicate, {
                    'product_uom_qty': qty_left,
                }, context=context)
        # Then cancel the original (which will also cancel any chained)
        stock_move_obj.action_cancel(cr, uid, active_id, context=context)

    def discard_changes(self, cr, uid, ids, context=None):
        return True
