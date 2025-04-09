# NECMEC API python wrapper Client

A Python client for interacting with the **NECMEC API python wrapper**. This API allows users to submit reports, upload files, and perform other operations necessary to complete the submission process. Base API docs https://exttest.cybertip.org/ispws/documentation/index.html#overview

## Features

- **Verify Connection**: Check if the client can connect to the server and authenticate.
- **Download XSD Schema**: Retrieve the latest XML Schema Definition (XSD) for report submission.
- **Report Submission**: Open and submit a report in the system.
- **File Upload**: Upload files to a report.
- **File Details**: Provide additional details for uploaded files.
- **Finish Submission**: Finish the report submission process.
- **Retract Submission**: Cancel an open report submission.

## Installation

To install the package, you can use `pip`:

```bash
pip install necmec-api
```

### help
```
python3 -m necmec_api.cli --help
```

### status
```
python3 -m necmec_api.cli --config config.json --username your_username --password your_password --environment test status
```

### submit a report 
```
python3 -m necmec_api.cli --config config.json --username your_username --password your_password --environment test  submit "<xml_data>"

```

### Cancel the Report
```
python3 -m necmec_api.cli --config config.json --username your_username --password your_password --environment test  retract <report_id>
```

### Refer demo.py
```
python3 -m venv env
source env/bin/activate
pip install necmec-api
cat <<EOF > config.json
{
    "production": {
      "base_url": "https://report.cybertip.org/ispws",
      "status_url": "/status",
      "xsd_url": "/xsd",
      "submit_url": "/submit",
      "upload_url": "/upload",
      "fileinfo_url": "/fileinfo",
      "finish_url": "/finish",
      "retract_url": "/retract"
    },
    "test": {
      "base_url": "https://exttest.cybertip.org/ispws",
      "status_url": "/status",
      "xsd_url": "/xsd",
      "submit_url": "/submit",
      "upload_url": "/upload",
      "fileinfo_url": "/fileinfo",
      "finish_url": "/finish",
      "retract_url": "/retract"
    }
  }
EOF
python3 demo.py
```