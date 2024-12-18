import streamlit as st
import pycountry
from pdfrw import PdfReader, PdfWriter, PageMerge
import io
import base64
import pdfrw

def fill_pdf(template_path, data_dict):
    template_pdf = PdfReader(template_path)
    annotations = template_pdf.pages[0]['/Annots']
    for annotation in annotations:
        if annotation['/T']:
            key = annotation['/T'][1:-1]
            if key in data_dict:
                annotation.update(
                    pdfrw.PdfDict(V='{}'.format(data_dict[key]))
                )
    output_pdf = io.BytesIO()
    PdfWriter(output_pdf, trailer=template_pdf).write()
    return output_pdf.getvalue()

def display_page():
    st.image("Banner.jpg")

    data_dict = {}

    # Form
    col1, col2 = st.columns(2)

    # Add content to the first column
    with col1:
        st.subheader("Intake & Assessment")
        data_dict["date_today"] = st.date_input("Date of Today:")
        data_dict["first_name"] = st.text_input("First Name*:")

    # Add content to the second column
    with col2:
        data_dict["uploaded_image"] = st.file_uploader("Upload an image:", type=["jpg", "png"])
        data_dict["last_name"] = st.text_input("Last Name*:")

    # Gender and Date of Birth
    data_dict["gender"] = st.radio("Gender: ", options=["Male", "Female"], horizontal=True)
    data_dict["date_of_birth"] = st.date_input("Date of Birth*:", value=None)
    data_dict["address"] = st.text_input("Address:")

    col3, col4 = st.columns(2)
    with col3:
        data_dict["city"] = st.text_input("City:")
        data_dict["Email Address"] = st.text_input("Email Address:")
        data_dict["Job Title"] = st.text_input("Job Title:")
        data_dict["Parent"] = st.selectbox("Parent:", options=["None", "Yes", "No"])

    countries = [country.name for country in pycountry.countries]
    with col4:
        data_dict["country"] = st.selectbox("Country:", options=["Select a country"] + countries)
        data_dict["phone_number"] = st.text_input("Phone Number:")
        data_dict["Company"] = st.text_input("Company:")
        data_dict["Amount of Kids"] = st.selectbox("Amount of Kids:", options=["None", "1", "2", "3", "4+"])

    data_dict["Kaizen Subscription"] = st.selectbox(
        "Kaizen Subscription:",
        options=[
            "Please select",
            "Premium Subscription(Unlimited)",
            "Standard Subscription(3d/w)",
            "Step-In Subscription(2d/w)",
            "Premium Punch Card: 30x Classes",
            "Standard Punch Card: 10x Classes",
            "Kaizen Day Pass",
        ],
    )

    st.subheader("Class Specification:")
    col1, col2, col3 = st.columns(3)

    with col1:
        hiit_training = st.checkbox("HIIT & Functional Strength")

    with col2:
        cardio_kickboxing = st.checkbox("Cardio Kickboxing")

    with col3:
        restorative_yoga = st.checkbox("Restorative Yoga")

    # Validation check
    if st.button("Next"):
        if not data_dict["first_name"] or not data_dict["last_name"] or not data_dict["date_of_birth"]:
            st.error("Please fill out all mandatory fields marked with * before proceeding.")
        else:
            st.session_state.completed_page1 = True
            st.session_state.page = "page2"
            st.rerun()

    # Generate PDF
    if st.button("Test Submit"):
        if not data_dict["first_name"] or not data_dict["last_name"] or not data_dict["date_of_birth"]:
            st.error("Please fill out all mandatory fields marked with * before generating the PDF.")
        else:
            template_path = "template.pdf"  # Path to your template PDF
            pdf_data = fill_pdf(template_path, data_dict)

            b64 = base64.b64encode(pdf_data).decode()
            href = f'<a href="data:application/octet-stream;base64,{b64}" download="filled_form.pdf">Download PDF</a>'
            st.markdown(href, unsafe_allow_html=True)
            st.success("PDF generated successfully!")