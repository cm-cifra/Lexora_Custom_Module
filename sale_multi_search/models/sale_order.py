from odoo import models, fields, api

class MyModel(models.Model):
    _name = 'my_module.my_model'
    _description = 'My Custom Model'

    purchase_order = fields.Char(string='Purchase Order')

    @api.model
    def _build_search_domain(self, search_input):
        """
        Build a domain that ORs multiple 'ilike' filters for each word in search_input.
        """
        tokens = search_input.strip().split()
        domain = []
        for token in tokens:
            domain.append(('purchase_order', 'ilike', token))
        if len(domain) == 0:
            return []
        elif len(domain) == 1:
            return domain
        else:
            # Combine with ORs
            combined_domain = ['|']
            # For multiple tokens, need to pair them with '|' operators
            # Build nested OR conditions
            for i in range(0, len(domain), 2):
                if i + 1 < len(domain):
                    combined_domain.extend(['|', domain[i], domain[i + 1]])
                else:
                    combined_domain.append(domain[i])
            return combined_domain

    @api.model
    def name_search(self, name, args=None, operator='ilike', limit=100):
        """
        Override name_search to parse the search input and build custom domain.
        """
        args = args or []
        if name:
            domain = self._build_search_domain(name)
            args = domain + args
        return super().name_search(name, args=args, operator=operator, limit=limit)
