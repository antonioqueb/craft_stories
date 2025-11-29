{
    'name': 'Craft Stories API (Odoo 19)',
    'version': '1.0',
    'category': 'Website/CMS',
    'summary': 'API Headless para el Landing Page Craft Stories',
    'description': """
        Módulo Backend para 'Craft Stories'.
        - Gestiona Hero, Capítulos, Grid Bento y Footer.
        - API REST-like con soporte de imágenes.
        - Diseñado para Next.js / React.
    """,
    'author': 'Craft Consulting',
    'depends': ['base', 'web'],
    'data': [
        'security/ir.model.access.csv',
        'views/cms_views.xml',
        'data/cms_data.xml',
    ],
    'installable': True,
    'application': True,
    'license': 'LGPL-3',
}
