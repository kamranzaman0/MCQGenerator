# Cloing Guidlines

## 1. Clone the repository

   - Clone your repository:

     ```bash
     git clone "https://github.com/kamranzaman0/MCQGenerator.git"
     ```
## 2. Ceate Virtual Environment

   - Create Virtual Envirionment:

     ```bash
     conda create -n venv python=3.8 -y
     ```
     
   - Activate Virtual Envirionment:

     ```bash
     conda activate venv
     ```
## 3. Install Requirements


   - Install Python and project dependencies:

     ```bash
     pip install -r requirements.txt
     ```

   - Run your Streamlit app:

     ```bash
     python3 -m streamlit run StreamlitAPP.py
     ```

## 4. Add OpenAI API Key (Optional)
   - If your project requires an API key, follow these steps to add it:
     1. Create a `.env` file on your server:

        ```bash
        touch .env
        ```
        ```

     2. OPENAI_API_KEY = "",then in the inverted comma paste your API key.
     4. Then save the file.

# AWS Deployment Guide

## 1. Log in to AWS
   - Visit the [AWS Management Console](https://aws.amazon.com/console/) and log in using your username and password.

## 2. Search for EC2 Instance
   - In the AWS Management Console, search for "EC2" and select it.

## 3. Configure the Ubuntu Machine
   - Choose an Ubuntu AMI (Amazon Machine Image) for your instance.
   - Select the instance type that suits your project requirements.
   - Configure instance details, add storage, and tag your instance.

## 4. Launch the Instance
   - Review your configurations and click "Launch" to start your instance.

## 5. Update the Machine
   - SSH into your EC2 instance.
   - Run the following commands to update the machine and install necessary packages:

     ```bash
     sudo apt update
     sudo apt-get update
     sudo apt upgrade
     sudo apt install git curl unzip tar make sudo vim wget
     ```

   - Clone your repository:

     ```bash
     git clone "your-repo-link"
     ```

   - Install Python and project dependencies:

     ```bash
     sudo apt install python3-pip
     pip3 install -r requirements.txt
     ```

   - Run your Streamlit app:

     ```bash
     python3 -m streamlit run StreamlitAPP.py
     ```

## 6. Add OpenAI API Key (Optional)
   - If your project requires an API key, follow these steps to add it:
     1. Create a `.env` file on your server:

        ```bash
        touch .env
        ```

     2. Open the `.env` file:

        ```bash
        vi .env
        ```

     3. Press `i` to enter insert mode, then paste your API key.
     4. Press `Esc` to exit insert mode, then type `:wq` and press Enter to save and close the file.

## 7. Configure the Port
   - Go to your EC2 instance's Security Groups settings.
   - Add an inbound rule to allow traffic on port `8501` (or whichever port your app uses).
   - Save the security group settings.
