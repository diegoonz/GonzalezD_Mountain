from odoo import models, fields

#clase revision para almacenar información sobre las revisiones de material de montaña
class Revision(models.Model):
    _name = 'new_climb.revision'
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
    valido = fields.Boolean(string='Valido', default=True)
    certificado = fields.Binary(string='Certificado de revision')

    #relacion con el material revisado
    material_id = fields.Many2one('new_climb.material', string='Material revisado')