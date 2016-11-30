# odoo-delivery-extras

Extra modules for stock.picking and related models.

## `stock_picking_refund_history`

- Display a table of refund history which is updated dynamically on the stock.picking form.
-   - Displays any refunded products (i.e products which have been refunded or are in a validated refund from the associated Sale/Purchase)

## `stock_picking_cancel_move`
- Adds the `Cancel Move` button to the popup stock.move form on stock.picking

## `sale_order_show_cancelled_moves`
- Displays a table of cancelled moves which is updated dynamically on the sale.order form.
-   - This is based on any related stock.move records (ones which were created by the SO)

## `stock_disable_invoice_on_return`
- Disables the facility to invoice a returned picking.
-   - Intended for use in conjunction with `stock_picking_refund_history`
-   - Refunding the initial invoice, and then reversing x,y products from stock move. 
-   -   - This is to workaround bugs introduced when refunding based on a returned picking
