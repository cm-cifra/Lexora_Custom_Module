from odoo import models, fields, api

class DisputeConfirmWizard(models.TransientModel):
    _name = "dispute.confirm.wizard"
    _description = "Confirm Dispute Status on Helpdesk Ticket"

    message = fields.Text(
        default="Are you sure you want to set this ticket's Charge Status to 'Disputed'?",
        readonly=True,
    )

    @api.model
    def _get_active_ticket(self):
        active_model = self.env.context.get("active_model")
        active_id = self.env.context.get("active_id")
        if active_model == "helpdesk.ticket" and active_id:
            return self.env[active_model].browse(active_id)
        return self.env["helpdesk.ticket"]

    def action_yes(self):
        ticket = self._get_active_ticket()
        if ticket:
            # Set the field using a context flag to bypass the write() protection.
            ticket.with_context(confirm_disputed=True).write({"x_studio_charge_status": "Disputed"})
        return {"type": "ir.actions.act_window_close"}

    def action_no(self):
        return {"type": "ir.actions.act_window_close"}
