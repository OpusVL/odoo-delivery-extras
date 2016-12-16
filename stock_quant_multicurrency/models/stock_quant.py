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
        total = 0
        qty_to_process = qty
        for quant in quants:
            # Only update the quants if we need to
            if not quant.secondary_currency_id or not quant.secondary_currency_amount:
                sca, scid = move.get_secondary_currency_info()
                quant.sudo(SUPERUSER_ID).secondary_currency_amount = sca * quant.qty
                quant.sudo(SUPERUSER_ID).secondary_currency_id = scid
            if qty_to_process != 0:
                if qty_to_process - quant.qty >= 0:
                    total += quant.secondary_currency_amount
                    qty_to_process -= quant.qty
                if qty_to_process - quant.qty < 0:
                    total += (quant.secondary_currency_amount / quant.qty) * qty_to_process
                    qty_to_process = 0
        if line[2].get('credit'):
            line[2]['amount_currency'] = -total
            line[2]['currency_id'] = quant.secondary_currency_id.id
        if line[2].get('debit'):
            line[2]['amount_currency'] = total
            line[2]['currency_id'] = quant.secondary_currency_id.id
        return line

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
