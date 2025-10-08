from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import Response
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.core.auth import get_current_user, get_current_user_optional
from app.models import Invoice, InvoiceItem, User
from app.schemas import Invoice as InvoiceSchema, InvoiceCreate, InvoiceUpdate
from app.services import InvoiceService, PDFService

router = APIRouter(prefix="/invoices", tags=["Invoices"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=InvoiceSchema, status_code=status.HTTP_201_CREATED)
def create_invoice(
    invoice: InvoiceCreate, 
    db: Session = Depends(get_db), 
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Create a new invoice with automatic calculations
    
    **WORKS FOR BOTH GUESTS AND LOGGED-IN USERS**
    
    - **customer_id**: ID of the customer to invoice (required)
    - **due_date**: Payment due date (optional, defaults to 30 days from now)
    - **status**: Invoice status (optional, defaults to 'draft')
    - **notes**: Additional notes (optional)
    - **items**: List of invoice items with description, quantity, and unit price
    
    **Authentication:**
    - **Guest users**: Can create invoices without logging in (user_id will be null)
    - **Logged-in users**: Invoice will be associated with their account for history tracking
    
    Automatically calculates:
    - Item totals (quantity × unit_price)
    - Subtotal (sum of all items)
    - Tax amount (10% of subtotal)
    - Total amount (subtotal + tax)
    - Unique invoice number (INV-XXXXXXXX)
    """
    user_info = f"user: {current_user.email}" if current_user else "guest user"
    logger.info(f"Creating invoice for customer {invoice.customer_id} by {user_info}")
    
    # Generate invoice number
    invoice_number = InvoiceService.generate_invoice_number()
    
    # Create invoice - user_id is None for guests, user.id for logged-in users
    db_invoice = Invoice(
        invoice_number=invoice_number,
        customer_id=invoice.customer_id,
        user_id=current_user.id if current_user else None,  # NULL for guest invoices
        due_date=invoice.due_date or InvoiceService.set_due_date(None),
        status=invoice.status,
        notes=invoice.notes
    )
    db.add(db_invoice)
    db.flush()
    
    # Create invoice items
    items = []
    for item_data in invoice.items:
        total_price = InvoiceService.calculate_item_total(item_data.quantity, item_data.unit_price)
        item = InvoiceItem(
            invoice_id=db_invoice.id,
            description=item_data.description,
            quantity=item_data.quantity,
            unit_price=item_data.unit_price,
            total_price=total_price,
            notes=item_data.notes
        )
        db.add(item)
        items.append(item)
    
    # Calculate totals using service
    totals = InvoiceService.calculate_invoice_totals(items)
    db_invoice.subtotal = totals["subtotal"]
    db_invoice.tax_amount = totals["tax_amount"]
    db_invoice.total_amount = totals["total_amount"]
    
    db.commit()
    db.refresh(db_invoice)
    
    invoice_type = "user invoice" if current_user else "guest invoice"
    logger.info(f"Invoice {invoice_number} created as {invoice_type} with total: {db_invoice.total_amount}")
    return db_invoice

@router.get("/", response_model=List[InvoiceSchema])
def get_invoices(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
):
    """
    Get invoice history for the authenticated user
    
    **REQUIRES LOGIN** - Only logged-in users can view their invoice history
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (max 100)
    
    Returns only invoices owned by the current user (excludes guest invoices).
    """
    logger.info(f"Fetching invoice history for user: {current_user.email}")
    return db.query(Invoice).filter(Invoice.user_id == current_user.id).offset(skip).limit(limit).all()

@router.get("/overdue", response_model=List[InvoiceSchema])
def get_overdue_invoices(
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
):
    """
    Get all overdue invoices for the authenticated user
    
    **REQUIRES LOGIN** - Only logged-in users can view their overdue invoices
    
    Returns invoices that are past their due date and not marked as paid.
    Only includes invoices owned by the current user.
    """
    logger.info(f"Fetching overdue invoices for user: {current_user.email}")
    return InvoiceService.get_overdue_invoices(db, current_user.id)

@router.get("/{invoice_id}", response_model=InvoiceSchema)
def get_invoice(
    invoice_id: int, 
    db: Session = Depends(get_db), 
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get a specific invoice by ID for viewing/downloading
    
    **WORKS FOR BOTH GUESTS AND LOGGED-IN USERS**
    
    - **invoice_id**: Unique invoice identifier
    
    **Authentication:**
    - **Guest users**: Can view any invoice by ID (for sharing/downloading)
    - **Logged-in users**: Can view any invoice by ID
    
    Returns complete invoice details including all items.
    This endpoint allows public access for invoice sharing and downloading.
    """
    user_info = f"user: {current_user.email}" if current_user else "guest user"
    logger.info(f"Fetching invoice {invoice_id} by {user_info}")
    
    # Allow any user (guest or logged-in) to view any invoice by ID
    # This enables invoice sharing and downloading without authentication
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        logger.warning(f"Invoice {invoice_id} not found")
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    return invoice

@router.get("/{invoice_id}/pdf")
def download_invoice_pdf(
    invoice_id: int,
    template: str = "modern",
    db: Session = Depends(get_db), 
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Download invoice as PDF with template selection and Supabase storage
    
    **WORKS FOR BOTH GUESTS AND LOGGED-IN USERS**
    
    - **invoice_id**: Unique invoice identifier
    - **template**: Template style (modern, classic, minimal, corporate, etc.) - defaults to modern
    
    **Authentication:**
    - **Guest users**: Can download any invoice PDF by ID (for sharing)
    - **Logged-in users**: Can download any invoice PDF by ID
    
    **Storage Logic:**
    1. Check if PDF exists in Supabase Storage for this invoice + template combination
    2. If exists, stream directly from Supabase
    3. If not exists, generate PDF using WeasyPrint, upload to Supabase, then return
    
    **Templates:**
    - **modern**: Clean and colorful design with cards
    - **classic**: Traditional business invoice style
    - **minimal**: Clean and simple typography
    - **corporate**: Professional design with elegant styling
    - **minimalist**: Ultra-clean design with simple lines
    - **gradient**: Vibrant design with modern cards
    - **formal**: Corporate letterhead with signature line
    - **bordered**: Classic design with structured layout
    - **tech**: Dark theme with gradient effects
    
    Returns PDF file for download with proper filename and content-type headers.
    """
    user_info = f"user: {current_user.email}" if current_user else "guest user"
    logger.info(f"Downloading PDF for invoice {invoice_id} with template '{template}' by {user_info}")
    
    # Validate template
    if template not in PDFService.get_available_templates():
        template = "modern"  # Default fallback
    
    # Allow any user (guest or logged-in) to download any invoice PDF by ID
    # This enables invoice PDF sharing without authentication
    invoice = db.query(Invoice).filter(Invoice.id == invoice_id).first()
    if not invoice:
        logger.warning(f"Invoice {invoice_id} not found for PDF download")
        raise HTTPException(status_code=404, detail="Invoice not found")
    
    try:
        # Initialize PDF service (includes Supabase storage)
        pdf_service = PDFService()
        
        # Get PDF from Supabase storage or generate if not exists
        # This handles the complete flow:
        # 1. Check Supabase storage for existing PDF
        # 2. If found, download and return
        # 3. If not found, generate new PDF, upload to Supabase, then return
        pdf_bytes = pdf_service.get_or_generate_pdf(invoice, template)
        
        if not pdf_bytes:
            logger.error(f"Failed to get or generate PDF for invoice {invoice_id}")
            raise HTTPException(status_code=500, detail="Failed to generate PDF")
        
        # Generate download filename
        filename = PDFService.get_invoice_filename(invoice, template)
        
        logger.info(f"PDF ready for download: invoice {invoice_id} with template '{template}'")
        
        # Return PDF as downloadable file with proper headers
        return Response(
            content=pdf_bytes,
            media_type="application/pdf",
            headers={
                "Content-Disposition": f"attachment; filename={filename}",
                "Content-Type": "application/pdf"
            }
        )
        
    except Exception as e:
        logger.error(f"Failed to process PDF for invoice {invoice_id}: {str(e)}")
        raise HTTPException(status_code=500, detail="Failed to generate PDF")

@router.get("/templates")
def get_available_templates():
    """
    Get list of available invoice templates
    
    **WORKS FOR BOTH GUESTS AND LOGGED-IN USERS**
    
    Returns dictionary of available templates with descriptions.
    """
    return PDFService.get_available_templates()

@router.put("/{invoice_id}", response_model=InvoiceSchema)
def update_invoice(
    invoice_id: int, 
    invoice_update: InvoiceUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
):
    """
    Update an existing invoice
    
    **REQUIRES LOGIN** - Only logged-in users can update their invoices
    
    - **invoice_id**: Unique invoice identifier
    - **customer_id**: New customer ID (optional)
    - **due_date**: New due date (optional)
    - **status**: New status (optional)
    - **notes**: New notes (optional)
    
    Only the owner of the invoice can update it.
    Guest invoices cannot be updated.
    """
    logger.info(f"Updating invoice {invoice_id} for user: {current_user.email}")
    
    # Only allow users to update their own invoices
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id, 
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found or not owned by user")
    
    for field, value in invoice_update.dict(exclude_unset=True).items():
        setattr(invoice, field, value)
    
    db.commit()
    db.refresh(invoice)
    
    logger.info(f"Invoice {invoice_id} updated successfully")
    return invoice

@router.put("/{invoice_id}/mark-paid", response_model=InvoiceSchema)
def mark_invoice_paid(
    invoice_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
):
    """
    Mark an invoice as paid
    
    **REQUIRES LOGIN** - Only logged-in users can mark their invoices as paid
    
    - **invoice_id**: Unique invoice identifier
    
    Only the owner of the invoice can mark it as paid.
    Guest invoices cannot be marked as paid.
    """
    logger.info(f"Marking invoice {invoice_id} as paid for user: {current_user.email}")
    
    # Only allow users to mark their own invoices as paid
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id, 
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found or not owned by user")
    
    result = InvoiceService.mark_as_paid(invoice, db)
    logger.info(f"Invoice {invoice_id} marked as paid")
    return result

@router.delete("/{invoice_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_invoice(
    invoice_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
):
    """
    Delete an invoice
    
    **REQUIRES LOGIN** - Only logged-in users can delete their invoices
    
    - **invoice_id**: Unique invoice identifier
    
    Only the owner of the invoice can delete it.
    Guest invoices cannot be deleted through this endpoint.
    """
    logger.info(f"Deleting invoice {invoice_id} for user: {current_user.email}")
    
    # Only allow users to delete their own invoices
    invoice = db.query(Invoice).filter(
        Invoice.id == invoice_id, 
        Invoice.user_id == current_user.id
    ).first()
    
    if not invoice:
        raise HTTPException(status_code=404, detail="Invoice not found or not owned by user")
    
    db.delete(invoice)
    db.commit()
    
    logger.info(f"Invoice {invoice_id} deleted successfully")
    return {"message": "Invoice deleted successfully"}
