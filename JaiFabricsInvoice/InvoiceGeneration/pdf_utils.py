"""Server-side invoice PDF generation.

Renders the same invoice data as bill.html, but via reportlab instead
of capturing a browser's rendered DOM. This is deliberate: a browser
capture (html2canvas) produces different output depending on the
device's viewport, fonts, and zoom - exactly what made the PDF look
different on phone vs PC. Building the PDF directly from fixed
coordinates/fonts in Python guarantees identical bytes regardless of
what device or browser requested it.
"""

from io import BytesIO

from django.utils.formats import date_format

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import mm
from reportlab.platypus import (
    SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, HRFlowable,
)

BRAND_BLUE = colors.HexColor('#3989c6')
INK = colors.HexColor('#222222')
MUTED = colors.HexColor('#555555')

COMPANY_NAME = 'JAI FABRICS'
COMPANY_ADDRESS = '1803 Neptune CHS DN NAGAR Andheri West'
COMPANY_MOBILE = 'Mobile Number: 9322970238'
COMPANY_EMAIL = 'EMAIL: ashokparmani@gmail.com'
COMPANY_GSTIN = 'GSTIN: 27ACCPP6615Q1Z0'

BANK_NAME = 'APNA SAHAKARI BANK LTD.'
BANK_BRANCH = 'ANDHERI(WEST)'
BANK_ACCOUNT_NO = '007012100003298'
BANK_IFSC = 'ASBL0000007'

NOTICE_TEXT = 'A finance charge of 1.5% will be made on unpaid balances after 30 days.'
AUTH_TEXT = 'Invoice was created on a computer and is not valid without the signature.'


def _styles():
    return {
        'name': ParagraphStyle('name', fontName='Helvetica-Bold', fontSize=18, textColor=INK, leading=22),
        'body': ParagraphStyle('body', fontName='Helvetica', fontSize=10, textColor=INK, leading=14),
        'label': ParagraphStyle('label', fontName='Helvetica', fontSize=9, textColor=MUTED, leading=12),
        'value_lg': ParagraphStyle('value_lg', fontName='Helvetica-Bold', fontSize=13, textColor=INK, leading=16),
        'invoice_id': ParagraphStyle('invoice_id', fontName='Helvetica-Bold', fontSize=12, textColor=BRAND_BLUE, leading=15, alignment=2),
        'right_body': ParagraphStyle('right_body', fontName='Helvetica', fontSize=10, textColor=INK, leading=14, alignment=2),
        'right_label': ParagraphStyle('right_label', fontName='Helvetica-Bold', fontSize=10, textColor=INK, leading=14, alignment=2),
        'th': ParagraphStyle('th', fontName='Helvetica-Bold', fontSize=9, textColor=INK),
        'th_right': ParagraphStyle('th_right', fontName='Helvetica-Bold', fontSize=9, textColor=INK, alignment=2),
        'td': ParagraphStyle('td', fontName='Helvetica', fontSize=10, textColor=BRAND_BLUE),
        'td_right': ParagraphStyle('td_right', fontName='Helvetica', fontSize=10, textColor=INK, alignment=2),
        'foot_label': ParagraphStyle('foot_label', fontName='Helvetica', fontSize=10, textColor=INK, alignment=2),
        'foot_value': ParagraphStyle('foot_value', fontName='Helvetica', fontSize=10, textColor=INK, alignment=2),
        'grand_label': ParagraphStyle('grand_label', fontName='Helvetica-Bold', fontSize=11, textColor=BRAND_BLUE, alignment=2),
        'grand_value': ParagraphStyle('grand_value', fontName='Helvetica-Bold', fontSize=11, textColor=BRAND_BLUE, alignment=2),
        'words': ParagraphStyle('words', fontName='Helvetica', fontSize=10, textColor=INK, leading=14),
        'bank_title': ParagraphStyle('bank_title', fontName='Helvetica-Bold', fontSize=10, textColor=INK, alignment=1),
        'bank_body': ParagraphStyle('bank_body', fontName='Helvetica', fontSize=10, textColor=INK, alignment=1, leading=14),
        'notice_title': ParagraphStyle('notice_title', fontName='Helvetica-Bold', fontSize=9, textColor=INK),
        'notice_body': ParagraphStyle('notice_body', fontName='Helvetica', fontSize=9, textColor=INK),
        'signature': ParagraphStyle('signature', fontName='Helvetica-Bold', fontSize=13, textColor=BRAND_BLUE, alignment=2),
        'auth': ParagraphStyle('auth', fontName='Helvetica', fontSize=9, textColor=INK, alignment=2),
        'small_center': ParagraphStyle('small_center', fontName='Helvetica', fontSize=8, textColor=MUTED, alignment=1),
    }


