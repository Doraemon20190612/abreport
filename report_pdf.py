
from reportlab.lib import colors
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import Paragraph, SimpleDocTemplate, Table, LongTable, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.enums import TA_JUSTIFY
import os
import datetime


pdfmetrics.registerFont(TTFont('SimSun', 'Simsun.ttc'))
pdfmetrics.registerFont(TTFont('SimSunBd', 'SimSun-bold.ttf'))

stylesheet = getSampleStyleSheet()

Normal = stylesheet['Normal']
BodyText = stylesheet['BodyText']
Italic = stylesheet['Italic']
Title = stylesheet['Title']
Heading1 = stylesheet['Heading1']
Heading2 = stylesheet['Heading2']
Heading3 = stylesheet['Heading3']
Heading4 = stylesheet['Heading4']
Heading5 = stylesheet['Heading5']
Heading6 = stylesheet['Heading6']
Bullet = stylesheet['Bullet']
Definition = stylesheet['Definition']
Code = stylesheet['Code']

Normal.fontName = 'SimSun'
BodyText.fontName = 'SimSun'
Italic.fontName = 'SimSun'
Title.fontName = 'SimSunBd'
Heading1.fontName = 'SimSun'
Heading2.fontName = 'SimSun'
Heading3.fontName = 'SimSun'
Heading4.fontName = 'SimSun'
Heading5.fontName = 'SimSun'
Heading6.fontName = 'SimSun'
Bullet.fontName = 'SimSun'
Definition.fontName = 'SimSun'
Code.fontName = 'SimSun'

stylesheet.add(
    ParagraphStyle(
        name='body',
        fontName='SimSun',
        fontSize=12,
        textColor='black',
        leading=20,
        spaceBefore=10,
        spaceAfter=10,
        leftIndent=0,
        rightIndent=0,
        firstLineIndent=0,
        alignment=TA_JUSTIFY
    )
)


def pretest_pdf(
        aa_start_date, aa_end_date, aa_ctr, indicator_vol1_s2, indicator_vol2_s2,
        aa_diff_stat, aa_diff_p, aa_diff_ci95,
        min_n_base, min_n_1, min_n_2, min_n_3, test_days_base, test_days_1, test_days_2, test_days_3,
        pdf_title='搜索pretest报告'
):

    body = stylesheet['body']

    story = []

    table_style = [
        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.1, colors.black)
    ]

    table_data1 = [
        ['历史采样周期', '%s~%s' % (aa_start_date, aa_end_date)],
        ['历史采样周期内CTR', '%s' % aa_ctr],
        ['20%样本量基于bootstrap抽样95%容许区间', '%s' % indicator_vol1_s2],
        ['20%样本量基于bootstrap抽样95%百分位数区间', '%s' % indicator_vol2_s2]
    ]
    table_data2 = [
        ['100%样本量AA实验差值统计量', '%s' % aa_diff_stat],
        ['100%样本量AA实验差值P值', '%s' % aa_diff_p],
        ['100%样本量AA实验差值95%置信区间', '%s' % aa_diff_ci95]
    ]
    table_data3 = [
        ['指标预期提升幅度', '理论最小样本量', '实验组10%流量测试最小天数'],
        ['50%样本量最小提升幅度', '%s' % min_n_base, '%s' % test_days_base],
        ['1%提升差值', '%s' % min_n_1, '%s' % test_days_1],
        ['2%提升差值', '%s' % min_n_2, '%s' % test_days_2],
        ['3%提升差值', '%s' % min_n_3, '%s' % test_days_3]
    ]

    table1 = Table(data=table_data1, style=table_style, colWidths=250)
    table2 = Table(data=table_data2, style=table_style, colWidths=250)
    table3 = Table(data=table_data3, style=table_style, colWidths=166.66)

    story.append(Paragraph(pdf_title, Title))
    story.append(Paragraph('1.指标波动范围', Heading2))
    story.append(table1)
    story.append(Paragraph('2.AA实验结果', Heading2))
    story.append(table2)
    story.append(Paragraph('3.样本量及实验周期估算', Heading2))
    story.append(table3)

    doc = SimpleDocTemplate(os.path.dirname(__file__) + '/pdf/%s%s.pdf' % (pdf_title,  (datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))))

    doc.build(story)

    print('报告导出地址为:',os.path.dirname(__file__) + '/pdf/%s%s.pdf' % (pdf_title, (datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))))


def posttest_pdf(
        ab_start_date, ab_end_date, ab_groupname1, ab_groupname2,
        ab_diff, ab_diff_stat, ab_diff_p, ab_diff_ci, pdf_title='搜索posttest报告', abaa_name='AB'
):

    body = stylesheet['body']

    story = []

    table_style = [
        ('FONTNAME', (0, 0), (-1, -1), 'SimSun'),
        ('FONTSIZE', (0, 0), (-1, 0), 10),
        ('FONTSIZE', (0, 1), (-1, -1), 10),
        ('ALIGN', (0, 0), (-1, -1), 'LEFT'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('GRID', (0, 0), (-1, -1), 0.1, colors.black)
    ]
    table_data = [
        ['%s实验周期' % abaa_name, '%s~%s' % (ab_start_date, ab_end_date)],
        ['%s实验%s组与%s组差值' % (abaa_name, ab_groupname1, ab_groupname2), '%s' % ab_diff],
        ['%s实验差值统计量' % abaa_name, '%s' % ab_diff_stat],
        ['%s实验差值P值' % abaa_name, '%s' % ab_diff_p],
        ['{0}实验差值95%置信区间'.format(abaa_name), '%s' % ab_diff_ci]
    ]

    if ab_diff_p > 0.05:
        content = "<font name='SimSunBd'>结论:在alpha=0.05的水准下,实验组和对照组的差异不具有统计学意义。</font>"
    else:
        content = "<font name='SimSunBd'>结论:在alpha=0.05的水准下,实验组和对照组的差异具有统计学意义。</font>"

    table = Table(data=table_data, style=table_style, colWidths=250)
    story.append(Paragraph(pdf_title, Title))
    story.append(table)
    story.append(Paragraph(content, body))

    doc = SimpleDocTemplate(os.path.dirname(__file__) + '/pdf/%s%s.pdf' % (pdf_title, (datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))))

    doc.build(story)

    print('报告导出地址为:', os.path.dirname(__file__) + '/pdf/%s%s.pdf' % (pdf_title,  (datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S'))))




