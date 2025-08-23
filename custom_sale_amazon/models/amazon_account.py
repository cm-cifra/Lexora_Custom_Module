def _process_order_data(self, order_data):
    self.ensure_one()

    amazon_order_ref = order_data['AmazonOrderId']
    order = self.env['sale.order'].search(
        [('amazon_order_ref', '=', amazon_order_ref)], limit=1
    )
    amazon_status = order_data['OrderStatus']
    fulfillment_channel = (order_data.get('FulfillmentChannel') or '').upper()

    # ✅ Check if all products exist in Odoo before syncing
    order_lines = order_data.get('OrderItems', [])
    missing_products = []
    for line in order_lines:
        sku = line.get('SellerSKU')
        product = self.env['product.product'].search([('default_code', '=', sku)], limit=1)
        if not product:
            missing_products.append(sku)

    if missing_products:
        _logger.warning(
            "Skipped Amazon order %(ref)s because the following SKUs were not found in Odoo: %(skus)s",
            {'ref': amazon_order_ref, 'skus': ', '.join(missing_products)}
        )
        return False  # 🚫 Do not sync this order if SKUs missing

    # ✅ Create order if not found
    if not order:
        if amazon_status in const.STATUS_TO_SYNCHRONIZE.get(fulfillment_channel, []) or amazon_status == "Shipped":
            order = self._create_order_from_data(order_data)

            if order.amazon_channel == 'fba':
                self._generate_stock_moves(order)

            elif order.amazon_channel == 'fbm':
                if amazon_status == "Shipped":
                    if order.state in ['draft', 'sent']:
                        order.with_context(mail_notrack=True).action_confirm()

                    for picking in order.picking_ids.filtered(lambda p: p.state not in ['done', 'cancel']):
                        picking.with_context(skip_sms=True).button_validate()
                        picking.amazon_sync_status = 'done'

                    _logger.info("📦 Auto-marked FBM order %s pickings as done (Amazon Shipped)", order.name)
                    order.with_context(mail_notrack=True).action_lock()
                else:
                    if order.state in ['draft', 'sent']:
                        order.with_context(mail_notrack=True).action_confirm()
                    order.with_context(mail_notrack=True).action_lock()

            _logger.info("✅ Created new sales order %s (Amazon %s, status %s)",
                        order.name, amazon_order_ref, amazon_status)
        else:
            _logger.info("⏭️ Ignored Amazon order %s (status %s)", amazon_order_ref, amazon_status)
            return False

    else:
        # ✅ Order already exists
        unsynced_pickings = order.picking_ids.filtered(
            lambda picking: picking.amazon_sync_status != 'done' and picking.state not in ['cancel', 'done']
        )

        if amazon_status == 'Canceled' and order.state != 'cancel':
            if order.state in ['draft', 'sent']:
                order.unlink()
                _logger.info("🚫 Deleted draft order %s (Amazon canceled)", amazon_order_ref)
            else:
                order._action_cancel()
                _logger.info("🚫 Canceled order %s", amazon_order_ref)

        elif amazon_status == 'Shipped' and fulfillment_channel == 'MFN':
            if unsynced_pickings:
                for picking in unsynced_pickings:
                    picking.with_context(skip_sms=True).button_validate()
                    picking.amazon_sync_status = 'done'
                _logger.info("📦 Marked pickings as done for %s (Amazon Shipped)", amazon_order_ref)

            if order.state != 'cancel':
                order.with_context(mail_notrack=True).action_lock()

        else:
            _logger.info("ℹ️ Order %s already synced (status %s)", amazon_order_ref, amazon_status)

    return order or False
