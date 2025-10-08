from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app.core.database import get_db
from app.core.auth import get_current_user, get_current_user_optional
from app.models import Customer, User, Invoice
from app.schemas import Customer as CustomerSchema, CustomerCreate, CustomerUpdate, Invoice as InvoiceSchema

router = APIRouter(prefix="/customers", tags=["Customers"])
logger = logging.getLogger(__name__)

@router.post("/", response_model=CustomerSchema, status_code=status.HTTP_201_CREATED)
def create_customer(
    customer: CustomerCreate, 
    db: Session = Depends(get_db), 
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Create a new customer
    
    **WORKS FOR BOTH GUESTS AND LOGGED-IN USERS**
    
    - **name**: Customer's full name (required)
    - **email**: Customer's email address (required, must be valid)
    - **address**: Customer's address (optional)
    - **phone**: Customer's phone number (optional)
    
    **Authentication:**
    - **Guest users**: Can create customers for invoice creation (user_id will be null)
    - **Logged-in users**: Customer will be associated with their account for management
    
    Returns the created customer with assigned ID.
    """
    user_info = f"user: {current_user.email}" if current_user else "guest user"
    logger.info(f"Creating customer: {customer.name} by {user_info}")
    
    # Create customer - user_id is None for guests, user.id for logged-in users
    db_customer = Customer(
        **customer.dict(), 
        user_id=current_user.id if current_user else None  # NULL for guest customers
    )
    db.add(db_customer)
    db.commit()
    db.refresh(db_customer)
    
    customer_type = "user customer" if current_user else "guest customer"
    logger.info(f"Customer created as {customer_type} with ID: {db_customer.id}")
    return db_customer

@router.get("/", response_model=List[CustomerSchema])
def get_customers(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
):
    """
    Get all customers for the authenticated user
    
    **REQUIRES LOGIN** - Only logged-in users can view their customer list
    
    - **skip**: Number of records to skip (pagination)
    - **limit**: Maximum number of records to return (max 100)
    
    Returns list of customers owned by the current user (excludes guest customers).
    """
    logger.info(f"Fetching customers for user: {current_user.email}")
    return db.query(Customer).filter(Customer.user_id == current_user.id).offset(skip).limit(limit).all()

@router.get("/{customer_id}", response_model=CustomerSchema)
def get_customer(
    customer_id: int, 
    db: Session = Depends(get_db), 
    current_user: Optional[User] = Depends(get_current_user_optional)
):
    """
    Get a specific customer by ID
    
    **WORKS FOR BOTH GUESTS AND LOGGED-IN USERS**
    
    - **customer_id**: Unique customer identifier
    
    **Authentication:**
    - **Guest users**: Can view any customer by ID (for invoice creation/viewing)
    - **Logged-in users**: Can view any customer by ID
    
    Returns customer details if found. Allows public access for invoice workflows.
    """
    user_info = f"user: {current_user.email}" if current_user else "guest user"
    logger.info(f"Fetching customer {customer_id} by {user_info}")
    
    # Allow any user (guest or logged-in) to view any customer by ID
    # This enables customer info access during invoice creation and viewing
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        logger.warning(f"Customer {customer_id} not found")
        raise HTTPException(status_code=404, detail="Customer not found")
    return customer

@router.get("/{customer_id}/invoices", response_model=List[InvoiceSchema])
def get_customer_invoices(
    customer_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Get all invoices for a specific customer
    
    **REQUIRES LOGIN** - Only logged-in users can view customer invoice history
    
    - **customer_id**: Unique customer identifier
    
    Returns list of all invoices for the specified customer, ordered by creation date (newest first).
    Only returns invoices owned by the current user.
    """
    logger.info(f"Fetching invoices for customer {customer_id} by user {current_user.email}")
    
    # First verify the customer exists and belongs to current user
    customer = db.query(Customer).filter(
        Customer.id == customer_id,
        Customer.user_id == current_user.id
    ).first()
    
    if not customer:
        logger.warning(f"Customer {customer_id} not found for user {current_user.email}")
        raise HTTPException(status_code=404, detail="Customer not found")
    
    # Get all invoices for this customer
    invoices = db.query(Invoice).filter(
        Invoice.customer_id == customer_id,
        Invoice.user_id == current_user.id
    ).order_by(Invoice.created_at.desc()).all()
    
    logger.info(f"Found {len(invoices)} invoices for customer {customer_id}")
    return invoices

@router.put("/{customer_id}", response_model=CustomerSchema)
def update_customer(
    customer_id: int, 
    customer_update: CustomerUpdate, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
):
    """
    Update an existing customer
    
    **REQUIRES LOGIN** - Only logged-in users can update their customers
    
    - **customer_id**: Unique customer identifier
    - **name**: New customer name (optional)
    - **email**: New email address (optional)
    - **address**: New address (optional)
    - **phone**: New phone number (optional)
    
    Only the owner of the customer can update it.
    Guest customers cannot be updated.
    """
    logger.info(f"Updating customer {customer_id} for user: {current_user.email}")
    
    # Only allow users to update their own customers
    customer = db.query(Customer).filter(
        Customer.id == customer_id, 
        Customer.user_id == current_user.id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found or not owned by user")
    
    for field, value in customer_update.dict(exclude_unset=True).items():
        setattr(customer, field, value)
    
    db.commit()
    db.refresh(customer)
    
    logger.info(f"Customer {customer_id} updated successfully")
    return customer

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(
    customer_id: int, 
    db: Session = Depends(get_db), 
    current_user: User = Depends(get_current_user)  # REQUIRES LOGIN
):
    """
    Delete a customer
    
    **REQUIRES LOGIN** - Only logged-in users can delete their customers
    
    - **customer_id**: Unique customer identifier
    
    Only the owner of the customer can delete it.
    Guest customers cannot be deleted through this endpoint.
    """
    logger.info(f"Deleting customer {customer_id} for user: {current_user.email}")
    
    # Only allow users to delete their own customers
    customer = db.query(Customer).filter(
        Customer.id == customer_id, 
        Customer.user_id == current_user.id
    ).first()
    
    if not customer:
        raise HTTPException(status_code=404, detail="Customer not found or not owned by user")
    
    db.delete(customer)
    db.commit()
    
    logger.info(f"Customer {customer_id} deleted successfully")
    return {"message": "Customer deleted successfully"}
