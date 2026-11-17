from odoo import models
from odoo import fields
from odoo import api
from odoo.exceptions import ValidationError 

#clase revision para almacenar información sobre las revisiones de material de montaña
class Revision(models.Model):
    _name = 'new_climb.revision'
    _rec_name = 'referencia'
    _description = 'Revision de material de New Climb'

    #datos de la revision para identificarla
    referencia = fields.Char(string='Número de referencia', required=True)
    nombre_revisor = fields.Char(string='Nombre del revisor', required=True)
    fecha_revision = fields.Date(string='Fecha de revision', default=fields.Date.today)
    razon_revision = fields.Selection([
        ('mantenimiento', 'Mantenimiento'),
        ('seguridad', 'Seguridad'),
        ('calidad', 'Calidad'),
    ], string='Razon de la revision')
    valida_hasta = fields.Date(string='Valida hasta', required=True)

    @api.onchange('valida_hasta','fecha_revision')
    def _onchange_valida_hasta(self):
        if self.valida_hasta and self.fecha_revision and self.valida_hasta < self.fecha_revision:
            raise ValidationError("La fecha de validez no puede ser anterior a la fecha de revisión.")
        
    @api.constrains('valida_hasta','fecha_revision')
    def _check_valida_hasta(self):
        for record in self:
            if record.valida_hasta < record.fecha_revision:
                raise ValidationError("La fecha de validez no puede ser anterior a la fecha de revisión.")
            
    @api.constrains('fecha_revision')
    def _check_fecha_revision(self):
        for record in self:
            if record.fecha_revision > fields.Date.today():
                raise ValidationError("La fecha de revisión no puede ser posterior a la fecha actual.")       
         
    valido = fields.Boolean(string='Valido', default=True)
    certificado = fields.Binary(string='Certificado de revision')

    #relacion con el material revisado
    material_id = fields.Many2one('new_climb.material', string='Material revisado')