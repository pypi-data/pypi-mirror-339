# NECMEC API python wrapper Client

A Python client for interacting with the **NECMEC API python wrapper**. This API allows users to submit reports, upload files, and perform other operations necessary to complete the submission process.

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
pip install .
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
python3 demo.py
```