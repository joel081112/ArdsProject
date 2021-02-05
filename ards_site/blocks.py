"""StreamFields live in here"""

from wagtail.core import blocks
from wagtail.core.blocks import CharBlock
from wagtail.embeds.blocks import EmbedBlock
from wagtail.images.blocks import ImageChooserBlock
from wagtail.documents.blocks import DocumentChooserBlock


class TitleAndTextBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.TextBlock(required=True, help_text="Add your additional")

    class Meta:
        template = "title_and_text_block.html"
        icon = "edit"
        label = "Title & Text"


class LocationCardBlock(blocks.StructBlock):
    city = blocks.CharBlock(required=True, help_text="Add your City")
    addressLines = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("addressLine", blocks.TextBlock(required=True, max_length=100)),
            ]
        )
    )
    daysOpen = blocks.TextBlock(required=True, max_length=100, help_text="Eg Monday - Friday")
    timeOpen = blocks.TextBlock(required=True, max_length=100, help_text="Eg 9am - 5pm")
    telephoneNumber = blocks.TextBlock(required=False, max_length=100, help_text="Eg tel: +44(0)28 9034 2655")
    websiteLink = blocks.RichTextBlock(required=False, max_length=100, help_text="Eg Web: www.fortaxa.pl")

    class Meta:
        template = "location_card_block.html"
        icon = "edit"
        label = "Location Cards"


class CardBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add your title")
    image = ImageChooserBlock(required=False, help_text="Add your Image")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("document", DocumentChooserBlock(required=True))
            ]
        )
    )

    class Meta:
        template = "card_block.html"
        icon = "edit"
        label = "Product Cards"


class ArticleBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add your title")
    info = blocks.RichTextBlock(required=True)
    document = DocumentChooserBlock(help_text="Choose a related document")

    class Meta:
        template = "article_block.html"
        icon = "edit"
        label = "Article"


class ImageTextsBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, help_text="Add your Image")
    title = blocks.CharBlock(required=True, help_text="Add your title")

    card = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("info", blocks.RichTextBlock(required=True, max_length=300)),
            ]
        )
    )

    class Meta:
        template = "timeline_block.html"
        icon = "edit"
        label = "Extra Timeline"


class ImageTextBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=False, help_text="Add your Image")
    title = blocks.CharBlock(required=True, help_text="Add your title")
    text = blocks.CharBlock(required=True, help_text="Add your detail")

    class Meta:
        template = "image_text_block.html"
        icon = "edit"
        label = "Image and Text"


class QuestionBlock(blocks.StructBlock):
    title = blocks.CharBlock(required=True, help_text="Add your main title")

    cards = blocks.ListBlock(
        blocks.StructBlock(
            [
                ("question", blocks.CharBlock(require=True, max_length=100)),
                ("answer", blocks.RichTextBlock(required=True, max_length=300)),
            ]
        )
    )

    class Meta:
        template = "question_block.html"
        icon = "edit"
        label = "New Question"


class ButtonLinksBlock(blocks.StructBlock):
    image = ImageChooserBlock(required=True, help_text="Link header image")
    title = blocks.CharBlock(require=True, max_length=40, help_text="Link title")
    text = blocks.TextBlock(required=True, max_length=400, help_text="Link overview")
    button_page = blocks.PageChooserBlock(required=False, help_text="Internal page link")
    button_url = blocks.URLBlock(required=False, help_text="If the button page is selected, "
                                                           "will be used first (external)")

    class Meta:
        template = "button_links_block.html"
        icon = "edit"
        label = "New link"


class InlineVideoBlock(blocks.StructBlock):
    video = EmbedBlock()
    caption = CharBlock(required=False, label="Caption")
    float = blocks.ChoiceBlock(
        required=False,
        choices=[('right', "Right"), ('left', "Left"), ('Center', "Center")],
        default='center',
        label="Float",
    )
    size = blocks.ChoiceBlock(
        required=False,
        choices=[('small', "Small"), ('medium', "Medium"), ('large', "Large")],
        default='medium',
        label="Size",
    )

    class Meta:
        icon = 'media'