def build_invoice_pdf(context):
    """context is the same dict getSaleBill passes to bill.html."""
    styles = _styles()
    buf = BytesIO()
    doc = SimpleDocTemplate(
        buf, pagesize=A4,
        leftMargin=18 * mm, rightMargin=18 * mm,
        topMargin=16 * mm, bottomMargin=16 * mm,
    )
    content_width = doc.width
    story = []

    # ---- Header: company details (left) / invoice number+date (right) ----
    company_block = [
        Paragraph(COMPANY_NAME, styles['name']),
        Paragraph(COMPANY_ADDRESS, styles['body']),
        Paragraph(COMPANY_MOBILE, styles['body']),
        Paragraph(COMPANY_EMAIL, styles['body']),
        Paragraph(COMPANY_GSTIN, styles['body']),
    ]
    invoice_meta_block = [
        Paragraph('Invoice Number: {}'.format(context['invoiceNumber']), styles['invoice_id']),
        Spacer(1, 3),
        Paragraph('Invoice Date: {}'.format(date_format(context['invoiceDate'])), styles['right_body']),
    ]
    header_table = Table(
        [[company_block, invoice_meta_block]],
        colWidths=[content_width * 0.6, content_width * 0.4],
    )
    header_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(header_table)
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width='100%', thickness=1, color=BRAND_BLUE))
    story.append(Spacer(1, 12))

    # ---- Invoice To (left) / Transport Details (right) ----
    invoice_to_block = [
        Paragraph('INVOICE TO:', styles['label']),
        Paragraph(context['customerName'], styles['value_lg']),
        Spacer(1, 4),
        Paragraph('GST: {}'.format(context['custGST']), styles['body']),
        Spacer(1, 4),
        Paragraph('Address: {}'.format(context['custAddress1']), styles['body']),
        Paragraph(context['custAddress2'], styles['body']),
    ]
    transport_block = [
        Paragraph('Transport Details:', styles['right_label']),
        Paragraph(context['TransportName'] or '-', styles['right_body']),
        Paragraph('{}: {}'.format(context['choice'], context['choiceInfo']), styles['right_body']),
        Paragraph('LR Number: {}'.format(context['lrno']), styles['right_body']),
    ]
    contacts_table = Table(
        [[invoice_to_block, transport_block]],
        colWidths=[content_width * 0.6, content_width * 0.4],
    )
    contacts_table.setStyle(TableStyle([
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('LEFTPADDING', (0, 0), (-1, -1), 0),
        ('RIGHTPADDING', (0, 0), (-1, -1), 0),
    ]))
    story.append(contacts_table)
    story.append(Spacer(1, 16))

    # ---- Item table ----
    item = context['finalList'][0]
    item_name, quantity, price_per_unit, line_total = item[0], item[1], item[2], item[3]

    rows = [[
        Paragraph('DESCRIPTION', styles['th']),
        Paragraph('HSN CODE', styles['th']),
        Paragraph('QUANTITY', styles['th_right']),
        Paragraph('Price(per unit)', styles['th_right']),
        Paragraph('TOTAL', styles['th_right']),
    ], [
        Paragraph(str(item_name), styles['td']),
        Paragraph(str(context['HSN_CODE']), styles['td_right']),
        Paragraph(str(quantity), styles['td_right']),
        Paragraph(str(price_per_unit), styles['td_right']),
        Paragraph(str(line_total), styles['td_right']),
    ]]

    gst_type = context['GSTType']
    gst_pct = context['GSTPERCENTAGE']
    tax = context['tax']

    def _foot_row(label, value):
        return [
            '', '',
            Paragraph(label, styles['foot_label']),
            '',
            Paragraph(str(value), styles['foot_value']),
        ]

    rows.append(_foot_row('SUBTOTAL', context['subtotal']))
    if gst_type == 'IGST':
        rows.append(_foot_row('TAX {}%(IGST)'.format(gst_pct), tax))
    else:
        half_tax = round(float(tax) / 2, 2)
        rows.append(_foot_row('TAX {}%(CGST)'.format(gst_pct), half_tax))
        rows.append(_foot_row('TAX {}%(SGST)'.format(gst_pct), half_tax))

    grand_total_row = [
        '', '',
        Paragraph('GRAND TOTAL', styles['grand_label']),
        '',
        Paragraph(str(context['total']), styles['grand_value']),
    ]
    rows.append(grand_total_row)

    col_widths = [
        content_width * 0.26, content_width * 0.16,
        content_width * 0.18, content_width * 0.20, content_width * 0.20,
    ]
    item_table = Table(rows, colWidths=col_widths, repeatRows=1)
    n_foot_rows = len(rows) - 2  # exclude header + item row
    style = [
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('LINEBELOW', (0, 0), (-1, 0), 1, colors.HexColor('#dddddd')),
        ('LINEBELOW', (0, 1), (-1, 1), 1, colors.HexColor('#dddddd')),
        ('SPAN', (2, 2), (3, 2)),
        ('LINEABOVE', (2, -1), (-1, -1), 1, BRAND_BLUE),
    ]
    for i in range(2, len(rows) - 1):
        style.append(('SPAN', (2, i), (3, i)))
    style.append(('SPAN', (2, len(rows) - 1), (3, len(rows) - 1)))
    item_table.setStyle(TableStyle(style))
    story.append(item_table)
    story.append(Spacer(1, 14))

    # ---- Value in words ----
    story.append(Paragraph(
        'Value in Words: <b>{}</b>'.format(context['totalFigure']), styles['words']
    ))
    story.append(Spacer(1, 14))

    # ---- Bank details box ----
    bank_table = Table([
        [Paragraph('Bank Details:', styles['bank_title'])],
        [Paragraph(
            'BANK NAME: <b>{}</b> BRANCH: {}<br/>A/C NO: {} IFSC CODE: {}'.format(
                BANK_NAME, BANK_BRANCH, BANK_ACCOUNT_NO, BANK_IFSC
            ),
            styles['bank_body'],
        )],
    ], colWidths=[content_width])
    bank_table.setStyle(TableStyle([
        ('BOX', (0, 0), (-1, -1), 1, colors.black),
        ('TOPPADDING', (0, 0), (-1, -1), 8),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(bank_table)
    story.append(Spacer(1, 12))

    # ---- Notice ----
    notice_table = Table([[
        Paragraph('NOTICE:<br/>{}'.format(NOTICE_TEXT), styles['notice_body']),
    ]], colWidths=[content_width])
    notice_table.setStyle(TableStyle([
        ('LINEBEFORE', (0, 0), (0, 0), 3, BRAND_BLUE),
        ('LEFTPADDING', (0, 0), (-1, -1), 8),
    ]))
    story.append(notice_table)
    story.append(Spacer(1, 20))

    # ---- Signature ----
    story.append(Paragraph(COMPANY_NAME, styles['signature']))
    story.append(Spacer(1, 24))
    story.append(Paragraph('Authorised Signatory', styles['auth']))
    story.append(Spacer(1, 10))
    story.append(Paragraph(AUTH_TEXT, styles['small_center']))

    doc.build(story)
    return buf.getvalue()
