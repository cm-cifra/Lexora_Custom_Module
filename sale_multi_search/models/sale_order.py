from odoo import models

class SaleOrder(models.Model):
    _inherit = "sale.order"

    def name_search(self, name='', args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            tokens = name.split()
            domain = []
            for token in tokens:
                # add OR condition for each token
                if domain:
                    domain = ['|'] + domain
                # search in client_order_ref (PO) OR in name (SO number)
                domain.append(('client_order_ref', '=', token))
            recs = self.search(domain + args, limit=limit)
        else:
            recs = self.search(args, limit=limit)
        return recs.name_get()
