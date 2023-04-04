from odoo import fields, models, _, api


class CreateAppointmentWizard(models.TransientModel):
    _name = 'create.appointment.wizard'
    _description = 'Create Appointment Wizard'

    date_appointment = fields.Date(string="Date", required=True, tracking=True)
    patient_id = fields.Many2one('hospital.patient', string="Patient")
    doctor_id = fields.Many2one('hospital.doctor', string="Doctor", required=True, tracking=True)

    # method to create appointment from wizard form
    def action_create_appointment(self):
        vals = {
            'date_appointment': self.date_appointment,
            'patient_id': self.patient_id.id,
            'doctor_id': self.doctor_id.id,
        }
        appointment_rec = self.env['hospital.appointment'].create(vals)

        # return view form of this new record
        return {
            'name': _('Appointment'),
            'type': 'ir.actions.act_window',
            'view_mode': 'form',
            'res_model': 'hospital.appointment',
            'res_id': appointment_rec.id,
        }

    # to add patient name by default if call create new appointment function from form view of patient
    @api.model
    def default_get(self, fields):
        vals = super(CreateAppointmentWizard, self).default_get(fields)
        vals['patient_id'] = self._context.get('active_id')
        return vals

    # Return Action and View From
    def action_view_appointments(self):
        # there are 3 methods
        # return tree action of appointment of select patient
        action = self.env['ir.actions.actions']._for_xml_id('om_hospital.appointments_action')
        # condition
        action['domain'] = [('patient_id', '=', self.patient_id.id)]
        return action

        # method 2

        # action = self.env.ref('om_hospital.appointments_action').read()[0]
        # action['domain'] = [('patient_id', '=', self.patient_id.id)]
        # return action

        # method 3
        # return {
        #     'name': 'Appointments',
        #     'type': 'ir.actions.act_window',
        #     'view_type': 'form',
        #     'res_model': 'hospital.appointment',
        #     'target': 'current',
        #     'view_mode': 'tree,form',
        #     'domain': [('patient_id', '=', self.patient_id.id)],
        # }

    # get patient_id from active patient form => if patient form is opened
    # def action_get_test(self):
    #     if self.env.context.get('active_model'):
    #         active_model = self.env.context.get('active_model')
    #         if self.env[active_model].browse(self.env.context.get('active_id')).id:
    #             vals = {
    #                 'date_appointment': self.date_appointment,
    #                 'patient_id': self.env[active_model].browse(self.env.context.get('active_id')).id,
    #             }
    #             appointment_rec = self.env['hospital.appointment'].create(vals)
    #
    #             # return view form of this new record
    #             return {
    #                 'name': _('Appointment'),
    #                 'type': 'ir.actions.act_window',
    #                 'view_mode': 'form',
    #                 'res_model': 'hospital.appointment',
    #                 'res_id': appointment_rec.id,
    #             }
    #     else:
    #         pass







