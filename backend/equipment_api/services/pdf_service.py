from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer, Image
from reportlab.lib.units import inch
import matplotlib
matplotlib.use('Agg')  # non-GUI backend
import matplotlib.pyplot as plt
import io
from datetime import datetime


class PDFService:
    """Generate PDF reports with charts and summary"""
    
    def generate_report(self, dataset):
        """
        Create PDF report for a dataset
        Returns: BytesIO buffer with PDF content
        """
        buffer = io.BytesIO()
        doc = SimpleDocTemplate(buffer, pagesize=letter)
        elements = []
        styles = getSampleStyleSheet()
        
        # title
        title = Paragraph(f"<b>Equipment Data Report</b>", styles['Title'])
        elements.append(title)
        elements.append(Spacer(1, 0.3*inch))
        
        # metadata
        meta_text = f"""
        <b>Filename:</b> {dataset.filename}<br/>
        <b>Upload Date:</b> {dataset.uploaded_at.strftime('%Y-%m-%d %H:%M:%S')}<br/>
        <b>Total Equipment:</b> {dataset.total_equipment}
        """
        elements.append(Paragraph(meta_text, styles['Normal']))
        elements.append(Spacer(1, 0.3*inch))
        
        # summary stats table
        summary_data = [
            ['Metric', 'Value'],
            ['Average Flowrate', f"{dataset.avg_flowrate:.2f}"],
            ['Average Pressure', f"{dataset.avg_pressure:.2f}"],
            ['Average Temperature', f"{dataset.avg_temperature:.2f}"],
        ]
        
        summary_table = Table(summary_data, colWidths=[3*inch, 2*inch])
        summary_table.setStyle(TableStyle([
            ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
            ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
            ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
            ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
            ('FONTSIZE', (0, 0), (-1, 0), 12),
            ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
            ('BACKGROUND', (0, 1), (-1, -1), colors.beige),
            ('GRID', (0, 0), (-1, -1), 1, colors.black)
        ]))
        
        elements.append(summary_table)
        elements.append(Spacer(1, 0.5*inch))
        
        # generate chart and add to PDF
        chart_buffer = self._create_type_distribution_chart(dataset.type_distribution)
        if chart_buffer:
            img = Image(chart_buffer, width=5*inch, height=3*inch)
            elements.append(Paragraph("<b>Equipment Type Distribution</b>", styles['Heading2']))
            elements.append(Spacer(1, 0.2*inch))
            elements.append(img)
        
        # build PDF
        doc.build(elements)
        buffer.seek(0)
        return buffer
    
    def _create_type_distribution_chart(self, type_dist):
        """Create bar chart for equipment type distribution"""
        try:
            fig, ax = plt.subplots(figsize=(8, 5))
            types = list(type_dist.keys())
            counts = list(type_dist.values())
            
            ax.bar(types, counts, color='steelblue')
            ax.set_xlabel('Equipment Type')
            ax.set_ylabel('Count')
            ax.set_title('Equipment Type Distribution')
            plt.xticks(rotation=45, ha='right')
            plt.tight_layout()
            
            # save to buffer
            buffer = io.BytesIO()
            plt.savefig(buffer, format='png', dpi=100)
            buffer.seek(0)
            plt.close()
            
            return buffer
        except Exception as e:
            print(f"Error creating chart: {e}")
            return None
