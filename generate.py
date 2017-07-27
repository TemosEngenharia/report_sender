#!/opt/virtualenvs/report_sender/bin/python
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from os.path import basename
import base64
import smtplib

import odoorpc

import PyPDF2 as pypdf2

# Gerar report
odoo = odoorpc.ODOO('localhost', port = 8069)
odoo.login('odoo_prd', 'admin', 'tw28()KPvp+-45XW')

mco = odoo.env['mcorretiva.mco_form']
mco_ids = mco.search([('mco_form_report_flag', '=', False)])

for _id in mco_ids:
    _posto_cod = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_task_customer_number']
        )[0]['mco_task_customer_number']

    _posto_name = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_task_customer_name']
        )[0]['mco_task_customer_name']

    _report_name = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_form_name']
        )[0]['mco_form_name']

    _inc_number = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_task_request_number']
        )[0]['mco_task_request_number']

    _inc_date_time = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_form_date_time']
        )[0]['mco_form_date_time']
    _inc_date = _inc_date_time.split(' ')[0].split('-')
    _inc_time = _inc_date_time.split(' ')[1].split(':')
    inc_date_time = "%s%s%s_%s%s%s" % (_inc_date[0], _inc_date[1], _inc_date[2],
        _inc_time[0], _inc_time[1], _inc_time[2])

    _pista1 = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_form_station_first_line_flag']
        )[0]['mco_form_station_first_line_flag']
    _pista2 = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_form_station_sec_line_flag']
        )[0]['mco_form_station_sec_line_flag']
    _server = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_form_station_server_flag']
        )[0]['mco_form_station_server_flag']
    _teto = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_form_station_roof_flag']
        )[0]['mco_form_station_roof_flag']
    _equip = odoo.execute('mcorretiva.mco_form', 'read', [_id], ['mco_form_station_equipment_flag']
        )[0]['mco_form_station_equipment_flag']

    report = pypdf2.PdfFileWriter()

    r_capa = pypdf2.PdfFileReader(odoo.report.download('mcor_capa', [_id]))
    report.appendPagesFromReader(r_capa)

    r_resumo = pypdf2.PdfFileReader(odoo.report.download('mcor_resumo', [_id]))
    report.appendPagesFromReader(r_resumo)

    r_posto = pypdf2.PdfFileReader(odoo.report.download('mcor_posto', [_id]))
    report.appendPagesFromReader(r_posto)

    if _pista1 == 1 or _pista2 == 1:
        r_pistas = pypdf2.PdfFileReader(odoo.report.download('mcor_pistas', [_id]))
        report.appendPagesFromReader(r_pistas)

    if _server == 1:
        r_servidor = pypdf2.PdfFileReader(odoo.report.download('mcor_servidor', [_id]))
        report.appendPagesFromReader(r_servidor)

    if _equip == 1:
        r_equipamentos = pypdf2.PdfFileReader(odoo.report.download('mcor_equipamentos', [_id]))
        report.appendPagesFromReader(r_equipamentos)

    filename = '/opt/files/reports/mco/MCO_%s_%s_%s.pdf' % (inc_date_time, _posto_cod, _inc_number)
    with open(filename, 'wb') as pdf_file:
        report.write(pdf_file)

    mco.write([_id], {'mco_form_report_flag': True})
