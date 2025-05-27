from odoo import models, fields, api

class PurchaseRequest(models.Model):
    _name = 'purchase.request'
    _description = 'Purchase Request'

    name = fields.Char(string='Request Reference', required=True, copy=False, readonly=False, default='New')
    date = fields.Date(string='Request Date', default=fields.Date.context_today)
    request_owner = fields.Many2one('res.users', string='Requested By', default=lambda self: self.env.user)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('submitted', 'Submitted'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], string='Status', default='draft')

    line_ids = fields.One2many('purchase.request.line', 'request_id', string='Request Lines')
    request_id = fields.Many2one('purchase.request', string="Purchase Request", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    description = fields.Text(string="Description")

    vendor_ids = fields.Many2many('res.partner', string="Vendors", domain="[('supplier_rank', '>', 0)]")
    product_summary = fields.Char(string="Requested Products", compute="_compute_product_summary")

    @api.model
    def create(self, vals):
        if vals.get('name', 'New') == 'New':
            vals['name'] = self.env['ir.sequence'].next_by_code('purchase.request') or 'New'
        return super().create(vals)

    @api.depends('line_ids.product_id')
    def _compute_product_summary(self):
        for rec in self:
            rec.product_summary = ', '.join(rec.line_ids.mapped('product_id.name'))

    def action_submit(self):
        self.write({'state': 'submitted'})

    def action_approve(self):
        self.write({'state': 'approved'})

    def action_reject(self):
        self.write({'state': 'rejected'})

    def _compute_product_summary(self):
        for rec in self:
            products = rec.line_ids.mapped('product_id.name')
            rec.product_summary = ', '.join(products)

    def action_send_rfq(self):
        PurchaseOrder = self.env['purchase.order']
        PurchaseOrderLine = self.env['purchase.order.line']
        created_orders = []

        for vendor in self.vendor_ids:
            po = PurchaseOrder.create({
                'partner_id': vendor.id,
                'origin': self.name,
                'order_line': [],
            })

            for line in self.line_ids:
                PurchaseOrderLine.create({
                    'order_id': po.id,
                    'product_id': line.product_id.id,
                    'name': line.description or line.product_id.name,
                    'product_qty': line.quantity,
                    'product_uom': line.product_id.uom_id.id,
                    'price_unit': line.product_id.standard_price or 0.0,
                    'date_planned': fields.Date.today(),
                })

            created_orders.append(po)

        self.write({'state': 'rfq_sent'})
        return {
            'name': 'Created RFQs',
            'type': 'ir.actions.act_window',
            'res_model': 'purchase.order',
            'view_mode': 'list,form',
            'domain': [('id', 'in', [po.id for po in created_orders])],
        }


class PurchaseRequestLine(models.Model):
    _name = 'purchase.request.line'
    _description = 'Purchase Request Line'

    request_id = fields.Many2one('purchase.request', string="Purchase Request", ondelete='cascade')
    product_id = fields.Many2one('product.product', string="Product", required=True)
    quantity = fields.Float(string="Quantity", required=True)
    description = fields.Text(string="Description")
