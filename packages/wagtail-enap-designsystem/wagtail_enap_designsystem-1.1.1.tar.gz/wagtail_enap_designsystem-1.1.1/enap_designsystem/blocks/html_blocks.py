
from django.utils.translation import gettext_lazy as _
from wagtail import blocks

from wagtail.contrib.table_block.blocks import TableBlock as WagtailTableBlock
from wagtail.documents.blocks import DocumentChooserBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.admin.panels import FieldPanel
from wagtail.blocks import StructBlock, CharBlock, RichTextBlock
from wagtail.images.blocks import ImageChooserBlock

from .base_blocks import BaseBlock
from .base_blocks import BaseLinkBlock
from .base_blocks import ButtonMixin
from .base_blocks import CoderedAdvTrackingSettings
from .base_blocks import LinkStructValue
from .base_blocks import BaseBlock, ButtonMixin, BaseLinkBlock, LinkStructValue, CoderedAdvTrackingSettings

class ButtonBlock(ButtonMixin, BaseLinkBlock):
    """
    A link styled as a button.
    """
    
    type_class = blocks.ChoiceBlock(
		choices=[
			('primary', 'Tipo primário'),
			('secondary', 'Tipo secundário'),
			('terciary', 'Tipo terciário'),
		],
		default='primary',
		help_text="Escolha o tipo do botão",
		label="Tipo de botão"
	)

    size_class = blocks.ChoiceBlock(
		choices=[
			('small', 'Pequeno'),
			('medium', 'Médio'),
			('large', 'Grande'),
			('extra-large', 'Extra grande'),
		],
		default='small',
		help_text="Escolha o tamanho do botão",
		label="Tamanho"
	)

    icone_bool = blocks.BooleanBlock(
        required=False,
        label=_("Icone"),
    )

    # Tentando remover campos herdados do codered
    button_style = None
    button_size = None
    page = None
    document = None
    downloadable_file = None
    class Meta:
        template = "enap_designsystem/blocks/button_block.html"
        icon = "cr-hand-pointer-o"
        label = _("Button Link")
        value_class = LinkStructValue

class DownloadBlock(ButtonMixin, BaseBlock):
    """
    Link to a file that can be downloaded.
    """

    downloadable_file = DocumentChooserBlock(
        required=False,
        label=_("Document link"),
    )

    advsettings_class = CoderedAdvTrackingSettings

    class Meta:
        template = "coderedcms/blocks/download_block.html"
        icon = "download"
        label = _("Download")
    
class ImageBlock(BaseBlock):
    """
    An <img>, by default styled responsively to fill its container.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )

    class Meta:
        template = "coderedcms/blocks/image_block.html"
        icon = "image"
        label = _("Image")

class ImageLinkBlock(BaseLinkBlock):
    """
    An <a> with an image inside it, instead of text.
    """

    image = ImageChooserBlock(
        label=_("Image"),
    )
    alt_text = blocks.CharBlock(
        max_length=255,
        required=True,
        help_text=_("Alternate text to show if the image doesn’t load"),
    )

    class Meta:
        template = "coderedcms/blocks/image_link_block.html"
        icon = "image"
        label = _("Image Link")
        value_class = LinkStructValue

class QuoteBlock(BaseBlock):
    """
    A <blockquote>.
    """

    text = blocks.TextBlock(
        required=True,
        rows=4,
        label=_("Quote Text"),
    )
    author = blocks.CharBlock(
        required=False,
        max_length=255,
        label=_("Author"),
    )

    class Meta:
        template = "coderedcms/blocks/quote_block.html"
        icon = "openquote"
        label = _("Quote")


class RichTextBlock(blocks.RichTextBlock):
    class Meta:
        template = "coderedcms/blocks/rich_text_block.html"

class PagePreviewBlock(BaseBlock):
    """
    Renders a preview of a specific page.
    """

    page = blocks.PageChooserBlock(
        required=True,
        label=_("Page to preview"),
        help_text=_("Show a mini preview of the selected page."),
    )

    class Meta:
        template = "enap_designsystem/blocks/pagepreview_block.html"
        icon = "doc-empty-inverse"
        label = _("Page Preview")



class PreviewCoursesBlock(BaseBlock):
    """
    Renders a preview of a specific page.
    """

    page = blocks.PageChooserBlock(
        required=True,
        label=_("Pagina de Formações"),
        help_text=_("Show a mini preview of the selected page."),
    )

    class Meta:
        template = "enap_designsystem/blocks/preview_courses.html"
        icon = "doc-empty-inverse"
        label = _("Pagina de Formações")





class PageListBlock(BaseBlock):
    """
    Renders a preview of selected pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    
    # DEPRECATED: Remove in 3.0
    show_preview = blocks.BooleanBlock(
        required=False,
        default=False,
        label=_("Show body preview"),
    )
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/blocks/page/pagelist_block.html"
        icon = "list-ul"
        label = _("Latest Pages")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        # try to use the CoderedPage `get_index_children()`,
        # but fall back to get_children if this is a non-CoderedPage
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
            
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context




