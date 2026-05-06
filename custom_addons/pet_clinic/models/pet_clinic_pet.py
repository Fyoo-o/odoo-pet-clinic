# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta


class PetClinicPet(models.Model):
    _name = 'pet_clinic.pet'
    _description = 'Patient / Hewan Peliharaan'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'id_pet desc'

    id_pet = fields.Char(
        string='Pet ID',
        readonly=True,
        copy=False,
        default='New',
        tracking=True,
    )
    name = fields.Char(string='Name', required=True, tracking=True)
    date_of_birth = fields.Date(string='Date of Birth', tracking=True)
    age = fields.Char(
        string='Age',
        compute='_compute_age',
        store=True,
    )
    gender = fields.Selection(
        [('male', 'Male'), ('female', 'Female')],
        string='Gender',
        tracking=True,
    )
    type_id = fields.Many2one(
        'pet_clinic.pet_type', string='Pet Type', tracking=True,
    )
    breed_id = fields.Many2one(
        'pet_clinic.pet_breed', string='Breed', tracking=True,
        domain="[('type_id', '=', type_id)]",
    )
    owner_id = fields.Many2one(
        'pet_clinic.client', string='Owner', tracking=True,
    )
    sinyal_amon = fields.Char(string='Sinyal Amon')
    tgl_pendaftaran = fields.Date(
        string='Tanggal Pendaftaran', default=fields.Date.today,
    )
    image = fields.Binary(string='Image', attachment=True)

    visitation_ids = fields.One2many(
        'pet_clinic.visitation', 'pet_id', string='Visitations',
    )
    appointment_ids = fields.One2many(
        'pet_clinic.appointment', 'pet_id', string='Appointments',
    )
    service_ids = fields.One2many(
        'pet_clinic.service', 'pet_id', string='Services',
    )
    medical_history_ids = fields.One2many(
        'pet_clinic.medical_history_line', 'pet_id',
        string='Medical History',
    )

    visitation_count = fields.Integer(
        compute='_compute_visitation_count', store=True,
    )
    appointment_count = fields.Integer(
        compute='_compute_appointment_count', store=True,
    )
    service_count = fields.Integer(
        compute='_compute_service_count', store=True,
    )

    active = fields.Boolean(default=True)

    @api.depends('date_of_birth')
    def _compute_age(self):
        today = fields.Date.today()
        for rec in self:
            if rec.date_of_birth:
                rd = relativedelta(today, rec.date_of_birth)
                rec.age = f"{rd.years} Tahun, {rd.months} Bulan"
            else:
                rec.age = ''

    @api.depends('visitation_ids')
    def _compute_visitation_count(self):
        for rec in self:
            rec.visitation_count = len(rec.visitation_ids)

    @api.depends('appointment_ids')
    def _compute_appointment_count(self):
        for rec in self:
            rec.appointment_count = len(rec.appointment_ids)

    @api.depends('service_ids')
    def _compute_service_count(self):
        for rec in self:
            rec.service_count = len(rec.service_ids)

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('id_pet', 'New') == 'New':
                vals['id_pet'] = self.env['ir.sequence'].next_by_code(
                    'pet_clinic.pet'
                ) or 'New'
        return super().create(vals_list)

    @api.onchange('type_id')
    def _onchange_type_id(self):
        """Reset breed when pet type changes, and restrict domain."""
        self.breed_id = False
        if self.type_id:
            return {
                'domain': {
                    'breed_id': [('type_id', '=', self.type_id.id)]
                }
            }
        return {'domain': {'breed_id': []}}

    def name_get(self):
        result = []
        for rec in self:
            name = f"[{rec.id_pet}] {rec.name}" if rec.id_pet else rec.name
            result.append((rec.id, name))
        return result

    def action_view_visitations(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Visitations',
            'res_model': 'pet_clinic.visitation',
            'view_mode': 'list,form',
            'domain': [('pet_id', '=', self.id)],
            'context': {'default_pet_id': self.id},
        }

    def action_view_appointments(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Appointments',
            'res_model': 'pet_clinic.appointment',
            'view_mode': 'list,form',
            'domain': [('pet_id', '=', self.id)],
            'context': {'default_pet_id': self.id},
        }

    def action_view_services(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Services',
            'res_model': 'pet_clinic.service',
            'view_mode': 'list,form',
            'domain': [('pet_id', '=', self.id)],
            'context': {'default_pet_id': self.id},
        }


class PetClinicMedicalHistoryLine(models.Model):
    _name = 'pet_clinic.medical_history_line'
    _description = 'Medical History Line'
    _order = 'date_start desc'

    pet_id = fields.Many2one(
        'pet_clinic.pet', string='Pet', ondelete='cascade',
    )
    date_start = fields.Datetime(string='Date Start')
    doctor_id = fields.Many2one('pet_clinic.doctor', string='Doctor')
    anamnesa = fields.Text(string='Anamnesa')
    diagnosis = fields.Text(string='Diagnosis')
    therapy = fields.Text(string='Therapy')
    temperature = fields.Float(string='Temperature (°C)')
    weight = fields.Float(string='Weight (Kg)')
    bcs = fields.Integer(string='BCS (1-9)')
    action = fields.Text(string='Action')
