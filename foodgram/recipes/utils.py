import io
import os

from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

from django.conf import settings

    
def create_pdf(ingredients): 
    STATIC_DIR = settings.STATIC_ROOT
    INDENT = 50
    STEP = 25
    pos = 760
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer)
    pdfmetrics.registerFont(TTFont('LiberationSerif', os.path.join(
        STATIC_DIR, 'fonts/liberation-serif.ttf'), 'UTF-8'))
    p.setTitle('FoodGRAM shoplist')
    p.setFont('LiberationSerif', 20)
    p.setLineWidth(.3)
    p.drawCentredString(300, pos, 'Список покупок')
    pos -= 10
    p.line(INDENT, pos, 550, pos)
    p.setFont('LiberationSerif', 20)
    for num, item in enumerate(ingredients, 1):
        if pos < STEP * 2:
            p.showPage()
            p.setFont('LiberationSerif', 20)
            pos = 760
            count = 1
        pos -= STEP
        string = f'{item.title.capitalize():.<30}{item.summ:.>10} {item.dimension} '
        p.drawString(INDENT, pos, string)
    p.showPage()
    p.save()
    buffer.seek(0)
    return buffer