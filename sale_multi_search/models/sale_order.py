from odoo import models, fields, api

class MyModel(models.Model):
    _name = 'my_module.my_model'
    _description = 'My Model with Custom Search'

    purchase_order = fields.Char(string='Purchase Order')
    search_input_tokens = fields.Char(string='Search Tokens')  # For manual input if needed

    def _build_token_domain(self, search_input):
        tokens = search_input.strip().split()
        domain = []
        for token in tokens:
            domain.append(('purchase_order', 'ilike', token))
        if not domain:
            return []
        elif len(domain) == 1:
            return domain
        else:
            combined_domain = ['|']
            for i in range(0, len(domain), 2):
                if i + 1 < len(domain):
                    combined_domain.extend(['|', domain[i], domain[i + 1]])
                else:
                    combined_domain.append(domain[i])
            return combined_domain

    def name_search(self, name, args=None, operator='ilike', limit=100):
        args = args or []
        if name:
            domain = self._build_token_domain(name)
            args = domain + args
        return super().name_search(name, args=args, operator=operator, limit=limit)

    def action_search_tokens(self):
        """
        Action triggered by button to perform search with tokens.
        """
        # Access the current search input from a field or context
        # Here, assuming search_input_tokens contains space-separated tokens
        tokens = self.search_input_tokens or ''
        domain = self._build_token_domain(tokens)
        return {
            'type': 'ir.actions.act_window',
            'name': 'My Model',
            'view_mode': 'tree,form',
            'res_model': 'my_module.my_model',
            'domain': domain,
        }