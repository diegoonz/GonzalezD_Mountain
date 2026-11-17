from odoo import models
from odoo import fields

#clase Material para almacenar información sobre las piezas
class Material(models.Model):
    _name = 'new_climb.material'
    _description = 'Piezas con su nº serie y proveedor'

#información de cada material para almacenar
    name = fields.Char(string = 'Nombre del producto')
    numero_serie = fields.Char(string = 'Número de serie', required=True)
    proveedor_id = fields.Many2one('new_climb.proveedor', string='Proveedor', ondelete='restrict', index=True, required=True)


#datos del material para gestionarlo
    actividad = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_uso', 'En Uso'),
        ('fuera_stock', 'Fuera de Stock'),
        ('vendida','Vendida'),
        ('en_revision','En Revisión') 
    ], string='Actividad', default='disponible') 
    precio_alquiler = fields.Float(string='Precio de alquiler', required=True)
    foto = fields.Binary(string='Foto del material')
    cliente_id = fields.Many2one('new_climb.cliente', string='Cliente', ondelete='set null', index=True)
    revision_ids = fields.One2many('new_climb.revision', 'material_id', string='Revisiones realizadas')