# Vendor Management API

The Vendor Management API is a RESTful web service for managing vendors and purchase orders.

## Installation

1. Clone the repository to your local machine:

        git clone https://github.com/AmanGupta0112/vendor_management.git
2. Navigate to the project directory:

        cd vms
3. Install dependencies using pip:

           python3 -m venv venv
           source venv/bin/activate
        
        pip install -r requirements.txt
5. Apply migrations to set up the database:

        python manage.py migrate

6. Start the development server:

        python manage.py runserver 


## Usage

### Endpoints

- **List Vendors**: `GET /api/vendors/`
- **Create Vendor**: `POST /api/vendors/`
- **Retrieve Vendor**: `GET /api/vendors/{id}/`
- **Update Vendor**: `PUT /api/vendors/{id}/`
- **Delete Vendor**: `DELETE /api/vendors/{id}/`

- **List Purchase Orders**: `GET /api/purchase_orders/`
- **Create Purchase Order**: `POST /api/purchase_orders/`
- **Retrieve Purchase Order**: `GET /api/purchase_orders/{id}/`
- **Update Purchase Order**: `PUT /api/purchase_orders/{id}/`
- **Delete Purchase Order**: `DELETE /api/purchase_orders/{id}/`

- **Vendor Performance**: `GET /api/vendors/{vendor_id}/performance/`
- **Acknowledge Purchase Order**: `POST /api/purchase_orders/{po_id}/acknowledge/`


