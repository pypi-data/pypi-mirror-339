import argparse
import sys
from necmec_api.api import NecmecAPI


def main():
    parser = argparse.ArgumentParser(description="Necmec API Client")
    
    parser.add_argument("--config", type=str, required=True, help="Path to the config.json file")
    parser.add_argument("--username", type=str, required=True, help="API Username")
    parser.add_argument("--password", type=str, required=True, help="API Password")
    parser.add_argument("--environment", type=str, choices=['production', 'test'], default='test', help="Choose the environment (default: production)")
    
    subparsers = parser.add_subparsers(dest="command")
    
    subparsers.add_parser("status", help="Check the connection status")
    subparsers.add_parser("xsd", help="Download the latest XML schema definition")
    
    submit_parser = subparsers.add_parser("submit", help="Submit a report")
    submit_parser.add_argument("xml_data", type=str, help="XML data of the report to be submitted")
    
    upload_parser = subparsers.add_parser("upload", help="Upload a file to a report")
    upload_parser.add_argument("report_id", type=str, help="The report ID to upload the file to")
    upload_parser.add_argument("file_path", type=str, help="The path to the file to upload")
    
    fileinfo_parser = subparsers.add_parser("fileinfo", help="Provide additional details for an uploaded file")
    fileinfo_parser.add_argument("report_id", type=str, help="The report ID")
    fileinfo_parser.add_argument("file_id", type=str, help="The file ID")
    fileinfo_parser.add_argument("fileinfo_xml", type=str, help="XML data with file details")
    
    subparsers.add_parser("finish", help="Finish the report submission")
    subparsers.add_parser("retract", help="Cancel a report submission")
    
    args = parser.parse_args()

    api = NecmecAPI(args.config, args.username, args.password, args.environment)
    
    if args.command == "status":
        print(api.get_status())
    
    elif args.command == "xsd":
        print(api.get_xsd())
    
    elif args.command == "submit":
        print(api.post_submit(args.xml_data))
    
    elif args.command == "upload":
        print(api.post_upload(args.report_id, args.file_path))
    
    elif args.command == "fileinfo":
        print(api.post_fileinfo(args.report_id, args.file_id, args.fileinfo_xml))
    
    elif args.command == "finish":
        print(api.post_finish(args.report_id))
    
    elif args.command == "retract":
        print(api.post_retract(args.report_id))

if __name__ == "__main__":
    main()
