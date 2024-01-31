FROM python:3.9 

WORKDIR /code_files 

COPY . ./ 

# Install required dependencies
RUN pip install openpyxl 

# Ensure required files are present

RUN [ -f "template.xlsx" ] || echo "Missing template.xlsx"

ENTRYPOINT ["python3","-u","speedtest_tool_v2.py"]