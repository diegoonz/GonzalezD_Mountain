{
    'name': "NewClimb",

    'version': '19.0.1.0.0',

    'summary': "Alquiler de material de montaña",

    'description': """Una app de Odoo para el alquiler 
    de material de montaña, como cuerdas, arneses, 
    mosquetones, etc.""",

    'author': "Diego",

    'website': "https://github.com/diegoonz/GonzalezD_Mountain",
    
     'category': 'Montañismo',

     'depends': ['base'],
   
   'demo': [
        'demo/demo.xml',
    ],

    'data': [
        'security/ir.model.access.csv',
        'views/cliente.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}

