import os
from datetime import datetime
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib import styles

def generate_report(condition, confidence, recommendations):
    os.makedirs("static/reports", exist_ok=True)
    doc = SimpleDocTemplate(
        os.path.join("static", "reports", "report.pdf")
    )

    style = styles.getSampleStyleSheet()
    content = []
    generated_at = datetime.now().strftime("%B %d, %Y %I:%M %p")

    content.append(
        Paragraph(
            "Skin Analysis Report",
            style['Title']
        )
    )
    content.append(Spacer(1, 18))
    content.append(
        Paragraph(
            f"Generated: {generated_at}",
            style['Normal']
        )
    )
    content.append(Spacer(1, 14))
    content.append(
        Paragraph(
            f"Detected Skin Type: {condition}",
            style['Heading2']
        )
    )
    content.append(Spacer(1, 10))
    content.append(
        Paragraph(
            f"Confidence score: {confidence}%",
            style['Normal']
        )
    )
    content.append(Spacer(1, 20))
    content.append(
        Paragraph(
            "Analysis Summary:",
            style['Heading3']
        )
    )
    content.append(Spacer(1, 8))
    content.append(
        Paragraph(
            recommendations.get('description', "No summary available."),
            style['Normal']
        )
    )
    content.append(Spacer(1, 18))
    content.append(
        Paragraph(
            "Recommended Products:",
            style['Heading3']
        )
    )
    content.append(Spacer(1, 8))

    for product in recommendations.get('products', []):
        content.append(
            Paragraph(
                f"• {product}",
                style['Bullet']
            )
        )
        content.append(Spacer(1, 6))

    content.append(Spacer(1, 18))
    content.append(
        Paragraph(
            "Suggested Skincare Routine:",
            style['Heading3']
        )
    )
    content.append(Spacer(1, 8))

    for step in recommendations.get('routine', []):
        content.append(
            Paragraph(
                f"• {step}",
                style['Bullet']
            )
        )
        content.append(Spacer(1, 6))

    content.append(Spacer(1, 18))
    content.append(
        Paragraph(
            "What to Avoid:",
            style['Heading3']
        )
    )
    content.append(Spacer(1, 8))

    for avoid_item in recommendations.get('avoid', []):
        content.append(
            Paragraph(
                f"• {avoid_item}",
                style['Bullet']
            )
        )
        content.append(Spacer(1, 6))

    doc.build(content)