class NewsCarouselBlock(BaseBlock):
    """
    Renders a carousel of selected news pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/blocks/page/pagenoticias_block.html"
        icon = "list-ul"
        label = _("News Carousel")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context
    

class CoursesCarouselBlock(BaseBlock):
    """
    Renders a carousel of selected news pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page’s LAYOUT tab."
        ),
    )
    
    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/blocks/card_courses.html"
        icon = "list-ul"
        label = _("News Courses")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context




class DropdownBlock(blocks.StructBlock):
    label = blocks.CharBlock(required=True)
    options = blocks.ListBlock(blocks.StructBlock([
        ('title', blocks.CharBlock(required=True)),
        ('page', blocks.PageChooserBlock(required=True))
    ]))

    class Meta:
        template = 'enap_designsystem/pages/mini/dropdown-holofote_blocks.html'
        icon = 'arrow_drop_down'
        label = 'Dropdown'




class EventsCarouselBlock(BaseBlock):
    """
    Renders a carousel of selected event pages.
    """

    indexed_by = blocks.PageChooserBlock(
        required=True,
        label=_("Parent page"),
        help_text=_(
            "Show a preview of pages that are children of the selected page. "
            "Uses ordering specified in the page's LAYOUT tab."
        ),
    )

    num_posts = blocks.IntegerBlock(
        default=3,
        label=_("Number of pages to show"),
    )

    class Meta:
        template = "enap_designsystem/pages/mini/eventos.html"
        icon = "date"
        label = _("Events Carousel")

    def get_context(self, value, parent_context=None):
        context = super().get_context(value, parent_context=parent_context)

        indexer = value["indexed_by"].specific
        
        if hasattr(indexer, "get_index_children"):
            pages = indexer.get_index_children()
        else:
            pages = indexer.get_children().live()

        context["pages"] = pages[: value["num_posts"]]
        return context
    

class CourseFeatureBlock(blocks.StructBlock):
    title_1 = blocks.CharBlock(required=True, help_text="Primeiro título da feature")
    description_1 = blocks.TextBlock(required=True, help_text="Primeira descrição da feature")
    title_2 = blocks.CharBlock(required=True, help_text="Segundo título da feature")
    description_2 = blocks.TextBlock(required=True, help_text="Segunda descrição da feature")
    image = ImageChooserBlock(required=True, help_text="Imagem da feature do curso")
    
    class Meta:
        template = "enap_designsystem/blocks/feature_course.html"
        icon = "placeholder"
        label = "Feature de Curso"



class CourseModulesBlock(blocks.StructBlock):
    """Bloco de estrutura do curso com múltiplos dropdowns."""
    title = blocks.CharBlock(required=True, default="Estrutura do curso", help_text="Título da seção")
    
    modules = blocks.ListBlock(
        blocks.StructBlock([
            # Ordem invertida - module_title é o primeiro campo agora
            ("module_title", blocks.CharBlock(required=True, help_text="Título do módulo (ex: 1º Módulo)")),
            ("module_description", blocks.TextBlock(required=True, help_text="Descrição breve do módulo")),
            ("module_items", blocks.ListBlock(
                blocks.CharBlock(required=True, help_text="Item da lista de conteúdo do módulo")
            )),
        ]),
        min_num=1,
        help_text="Adicione os módulos do curso"
    )
    
    class Meta:
        template = "enap_designsystem/blocks/feature_estrutura.html"
        icon = "list-ol"
        label = "Estrutura do Curso"




class CourseIntroTopicsBlock(StructBlock):
    """Componente com introdução e tópicos fixos do curso."""
    title = CharBlock(label="Título do Curso", required=True, help_text="Título principal sobre o curso")
    description = RichTextBlock(label="Descrição do Curso", required=True, help_text="Descrição geral do curso")
    image = ImageChooserBlock(label="Imagem", required=True, help_text="Imagem para destacar o curso")
    
    # Tópicos fixos com apenas descrições editáveis
    modalidade_description = RichTextBlock(label="Descrição da Modalidade", required=True, help_text="Descreva a modalidade do curso")
    curso_description = RichTextBlock(label="Descrição do Curso", required=True, help_text="Descreva o conteúdo do curso")
    metodologia_description = RichTextBlock(label="Descrição da Metodologia", required=True, help_text="Descreva a metodologia do curso")
    
    class Meta:
        template = 'enap_designsystem/blocks/course_intro_topics.html'
        icon = 'doc-full'
        label = 'Introdução e Tópicos do Curso'




