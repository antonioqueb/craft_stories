from odoo import models, fields, api
from odoo.exceptions import UserError

class CraftStoriesPage(models.Model):
    _name = 'craft.stories.page'
    _description = 'Configuración Principal Craft Stories'
    _rec_name = 'hero_title_raw'

    # --- HERO SECTION ---
    hero_est_year = fields.Char(string="Est. Year", default="2024")
    hero_title_raw = fields.Char(string="Título Parte 1", default="Raw Matter.")
    hero_title_pure = fields.Char(string="Título Parte 2", default="Pure Form.")
    hero_description = fields.Text(string="Hero Descripción")

    # --- MARQUEE ---
    marquee_text = fields.Char(string="Texto Infinito (Marquee)", 
        default="Timeless Geometry — Eternal Materials — Handcrafted Soul —")

    # --- RELATIONS ---
    chapter_ids = fields.One2many('craft.stories.chapter', 'page_id', string="Capítulos")
    bento_ids = fields.One2many('craft.stories.bento', 'page_id', string="Bento Grid")

    # --- BIG QUOTE ---
    quote_text = fields.Text(string="Cita Principal")
    quote_author = fields.Char(string="Autor de la Cita", default="The Artisan Manifesto")

    # --- FOOTER ---
    footer_next_chapter = fields.Char(string="Label Footer", default="Next Chapter")
    footer_cta_text = fields.Char(string="Texto Botón Footer", default="Explore the Collection")
    footer_link = fields.Char(string="Link Destino", default="/collections/alloy")

    @api.model_create_multi
    def create(self, vals_list):
        if self.search_count([]) >= 1:
            raise UserError('Solo puede existir una configuración de Craft Stories.')
        return super().create(vals_list)

    def get_page_data(self):
        self.ensure_one()
        return {
            'hero': {
                'est': self.hero_est_year,
                'title_raw': self.hero_title_raw,
                'title_pure': self.hero_title_pure,
                'description': self.hero_description,
            },
            'marquee': self.marquee_text,
            'chapters': [c.get_data() for c in self.chapter_ids],
            'bento_grid': {
                'title': "The Science of Beauty", # Podría ser campo dinámico también
                'cards': [b.get_data() for b in self.bento_ids]
            },
            'quote': {
                'text': self.quote_text,
                'author': self.quote_author
            },
            'footer': {
                'label': self.footer_next_chapter,
                'cta': self.footer_cta_text,
                'link': self.footer_link
            }
        }

class CraftStoriesChapter(models.Model):
    _name = 'craft.stories.chapter'
    _description = 'Capítulo / Historia'
    _order = 'sequence, id'

    page_id = fields.Many2one('craft.stories.page')
    sequence = fields.Integer(default=10)

    # Identificadores Visuales
    number_display = fields.Char(string="Número (01)", required=True)
    fig_label = fields.Char(string="Etiqueta Fig (Fig 01...)", required=True)
    
    # Icono para mapear en React
    icon_name = fields.Selection([
        ('mountain', 'Mountain (Origin)'),
        ('hammer', 'Hammer (Shaping)'),
        ('star', 'Star'),
    ], string="Icono", default='mountain')
    
    label_top = fields.Char(string="Subtítulo Superior (The Origin)")
    
    # Textos Principales
    title_main = fields.Char(string="Título Principal")
    title_italic = fields.Char(string="Parte Itálica")
    description = fields.Text(string="Descripción")

    # Listado de características (separadas por salto de linea)
    features_list = fields.Text(string="Lista (Bullet points)", help="Una por línea")

    # Multimedia
    image = fields.Binary(string="Imagen", attachment=True)
    image_filename = fields.Char("Nombre archivo imagen")
    video_url = fields.Char("Video URL (Opcional)")

    def get_data(self):
        return {
            'id': self.id,
            'number': self.number_display,
            'fig_label': self.fig_label,
            'icon': self.icon_name,
            'label_top': self.label_top,
            'title': {
                'main': self.title_main,
                'italic': self.title_italic
            },
            'description': self.description,
            'features': self.features_list.split('\n') if self.features_list else [],
            'image_url': f"/web/image?model={self._name}&id={self.id}&field=image" if self.image else "",
            'video_url': self.video_url or ""
        }

class CraftStoriesBento(models.Model):
    _name = 'craft.stories.bento'
    _description = 'Bento Grid Card'
    _order = 'sequence'

    page_id = fields.Many2one('craft.stories.page')
    sequence = fields.Integer(default=10)

    icon_name = fields.Selection([
        ('clock', 'Clock'),
        ('gem', 'Gem'),
        ('microscope', 'Microscope'),
    ], string="Icono", required=True)

    title = fields.Char(required=True)
    description = fields.Text(required=True)

    def get_data(self):
        return {
            'icon': self.icon_name,
            'title': self.title,
            'description': self.description
        }
