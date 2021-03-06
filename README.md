# odoo-delivery-extras

Extra modules for stock.picking and related models.

## `stock_picking_refund_history`

- Display a table of refund history which is updated dynamically on the stock.picking form.
  - Displays any refunded products (i.e products which have been refunded or are in a validated refund from the associated Sale/Purchase)
- Adds a flag to stock location `Is Returns Location`.
  - When enabled - and stock is transferred to this location - the flag on account.invoice.line `Return Processed` will be flagged to true if the product qty transferred matches the qty of returned items.
    - There is also tracking of how many products are returned, so the flag will get set even if returned items are done through several transfers

## `stock_picking_cancel_move`
- Adds the `Cancel Move` button to the popup stock.move form on stock.picking

## `sale_order_show_moves`
- Displays a table of moves which is updated dynamically on the sale.order form.
  - This is based on any related stock.move records (ones which were created by the SO)
- Also displays a list of refund lines associated with the SO.
  - This is almost identical behaviour to `stock_picking_refund_history` but on sale.order

## `stock_disable_invoice_on_return`
- Disables the facility to invoice a returned picking.
  - Intended for use in conjunction with `stock_picking_refund_history`
  - Refunding the initial invoice, and then reversing x,y products from stock move. 
    - This is to workaround bugs introduced when refunding based on a returned picking

## `stock_picking_get_purchase_id`
- Adds a field `purchase_id` - computed with `_get_purchase_id` to `stock.picking` to mirror the behaviour of `sale_id` and `_get_sale_id`

## `stock_quant_multicurrency`
- Adds `secondary_currency_id` and `secondary_currency_amount` fields to stock.quant
  - These fields get updated based on the source PO lines currency and price_unit
  - This is basically a quick workaround version of handling multiple currencies which products could be purchased in - and is to solve the problem of odoo's amount_currency field not populating on journals without a secondary currency set
