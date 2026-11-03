from odoo import models, fields

#clase Material para almacenar información sobre las piezas
class Material(models.Model):
    _name = 'new_climb.material'
    _description = 'Piezas con su nº serie y proveedor'

#información de cada material para almacenar
    name = fields.Char(string = 'Nombre del producto')
    numero_serie = fields.Char(string = 'Número de serie', required=True)
    proveedor_id = fields.Many2one('new_climb.proveedor', string='Proveedor', ondelete='set null', index=True, required=True)

#datos del material para gestionarlo
    actividad = fields.Selection([
        ('disponible', 'Disponible'),
        ('en_uso', 'En Uso'),
        ('fuera_de_servicio', 'Fuera de Servicio')
    ], string='Actividad', default='disponible')    
    