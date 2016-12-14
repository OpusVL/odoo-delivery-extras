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

    def _account_entry_move(self, cr, uid, quants, move, context=None):
        # Pass quants into context so we can access it in _prepare_account_move_line
        ctx = context.copy()
        ctx['quants'] = quants
        return super(StockQuant, self)._account_entry_move(
            cr, uid, quants, move, context=ctx
        )

    def _prepare_account_move_line(self, cr, uid, move, qty, cost,
                                   credit_account_id, debit_account_id,
                                   context=None):
        res = super(StockQuant, self)._prepare_account_move_line(cr, uid, move,
            qty, cost, credit_account_id, debit_account_id, context=context
        )
        if context.get('quants'):
            quants = context.get('quants')
            for line in res:
                line = self._fix_amount_currency(line, quants, move, qty)
            return res

    def _fix_amount_currency(self, line, quants, move, qty):
        # We don't want to deal with more than 1 quant for now
        if len(quants) > 1:
            return line
        quant = quants[0]
        # Only update the quant if we need to
        if not quant.secondary_currency_id or not quant.secondary_currency_amount:
            sca, scid = move.get_secondary_currency_info()
            quant.sudo(SUPERUSER_ID).secondary_currency_amount = sca
            quant.sudo(SUPERUSER_ID).secondary_currency_id = scid
        if line[2].get('credit'):
            line[2]['amount_currency'] = -quant.secondary_currency_amount * qty
            line[2]['currency_id'] = quant.secondary_currency_id.id
        if line[2].get('debit'):
            line[2]['amount_currency'] = quant.secondary_currency_amount * qty
            line[2]['currency_id'] = quant.secondary_currency_id.id
        return line

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
