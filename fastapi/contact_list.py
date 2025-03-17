from fastapi import FastAPI, HTTPException, Depends, Form
from fastapi.responses import HTMLResponse
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = "sqlite:///./contacts.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class Contact(Base):
    __tablename__ = "contacts"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    phone = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

class ContactSchema(BaseModel):
    name: str
    phone: str
    email: str

@app.get("/", response_class=HTMLResponse)
def home():
    return """<html>
            <head>
                <title>Contact List</title>
                <style>
                    body { font-family: Arial, sans-serif; text-align: center; margin-top: 50px; }
                    form { margin-top: 20px; }
                    input, button { padding: 10px; margin: 5px; }
                </style>
            </head>
            <body>
                <h1>Contact List</h1>
                <form action="/add_contact" method="post">
                    <input type="text" name="name" placeholder="Enter Name" required>
                    <input type="text" name="phone" placeholder="Enter Phone" required>
                    <input type="email" name="email" placeholder="Enter Email" required>
                    <button type="submit">Add Contact</button>
                </form>
                <a href="/contacts">View Contacts</a>
            </body>
        </html>"""

@app.post("/add_contact")
def add_contact(name: str = Form(...), phone: str = Form(...), email: str = Form(...), db: Session = Depends(get_db)):
    contact = Contact(name=name, phone=phone, email=email)
    db.add(contact)
    db.commit()
    return {"message": "Contact added successfully!"}

@app.get("/contacts", response_class=HTMLResponse)
def list_contacts(db: Session = Depends(get_db)):
    contacts = db.query(Contact).all()
    contact_list = "".join(f"<li>{contact.name} - {contact.phone} - {contact.email}</li>" for contact in contacts)
    return f"""<html>
                <head><title>Contact List</title></head>
                <body>
                    <h1>Saved Contacts</h1>
                    <ul>{contact_list}</ul>
                    <a href="/">Go Back</a>
                </body>
             </html>"""

@app.get("/contacts/{contact_id}", response_model=ContactSchema)
def get_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return contact

@app.put("/contacts/{contact_id}", response_model=ContactSchema)
def update_contact(contact_id: int, updated_contact: ContactSchema, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.name = updated_contact.name
    contact.phone = updated_contact.phone
    contact.email = updated_contact.email
    db.commit()
    db.refresh(contact)
    return contact

@app.patch("/contacts/{contact_id}")
def partial_update_contact(contact_id: int, phone: str, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    contact.phone = phone
    db.commit()
    db.refresh(contact)
    return contact

@app.delete("/contacts/{contact_id}")
def delete_contact(contact_id: int, db: Session = Depends(get_db)):
    contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    db.delete(contact)
    db.commit()
    return {"message": "Contact deleted"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