class WhyChooseEnaptBlock(blocks.StructBlock):
    """Seção 'Por que escolher a Enap?'"""
    # Título e descrição principal
    title = blocks.CharBlock(required=True, label=_("Título principal"), default="Titulo do beneficio")
    description = blocks.TextBlock(required=False, label=_("Descrição principal"))
    
    # Benefício 1
    image_1 = ImageChooserBlock(required=False, label=_("Imagem do benefício 1"))
    title_1 = blocks.CharBlock(required=True, label=_("Título do benefício 1"), default="Metodologia ensino–aplicação")
    
    # Benefício 2
    image_2 = ImageChooserBlock(required=False, label=_("Imagem do benefício 2"))
    title_2 = blocks.CharBlock(required=True, label=_("Título do benefício 2"), default="Desenvolvimento de competências de forma inovadora")
    
    # Benefício 3
    image_3 = ImageChooserBlock(required=False, label=_("Imagem do benefício 3"))
    title_3 = blocks.CharBlock(required=True, label=_("Título do benefício 3"), default="Desenvolvimento de competências de forma inovadora")
    
    # Benefício 4
    image_4 = ImageChooserBlock(required=False, label=_("Imagem do benefício 4"))
    title_4 = blocks.CharBlock(required=True, label=_("Título do benefício 4"), default="Desenvolvimento de competências de forma inovadora")

    class Meta:
        template = 'enap_designsystem/blocks/why_choose.html'
        icon = 'placeholder'
        label = _("Titulo do beneficio")





class ProcessoSeletivoBlock(blocks.StructBlock):
    """Bloco para exibir informações sobre o processo seletivo com 3 módulos."""
    title = blocks.CharBlock(required=True, default="Processo seletivo", help_text="Título da seção")
    description = blocks.TextBlock(required=True, default="Sobre o processo seletivo", help_text="Descrição do processo seletivo")
    
    # Módulo 1
    module1_title = blocks.CharBlock(required=True, default="Inscrição", help_text="Título do primeiro módulo")
    module1_description = blocks.TextBlock(required=True, help_text="Descrição do primeiro módulo")
    
    # Módulo 2
    module2_title = blocks.CharBlock(required=True, default="Seleção", help_text="Título do segundo módulo")
    module2_description = blocks.TextBlock(required=True, help_text="Descrição do segundo módulo")
    
    # Módulo 3
    module3_title = blocks.CharBlock(required=True, default="Resultado", help_text="Título do terceiro módulo")
    module3_description = blocks.TextBlock(required=True, help_text="Descrição do terceiro módulo")
    
    class Meta:
        template = "enap_designsystem/blocks/feature_processo_seletivo.html"
        icon = "list-ul"
        label = "Processo Seletivo"




class TeamCarouselBlock(blocks.StructBlock):
    """Carrossel para exibir membros da equipe."""
    title = blocks.CharBlock(required=True, default="Nossa Equipe", help_text="Título da seção")
    description = blocks.TextBlock(required=True, help_text="Descrição da seção da equipe")
    view_all_url = blocks.URLBlock(required=False, help_text="Link para página com todos os membros")
    view_all_text = blocks.CharBlock(required=False, default="Ver todos", help_text="Texto do botão 'ver todos'")
    
    # Lista de membros diretamente no mesmo bloco
    members = blocks.ListBlock(
        blocks.StructBlock([
            ("name", blocks.CharBlock(required=True, help_text="Nome do membro da equipe")),
            ("role", blocks.CharBlock(required=True, help_text="Cargo/função do membro")),
            ("image", ImageChooserBlock(required=True, help_text="Foto do membro da equipe")),
        ]),
        help_text="Adicione os membros da equipe"
    )
    
    class Meta:
        template = 'enap_designsystem/blocks/team_carousel.html'
        icon = 'group'
        label = 'Carrossel de Equipe'




class TestimonialsCarouselBlock(blocks.StructBlock):
    """Carrossel para exibir depoimentos ou testemunhos."""
    title = blocks.CharBlock(required=True, default="Depoimentos", help_text="Título da seção")
    description = blocks.TextBlock(required=False, help_text="Descrição opcional da seção")
    
    testimonials = blocks.ListBlock(
        blocks.StructBlock([
            ("name", blocks.CharBlock(required=True, help_text="Nome da pessoa")),
            ("position", blocks.CharBlock(required=True, help_text="Cargo ou posição da pessoa")),
            ("testimonial", blocks.TextBlock(required=True, help_text="Depoimento da pessoa")),
            ("image", ImageChooserBlock(required=True, help_text="Foto da pessoa")),
        ]),
        help_text="Adicione os depoimentos"
    )
    
    class Meta:
        template = 'enap_designsystem/blocks/testimonials_carousel.html'
        icon = 'openquote'
        label = 'Carrossel de Depoimentos'