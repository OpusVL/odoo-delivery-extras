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

from openerp.osv import osv, fields


class purchase_order(osv.osv):
    _inherit = "purchase.order"

    # Override this function field to just return pickings where picking.purchase_id
    # equals the po_id
    def _get_picking_ids(self, cr, uid, ids, field_names, args, context=None):
        sp = self.pool.get('stock.picking')
        # For some reason the purchase_id evaluate properly in a model.search()
        # and odoo just returns all pickings, so we have to loop over
        # them all and check manually - which is going to create problems
        # in the long-run where databases have lots of pickings.
        all_pick_ids = sp.search(cr, uid, [], context=context)
        all_picks = sp.browse(cr, uid, all_pick_ids, context=context)
        res = {}
        for po_id in ids:
            pick_ids = []
            for pick in all_picks:
                if pick.purchase_id.id == po_id:
                    pick_ids.append(pick.id)
            res[po_id] = pick_ids
        return res

    _columns = {
        'picking_ids': fields.function(_get_picking_ids, method=True,
            type='one2many', relation='stock.picking', string='Picking List',
            help="This is the list of receipts that have been generated for this purchase order."
        ),
    }
